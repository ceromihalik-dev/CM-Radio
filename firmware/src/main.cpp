#include <Arduino.h>
#include <esp_system.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <ESPmDNS.h>
#include "BoardConfig.h"
#include "Settings.h"
#include "Player.h"
#include "WebUi.h"
#include "WifiScan.h"
#include "BackupConfig.h"
#include "FirmwareUpdate.h"
#include "SoundConfig.h"
#include "SetupPassword.h"
#include "StationRecovery.h"
#include "PasswordResetButton.h"
#include <memory>
#include <new>
#include <esp_wifi.h>

namespace {
WebServer server(80);
DNSServer dns;
Settings settings;
SettingsStore store;
PasswordResetButton passwordResetButton;
constexpr uint8_t setupResetPin = 0; // BOOT/IO0, active low; strap pin unchanged at boot.
bool storageReady = false;
bool apActive = false;
bool mdnsActive = false;
bool dirty = false;
bool applyWifi = false;
bool applyAudioConfig = false;
bool applyFallback = false;
bool applySound = false,applyMono=false,applyName=false;
uint32_t wifiLosses=0,recoveryEpoch=0,recoveryNextAt=0,stationRevision=0;
bool recoveryReady=false;String recoveryMessage="Noch keine Adresspruefung";
String deviceHost="cm-radio",deviceSuffix;
bool soundPreview = false,previewLoudness=false;
int previewBass=0,previewTreble=0,previewBalance=0;
bool stopAfterRestore = false;
WifiScan wifiScan;
struct ScanDriver {
    bool reconnect = false;
    void prepare() {
        reconnect = WiFi.getAutoReconnect();
        WiFi.setAutoReconnect(false);
        // Preserve the setup AP and an established home-network connection.
        // Cancel an unfinished station connection before asking for a scan.
        WiFi.enableSTA(true);
        if (WiFi.status() != WL_CONNECTED) WiFi.disconnect(false, false);
        WiFi.scanDelete();
    }
    int start() {
        const int result = WiFi.scanNetworks(true, false);
        if (result == WIFI_SCAN_FAILED) Serial.println("WLAN-Suche: Start abgelehnt; Wiederholung folgt");
        return result;
    }
    int complete() { return WiFi.scanComplete(); }
    void cancel() { esp_wifi_scan_stop(); }
    void restore() { WiFi.setAutoReconnect(reconnect); }
} scanDriver;
uint32_t saveAt = 0;
uint32_t wifiAt = 0;
uint32_t lastConnectAttempt = 0;
uint32_t offlineSince = 0;
bool wasOnline = false;
String apName;
String apPassword;
bool setupPasswordRequired = true;
bool restartAp = false;
uint32_t restartApAt = 0;
String serialLine;
String diagnostic;

void sendJson(int status, const JsonDocument& document) {
    String response;
    serializeJson(document, response);
    server.sendHeader("Cache-Control", "no-store");
    server.send(status, "application/json; charset=utf-8", response);
}
void error(int code, const char* message) {
    StaticJsonDocument<256> response;
    response["error"] = message;
    sendJson(code, response);
}
void accepted() {
    StaticJsonDocument<64> response;
    response["accepted"] = true;
    sendJson(202, response);
}
bool body(JsonDocument& document) {
    if (setupPasswordRequired && server.uri() != "/api/v1/setup/password") { error(428, "Zuerst das Passwort fuer den Setup-Zugang aendern");return false; }
    if (restartAp) {error(409, "Setup-WLAN wird neu gestartet; kurz warten");return false;}
    ++recoveryEpoch;
    if (firmwareUpdate::busy()) { error(409, "Firmwareupdate aktiv; Bedienung gesperrt");return false; }
    // Browser writes must come from this device; non-browser local API clients
    // may omit Origin. This is not an authentication mechanism.
    const String origin = server.header("Origin");
    if (!origin.isEmpty() && origin != "http://" + server.hostHeader()) {
        error(403, "Fremder Browser-Ursprung");
        return false;
    }
    if (server.arg("plain").length() > 16384) {
        error(413, "Anfrage zu gross");
        return false;
    }
    if (!server.header("Content-Type").startsWith("application/json")) {
        error(415, "Content-Type muss application/json sein");
        return false;
    }
    if (deserializeJson(document, server.arg("plain")) || !document.is<JsonObject>() || document.overflowed()) {
        error(400, "Ungueltiges JSON-Objekt");
        return false;
    }
    return true;
}
bool persist(const Settings& candidate) {
    if (!storageReady || !store.save(candidate)) {
        error(507, "Einstellungen konnten nicht gespeichert werden");
        return false;
    }
    settings = candidate;
    dirty = false;
    return true;
}
void startAp() {
    if (apActive) return;
    WiFi.mode(WIFI_AP_STA);
    if (!WiFi.softAP(apName.c_str(), apPassword.c_str())) {
        diagnostic = "Setup-WLAN konnte nicht gestartet werden";
        return;
    }
    dns.start(53, "*", WiFi.softAPIP());
    apActive = true;
    Serial.printf("Setup-WLAN: %s\nSetup: http://192.168.4.1\n", apName.c_str());
    Serial.println(setupPasswordRequired ? "Erstpasswort: passwort; im Browser aendern" : "Setup-Passwort: gespeichertes eigenes Passwort verwenden");
}
void stopAp() {
    if (!apActive) return;
    dns.stop();
    WiFi.softAPdisconnect(true);
    apActive = false;
    WiFi.mode(WIFI_STA);
}
void applyDeviceName(){
    deviceHost=settings.deviceName;deviceHost.toLowerCase();deviceHost.replace(" ","-");deviceHost.replace("_","-");
    WiFi.setHostname(deviceHost.c_str());
    if(mdnsActive){MDNS.end();mdnsActive=MDNS.begin(deviceHost.c_str());if(mdnsActive)MDNS.addService("http","tcp",80);}
    apName=settings.deviceName+"-"+deviceSuffix;
    if(apActive){restartAp=true;restartApAt=millis()+2500;}
}
bool requestRecovery(int index){
    if(!recoveryReady||wifiScan.busy()||WiFi.status()!=WL_CONNECTED||index<0||index>=int(settings.count))return false;
    recovery::Job job{};job.epoch=recoveryEpoch;job.index=index;
    strlcpy(job.name,settings.stations[index].name.c_str(),sizeof(job.name));strlcpy(job.url,settings.stations[index].url.c_str(),sizeof(job.url));strlcpy(job.id,settings.stations[index].directoryId.c_str(),sizeof(job.id));
    if(!recovery::request(job))return false;
    recoveryNextAt=millis()+600000;recoveryMessage="Senderadresse wird im Verzeichnis geprueft";return true;
}
void connectWifi() {
    WiFi.disconnect(false, false);
    if (!apActive) WiFi.mode(WIFI_STA);
    if (settings.ssid.isEmpty()) startAp();
    else WiFi.begin(settings.ssid.c_str(), settings.password.c_str());
    lastConnectAttempt = millis();
    offlineSince = millis();
}
const char* fallbackUrl() {
    return settings.fallbackStation >= 0 ? settings.stations[settings.fallbackStation].url.c_str() : "";
}
void writeBackup(JsonDocument& document) {
    document["format"] = "CM-Radio-Backup";document["schema"] = 2;
    document["sourceVersion"] = board::version;document["sourceBuild"] = board::build;
    JsonObject config = document.createNestedObject("settings");
    config["deviceName"]=settings.deviceName;config["mono"]=settings.mono;config["autoRecover"]=settings.autoRecover;
    config["selected"] = settings.selected;config["volume"] = settings.volume;config["autoplay"] = settings.autoplay;
    config["loudness"]=settings.loudness;config["bass"]=settings.bass;config["treble"]=settings.treble;config["balance"]=settings.balance;
    config["volumeLimit"] = settings.volumeLimit;config["softStartSeconds"] = settings.softStartSeconds;config["fallbackStation"] = settings.fallbackStation;
    JsonArray list = config.createNestedArray("stations");
    for (size_t i = 0; i < settings.count; ++i) {JsonObject item = list.createNestedObject();item["name"] = settings.stations[i].name;item["url"] = settings.stations[i].url;item["logo"]=settings.stations[i].logo;item["directoryId"]=settings.stations[i].directoryId;}
}
void restoreBackup(bool validateOnly) {
    DynamicJsonDocument request(24576);if (!body(request)) return;
    std::unique_ptr<backup::Data> data(new(std::nothrow) backup::Data);
    if (!data) {error(503, "Zu wenig Speicher fuer Wiederherstellung");return;}
    const char* reason = nullptr;
    if (!backup::read(request, *data, reason)) {error(400, reason);return;}
    if (validateOnly) {
        StaticJsonDocument<384> response;response["loudness"]=data->loudness;response["bass"]=data->bass;response["treble"]=data->treble;response["balance"]=data->balance;response["valid"] = true;response["stationCount"] = data->count;response["volume"] = data->volume;response["volumeLimit"] = data->volumeLimit;response["wifiPreserved"] = true;sendJson(200, response);return;
    }
    Settings candidate = settings;
    candidate.deviceName=data->deviceName;candidate.mono=data->mono;candidate.autoRecover=data->autoRecover;
    candidate.count = data->count;candidate.selected = data->selected;candidate.volume = data->volume;
    candidate.volumeLimit = data->volumeLimit;candidate.softStartSeconds = data->softStartSeconds;
    candidate.loudness=data->loudness;candidate.bass=data->bass;candidate.treble=data->treble;candidate.balance=data->balance;
    candidate.autoplay = data->autoplay;candidate.fallbackStation = data->fallbackStation;
    for (size_t i = 0; i < candidate.count; ++i) candidate.stations[i] = {data->stations[i].name, data->stations[i].url,data->stations[i].logo,data->stations[i].directoryId};
    if (!persist(candidate)) return;
    soundPreview = false;
    applyAudioConfig = true;applyFallback = true;applySound = true;applyMono=true;applyName=true;++recoveryEpoch;++stationRevision;stopAfterRestore = true;
    accepted();
}
void routes() {
    const char* headers[] = {"Content-Type", "Origin", "X-CM-Update-Token"};
    server.collectHeaders(headers, 3);
    firmwareUpdate::begin(server, [] {if (!dirty) return true;if (!storageReady || !store.save(settings)) return false;dirty = false;return true;}, [] {return !setupPasswordRequired && !restartAp;});
    server.on("/", HTTP_GET, [] {
        server.sendHeader("Cache-Control", "no-cache");
        server.send_P(200, "text/html; charset=utf-8", WEB_UI);
    });
    server.on("/api/v1/setup/password", HTTP_POST, [] {
        StaticJsonDocument<512> request;if (!body(request)) return;
        if (!request["password"].is<const char*>() || !setupAccess::valid(request["password"])) {error(400,"Neues Passwort: 8 bis 63 druckbare ASCII-Zeichen; nicht passwort");return;}
        if (!setupPasswordRequired && (!request["currentPassword"].is<const char*>() || apPassword != request["currentPassword"].as<const char*>())) {error(403,"Bisheriges Setup-Passwort stimmt nicht");return;}
        const String password=request["password"].as<const char*>();
        if (!storageReady || !store.saveSetupPassword(password)) {error(507,"Setup-Passwort konnte nicht gespeichert werden");return;}
        apPassword=password;setupPasswordRequired=false;
        restartAp=apActive;restartApAt=millis()+2500;
        StaticJsonDocument<128> response;response["accepted"]=true;response["reconnectRequired"]=restartAp;sendJson(200,response);
    });
    server.on("/api/v1/station/recover",HTTP_POST,[]{StaticJsonDocument<128> request;if(!body(request))return;if(!requestRecovery(settings.selected)){error(409,"WLAN fehlt oder Adresspruefung bereits aktiv");return;}accepted();});
    server.on("/api/v1/status", HTTP_GET, [] {
        const PlayerStatus p = player::status();
        DynamicJsonDocument response(6144);
        response["name"] = "CM-Radio";response["deviceName"]=settings.deviceName;response["hostname"]=deviceHost;response["mono"]=settings.mono;response["effectiveMono"]=p.mono;response["autoRecover"]=settings.autoRecover;
        response["wifiLosses"]=wifiLosses;response["offlineSeconds"]=WiFi.status()==WL_CONNECTED?0:(millis()-offlineSince)/1000;response["connectionAttempts"]=p.connectionAttempts;response["streamBreaks"]=p.streamBreaks;response["streamSeconds"]=p.streamSeconds;response["lastStreamError"]=p.lastError;response["recoveryBusy"]=recovery::busy();response["recoveryMessage"]=recoveryMessage;response["stationRevision"]=stationRevision;
        response["version"] = board::version;
        response["build"] = board::build;
        response["board"] = board::name;
        response["wifiConnected"] = WiFi.status() == WL_CONNECTED;
        response["ip"] = WiFi.localIP().toString();
        response["setupActive"] = apActive;response["setupPasswordRequired"] = setupPasswordRequired;
        response["setupSsid"] = apActive ? apName : "";
        response["rssi"] = WiFi.status() == WL_CONNECTED ? WiFi.RSSI() : 0;
        response["audioReady"] = p.ready;
        response["updating"] = firmwareUpdate::busy();
        response["requested"] = p.requested;
        response["running"] = p.running;
        response["state"] = !p.ready ? "error" : !p.requested ? "stopped" : !p.running ? "connecting" : "streaming";
        response["stationIndex"] = settings.selected;
        int playingStationIndex = -1;
        if (p.requested) for (size_t i = 0; i < settings.count; ++i) if (settings.stations[i].url == p.actualUrl) {playingStationIndex = i;break;}
        response["playingStationIndex"] = playingStationIndex;
        String audibleName = settings.stations[settings.selected].name;
        if (p.fallbackActive) {
            audibleName = "Ersatzsender";
            for (size_t i = 0; i < settings.count; ++i) if (settings.stations[i].url == p.actualUrl) {audibleName = settings.stations[i].name;break;}
        }
        response["station"] = audibleName;
        const int logoIndex=p.requested?playingStationIndex:static_cast<int>(settings.selected);
        response["stationLogo"]=logoIndex>=0?settings.stations[logoIndex].logo:"";
        response["requestedStation"] = settings.stations[settings.selected].name;
        response["loudness"]=settings.loudness;response["previewLoudness"]=soundPreview?previewLoudness:settings.loudness;response["bass"]=settings.bass;response["treble"]=settings.treble;response["balance"]=settings.balance;
        response["soundPreview"]=soundPreview;response["previewBass"]=soundPreview?previewBass:settings.bass;response["previewTreble"]=soundPreview?previewTreble:settings.treble;response["previewBalance"]=soundPreview?previewBalance:settings.balance;
        response["fallbackStation"] = settings.fallbackStation;
        response["fallbackActive"] = p.fallbackActive;
        response["title"] = p.title;
        response["message"] = diagnostic.isEmpty() ? p.message : diagnostic;
        response["volume"] = settings.volume;response["volumeSteps"] = rules::maxVolume;
        response["maxVolume"] = rules::maxVolume;
        response["volumeLimit"] = settings.volumeLimit;
        response["softStartSeconds"] = settings.softStartSeconds;
        response["effectiveVolume"] = p.volume;
        response["effectiveBass"]=p.effectiveBass;response["effectiveTreble"]=p.effectiveTreble;
        response["ramping"] = p.ramping;
        response["sleepRemainingSeconds"] = p.sleepRemainingSeconds;
        response["audioConfigPending"] = applyAudioConfig || applyFallback || applySound || applyMono;
        response["restoreStopPending"] = stopAfterRestore;
        response["autoplay"] = settings.autoplay;
        response["settingsPending"] = dirty;
        response["storageReady"] = storageReady;
        response["uptimeSeconds"] = millis() / 1000;
        response["freeHeap"] = ESP.getFreeHeap();
        response["minFreeHeap"] = ESP.getMinFreeHeap();
        response["resetReason"] = static_cast<int>(esp_reset_reason());
        response["psramBytes"] = ESP.getPsramSize();
        response["flashBytes"] = ESP.getFlashChipSize();
        sendJson(200, response);
    });
    server.on("/api/v1/stations", HTTP_GET, [] {
        DynamicJsonDocument response(24576);
        JsonArray list = response.createNestedArray("stations");
        for (size_t i = 0; i < settings.count; ++i) {
            JsonObject station = list.createNestedObject();
            station["name"] = settings.stations[i].name;
            station["url"] = settings.stations[i].url;station["logo"]=settings.stations[i].logo;station["directoryId"]=settings.stations[i].directoryId;
        }
        sendJson(200, response);
    });
    server.on("/api/v1/stations", HTTP_PUT, [] {
        DynamicJsonDocument request(24576);
        if (!body(request)) return;
        if (!request["stations"].is<JsonArray>()) { error(400, "stations muss ein Array sein"); return; }
        JsonArray list = request["stations"];
        if (list.size() == 0 || list.size() > rules::maxStations) { error(400, "1 bis 10 Sender erforderlich"); return; }
        Settings candidate = settings;
        candidate.count = list.size();
        candidate.selected = 0;
        const String current = settings.stations[settings.selected].url;
        const String previousFallback = fallbackUrl();
        candidate.fallbackStation = -1;
        bool currentFound = false;
        for (size_t i = 0; i < candidate.count; ++i) {
            if (!list[i]["name"].is<const char*>() || !list[i]["url"].is<const char*>()) { error(400, "Sender braucht name und url"); return; }
            String name = list[i]["name"].as<String>();
            String url = list[i]["url"].as<String>();
            name.trim(); url.trim();
            if (name.isEmpty() || name.length() >= rules::maxName || !rules::validUrl(url.c_str())) { error(400, "Ungueltiger Sendername oder HTTP(S)-Stream"); return; }
            if (list[i].containsKey("logo")&&!list[i]["logo"].is<const char*>()){error(400,"Logo muss eine HTTPS-Adresse sein");return;}
            String logo=list[i]["logo"]|"";logo.trim();
            if(!rules::validLogo(logo.c_str())){error(400,"Ungueltige HTTPS-Logo-Adresse");return;}
            if(list[i].containsKey("directoryId")&&(!list[i]["directoryId"].is<const char*>()||!deviceOptions::validId(list[i]["directoryId"]))){error(400,"Ungueltige Radio-Browser-ID");return;}
            candidate.stations[i] = {name, url,logo,list[i]["directoryId"]|""};
            if (!previousFallback.isEmpty() && url == previousFallback) candidate.fallbackStation = i;
            if (url == current) { candidate.selected = i; currentFound = true; }
        }
        if (!persist(candidate)) return;
        applyFallback = true;
        if (!currentFound && !player::stop()) { error(503, "Gespeichert; Audio-Warteschlange voll"); return; }
        accepted();
    });
    server.on("/api/v1/play", HTTP_POST, [] {
        StaticJsonDocument<256> request;
        if (!body(request)) return;
        if (!request["station"].is<int>()) { error(400, "station muss eine Ganzzahl sein"); return; }
        const int index = request["station"].as<int>();
        if (index < 0 || index >= static_cast<int>(settings.count)) { error(400, "Senderindex ungueltig"); return; }
        if (stopAfterRestore) {error(409, "Wiederherstellung wird angewendet; kurz warten");return;}
        if (!player::status().ready) { error(503, "Audio nicht bereit"); return; }
        Settings candidate = settings;
        candidate.selected = index;
        if (!persist(candidate)) return;
        if (!player::play(settings.stations[index].url.c_str(), fallbackUrl())) { error(503, "Audio-Warteschlange voll"); return; }
        accepted();
    });
    server.on("/api/v1/stop", HTTP_POST, [] {
        StaticJsonDocument<64> request;
        if (!body(request)) return;
        if (!player::stop()) { error(503, "Audio-Warteschlange voll"); return; }
        accepted();
    });
    server.on("/api/v1/volume", HTTP_POST, [] {
        StaticJsonDocument<128> request;
        if (!body(request)) return;
        if (!request["volume"].is<int>()) { error(400, "volume muss eine Ganzzahl sein"); return; }
        const int value = request["volume"].as<int>();
        if (value < 0 || value > settings.volumeLimit) { error(400, "Lautstaerke ueberschreitet die eingestellte Grenze"); return; }
        if (!player::volume(value)) { error(503, "Audio-Warteschlange voll"); return; }
        settings.volume = value;
        dirty = true;
        saveAt = millis() + 2000;
        accepted();
    });
    server.on("/api/v1/config", HTTP_GET, [] {
        StaticJsonDocument<512> response;
        response["deviceName"]=settings.deviceName;response["mono"]=settings.mono;response["autoRecover"]=settings.autoRecover;
        response["ssid"] = settings.ssid;
        response["autoplay"] = settings.autoplay;
        response["volumeLimit"] = settings.volumeLimit;
        response["softStartSeconds"] = settings.softStartSeconds;
        response["loudness"]=settings.loudness;response["previewLoudness"]=soundPreview?previewLoudness:settings.loudness;response["bass"]=settings.bass;response["treble"]=settings.treble;response["balance"]=settings.balance;
        response["soundPreview"]=soundPreview;response["previewBass"]=soundPreview?previewBass:settings.bass;response["previewTreble"]=soundPreview?previewTreble:settings.treble;response["previewBalance"]=soundPreview?previewBalance:settings.balance;
        response["fallbackStation"] = settings.fallbackStation;
        sendJson(200, response);
    });
    server.on("/api/v1/config", HTTP_POST, [] {
        StaticJsonDocument<512> request;
        if (!body(request)) return;
        Settings candidate = settings;
        if (!request.containsKey("autoplay") && !request.containsKey("volumeLimit") && !request.containsKey("softStartSeconds") && !request.containsKey("fallbackStation") && !request.containsKey("bass") && !request.containsKey("treble") && !request.containsKey("balance") && !request.containsKey("loudness") && !request.containsKey("deviceName") && !request.containsKey("mono") && !request.containsKey("autoRecover")) { error(400, "Keine bekannte Einstellung"); return; }
        if(request.containsKey("deviceName")){if(!request["deviceName"].is<const char*>()||!deviceOptions::validName(request["deviceName"])){error(400,"Geraetename: 1 bis 24 ASCII-Buchstaben/Ziffern, Leerzeichen, - oder _");return;}candidate.deviceName=request["deviceName"].as<const char*>();}
        for(const char* key:{"mono","autoRecover"})if(request.containsKey(key)&&!request[key].is<bool>()){error(400,"mono/autoRecover muessen boolesch sein");return;}
        if(request.containsKey("mono"))candidate.mono=request["mono"];
        if(request.containsKey("autoRecover"))candidate.autoRecover=request["autoRecover"];
        const bool monoChanged=candidate.mono!=settings.mono,nameChanged=candidate.deviceName!=settings.deviceName;
        if (request.containsKey("autoplay")) {
            if (!request["autoplay"].is<bool>()) { error(400, "autoplay muss boolesch sein"); return; }
            candidate.autoplay = request["autoplay"].as<bool>();
        }
        if (request.containsKey("volumeLimit")) {
            if (!request["volumeLimit"].is<int>() || request["volumeLimit"].as<int>() < 0 || request["volumeLimit"].as<int>() > 50) { error(400, "volumeLimit muss 0 bis 50 sein"); return; }
            candidate.volumeLimit = request["volumeLimit"].as<int>();
            if (candidate.volume > candidate.volumeLimit) candidate.volume = candidate.volumeLimit;
        }
        if (request.containsKey("softStartSeconds")) {
            if (!request["softStartSeconds"].is<int>() || request["softStartSeconds"].as<int>() < 0 || request["softStartSeconds"].as<int>() > 30) { error(400, "softStartSeconds muss 0 bis 30 sein"); return; }
            candidate.softStartSeconds = request["softStartSeconds"].as<int>();
        }
        if (request.containsKey("fallbackStation")) {
            if (!request["fallbackStation"].is<int>() || request["fallbackStation"].as<int>() < -1 || request["fallbackStation"].as<int>() >= static_cast<int>(settings.count)) {error(400, "Ungueltiger Ersatzsenderindex");return;}
            candidate.fallbackStation = request["fallbackStation"].as<int>();
        }
        int bass=candidate.bass,treble=candidate.treble,balance=candidate.balance;
        if (!sound::read(request.as<JsonObjectConst>(),bass,treble,balance)) {error(400,"Bass/Hoehen: -12 bis +6 dB; Balance: -16 bis +16");return;}
        bool loudness=candidate.loudness;
        if(!sound::readLoudness(request.as<JsonObjectConst>(),loudness)){error(400,"Loudness muss boolesch sein");return;}
        const bool hasSound=request.containsKey("bass")||request.containsKey("treble")||request.containsKey("balance")||request.containsKey("loudness");
        const bool soundChanged=(hasSound&&soundPreview)||bass!=settings.bass||treble!=settings.treble||balance!=settings.balance||loudness!=settings.loudness;
        candidate.loudness=loudness;
        candidate.bass=bass;candidate.treble=treble;candidate.balance=balance;
        const bool fallbackChanged = candidate.fallbackStation != settings.fallbackStation;
        const bool audioChanged = candidate.volumeLimit != settings.volumeLimit || candidate.softStartSeconds != settings.softStartSeconds;
        if (!persist(candidate)) return;
        if(monoChanged)applyMono=true;if(nameChanged)applyName=true;
        if (hasSound) soundPreview = false;
        if (soundChanged) applySound = true;
        if (audioChanged) applyAudioConfig = true;
        if (fallbackChanged) applyFallback = true;
        accepted();
    });
    server.on("/api/v1/sound/preview", HTTP_POST, [] {
        StaticJsonDocument<256> request;if (!body(request)) return;
        int bass=0,treble=0,balance=0;bool loudness=false;
        if (!request.containsKey("bass")||!request.containsKey("treble")||!request.containsKey("balance")||!sound::read(request.as<JsonObjectConst>(),bass,treble,balance)||!sound::readLoudness(request.as<JsonObjectConst>(),loudness)) {error(400,"Alle drei gueltigen Klangwerte erforderlich");return;}
        if (stopAfterRestore || applySound) {error(409,"Gespeicherter Klang wird noch angewendet; kurz warten");return;}
        if (!player::status().ready || !player::sound(bass,treble,balance,loudness)) {error(503,"Audio nicht bereit oder Warteschlange voll");return;}
        previewLoudness=loudness;previewBass=bass;previewTreble=treble;previewBalance=balance;soundPreview=true;accepted();
    });
    server.on("/api/v1/sound/reset", HTTP_POST, [] {
        StaticJsonDocument<128> request;if (!body(request)) return;
        if (!player::status().ready || !player::sound(settings.bass,settings.treble,settings.balance,settings.loudness)) {error(503,"Audio nicht bereit oder Warteschlange voll");return;}
        soundPreview=false;accepted();
    });
    server.on("/api/v1/backup", HTTP_GET, [] {
        DynamicJsonDocument response(24576);writeBackup(response);
        if (response.overflowed()) {error(503, "Sicherung konnte nicht erstellt werden");return;}
        sendJson(200, response);
    });
    server.on("/api/v1/restore/validate", HTTP_POST, [] {restoreBackup(true);});
    server.on("/api/v1/restore", HTTP_POST, [] {restoreBackup(false);});
    server.on("/api/v1/sleep", HTTP_POST, [] {
        StaticJsonDocument<128> request;
        if (!body(request)) return;
        if (!request["minutes"].is<int>() || request["minutes"].as<int>() < 0 || request["minutes"].as<int>() > 180) { error(400, "minutes muss 0 bis 180 sein (0 beendet den Timer)"); return; }
        if (!player::status().ready) { error(503, "Audio nicht bereit"); return; }
        if (!player::sleep(request["minutes"].as<int>())) { error(503, "Audio-Warteschlange voll"); return; }
        accepted();
    });
    server.on("/api/v1/wifi/scan", HTTP_POST, [] {
        StaticJsonDocument<64> request;
        if (!body(request)) return;
        if (applyWifi) { error(409, "WLAN-Verbindung wird gerade geaendert"); return; }
        wifiScan.request(millis(), scanDriver);
        accepted();
    });
    server.on("/api/v1/wifi/scan", HTTP_GET, [] {
        const int count = wifiScan.result();
        if (!wifiScan.started() || (!wifiScan.busy() && count == WIFI_SCAN_FAILED)) { error(503, "WLAN-Suche nicht gestartet oder fehlgeschlagen"); return; }
        DynamicJsonDocument response(8192);
        response["scanning"] = wifiScan.busy();
        JsonArray networks = response.createNestedArray("networks");
        if (count >= 0) {
            // Framework scan results are sorted by signal strength. Keep the
            // strongest access point per SSID and bound the response size.
            for (int i = 0; i < count && networks.size() < 20; ++i) {
                const String ssid = WiFi.SSID(i);
                if (ssid.isEmpty()) continue;
                bool duplicate = false;
                for (JsonObject item : networks) {
                    if (ssid == item["ssid"].as<const char*>()) { duplicate = true; break; }
                }
                if (duplicate) continue;
                JsonObject item = networks.createNestedObject();
                item["ssid"] = ssid;
                item["rssi"] = WiFi.RSSI(i);
                item["channel"] = WiFi.channel(i);
                item["secure"] = WiFi.encryptionType(i) != WIFI_AUTH_OPEN;
            }
        }
        sendJson(200, response);
    });
    server.on("/api/v1/wifi", HTTP_POST, [] {
        StaticJsonDocument<512> request;
        if (!body(request)) return;
        if (wifiScan.busy()) { error(409, "Bitte WLAN-Suche abwarten"); return; }
        if (!request["ssid"].is<const char*>() || !request["password"].is<const char*>()) { error(400, "ssid und password erforderlich"); return; }
        Settings candidate = settings;
        candidate.ssid = request["ssid"].as<String>();
        candidate.password = request["password"].as<String>();
        if (!rules::validWifi(candidate.ssid.c_str(), candidate.password.c_str())) { error(400, "SSID: 1-32 Bytes; Passwort: leer oder 8-63 Bytes"); return; }
        if (!persist(candidate)) return;
        applyWifi = true;
        wifiAt = millis() + 1500;
        accepted();
    });
    server.onNotFound([] {
        if (server.uri().startsWith("/api/")) { error(404, "API-Endpunkt nicht gefunden"); return; }
        if (server.method() != HTTP_GET) { error(405, "Methode nicht erlaubt"); return; }
        server.sendHeader("Location", "/", true);
        server.send(302, "text/plain", "CM-Radio Setup");
    });
    server.begin();
}
bool resetSetupAccess(){
    if(!storageReady || !store.resetSetupPassword())return false;
    apPassword=setupAccess::initialPassword;setupPasswordRequired=true;
    restartAp=apActive;restartApAt=millis()+2500;if(!apActive)startAp();
    Serial.println("Setup-Passwort auf passwort zurueckgesetzt; im Browser aendern");
    return true;
}
void serialCommands() {
    while (Serial.available()) {
        const char c = static_cast<char>(Serial.read());
        if (c == '\n') {
            serialLine.trim();
            if (serialLine == "setup") startAp();
            else if (serialLine == "reset-ap-password") {
                if(!resetSetupAccess())Serial.println("Setup-Passwort konnte nicht zurueckgesetzt werden");
            }
            else if (serialLine == "status") {
                Serial.printf("CM-Radio %s build %s | Flash %u | PSRAM %u | IP %s | Audio %s\n", board::version, board::build, ESP.getFlashChipSize(), ESP.getPsramSize(), WiFi.localIP().toString().c_str(), player::status().ready ? "bereit" : "Fehler");
            } else if (serialLine == "reset-wifi") {
                Settings candidate = settings;
                candidate.ssid = "";
                candidate.password = "";
                if (storageReady && store.save(candidate)) {
                    settings = candidate;
                    dirty = false;
                    connectWifi();
                    startAp();
                } else Serial.println("WLAN konnte nicht zurueckgesetzt werden");
            }
            serialLine = "";
        } else if (c != '\r' && serialLine.length() < 64) serialLine += c;
    }
}
}

void setup() {
    // Keep the amplifiers muted even if storage or PSRAM initialization fails.
    pinMode(board::amplifierEnable, OUTPUT);
    digitalWrite(board::amplifierEnable, LOW);
    Serial.begin(115200);
    pinMode(setupResetPin, INPUT_PULLUP);
    Serial.printf("\nCM-Radio %s build %s | %s\nFlash: %u Bytes | PSRAM: %u Bytes\n", board::version, board::build, board::name, ESP.getFlashChipSize(), ESP.getPsramSize());
    storageReady = store.begin();
    if (!storageReady) diagnostic = "NVS-Speicher nicht verfuegbar";
    if (!store.load(settings)) diagnostic = "Gespeicherte Konfiguration ungueltig; Standard geladen";
    WiFi.persistent(false);
    WiFi.setHostname("cm-radio");
    WiFi.setSleep(false);
    WiFi.setAutoReconnect(true);
    char suffix[7];
    snprintf(suffix, sizeof(suffix), "%06X", static_cast<unsigned>(ESP.getEfuseMac() & 0xffffff));
    deviceSuffix=suffix;applyDeviceName();
    recoveryReady=recovery::begin();
    apPassword = storageReady ? store.setupPassword() : String(setupAccess::initialPassword);
    setupPasswordRequired = apPassword == setupAccess::initialPassword;
    if (!psramFound()) diagnostic = "PSRAM fehlt: Audio bleibt deaktiviert";
    else if (ESP.getFlashChipSize() != 8U * 1024U * 1024U) diagnostic = "Flashgroesse passt nicht zur WROVER-N8R8-Konfiguration";
    else if (!player::begin(settings.volume, settings.volumeLimit, settings.softStartSeconds,settings.bass,settings.treble,settings.balance,settings.loudness,settings.mono)) diagnostic = "Audio-Task konnte nicht gestartet werden";
    else if (settings.autoplay) player::play(settings.stations[settings.selected].url.c_str(), fallbackUrl());
    connectWifi();
    routes();
    Serial.println("Serielle Befehle: status, setup, reset-wifi, reset-ap-password (jeweils mit Enter)");
}

void loop() {
    const uint32_t now = millis();
    firmwareUpdate::tick();
    if(firmwareUpdate::busy())passwordResetButton.inhibit();
    const PasswordResetButton::Action resetAction=firmwareUpdate::busy()?PasswordResetButton::None:passwordResetButton.tick(digitalRead(setupResetPin)==LOW,now);
    if(resetAction==PasswordResetButton::Factory && !firmwareUpdate::busy()){
        if(storageReady && store.factoryReset()){
            dirty=false;Serial.println("Werkseinstellungen wiederhergestellt; Neustart");ESP.restart();return;
        }
        Serial.println("Werkseinstellungen konnten nicht wiederhergestellt werden");
    }
    if(resetAction==PasswordResetButton::Password && !firmwareUpdate::busy()){
        if(!resetSetupAccess())Serial.println("Setup-Passwort konnte nicht zurueckgesetzt werden");
    }
    if(restartAp && !wifiScan.busy() && !firmwareUpdate::busy() && rules::reached(now,restartApAt)){
        restartAp=false;
        if(apActive){
            dns.stop();WiFi.softAPdisconnect(false);apActive=false;
            startAp();
        }
    }
    wifiScan.tick(now, scanDriver);
    if (stopAfterRestore && (!player::status().ready || player::stop())) stopAfterRestore = false;
    if (!stopAfterRestore) {
        if (applyAudioConfig && player::configure(settings.volumeLimit, settings.softStartSeconds, settings.volume)) applyAudioConfig = false;
        if (applySound && player::sound(settings.bass,settings.treble,settings.balance,settings.loudness)) applySound = false;
        if (applyFallback && player::fallback(fallbackUrl())) applyFallback = false;
    }
    server.handleClient();
    if (apActive) dns.processNextRequest();
    if (!firmwareUpdate::busy()) serialCommands();
    if (!firmwareUpdate::busy() && applyWifi && rules::reached(now, wifiAt)) {
        applyWifi = false;
        connectWifi();
    }
    if(applyName&&!firmwareUpdate::busy()){applyDeviceName();applyName=false;}
    if(applyMono&&!firmwareUpdate::busy()&&player::mono(settings.mono))applyMono=false;
    recovery::Result result;
    if(recovery::take(result)){
        recoveryMessage=result.message;
        if(result.found && result.job.epoch==recoveryEpoch && !firmwareUpdate::busy() && result.job.index<int(settings.count) && settings.stations[result.job.index].url==result.job.url){
            Settings candidate=settings;candidate.stations[result.job.index].url=result.url;candidate.stations[result.job.index].directoryId=result.id;
            if(storageReady&&store.save(candidate)){
                settings=candidate;dirty=false;++stationRevision;applyFallback=true;
                auto p=player::status();if(p.requested&&!p.running&&!p.fallbackActive&&settings.selected==size_t(result.job.index))player::play(result.url,fallbackUrl());
                recoveryMessage="Senderadresse erneuert und gespeichert";
            }else recoveryMessage="Neue Adresse konnte nicht gespeichert werden";
        }else if(result.found)recoveryMessage="Adresspruefung wegen zwischenzeitlicher Bedienung verworfen";
    }
    const bool online = WiFi.status() == WL_CONNECTED;
    if (online && !wasOnline && !wifiScan.busy()) {
        Serial.printf("WLAN verbunden: http://%s / http://%s.local\n", WiFi.localIP().toString().c_str(),deviceHost.c_str());
        stopAp();
        mdnsActive = MDNS.begin(deviceHost.c_str());
        if (mdnsActive) MDNS.addService("http", "tcp", 80);
    } else if (!online && wasOnline && !wifiScan.busy()) {
        ++wifiLosses;offlineSince = now;
        if (mdnsActive) MDNS.end();
        mdnsActive = false;
    }
    if (!wifiScan.busy()) wasOnline = online;
    if (!online && !settings.ssid.isEmpty()) {
        if (now - offlineSince >= 30000) startAp();
        if (!wifiScan.busy() && now - lastConnectAttempt >= 20000) {
            WiFi.begin(settings.ssid.c_str(), settings.password.c_str());
            lastConnectAttempt = now;
        }
    }
    auto recoveryStatus=player::status();
    if(settings.autoRecover && !setupPasswordRequired && online && !firmwareUpdate::busy() && !recovery::busy() && recoveryStatus.requested && recoveryStatus.consecutiveAttempts>=3 && rules::reached(now,recoveryNextAt))requestRecovery(settings.selected);
    if (dirty && rules::reached(now, saveAt)) {
        if (storageReady && store.save(settings)) {
            dirty = false;
            if (diagnostic == "Speichern fehlgeschlagen; neuer Versuch folgt") diagnostic = "";
        } else {
            diagnostic = "Speichern fehlgeschlagen; neuer Versuch folgt";
            saveAt = now + 5000;
        }
    }
    delay(2);
}

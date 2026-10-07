#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <ESPmDNS.h>
#include "BoardConfig.h"
#include "Settings.h"
#include "Player.h"
#include "WebUi.h"

namespace {
WebServer server(80);
DNSServer dns;
Settings settings;
SettingsStore store;
bool storageReady = false;
bool apActive = false;
bool mdnsActive = false;
bool dirty = false;
bool applyWifi = false;
uint32_t saveAt = 0;
uint32_t wifiAt = 0;
uint32_t lastConnectAttempt = 0;
uint32_t offlineSince = 0;
bool wasOnline = false;
String apName;
String apPassword;
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
    // Browser writes must come from this device; non-browser local API clients
    // may omit Origin. This is not an authentication mechanism.
    const String origin = server.header("Origin");
    if (!origin.isEmpty() && origin != "http://" + server.hostHeader()) {
        error(403, "Fremder Browser-Ursprung");
        return false;
    }
    if (server.arg("plain").length() > 8192) {
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
    Serial.printf("Setup-WLAN: %s\nSetup-Passwort: %s\nSetup: http://192.168.4.1\n", apName.c_str(), apPassword.c_str());
}
void stopAp() {
    if (!apActive) return;
    dns.stop();
    WiFi.softAPdisconnect(true);
    apActive = false;
    WiFi.mode(WIFI_STA);
}
void connectWifi() {
    WiFi.disconnect(false, false);
    if (!apActive) WiFi.mode(WIFI_STA);
    if (settings.ssid.isEmpty()) startAp();
    else WiFi.begin(settings.ssid.c_str(), settings.password.c_str());
    lastConnectAttempt = millis();
    offlineSince = millis();
}
void routes() {
    const char* headers[] = {"Content-Type", "Origin"};
    server.collectHeaders(headers, 2);
    server.on("/", HTTP_GET, [] {
        server.sendHeader("Cache-Control", "no-cache");
        server.send_P(200, "text/html; charset=utf-8", WEB_UI);
    });
    server.on("/api/v1/status", HTTP_GET, [] {
        const PlayerStatus p = player::status();
        DynamicJsonDocument response(2048);
        response["name"] = "CM-Radio";
        response["version"] = board::version;
        response["board"] = board::name;
        response["wifiConnected"] = WiFi.status() == WL_CONNECTED;
        response["ip"] = WiFi.localIP().toString();
        response["setupActive"] = apActive;
        response["setupSsid"] = apActive ? apName : "";
        response["rssi"] = WiFi.status() == WL_CONNECTED ? WiFi.RSSI() : 0;
        response["audioReady"] = p.ready;
        response["requested"] = p.requested;
        response["running"] = p.running;
        response["state"] = !p.ready ? "error" : !p.requested ? "stopped" : !p.running ? "connecting" : "streaming";
        response["stationIndex"] = settings.selected;
        response["station"] = settings.stations[settings.selected].name;
        response["title"] = p.title;
        response["message"] = diagnostic.isEmpty() ? p.message : diagnostic;
        response["volume"] = settings.volume;
        response["maxVolume"] = rules::maxVolume;
        response["autoplay"] = settings.autoplay;
        response["settingsPending"] = dirty;
        response["storageReady"] = storageReady;
        response["uptimeSeconds"] = millis() / 1000;
        response["freeHeap"] = ESP.getFreeHeap();
        response["psramBytes"] = ESP.getPsramSize();
        response["flashBytes"] = ESP.getFlashChipSize();
        sendJson(200, response);
    });
    server.on("/api/v1/stations", HTTP_GET, [] {
        DynamicJsonDocument response(12288);
        JsonArray list = response.createNestedArray("stations");
        for (size_t i = 0; i < settings.count; ++i) {
            JsonObject station = list.createNestedObject();
            station["name"] = settings.stations[i].name;
            station["url"] = settings.stations[i].url;
        }
        sendJson(200, response);
    });
    server.on("/api/v1/stations", HTTP_PUT, [] {
        DynamicJsonDocument request(12288);
        if (!body(request)) return;
        if (!request["stations"].is<JsonArray>()) { error(400, "stations muss ein Array sein"); return; }
        JsonArray list = request["stations"];
        if (list.size() == 0 || list.size() > rules::maxStations) { error(400, "1 bis 10 Sender erforderlich"); return; }
        Settings candidate = settings;
        candidate.count = list.size();
        candidate.selected = 0;
        const String current = settings.stations[settings.selected].url;
        bool currentFound = false;
        for (size_t i = 0; i < candidate.count; ++i) {
            if (!list[i]["name"].is<const char*>() || !list[i]["url"].is<const char*>()) { error(400, "Sender braucht name und url"); return; }
            String name = list[i]["name"].as<String>();
            String url = list[i]["url"].as<String>();
            name.trim(); url.trim();
            if (name.isEmpty() || name.length() >= rules::maxName || !rules::validUrl(url.c_str())) { error(400, "Ungueltiger Sendername oder HTTP(S)-Stream"); return; }
            candidate.stations[i] = {name, url};
            if (url == current) { candidate.selected = i; currentFound = true; }
        }
        if (!persist(candidate)) return;
        if (!currentFound && !player::stop()) { error(503, "Gespeichert; Audio-Warteschlange voll"); return; }
        accepted();
    });
    server.on("/api/v1/play", HTTP_POST, [] {
        StaticJsonDocument<256> request;
        if (!body(request)) return;
        if (!request["station"].is<int>()) { error(400, "station muss eine Ganzzahl sein"); return; }
        const int index = request["station"].as<int>();
        if (index < 0 || index >= static_cast<int>(settings.count)) { error(400, "Senderindex ungueltig"); return; }
        if (!player::status().ready) { error(503, "Audio nicht bereit"); return; }
        Settings candidate = settings;
        candidate.selected = index;
        if (!persist(candidate)) return;
        if (!player::play(settings.stations[index].url.c_str())) { error(503, "Audio-Warteschlange voll"); return; }
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
        if (value < 0 || value > rules::maxVolume) { error(400, "Lautstaerke muss 0 bis 21 sein"); return; }
        if (!player::volume(value)) { error(503, "Audio-Warteschlange voll"); return; }
        settings.volume = value;
        dirty = true;
        saveAt = millis() + 2000;
        accepted();
    });
    server.on("/api/v1/config", HTTP_GET, [] {
        StaticJsonDocument<256> response;
        response["ssid"] = settings.ssid;
        response["autoplay"] = settings.autoplay;
        sendJson(200, response);
    });
    server.on("/api/v1/config", HTTP_POST, [] {
        StaticJsonDocument<256> request;
        if (!body(request)) return;
        if (!request["autoplay"].is<bool>()) { error(400, "autoplay muss boolesch sein"); return; }
        Settings candidate = settings;
        candidate.autoplay = request["autoplay"].as<bool>();
        if (!persist(candidate)) return;
        accepted();
    });
    server.on("/api/v1/wifi", HTTP_POST, [] {
        StaticJsonDocument<512> request;
        if (!body(request)) return;
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
void serialCommands() {
    while (Serial.available()) {
        const char c = static_cast<char>(Serial.read());
        if (c == '\n') {
            serialLine.trim();
            if (serialLine == "setup") startAp();
            else if (serialLine == "status") {
                Serial.printf("CM-Radio %s | Flash %u | PSRAM %u | IP %s | Audio %s\n", board::version, ESP.getFlashChipSize(), ESP.getPsramSize(), WiFi.localIP().toString().c_str(), player::status().ready ? "bereit" : "Fehler");
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
    Serial.printf("\nCM-Radio %s | %s\nFlash: %u Bytes | PSRAM: %u Bytes\n", board::version, board::name, ESP.getFlashChipSize(), ESP.getPsramSize());
    storageReady = store.begin();
    if (!storageReady) diagnostic = "NVS-Speicher nicht verfuegbar";
    if (!store.load(settings)) diagnostic = "Gespeicherte Konfiguration ungueltig; Standard geladen";
    WiFi.persistent(false);
    WiFi.setHostname("cm-radio");
    WiFi.setSleep(false);
    WiFi.setAutoReconnect(true);
    char suffix[7];
    snprintf(suffix, sizeof(suffix), "%06X", static_cast<unsigned>(ESP.getEfuseMac() & 0xffffff));
    apName = "CM-Radio-" + String(suffix);
    char key[17];
    snprintf(key, sizeof(key), "%08X%08X", static_cast<unsigned>(esp_random()), static_cast<unsigned>(esp_random()));
    apPassword = key;
    if (!psramFound()) diagnostic = "PSRAM fehlt: Audio bleibt deaktiviert";
    else if (ESP.getFlashChipSize() != 8U * 1024U * 1024U) diagnostic = "Flashgroesse passt nicht zur WROVER-N8R8-Konfiguration";
    else if (!player::begin(settings.volume)) diagnostic = "Audio-Task konnte nicht gestartet werden";
    else if (settings.autoplay) player::play(settings.stations[settings.selected].url.c_str());
    connectWifi();
    routes();
    Serial.println("Serielle Befehle: status, setup, reset-wifi (jeweils mit Enter)");
}

void loop() {
    const uint32_t now = millis();
    server.handleClient();
    if (apActive) dns.processNextRequest();
    serialCommands();
    if (applyWifi && rules::reached(now, wifiAt)) {
        applyWifi = false;
        connectWifi();
    }
    const bool online = WiFi.status() == WL_CONNECTED;
    if (online && !wasOnline) {
        Serial.printf("WLAN verbunden: http://%s / http://cm-radio.local\n", WiFi.localIP().toString().c_str());
        stopAp();
        mdnsActive = MDNS.begin("cm-radio");
        if (mdnsActive) MDNS.addService("http", "tcp", 80);
    } else if (!online && wasOnline) {
        offlineSince = now;
        if (mdnsActive) MDNS.end();
        mdnsActive = false;
    }
    wasOnline = online;
    if (!online && !settings.ssid.isEmpty()) {
        if (now - offlineSince >= 30000) startAp();
        if (now - lastConnectAttempt >= 20000) {
            WiFi.begin(settings.ssid.c_str(), settings.password.c_str());
            lastConnectAttempt = now;
        }
    }
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

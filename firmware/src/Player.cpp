#include "Player.h"
#include "BoardConfig.h"
#include "PlaybackControls.h"
#include "FallbackPolicy.h"
#include <Audio.h>
#include <WiFi.h>
#include <memory>

namespace {
enum class Operation { Play, Stop, Volume, Configure, Sleep, Fallback };
struct Command { Operation operation; uint8_t volume; uint8_t limit; uint8_t seconds; uint16_t minutes; char url[rules::maxUrl]; char fallbackUrl[rules::maxUrl]; };
QueueHandle_t commands;
portMUX_TYPE stateLock = portMUX_INITIALIZER_UNLOCKED;
PlayerStatus snapshot;
bool updateRequested = false;
uint8_t initialLimit = 21, initialSoftStart = 5;
void message(const char* text) {
    portENTER_CRITICAL(&stateLock);
    strlcpy(snapshot.message, text ? text : "", sizeof(snapshot.message));
    portEXIT_CRITICAL(&stateLock);
}
void audioWorker(void*) {
    // All Audio methods belong to this task. HTTP never touches the decoder.
    std::unique_ptr<Audio> audio(new Audio);
    audio->setConnectionTimeout(1800, 2500);
    if (!audio->setPinout(board::bclk, board::lrclk, board::data)) {
        message("I2S konnte nicht initialisiert werden");
        vTaskDelete(nullptr);
        return;
    }
    VolumeEnvelope envelope;
    SleepTimer sleepTimer;
    FallbackPolicy fallbackPolicy;
    char fallbackUrl[rules::maxUrl] = {};
    envelope.configure(initialLimit, initialSoftStart, snapshot.volume);
    uint8_t vol = envelope.tick(millis());
    audio->setVolume(vol);
    bool wasRunning = false;
    portENTER_CRITICAL(&stateLock);
    snapshot.ready = true;
    portEXIT_CRITICAL(&stateLock);
    char requestedUrl[rules::maxUrl] = {};
    bool wanted = false;
    uint32_t nextRetry = 0;
    unsigned attempts = 0;
    for (;;) {
        portENTER_CRITICAL(&stateLock);
        const bool updating = updateRequested;
        portEXIT_CRITICAL(&stateLock);
        if (updating) {
            if (!snapshot.updating) {
                digitalWrite(board::amplifierEnable, LOW);
                audio->stopSong();wanted = false;wasRunning = false;
                sleepTimer.cancel();envelope.stop();fallbackPolicy.reset();
                requestedUrl[0] = '\0';xQueueReset(commands);
                portENTER_CRITICAL(&stateLock);
                snapshot.updating = true;snapshot.requested = false;snapshot.running = false;
                snapshot.sleepRemainingSeconds = 0;snapshot.fallbackActive = false;snapshot.actualUrl[0] = '\0';snapshot.title[0] = '\0';
                portEXIT_CRITICAL(&stateLock);
                message("Firmwareupdate; Audio gestoppt");
            }
            vTaskDelay(pdMS_TO_TICKS(10));continue;
        }
        portENTER_CRITICAL(&stateLock);snapshot.updating = false;portEXIT_CRITICAL(&stateLock);
        Command c{};
        while (xQueueReceive(commands, &c, 0) == pdTRUE) {
            if (c.operation == Operation::Volume) {
                envelope.setTarget(c.volume);
            } else if (c.operation == Operation::Configure) {
                envelope.configure(c.limit, c.seconds, c.volume);
            } else if (c.operation == Operation::Sleep) {
                sleepTimer.set(millis(), c.minutes);
            } else if (c.operation == Operation::Fallback) {
                strlcpy(fallbackUrl, c.url, sizeof(fallbackUrl));
            } else {
                digitalWrite(board::amplifierEnable, LOW);
                audio->stopSong();
                wanted = c.operation == Operation::Play;
                fallbackPolicy.reset();
                if (wanted) strlcpy(fallbackUrl, c.fallbackUrl, sizeof(fallbackUrl));
                wasRunning = false;
                if (wanted) envelope.prepare();
                else { envelope.stop(); sleepTimer.cancel(); }
                audio->setVolume(envelope.tick(millis()));
                strlcpy(requestedUrl, wanted ? c.url : "", sizeof(requestedUrl));
                attempts = 0;
                nextRetry = millis();
                portENTER_CRITICAL(&stateLock);
                snapshot.title[0] = '\0';
                portEXIT_CRITICAL(&stateLock);
                message(wanted ? "Stream wird verbunden" : "Gestoppt");
            }
        }
        if (sleepTimer.expired(millis())) {
            wanted = false;
            fallbackPolicy.reset();
            requestedUrl[0] = '\0';
            envelope.stop();
            digitalWrite(board::amplifierEnable, LOW);
            audio->stopSong();
            portENTER_CRITICAL(&stateLock);
            snapshot.title[0] = '\0';
            portEXIT_CRITICAL(&stateLock);
            message("Sleep-Timer abgelaufen");
        }
        const bool online = WiFi.status() == WL_CONNECTED;
        if (!online) fallbackPolicy.offline();
        if (!online && audio->isRunning()) {
            digitalWrite(board::amplifierEnable, LOW);
            audio->stopSong();
            message("Warte auf WLAN");
        }
        if (wanted && online && !audio->isRunning() && rules::reached(millis(), nextRetry)) {
            digitalWrite(board::amplifierEnable, LOW);
            if (fallbackPolicy.switchNow(online, fallbackUrl[0] && strcmp(fallbackUrl, requestedUrl) != 0)) {
                strlcpy(requestedUrl, fallbackUrl, sizeof(requestedUrl));
                attempts = 0;
                portENTER_CRITICAL(&stateLock);
                snapshot.title[0] = '\0';
                portEXIT_CRITICAL(&stateLock);
                message("Wechsel auf Ersatzsender");
            }
            fallbackPolicy.attempted();
            envelope.prepare();
            audio->setVolume(envelope.tick(millis()));
            const bool connected = audio->connecttohost(requestedUrl);
            nextRetry = millis() + rules::retryDelay(attempts++);
            if (!connected) message("Stream nicht erreichbar; neuer Versuch folgt");
            else message("Stream verbunden; Audio wird gepuffert");
        }
        audio->loop();
        const bool running = audio->isRunning() && online;
        if (running && !wasRunning) envelope.start(millis());
        if (!running && wasRunning) envelope.stop();
        wasRunning = running;
        const uint8_t effective = envelope.tick(millis());
        if (vol != effective) { vol = effective; audio->setVolume(vol); }
        digitalWrite(board::amplifierEnable, running && online && vol > 0 ? HIGH : LOW);
        if (running && audio->getAudioCurrentTime() > 5) { attempts = 0; fallbackPolicy.stable(); }
        portENTER_CRITICAL(&stateLock);
        snapshot.requested = wanted;
        snapshot.running = running && online;
        snapshot.volume = vol;
        snapshot.ramping = envelope.ramping();
        snapshot.fallbackActive = wanted && fallbackPolicy.active();
        strlcpy(snapshot.actualUrl, wanted ? requestedUrl : "", sizeof(snapshot.actualUrl));
        snapshot.sleepRemainingSeconds = sleepTimer.remaining(millis());
        portEXIT_CRITICAL(&stateLock);
        vTaskDelay(1);
    }
}
bool enqueue(const Command& command) {
    return commands && xQueueSend(commands, &command, 0) == pdTRUE;
}
}

bool player::begin(uint8_t volume, uint8_t limit, uint8_t softStartSeconds) {
    initialLimit = limit;
    initialSoftStart = softStartSeconds;
    pinMode(board::amplifierEnable, OUTPUT);
    digitalWrite(board::amplifierEnable, LOW);
    snapshot.volume = volume > limit ? limit : volume;
    commands = xQueueCreate(8, sizeof(Command));
    if (!commands) return false;
    return xTaskCreatePinnedToCore(audioWorker, "CM-RadioAudio", 12288, nullptr, 2, nullptr, 0) == pdPASS;
}
bool player::play(const char* url, const char* fallbackUrl) {
    if (!rules::validUrl(url) || (fallbackUrl[0] && !rules::validUrl(fallbackUrl))) return false;
    Command c{};
    c.operation = Operation::Play;
    strlcpy(c.url, url, sizeof(c.url));
    strlcpy(c.fallbackUrl, fallbackUrl, sizeof(c.fallbackUrl));
    return enqueue(c);
}
bool player::fallback(const char* url) {
    if (url[0] && !rules::validUrl(url)) return false;
    Command c{};c.operation = Operation::Fallback;strlcpy(c.url, url, sizeof(c.url));return enqueue(c);
}
bool player::stop() {
    Command c{};
    c.operation = Operation::Stop;
    return enqueue(c);
}
bool player::volume(uint8_t value) {
    if (value > rules::maxVolume) return false;
    Command c{};
    c.operation = Operation::Volume;
    c.volume = value;
    return enqueue(c);
}
bool player::configure(uint8_t limit, uint8_t seconds, uint8_t volume) {
    if (limit > 21 || seconds > 30 || volume > limit) return false;
    Command c{};
    c.operation = Operation::Configure;
    c.limit = limit; c.seconds = seconds; c.volume = volume;
    return enqueue(c);
}
bool player::sleep(unsigned minutes) {
    if (minutes > 180) return false;
    Command c{};
    c.operation = Operation::Sleep;
    c.minutes = minutes;
    return enqueue(c);
}
PlayerStatus player::status() {
    portENTER_CRITICAL(&stateLock);
    const PlayerStatus s = snapshot;
    portEXIT_CRITICAL(&stateLock);
    return s;
}
void audio_info(const char* info) { message(info); }
void audio_showstreamtitle(const char* title) {
    portENTER_CRITICAL(&stateLock);
    strlcpy(snapshot.title, title ? title : "", sizeof(snapshot.title));
    portEXIT_CRITICAL(&stateLock);
}

void player::setUpdating(bool updating) {
    portENTER_CRITICAL(&stateLock);updateRequested = updating;portEXIT_CRITICAL(&stateLock);
}

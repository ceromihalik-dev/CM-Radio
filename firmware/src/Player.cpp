#include "Player.h"
#include "BoardConfig.h"
#include <Audio.h>
#include <WiFi.h>
#include <memory>

namespace {
enum class Operation { Play, Stop, Volume };
struct Command { Operation operation; uint8_t volume; char url[rules::maxUrl]; };
QueueHandle_t commands;
portMUX_TYPE stateLock = portMUX_INITIALIZER_UNLOCKED;
PlayerStatus snapshot;
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
    uint8_t vol = snapshot.volume;
    audio->setVolume(vol);
    portENTER_CRITICAL(&stateLock);
    snapshot.ready = true;
    portEXIT_CRITICAL(&stateLock);
    char requestedUrl[rules::maxUrl] = {};
    bool wanted = false;
    uint32_t nextRetry = 0;
    unsigned attempts = 0;
    for (;;) {
        Command c{};
        while (xQueueReceive(commands, &c, 0) == pdTRUE) {
            if (c.operation == Operation::Volume) {
                vol = c.volume;
                audio->setVolume(vol);
            } else {
                digitalWrite(board::amplifierEnable, LOW);
                audio->stopSong();
                wanted = c.operation == Operation::Play;
                strlcpy(requestedUrl, wanted ? c.url : "", sizeof(requestedUrl));
                attempts = 0;
                nextRetry = millis();
                portENTER_CRITICAL(&stateLock);
                snapshot.title[0] = '\0';
                portEXIT_CRITICAL(&stateLock);
                message(wanted ? "Stream wird verbunden" : "Gestoppt");
            }
        }
        const bool online = WiFi.status() == WL_CONNECTED;
        if (!online && audio->isRunning()) {
            digitalWrite(board::amplifierEnable, LOW);
            audio->stopSong();
            message("Warte auf WLAN");
        }
        if (wanted && online && !audio->isRunning() && rules::reached(millis(), nextRetry)) {
            digitalWrite(board::amplifierEnable, LOW);
            const bool connected = audio->connecttohost(requestedUrl);
            nextRetry = millis() + rules::retryDelay(attempts++);
            if (!connected) message("Stream nicht erreichbar; neuer Versuch folgt");
            else message("Stream verbunden; Audio wird gepuffert");
        }
        audio->loop();
        const bool running = audio->isRunning();
        digitalWrite(board::amplifierEnable, running && online && vol > 0 ? HIGH : LOW);
        if (running && audio->getAudioCurrentTime() > 5) attempts = 0;
        portENTER_CRITICAL(&stateLock);
        snapshot.requested = wanted;
        snapshot.running = running && online;
        snapshot.volume = vol;
        portEXIT_CRITICAL(&stateLock);
        vTaskDelay(1);
    }
}
bool enqueue(const Command& command) {
    return commands && xQueueSend(commands, &command, 0) == pdTRUE;
}
}

bool player::begin(uint8_t volume) {
    pinMode(board::amplifierEnable, OUTPUT);
    digitalWrite(board::amplifierEnable, LOW);
    snapshot.volume = volume;
    commands = xQueueCreate(8, sizeof(Command));
    if (!commands) return false;
    return xTaskCreatePinnedToCore(audioWorker, "CM-RadioAudio", 12288, nullptr, 2, nullptr, 0) == pdPASS;
}
bool player::play(const char* url) {
    if (!rules::validUrl(url)) return false;
    Command c{};
    c.operation = Operation::Play;
    strlcpy(c.url, url, sizeof(c.url));
    return enqueue(c);
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

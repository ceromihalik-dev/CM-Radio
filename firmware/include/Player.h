#pragma once
#include <Arduino.h>
#include "Validation.h"

struct PlayerStatus {
    bool requested = false;
    bool running = false;
    bool ready = false;
    bool updating = false;
    uint8_t volume = 5;
    bool ramping = false;
    bool fallbackActive = false;
    char actualUrl[rules::maxUrl] = {};
    uint32_t sleepRemainingSeconds = 0;
    char title[192] = {};
    char message[192] = {};
};
namespace player {
bool begin(uint8_t volume, uint8_t limit, uint8_t softStartSeconds);
bool configure(uint8_t limit, uint8_t softStartSeconds, uint8_t volume);
bool sleep(unsigned minutes);
bool play(const char* url, const char* fallbackUrl = "");
bool fallback(const char* url);
bool stop();
void setUpdating(bool updating);
bool volume(uint8_t value);
PlayerStatus status();
}

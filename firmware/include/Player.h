#pragma once
#include <Arduino.h>
#include "Validation.h"

struct PlayerStatus {
    bool requested = false;
    bool running = false;
    bool ready = false;
    uint8_t volume = 5;
    char title[192] = {};
    char message[192] = {};
};
namespace player {
bool begin(uint8_t volume);
bool play(const char* url);
bool stop();
bool volume(uint8_t value);
PlayerStatus status();
}

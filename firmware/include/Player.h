#pragma once
#include <Arduino.h>
#include "Validation.h"

struct PlayerStatus {
    uint32_t connectionAttempts=0,streamBreaks=0,consecutiveAttempts=0,streamSeconds=0;
    char lastError[128]={};
    bool mono=false;
    bool requested = false;
    bool running = false;
    bool ready = false;
    bool updating = false;
    uint8_t volume = 11;
    bool ramping = false;
    int8_t effectiveBass = 0, effectiveTreble = 0;
    bool fallbackActive = false;
    char actualUrl[rules::maxUrl] = {};
    uint32_t sleepRemainingSeconds = 0;
    char title[192] = {};
    char message[192] = {};
};
namespace player {
bool begin(uint8_t volume, uint8_t limit, uint8_t softStartSeconds, int8_t bass = 0, int8_t treble = 0, int8_t balance = 0, bool loudness = false,bool mono = false);
bool configure(uint8_t limit, uint8_t softStartSeconds, uint8_t volume);
bool sound(int bass, int treble, int balance, bool loudness = false);
bool mono(bool enabled);
bool sleep(unsigned minutes);
bool play(const char* url, const char* fallbackUrl = "");
bool fallback(const char* url);
bool stop();
void setUpdating(bool updating);
bool volume(uint8_t value);
PlayerStatus status();
}

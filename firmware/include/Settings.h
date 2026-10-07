#pragma once
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include "Validation.h"

struct Station { String name; String url; };
struct Settings {
    String ssid;
    String password;
    Station stations[rules::maxStations];
    size_t count = 1;
    size_t selected = 0;
    uint8_t volume = 5;
    bool autoplay = true;
};
class SettingsStore {
public:
    bool begin();
    bool load(Settings& value);
    bool save(const Settings& value);
private:
    Preferences preferences;
};

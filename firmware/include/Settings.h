#pragma once
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include "Validation.h"

struct Station { String name; String url; String logo; };
struct Settings {
    String ssid;
    String password;
    Station stations[rules::maxStations];
    size_t count = 1;
    size_t selected = 0;
    uint8_t volume = 11;
    bool autoplay = true;
    bool loudness = false;
    uint8_t volumeLimit = 50;
    uint8_t softStartSeconds = 5;
    int fallbackStation = -1;
    int8_t bass = 0, treble = 0, balance = 0;
};
class SettingsStore {
public:
    bool begin();
    String setupPassword();
    bool saveSetupPassword(const String& password);
    bool resetSetupPassword();
    bool load(Settings& value);
    bool save(const Settings& value);
private:
    Preferences preferences;
};

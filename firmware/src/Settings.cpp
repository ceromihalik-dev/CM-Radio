#include "Settings.h"

bool SettingsStore::begin() { return preferences.begin("cm-radio", false); }
bool SettingsStore::load(Settings& s) {
    s = Settings{};
    s.stations[0] = {"Radio Paradise (Teststream)", "http://stream.radioparadise.com/mp3-128"};
    const String raw = preferences.getString("config", "");
    if (raw.isEmpty()) return true;
    if (raw.length() > 8192) return false;
    DynamicJsonDocument d(12288);
    if (deserializeJson(d, raw) || d["schema"].as<int>() != 1) return false;
    const String ssid = d["ssid"] | "";
    const String password = d["password"] | "";
    if (!ssid.isEmpty() && !rules::validWifi(ssid.c_str(), password.c_str())) return false;
    const JsonArray list = d["stations"].as<JsonArray>();
    if (list.size() == 0 || list.size() > rules::maxStations) return false;
    Settings candidate;
    candidate.ssid = ssid;
    candidate.password = password;
    candidate.count = list.size();
    for (size_t i = 0; i < candidate.count; ++i) {
        const String name = list[i]["name"] | "";
        const String url = list[i]["url"] | "";
        if (name.isEmpty() || name.length() >= rules::maxName || !rules::validUrl(url.c_str())) return false;
        candidate.stations[i] = {name, url};
    }
    const int selected = d["selected"] | 0;
    const int volume = d["volume"] | 5;
    if (selected < 0 || selected >= static_cast<int>(candidate.count) || volume < 0 || volume > rules::maxVolume) return false;
    candidate.selected = selected;
    candidate.volume = volume;
    candidate.autoplay = d["autoplay"] | true;
    s = candidate;
    return true;
}
bool SettingsStore::save(const Settings& s) {
    DynamicJsonDocument d(12288);
    d["schema"] = 1;
    d["ssid"] = s.ssid;
    d["password"] = s.password;
    d["selected"] = s.selected;
    d["volume"] = s.volume;
    d["autoplay"] = s.autoplay;
    JsonArray list = d.createNestedArray("stations");
    for (size_t i = 0; i < s.count; ++i) {
        JsonObject station = list.createNestedObject();
        station["name"] = s.stations[i].name;
        station["url"] = s.stations[i].url;
    }
    if (d.overflowed()) return false;
    String raw;
    serializeJson(d, raw);
    return preferences.putString("config", raw) == raw.length();
}

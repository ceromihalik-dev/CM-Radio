#include "Settings.h"
#include "SoundConfig.h"

bool SettingsStore::begin() { return preferences.begin("cm-radio", false); }
bool SettingsStore::load(Settings& s) {
    s = Settings{};
    s.stations[0] = {"Radio Paradise (Teststream)", "http://stream.radioparadise.com/mp3-128"};
    const String raw = preferences.getString("config", "");
    if (raw.isEmpty()) return true;
    if (raw.length() > 8192) return false;
    DynamicJsonDocument d(12288);
    if (deserializeJson(d, raw)) return false;
    const int schema = d["schema"] | 0;
    if (schema != 1) return false;
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
    if (d.containsKey("volumeLimit") && !d["volumeLimit"].is<int>()) return false;
    if (d.containsKey("softStartSeconds") && !d["softStartSeconds"].is<int>()) return false;
    const int limit = d["volumeLimit"] | 21;
    const int softStart = d["softStartSeconds"] | 5;
    if (limit < 0 || limit > 21 || softStart < 0 || softStart > 30) return false;
    candidate.volumeLimit = limit;
    if (d.containsKey("fallbackStation") && !d["fallbackStation"].is<int>()) return false;
    const int fallback = d["fallbackStation"] | -1;
    if (fallback < -1 || fallback >= static_cast<int>(candidate.count)) return false;
    candidate.fallbackStation = fallback;
    candidate.softStartSeconds = softStart;
    candidate.volume = volume > limit ? limit : volume;
    int bass=0,treble=0,balance=0;
    if (!sound::read(d.as<JsonObjectConst>(),bass,treble,balance)) return false;
    candidate.bass=bass;candidate.treble=treble;candidate.balance=balance;
    candidate.autoplay = d["autoplay"] | true;
    s = candidate;
    return true;
}
bool SettingsStore::save(const Settings& s) {
    DynamicJsonDocument d(12288);
    d["schema"] = 1;
    d["bass"]=s.bass;d["treble"]=s.treble;d["balance"]=s.balance;
    d["ssid"] = s.ssid;
    d["password"] = s.password;
    d["selected"] = s.selected;
    d["volume"] = s.volume;
    d["autoplay"] = s.autoplay;
    d["volumeLimit"] = s.volumeLimit;
    d["softStartSeconds"] = s.softStartSeconds;
    d["fallbackStation"] = s.fallbackStation;
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

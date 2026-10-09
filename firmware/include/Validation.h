#pragma once
#include <stdint.h>
#include <stddef.h>
#include <string.h>

namespace rules {
constexpr size_t maxStations = 10;
constexpr size_t maxName = 64;
constexpr size_t maxUrl = 384;
constexpr uint8_t maxVolume = 50;
// Round down so migration never increases the stored maximum gain.
inline int legacyVolume(int value) { return value * 50 / 21; }
inline bool validUrl(const char* url) {
    if (!url || strlen(url) < 8 || strlen(url) >= maxUrl) return false;
    const char* host = nullptr;
    if (strncmp(url, "http://", 7) == 0) host = url + 7;
    else if (strncmp(url, "https://", 8) == 0) host = url + 8;
    else return false;
    if (!*host || *host == '/' || *host == '?' || *host == '#') return false;
    for (const char* p = url; *p; ++p)
        if (static_cast<unsigned char>(*p) <= 32 || *p == 127 || *p == '\\') return false;
    for (const char* p = host; *p && *p != '/' && *p != '?' && *p != '#'; ++p)
        if (*p == '@') return false;
    return true;
}
inline bool validLogo(const char* url){return url && (!*url || (strncmp(url,"https://",8)==0 && validUrl(url)));}
inline bool validWifi(const char* ssid, const char* password) {
    if (!ssid || !password || !*ssid || strlen(ssid) > 32) return false;
    const size_t n = strlen(password);
    return n == 0 || (n >= 8 && n <= 63);
}
inline uint32_t retryDelay(unsigned attempt) {
    const unsigned shift = attempt > 4 ? 4 : attempt;
    return 2000U << shift;
}
inline bool reached(uint32_t now, uint32_t deadline) {
    return static_cast<int32_t>(now - deadline) >= 0;
}
}

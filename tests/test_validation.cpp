#include "Validation.h"
#include <cassert>
#include <string>
#include <iostream>
int main() {
    assert(rules::validUrl("http://stream.example.org:8000/live.mp3"));
    assert(rules::validUrl("https://stream.example.org/live?format=aac"));
    for (const char* bad : {"", "https://", "http:///live", "http://?q", "ftp://example.org/live", "http://user:secret@example.org/live", "http://example.org/with space", "http://example.org/\nHeader:bad", "http://example.org/\\bad"})
        assert(!rules::validUrl(bad));
    assert(!rules::validUrl(nullptr));
    assert(!rules::validUrl(("http://example.org/" + std::string(384, 'a')).c_str()));
    assert(rules::validWifi("Home", "12345678"));
    assert(rules::validWifi("Open", ""));
    assert(!rules::validWifi("", "12345678"));
    assert(!rules::validWifi("Home", "1234567"));
    assert(!rules::validWifi(std::string(33, 's').c_str(), "12345678"));
    assert(!rules::validWifi("Home", std::string(64, 'p').c_str()));
    assert(rules::retryDelay(0) == 2000);
    assert(rules::retryDelay(1) == 4000);
    assert(rules::retryDelay(99) == 32000);
    assert(!rules::reached(0xfffffff0U, 0x00000010U));
    assert(rules::reached(0x00000011U, 0x00000010U));
    assert(rules::reached(123, 123));
    std::cout << "URL/WLAN validation, reconnect limits, millis rollover: PASS\n";
}

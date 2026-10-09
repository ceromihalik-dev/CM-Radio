#pragma once
#include <WebServer.h>
#include <ArduinoJson.h>
#include <functional>
namespace firmwareUpdate {
void begin(WebServer& server,std::function<bool()> flushSettings);
bool busy();
void tick();
void status(JsonObject response);
}

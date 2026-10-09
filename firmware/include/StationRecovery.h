#pragma once
#include <Arduino.h>
#include "Validation.h"
namespace recovery {
struct Job {uint32_t epoch;int index;char name[rules::maxName],url[rules::maxUrl],id[37];};
struct Result {Job job;bool found;char url[rules::maxUrl],id[37],message[128];};
bool begin();bool request(const Job& job);bool take(Result& result);bool busy();
}

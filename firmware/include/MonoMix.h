#pragma once
#include <stdint.h>
namespace monoMix {
inline void frame(int16_t* samples) {
    const int16_t mixed = (int32_t(samples[0]) + int32_t(samples[1])) / 2;
    samples[0] = mixed; samples[1] = mixed;
}
}

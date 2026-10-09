#pragma once
#include <stdint.h>

class SleepTimer {
public:
    bool set(uint32_t now, unsigned minutes) {
        if (minutes > 180) return false;
        active_ = minutes != 0;
        deadline_ = now + minutes * 60000U;
        return true;
    }
    void cancel() { active_ = false; }
    bool expired(uint32_t now) {
        if (!active_ || static_cast<int32_t>(now - deadline_) < 0) return false;
        active_ = false;
        return true;
    }
    uint32_t remaining(uint32_t now) const {
        if (!active_ || static_cast<int32_t>(now - deadline_) >= 0) return 0;
        return (deadline_ - now + 999U) / 1000U;
    }
private:
    bool active_ = false;
    uint32_t deadline_ = 0;
};

class VolumeEnvelope {
public:
    void configure(uint8_t limit, uint8_t seconds, uint8_t target) {
        limit_ = limit > 21 ? 21 : limit;
        seconds_ = seconds > 30 ? 30 : seconds;
        setTarget(target);
    }
    void setTarget(uint8_t target) {
        target_ = target > limit_ ? limit_ : target;
        current_ = target_;
        ramping_ = false;
    }
    void prepare() { current_ = seconds_ ? 0 : target_; ramping_ = false; }
    void start(uint32_t now) {
        began_ = now;
        current_ = seconds_ ? 0 : target_;
        ramping_ = seconds_ != 0 && target_ != 0;
    }
    void stop() { current_ = 0; ramping_ = false; }
    uint8_t tick(uint32_t now) {
        if (ramping_) {
            const uint32_t elapsed = now - began_;
            const uint32_t duration = seconds_ * 1000U;
            if (elapsed >= duration) { current_ = target_; ramping_ = false; }
            else current_ = target_ * elapsed / duration;
        }
        return current_;
    }
    bool ramping() const { return ramping_; }
private:
    uint8_t limit_ = 21, seconds_ = 5, target_ = 5, current_ = 5;
    bool ramping_ = false;
    uint32_t began_ = 0;
};

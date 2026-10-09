#pragma once
#include <stdint.h>

// The Arduino WiFi scan API returns -1 while running and -2 on failure.
// Keep connection retries paused from preparation until completion/timeout.
class WifiScan {
public:
    bool busy() const { return preparing_ || running_; }
    bool started() const { return started_; }
    int result() const { return result_; }
    template<class Driver> void request(uint32_t now, Driver& driver) {
        if (busy()) return;
        driver.prepare();
        started_ = true;
        preparing_ = true;
        running_ = false;
        result_ = -1;
        attempts_ = 0;
        began_ = now;
        due_ = now + 300;
    }
    template<class Driver> void tick(uint32_t now, Driver& driver) {
        if (!busy()) return;
        if (uint32_t(now - began_) >= 12000) { driver.cancel(); finish(-2, driver); return; }
        if (preparing_ && int32_t(now - due_) >= 0) {
            const int result = driver.start();
            ++attempts_;
            if (result == -2) {
                if (attempts_ >= 3) finish(-2, driver);
                else due_ = now + 500;
            } else {
                preparing_ = false;
                running_ = result == -1;
                if (!running_) finish(result, driver);
            }
        } else if (running_) {
            const int result = driver.complete();
            if (result != -1) finish(result, driver);
        }
    }
private:
    template<class Driver> void finish(int result, Driver& driver) {
        result_ = result;
        preparing_ = running_ = false;
        driver.restore();
    }
    bool preparing_ = false, running_ = false, started_ = false;
    int result_ = -2;
    uint8_t attempts_ = 0;
    uint32_t began_ = 0, due_ = 0;
};

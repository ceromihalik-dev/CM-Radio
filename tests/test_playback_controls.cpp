#include "PlaybackControls.h"
#include "PasswordResetButton.h"
#include <cassert>
#include <cstdio>
int main(){
 PasswordResetButton button;assert(button.tick(true,0)==PasswordResetButton::None);assert(button.tick(true,40000)==PasswordResetButton::None);assert(button.tick(false,40001)==PasswordResetButton::None);
 assert(button.tick(true,50000)==PasswordResetButton::None);assert(button.tick(false,59999)==PasswordResetButton::None);
 button.tick(true,60000);assert(button.tick(true,70000)==PasswordResetButton::None);assert(button.tick(false,70000)==PasswordResetButton::Password);assert(button.tick(false,70001)==PasswordResetButton::None);
 button.tick(true,80000);assert(button.tick(false,139999)==PasswordResetButton::Password);
 button.tick(true,150000);assert(button.tick(true,210000)==PasswordResetButton::None);assert(button.tick(false,210000)==PasswordResetButton::Factory);assert(button.tick(false,210001)==PasswordResetButton::None);
 button.tick(true,220000);button.inhibit();assert(button.tick(true,300000)==PasswordResetButton::None);assert(button.tick(false,300001)==PasswordResetButton::None);
 PasswordResetButton rollover;rollover.tick(false,0);rollover.tick(true,0xfffffff0U);assert(rollover.tick(false,9984)==PasswordResetButton::Password);
 SleepTimer timer;assert(timer.remaining(0)==0);assert(!timer.set(0,181));
 assert(timer.set(1000,1));assert(timer.remaining(1000)==60);assert(!timer.expired(60999));assert(timer.expired(61000));assert(!timer.expired(61001));
 timer.set(100,30);timer.set(200,15);assert(timer.remaining(200)==900);timer.cancel();assert(!timer.expired(999999));
 timer.set(0xfffffff0U,1);assert(timer.remaining(0xfffffff0U)==60);assert(timer.expired(59984));timer.set(0,0);assert(timer.remaining(0)==0);
 VolumeEnvelope envelope;envelope.configure(10,5,20);envelope.prepare();assert(envelope.tick(0)==0);envelope.start(1000);assert(envelope.tick(3500)==5);assert(envelope.tick(6000)==10);assert(!envelope.ramping());
 envelope.start(10000);envelope.setTarget(50);assert(envelope.tick(10001)==10 && !envelope.ramping());envelope.stop();assert(envelope.tick(10002)==0);
 envelope.configure(3,5,10);assert(envelope.tick(0)==3);envelope.start(0xfffffff0U);assert(envelope.tick(2484)==1);assert(envelope.tick(4984)==3);
 envelope.configure(0,5,10);envelope.start(0);assert(envelope.tick(100000)==0 && !envelope.ramping());
 envelope.configure(21,0,8);envelope.prepare();assert(envelope.tick(0)==8);envelope.start(0);assert(!envelope.ramping());
 envelope.configure(50,5,50);envelope.start(1000);assert(envelope.tick(3500)==25);assert(envelope.tick(6000)==50);envelope.configure(255,0,255);assert(envelope.tick(0)==50);
 puts("Sleep timer expiry, replace/cancel, bounds, volume ceiling, ramp, manual override and rollover: PASS");
}

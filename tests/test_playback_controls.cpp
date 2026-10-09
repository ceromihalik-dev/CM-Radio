#include "PlaybackControls.h"
#include "PasswordResetButton.h"
#include <cassert>
#include <cstdio>
int main(){
 PasswordResetButton button;assert(!button.tick(true,0));assert(!button.tick(true,15000));assert(!button.tick(false,15001));assert(!button.tick(true,16000));assert(!button.tick(true,25999));assert(button.tick(true,26000));assert(!button.tick(true,40000));assert(!button.tick(false,40001));assert(!button.tick(true,50000));assert(!button.tick(false,51000));assert(!button.tick(true,60000));assert(!button.tick(true,69999));assert(button.tick(true,70000));
 PasswordResetButton rollover;rollover.tick(false,0);rollover.tick(true,0xfffffff0U);assert(!rollover.tick(true,9983));assert(rollover.tick(true,9984));
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

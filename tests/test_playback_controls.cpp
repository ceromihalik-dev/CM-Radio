#include "PlaybackControls.h"
#include <cassert>
#include <cstdio>
int main(){
 SleepTimer timer;assert(timer.remaining(0)==0);assert(!timer.set(0,181));
 assert(timer.set(1000,1));assert(timer.remaining(1000)==60);assert(!timer.expired(60999));assert(timer.expired(61000));assert(!timer.expired(61001));
 timer.set(100,30);timer.set(200,15);assert(timer.remaining(200)==900);timer.cancel();assert(!timer.expired(999999));
 timer.set(0xfffffff0U,1);assert(timer.remaining(0xfffffff0U)==60);assert(timer.expired(59984));timer.set(0,0);assert(timer.remaining(0)==0);
 VolumeEnvelope envelope;envelope.configure(10,5,20);envelope.prepare();assert(envelope.tick(0)==0);envelope.start(1000);assert(envelope.tick(3500)==5);assert(envelope.tick(6000)==10);assert(!envelope.ramping());
 envelope.start(10000);envelope.setTarget(50);assert(envelope.tick(10001)==10 && !envelope.ramping());envelope.stop();assert(envelope.tick(10002)==0);
 envelope.configure(3,5,10);assert(envelope.tick(0)==3);envelope.start(0xfffffff0U);assert(envelope.tick(2484)==1);assert(envelope.tick(4984)==3);
 envelope.configure(0,5,10);envelope.start(0);assert(envelope.tick(100000)==0 && !envelope.ramping());
 envelope.configure(21,0,8);envelope.prepare();assert(envelope.tick(0)==8);envelope.start(0);assert(!envelope.ramping());
 puts("Sleep timer expiry, replace/cancel, bounds, volume ceiling, ramp, manual override and rollover: PASS");
}

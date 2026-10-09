#pragma once
#include <stdint.h>
class FallbackPolicy {
public:
 void reset(){attempts_=0;active_=false;}
 void attempted(){if(!active_&&attempts_<3)++attempts_;}
 void stable(){attempts_=0;}
 void offline(){attempts_=0;}
 bool switchNow(bool online,bool distinct){if(!online||!distinct||active_||attempts_<3)return false;active_=true;return true;}
 bool active()const{return active_;}
private:
 uint8_t attempts_=0;bool active_=false;
};

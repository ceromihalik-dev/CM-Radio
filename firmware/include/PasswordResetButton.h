#pragma once
#include <stdint.h>
// Start only after an observed release; one reset per ten-second hold.
class PasswordResetButton {
public:
 bool tick(bool pressed,uint32_t now){
  if(!pressed){armed_=true;holding_=false;fired_=false;return false;}
  if(!armed_||fired_)return false;
  if(!holding_){holding_=true;began_=now;return false;}
  if(now-began_<10000U)return false;
  fired_=true;return true;
 }
private:
 bool armed_=false,holding_=false,fired_=false;
 uint32_t began_=0;
};

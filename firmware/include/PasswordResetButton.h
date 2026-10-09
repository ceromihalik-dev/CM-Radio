#pragma once
#include <stdint.h>
// Action is decided on release, so a factory-reset hold never triggers an
// earlier password reset. A button held during boot must first be released.
class PasswordResetButton {
public:
 enum Action {None,Password,Factory};
 void inhibit(){armed_=false;holding_=false;}
 Action tick(bool pressed,uint32_t now){
  if(!pressed){
   armed_=true;
   if(!holding_)return None;
   holding_=false;
   const uint32_t duration=now-began_;
   return duration>=60000U?Factory:duration>=10000U?Password:None;
  }
  if(armed_&&!holding_){holding_=true;began_=now;}
  return None;
 }
private:
 bool armed_=false,holding_=false;
 uint32_t began_=0;
};

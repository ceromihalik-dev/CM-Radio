#pragma once
#include <ArduinoJson.h>
namespace sound {
inline bool valid(int bass,int treble,int balance){return bass>=-12&&bass<=6&&treble>=-12&&treble<=6&&balance>=-16&&balance<=16;}
// Optional fields preserve old NVS and schema-1 backups; supplied fields must be strict integers.
inline bool read(JsonObjectConst object,int& bass,int& treble,int& balance){
 const char* keys[]={"bass","treble","balance"};int* values[]={&bass,&treble,&balance};
 for(int i=0;i<3;++i)if(object.containsKey(keys[i])){if(!object[keys[i]].is<int>())return false;*values[i]=object[keys[i]].as<int>();}
 return valid(bass,treble,balance);
}
}

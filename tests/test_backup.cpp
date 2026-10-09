#include "BackupConfig.h"
#include <cassert>
#include <cstdio>
#include <string>
int main(){
 const char* fixture=R"JSON({"format":"CM-Radio-Backup","schema":1,"settings":{"stations":[{"name":"A","url":"https://example.org/a"},{"name":"B","url":"http://example.org/b"}],"selected":1,"volume":5,"volumeLimit":8,"softStartSeconds":3,"fallbackStation":0,"autoplay":true}})JSON";
 DynamicJsonDocument d(12288);assert(!deserializeJson(d,fixture));backup::Data out;const char* error=nullptr;assert(backup::read(d,out,error));assert(out.count==2&&out.selected==1&&out.volume==5&&out.fallbackStation==0);
 const char* fields[]={"selected","volume","volumeLimit","softStartSeconds","fallbackStation","autoplay"};
 for(const char* field:fields){deserializeJson(d,fixture);d["settings"][field]="bad";assert(!backup::read(d,out,error));}
 for(const char* field:fields){deserializeJson(d,fixture);d["settings"].remove(field);assert(!backup::read(d,out,error));}
 deserializeJson(d,fixture);d["settings"]["volume"]=9;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["selected"]=2;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["fallbackStation"]=2;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["volume"]=true;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["schema"]=true;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["schema"]=2;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["format"]="Other";assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["stations"][0]["url"]="javascript:alert(1)";assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["stations"][0]["name"]=std::string(64,'x');assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["stations"].as<JsonArray>().clear();assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["ssid"]="PRIVATE";d["settings"]["password"]="SECRET";assert(backup::read(d,out,error)); // Credentials are deliberately never part of Data.
 deserializeJson(d,fixture);d["settings"]["bass"]=-12;d["settings"]["treble"]=6;d["settings"]["balance"]=-16;assert(backup::read(d,out,error));assert(out.bass==-12&&out.treble==6&&out.balance==-16);
 deserializeJson(d,fixture);assert(backup::read(d,out,error));assert(out.bass==0&&out.treble==0&&out.balance==0);
 for(const char* field:{"bass","treble","balance"}){deserializeJson(d,fixture);d["settings"][field]=true;assert(!backup::read(d,out,error));deserializeJson(d,fixture);d["settings"][field]="0";assert(!backup::read(d,out,error));deserializeJson(d,fixture);d["settings"][field]=1.5;assert(!backup::read(d,out,error));}
 deserializeJson(d,fixture);d["settings"]["bass"]=7;assert(!backup::read(d,out,error));deserializeJson(d,fixture);d["settings"]["treble"]=-13;assert(!backup::read(d,out,error));deserializeJson(d,fixture);d["settings"]["balance"]=17;assert(!backup::read(d,out,error));
 deserializeJson(d,fixture);d["settings"]["bass"]=6;d["settings"]["treble"]=-12;d["settings"]["balance"]=16;assert(backup::read(d,out,error));
 int bass=1,treble=2,balance=3;DynamicJsonDocument partial(256);deserializeJson(partial,"{\"bass\":4}");assert(sound::read(partial.as<JsonObjectConst>(),bass,treble,balance));assert(bass==4&&treble==2&&balance==3);
 deserializeJson(d,fixture);assert(backup::read(d,out,error));assert(!out.loudness);d["settings"]["loudness"]=true;assert(backup::read(d,out,error));assert(out.loudness);d["settings"]["loudness"]=1;assert(!backup::read(d,out,error));d["settings"]["loudness"]="true";assert(!backup::read(d,out,error));
 for(int volume=0;volume<=21;++volume){auto t=sound::tone(6,6,true,volume);assert(t.bass<=6&&t.treble<=6);auto off=sound::tone(-3,2,false,volume);assert(off.bass==-3&&off.treble==2);}
 auto quiet=sound::tone(0,0,true,1);assert(quiet.bass==4&&quiet.treble==2);auto loud=sound::tone(0,0,true,15);assert(loud.bass==0&&loud.treble==0);auto muted=sound::tone(0,0,true,0);assert(muted.bass==0&&muted.treble==0);
 puts("Backup schema, roundtrip fields, strict types, missing fields, limits, stream validation and credential isolation: PASS");
}

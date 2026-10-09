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
 puts("Backup schema, roundtrip fields, strict types, missing fields, limits, stream validation and credential isolation: PASS");
}

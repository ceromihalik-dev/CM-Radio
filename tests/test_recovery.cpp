#include "MonoMix.h"
#include "RecoveryRules.h"
#include <cassert>
#include <cstdio>
int main(){
 int16_t frame[2]={32767,32767};monoMix::frame(frame);assert(frame[0]==32767&&frame[1]==32767);
 frame[0]=-32768;frame[1]=-32768;monoMix::frame(frame);assert(frame[0]==-32768&&frame[1]==-32768);
 frame[0]=12000;frame[1]=-4000;monoMix::frame(frame);assert(frame[0]==4000&&frame[1]==4000);

 DynamicJsonDocument d(4096);const char* id="11111111-2222-3333-4444-555555555555";char url[rules::maxUrl]={},newId[37]={};
 const char* json=R"([{"name":"Example Radio","stationuuid":"11111111-2222-3333-4444-555555555555","url_resolved":"https://example.org/new","codec":"MP3","hls":0,"lastcheckok":1}])";
 deserializeJson(d,json);assert(recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio","",url,newId));assert(!strcmp(url,"https://example.org/new"));assert(!strcmp(newId,id));assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Other","",url,newId));assert(recoveryRules::match(d.as<JsonArrayConst>(),"Renamed",id,url,newId));
 d[0]["hls"]=1;assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio",id,url,newId));deserializeJson(d,json);d[0]["codec"]="OPUS";assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio",id,url,newId));deserializeJson(d,json);d[0]["lastcheckok"]=0;assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio",id,url,newId));deserializeJson(d,json);d[0]["url_resolved"]="http://user:secret@example.org/";assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio",id,url,newId));
 deserializeJson(d,json);JsonObject another=d.as<JsonArray>().createNestedObject();another["name"]="Example Radio";assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio","",url,newId));d.clear();d.to<JsonArray>();assert(!recoveryRules::match(d.as<JsonArrayConst>(),"Example Radio","",url,newId));
 assert(deviceOptions::validName("Radio Wohnzimmer"));assert(!deviceOptions::validName(""));assert(!deviceOptions::validName("../../a"));assert(!deviceOptions::validName("-radio"));assert(!deviceOptions::validName("radio-"));assert(!deviceOptions::validName("Rädio"));assert(deviceOptions::validId(id));assert(!deviceOptions::validId("malformed"));
 puts("Recovery identity, ambiguous results, codecs, URLs and device names: PASS");
}

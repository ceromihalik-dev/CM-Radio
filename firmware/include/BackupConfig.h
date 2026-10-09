#pragma once
#include <ArduinoJson.h>
#include "Validation.h"
#include "SoundConfig.h"
#include "DeviceOptions.h"
namespace backup {
struct Station {char name[rules::maxName]={};char url[rules::maxUrl]={};char logo[rules::maxUrl]={};char directoryId[37]={};};
struct Data {
 char deviceName[25]="CM-Radio";bool mono=false,autoRecover=true;
 Station stations[rules::maxStations];int count=0,selected=0,volume=11,volumeLimit=50,softStartSeconds=5,fallbackStation=-1;bool autoplay=true,loudness=false;int bass=0,treble=0,balance=0;
};
inline bool integer(JsonVariantConst v,int lo,int hi){return v.is<int>()&&v.as<int>()>=lo&&v.as<int>()<=hi;}
// Caller discards Data on failure. This parser never touches live settings/NVS.
inline bool read(const JsonDocument& document,Data& out,const char*& error){
 error="Ungueltige CM-Radio-Sicherung";
 if(!document.is<JsonObjectConst>()||!document["format"].is<const char*>()||strcmp(document["format"],"CM-Radio-Backup")||!integer(document["schema"],1,2))return false;
 const bool legacy=document["schema"].as<int>()==1;const int scale=legacy?21:rules::maxVolume;
 JsonObjectConst config=document["settings"].as<JsonObjectConst>();
 if(config.isNull()||!config["stations"].is<JsonArrayConst>())return false;
 if(config.containsKey("deviceName")&&(!config["deviceName"].is<const char*>()||!deviceOptions::validName(config["deviceName"])))return false;
 for(const char* key:{"mono","autoRecover"})if(config.containsKey(key)&&!config[key].is<bool>())return false;
 strcpy(out.deviceName,config["deviceName"]|"CM-Radio");out.mono=config["mono"]|false;out.autoRecover=config["autoRecover"]|true;
 out.loudness=false;
 if(!sound::readLoudness(config,out.loudness)){error="Loudness muss boolesch sein";return false;}
 out.bass=out.treble=out.balance=0;
 if(!sound::read(config,out.bass,out.treble,out.balance)){error="Ungueltige Klangeinstellungen";return false;}
 JsonArrayConst stations=config["stations"].as<JsonArrayConst>();
 out.count=stations.size();
 if(out.count<1||out.count>int(rules::maxStations)){error="Sicherung braucht 1 bis 10 Sender";return false;}
 if(!integer(config["selected"],0,out.count-1)||!integer(config["volumeLimit"],0,scale)||!integer(config["volume"],0,config["volumeLimit"].as<int>())||!integer(config["softStartSeconds"],0,30)||!integer(config["fallbackStation"],-1,out.count-1)||!config["autoplay"].is<bool>()){error="Ungueltige Wiedergabeeinstellungen";return false;}
 for(int i=0;i<out.count;++i){
  JsonVariantConst station=stations[i];
  if(!station["name"].is<const char*>()||!station["url"].is<const char*>())return false;
  const char* name=station["name"],*url=station["url"];bool nonblank=false;
  for(const char* p=name;*p;++p)if(static_cast<unsigned char>(*p)>32)nonblank=true;
  if(!nonblank||strlen(name)>=rules::maxName||!rules::validUrl(url)){error="Ungueltiger Sendername oder Stream in Sicherung";return false;}
  if(station.as<JsonObjectConst>().containsKey("logo")&&!station["logo"].is<const char*>())return false;
  const char* logo=station["logo"]|"";if(!rules::validLogo(logo)){error="Ungueltige HTTPS-Logo-Adresse";return false;}strcpy(out.stations[i].logo,logo);
  if(station.as<JsonObjectConst>().containsKey("directoryId")&&(!station["directoryId"].is<const char*>()||!deviceOptions::validId(station["directoryId"])))return false;
  strcpy(out.stations[i].directoryId,station["directoryId"]|"");
  strcpy(out.stations[i].name,name);strcpy(out.stations[i].url,url);
 }
 out.selected=config["selected"];out.volume=legacy?rules::legacyVolume(config["volume"].as<int>()):config["volume"].as<int>();out.volumeLimit=legacy?rules::legacyVolume(config["volumeLimit"].as<int>()):config["volumeLimit"].as<int>();out.softStartSeconds=config["softStartSeconds"];out.fallbackStation=config["fallbackStation"];out.autoplay=config["autoplay"];
 return true;
}
}

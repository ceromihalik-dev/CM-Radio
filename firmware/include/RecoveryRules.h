#pragma once
#include <ArduinoJson.h>
#include "Validation.h"
#include "DeviceOptions.h"
#include <strings.h>
namespace recoveryRules {
// Never silently choose among duplicate names or among unsupported codecs.
inline bool match(JsonArrayConst rows,const char* name,const char* id,char* url,char* newId){
 if(rows.size()!=1)return false;
 JsonObjectConst row=rows[0];const char* foundId=row["stationuuid"]|"";
 if(!deviceOptions::validId(foundId)||!*foundId)return false;
 if(*id?strcasecmp(foundId,id)!=0:strcasecmp(row["name"]|"",name)!=0)return false;
 const char* codec=row["codec"]|"";
 if((strcasecmp(codec,"MP3")&&strcasecmp(codec,"AAC")&&strcasecmp(codec,"AAC+"))||(row["hls"]|0)!=0||(row["lastcheckok"]|0)!=1)return false;
 const char* stream=row["url_resolved"]|"";if(!*stream)stream=row["url"]|"";
 if(!rules::validUrl(stream))return false;
 strcpy(url,stream);strcpy(newId,foundId);return true;
}
}

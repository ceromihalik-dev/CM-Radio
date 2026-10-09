#include "FirmwareUpdate.h"
#include "UpdatePolicy.h"
#include "Player.h"
#include <Update.h>
#include <esp_ota_ops.h>
#include <mbedtls/sha256.h>
namespace {
WebServer* http=nullptr;
std::function<bool()> flush,setupAccessReady;
String phase="idle",failure,expectedHash,token;
size_t expectedSize=0;
uint32_t preparedAt=0,rebootAt=0;
ota::ImageGuard image;
mbedtls_sha256_context hash;
bool hashing=false,writing=false,uploadSeen=false;
void reply(int code,const char* text){StaticJsonDocument<256> d;d[code<400?"message":"error"]=text;String s;serializeJson(d,s);http->sendHeader("Cache-Control","no-store");http->send(code,"application/json",s);}
bool sameOrigin(){const String origin=http->header("Origin");return origin.isEmpty()||origin=="http://"+http->hostHeader();}
void cleanup(){if(writing)Update.abort();writing=false;if(hashing)mbedtls_sha256_free(&hash);hashing=false;}
void fail(const char* text){cleanup();failure=text;phase="failed";player::setUpdating(false);}
bool authorized(){return sameOrigin()&&!token.isEmpty()&&http->header("X-CM-Update-Token")==token;}
void upload(){
 HTTPUpload& u=http->upload();
 if(u.status==UPLOAD_FILE_START){
  uploadSeen=true;
  // Rejected clients cannot cancel another browser's prepared update.
  if(!authorized()||phase=="rebooting")return;
  if(phase!="prepared"){fail("Nur eine Firmwaredatei pro Update erlaubt");return;}
  if(!player::status().updating&&player::status().ready){fail("Audio noch nicht gestoppt; erneut vorbereiten");return;}
  if(u.name!="firmware"||u.filename!="firmware.bin"){fail("Nur firmware.bin aus dem Updatepaket verwenden");return;}
  image.reset(expectedSize);phase="receiving";
  mbedtls_sha256_init(&hash);hashing=true;if(mbedtls_sha256_starts_ret(&hash,0)){fail("SHA-256 konnte nicht gestartet werden");return;}
 }else if(u.status==UPLOAD_FILE_WRITE){
  if(!authorized()||phase!="receiving")return;
  if(uint32_t(millis()-preparedAt)>180000){fail("Upload-Zeitlimit erreicht");return;}
  const size_t previous=image.received();
  if(!image.accept(u.buf,u.currentSize)){fail("Ungueltiges ESP32-Anwendungsimage oder falsche Dateigroesse");return;}
  if(mbedtls_sha256_update_ret(&hash,u.buf,u.currentSize)){fail("SHA-256-Berechnung fehlgeschlagen");return;}
  if(!image.headerReady())return;
  size_t skip=0;
  if(!writing){
   if(!Update.begin(expectedSize,U_FLASH)){fail("Inaktiver Firmware-Slot nicht beschreibbar");return;}
   writing=true;
   if(Update.write(const_cast<uint8_t*>(image.header()),24)!=24){fail("Firmwareheader konnte nicht geschrieben werden");return;}
   skip=previous<24?24-previous:0;
  }
  if(u.currentSize>skip&&Update.write(u.buf+skip,u.currentSize-skip)!=u.currentSize-skip)fail("Fehler beim Schreiben der Firmware");
 }else if(u.status==UPLOAD_FILE_END){
  if(!authorized()||phase!="receiving")return;
  if(!image.complete()){fail("Firmwaredatei unvollstaendig");return;}
  uint8_t digest[32];if(mbedtls_sha256_finish_ret(&hash,digest)){fail("SHA-256-Abschluss fehlgeschlagen");return;}mbedtls_sha256_free(&hash);hashing=false;
  char encoded[65];for(size_t i=0;i<32;++i)snprintf(encoded+2*i,3,"%02x",digest[i]);
  if(expectedHash!=encoded){fail("SHA-256 passt nicht zum Paketmanifest; bisherige Firmware bleibt aktiv");return;}
  phase="verified";
 }else if(u.status==UPLOAD_FILE_ABORTED){if(authorized()&&(phase=="receiving"||phase=="verified"))fail("Upload abgebrochen; bisherige Firmware bleibt aktiv");}
}
}
bool firmwareUpdate::busy(){return phase=="prepared"||phase=="receiving"||phase=="verified"||phase=="rebooting";}
void firmwareUpdate::status(JsonObject d){d["phase"]=phase;d["error"]=failure;d["received"]=image.received();d["size"]=expectedSize;d["audioStopped"]=!player::status().ready||player::status().updating;}
void firmwareUpdate::tick(){
 if(phase=="prepared"&&uint32_t(millis()-preparedAt)>60000)fail("Updatevorbereitung abgelaufen; erneut starten");
 if((phase=="receiving"||phase=="verified")&&uint32_t(millis()-preparedAt)>180000)fail("Upload-Zeitlimit erreicht");
 if(phase=="rebooting"&&int32_t(millis()-rebootAt)>=0)ESP.restart();
}
void firmwareUpdate::begin(WebServer& server,std::function<bool()> flushSettings,std::function<bool()> setupReady){
 http=&server;flush=flushSettings;setupAccessReady=setupReady;
 server.on("/api/v1/update/status",HTTP_GET,[]{StaticJsonDocument<384>d;firmwareUpdate::status(d.to<JsonObject>());String s;serializeJson(d,s);http->sendHeader("Cache-Control","no-store");http->send(200,"application/json",s);});
 server.on("/api/v1/update/prepare",HTTP_POST,[]{
  if(!sameOrigin()){reply(403,"Fremder Browser-Ursprung");return;}
  if(!setupAccessReady()){reply(428,"Setup-Passwort zuerst aendern bzw. WLAN-Neustart abwarten");return;}
  if(firmwareUpdate::busy()){reply(409,"Update bereits vorbereitet oder aktiv");return;}
  if(!http->header("Content-Type").startsWith("application/json")||http->arg("plain").length()>2048){reply(400,"Ungueltige Update-Metadaten");return;}
  StaticJsonDocument<1024>d;
  if(deserializeJson(d,http->arg("plain"))||!d.is<JsonObject>()||d.overflowed()||!d["size"].is<unsigned>()||d["size"].as<unsigned>()<1024||d["size"].as<unsigned>()>ota::maxSize||!d["sha256"].is<const char*>()||!ota::validHash(d["sha256"])||!d["target"].is<const char*>()||strcmp(d["target"],"CM-Radio-WROVER-N8R8")){reply(400,"Manifest passt nicht zu CM-Radio WROVER-N8R8");return;}
  const esp_partition_t* slot=esp_ota_get_next_update_partition(nullptr);
  if(!slot||slot->size<d["size"].as<unsigned>()||ESP.getFlashChipSize()!=8U*1024U*1024U){reply(409,"Kein passender freier Firmware-Slot");return;}
  if(!flush()){reply(507,"Ausstehende Einstellungen konnten nicht gesichert werden");return;}
  expectedSize=d["size"];expectedHash=d["sha256"].as<String>();failure="";image.reset(expectedSize);uploadSeen=false;
  char key[33];snprintf(key,sizeof(key),"%08X%08X%08X%08X",static_cast<unsigned>(esp_random()),static_cast<unsigned>(esp_random()),static_cast<unsigned>(esp_random()),static_cast<unsigned>(esp_random()));token=key;
  phase="prepared";preparedAt=millis();player::setUpdating(true);
  StaticJsonDocument<128>r;r["token"]=token;String s;serializeJson(r,s);http->send(202,"application/json",s);
 });
 server.on("/api/v1/update/cancel",HTTP_POST,[]{if(!authorized()){reply(403,"Ungueltige Updatefreigabe");return;}if(phase!="prepared"&&phase!="receiving"&&phase!="verified"){reply(409,"Update nicht mehr abbrechbar");return;}cleanup();phase="idle";token="";player::setUpdating(false);reply(200,"Update abgebrochen; bei Bedarf manuell abspielen");});
 server.on("/api/v1/update",HTTP_POST,[]{
  if(!authorized()){reply(403,"Ungueltige Updatefreigabe");return;}
  if(uploadSeen&&phase=="verified"){if(!Update.end(false)){fail("Firmwarevalidierung oder Aktivierung fehlgeschlagen");reply(400,failure.c_str());return;}writing=false;phase="rebooting";rebootAt=millis()+1800;reply(200,"Firmware geprueft und aktiviert; Neustart folgt");return;}
  if(phase=="failed"){reply(400,failure.c_str());return;}
  if(phase=="prepared"||phase=="receiving")fail("Upload unvollstaendig oder keine Firmwaredatei");
  reply(400,failure.isEmpty()?"Keine Firmware hochgeladen":failure.c_str());
 },upload);
}

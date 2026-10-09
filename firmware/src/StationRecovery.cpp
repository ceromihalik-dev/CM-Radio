#include "StationRecovery.h"
#include "RecoveryRules.h"
#include <HTTPClient.h>
#include <WiFi.h>
namespace {
QueueHandle_t jobs=nullptr,results=nullptr;portMUX_TYPE lock=portMUX_INITIALIZER_UNLOCKED;bool active=false;
String encode(const char* s){String out;const char* hex="0123456789ABCDEF";for(;*s;++s){unsigned char c=*s;if(isalnum(c)||c=='-'||c=='_'||c=='.')out+=char(c);else{out+='%';out+=hex[c>>4];out+=hex[c&15];}}return out;}
void worker(void*){
 for(;;){recovery::Job job;if(xQueueReceive(jobs,&job,portMAX_DELAY)!=pdTRUE)continue;
  recovery::Result result{};result.job=job;strlcpy(result.message,"Keine eindeutige neue Senderadresse gefunden",sizeof(result.message));
  const char* mirrors[]={"de1.api.radio-browser.info","nl1.api.radio-browser.info"};
  for(const char* host:mirrors){
   if(WiFi.status()!=WL_CONNECTED)break;
   WiFiClient client;HTTPClient http;http.useHTTP10(true);http.setConnectTimeout(2000);http.setTimeout(4000);http.setUserAgent("CM-Radio/0.1.3");
   // Public directory lookup only; no credentials. Responses remain untrusted.
   String path=job.id[0]?"/json/stations/byuuid/"+String(job.id):"/json/stations/bynameexact/"+encode(job.name);
   if(!http.begin(client,"http://"+String(host)+path+"?hidebroken=true&limit=2"))continue;
   int code=http.GET();int length=http.getSize();
   if(code!=200||length>8192){http.end();strlcpy(result.message,"Senderverzeichnis nicht erreichbar oder Antwort zu gross",sizeof(result.message));continue;}
   String raw;raw.reserve(8192);uint32_t began=millis();WiFiClient* stream=http.getStreamPtr();
   while((stream->connected()||stream->available())&&millis()-began<6000&&raw.length()<=8192){
    int available=stream->available();if(available){char buffer[257];int count=stream->readBytes(buffer,available>256?256:available);buffer[count]=0;raw+=buffer;if(length>=0&&int(raw.length())>=length)break;}else vTaskDelay(pdMS_TO_TICKS(5));
   }
   http.end();if(raw.length()>8192||(length>=0&&int(raw.length())!=length))continue;
   DynamicJsonDocument document(16384);if(deserializeJson(document,raw))continue;
   if(recoveryRules::match(document.as<JsonArrayConst>(),job.name,job.id,result.url,result.id)&&strcmp(job.url,result.url)){
    result.found=true;strlcpy(result.message,"Neue Senderadresse gefunden",sizeof(result.message));break;
   }
  }
  xQueueSend(results,&result,portMAX_DELAY);
 }
}
}
bool recovery::begin(){jobs=xQueueCreate(1,sizeof(Job));results=xQueueCreate(1,sizeof(Result));return jobs&&results&&xTaskCreatePinnedToCore(worker,"CM-StationLookup",8192,nullptr,1,nullptr,1)==pdPASS;}
bool recovery::request(const Job& job){portENTER_CRITICAL(&lock);bool allowed=!active;if(allowed)active=true;portEXIT_CRITICAL(&lock);if(!allowed)return false;if(!jobs||xQueueSend(jobs,&job,0)!=pdTRUE){portENTER_CRITICAL(&lock);active=false;portEXIT_CRITICAL(&lock);return false;}return true;}
bool recovery::take(Result& result){if(!results||xQueueReceive(results,&result,0)!=pdTRUE)return false;portENTER_CRITICAL(&lock);active=false;portEXIT_CRITICAL(&lock);return true;}
bool recovery::busy(){portENTER_CRITICAL(&lock);bool value=active;portEXIT_CRITICAL(&lock);return value;}

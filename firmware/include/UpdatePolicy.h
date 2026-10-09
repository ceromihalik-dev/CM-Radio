#pragma once
#include <stdint.h>
#include <stddef.h>
#include <string.h>
namespace ota {
constexpr size_t maxSize = 3U * 1024U * 1024U;
inline bool validHash(const char* hash) {
 if(!hash || strlen(hash)!=64)return false;
 for(size_t i=0;i<64;++i)if(!((hash[i]>='0'&&hash[i]<='9')||(hash[i]>='a'&&hash[i]<='f')))return false;
 return true;
}
class ImageGuard {
public:
 void reset(size_t expected){expected_=expected;received_=0;headerBytes_=0;valid_=true;}
 bool accept(const uint8_t* bytes,size_t size){
  if(!valid_||received_>expected_||size>expected_-received_)return valid_=false;
  for(size_t i=0;i<size&&headerBytes_<24;++i)header_[headerBytes_++]=bytes[i];
  received_+=size;
  if(headerBytes_==24&&(header_[0]!=0xe9||header_[1]==0||header_[1]>16||header_[12]!=0||header_[13]!=0))return valid_=false;
  return true;
 }
 bool headerReady()const{return valid_&&headerBytes_==24;}
 const uint8_t* header()const{return header_;}
 bool complete()const{return headerReady()&&received_==expected_;}
 size_t received()const{return received_;}
private:
 size_t expected_=0,received_=0,headerBytes_=0;bool valid_=false;uint8_t header_[24]={};
};
}

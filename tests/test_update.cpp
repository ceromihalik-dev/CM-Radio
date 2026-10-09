#include "UpdatePolicy.h"
#include <cassert>
#include <cstdio>
#include <string>
int main(){
 assert(ota::validHash(std::string(64,'a').c_str()));assert(!ota::validHash(nullptr));assert(!ota::validHash("abc"));assert(!ota::validHash(std::string(64,'g').c_str()));
 uint8_t image[1024]={};image[0]=0xe9;image[1]=6;
 ota::ImageGuard g;g.reset(sizeof(image));assert(g.accept(image,12));assert(!g.headerReady());assert(g.accept(image+12,12));assert(g.headerReady());assert(!g.complete());assert(g.accept(image+24,1000));assert(g.complete());assert(!g.accept(image,1));
 g.reset(sizeof(image));image[12]=9;assert(!g.accept(image,1024));image[12]=0;image[0]=0xff;g.reset(sizeof(image));assert(!g.accept(image,1024));image[0]=0xe9;g.reset(sizeof(image));assert(!g.accept(image,1025));g.reset(sizeof(image));assert(g.accept(image,1000));assert(!g.complete());
 puts("OTA SHA-256 metadata, split header, ESP32 identity, invalid image, oversize and incomplete upload: PASS");
}

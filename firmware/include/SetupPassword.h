#pragma once
#include <string.h>
namespace setupAccess {
constexpr const char* initialPassword="passwort";
inline bool valid(const char* password){
 if(!password||strlen(password)<8||strlen(password)>63||strcmp(password,initialPassword)==0)return false;
 for(const char* p=password;*p;++p)if(static_cast<unsigned char>(*p)<32||static_cast<unsigned char>(*p)>126)return false;
 return true;
}
}

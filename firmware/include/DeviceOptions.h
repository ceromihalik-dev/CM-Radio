#pragma once
#include <string.h>
#include <ctype.h>
namespace deviceOptions {
inline bool validName(const char* n){if(!n||!*n||strlen(n)>24)return false;if(!isalnum(static_cast<unsigned char>(n[0]))||!isalnum(static_cast<unsigned char>(n[strlen(n)-1])))return false;bool letter=false;for(;*n;++n){unsigned char c=*n;if(!((c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c==' '||c=='-'||c=='_'))return false;if(isalnum(c))letter=true;}return letter;}
inline bool validId(const char* id){if(!id)return false;if(!*id)return true;if(strlen(id)!=36)return false;for(int i=0;i<36;++i){if(i==8||i==13||i==18||i==23){if(id[i]!='-')return false;}else if(!isxdigit(static_cast<unsigned char>(id[i])))return false;}return true;}
}

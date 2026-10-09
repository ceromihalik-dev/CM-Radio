#include "FallbackPolicy.h"
#include <cassert>
#include <cstdio>
int main(){FallbackPolicy p;assert(!p.switchNow(true,true));p.attempted();p.attempted();assert(!p.switchNow(true,true));p.attempted();assert(!p.switchNow(false,true));assert(!p.switchNow(true,false));assert(p.switchNow(true,true));assert(p.active());for(int i=0;i<20;++i)p.attempted();assert(!p.switchNow(true,true));p.reset();assert(!p.active());p.attempted();p.attempted();p.offline();assert(!p.switchNow(true,true));p.attempted();p.stable();assert(!p.switchNow(true,true));puts("Fallback threshold, offline, identity, single switch, stop/reset: PASS");}

#include "WifiScan.h"
#include <cassert>
#include <cstdio>
struct Driver {
    int prepares=0, starts=0, restores=0, cancels=0, startResult=-1, completion=-1;
    void prepare(){++prepares;} int start(){++starts;return startResult;}
    int complete(){return completion;} void restore(){++restores;} void cancel(){++cancels;}
};
int main(){
    Driver d;WifiScan scan;scan.request(100,d);scan.request(101,d);
    assert(d.prepares==1 && scan.busy());scan.tick(399,d);assert(d.starts==0);
    scan.tick(400,d);assert(d.starts==1 && scan.busy());
    d.completion=5;scan.tick(401,d);assert(!scan.busy() && scan.result()==5 && d.restores==1);
    d.startResult=-2;scan.request(1000,d);scan.tick(1300,d);scan.tick(1799,d);assert(d.starts==2);
    scan.tick(1800,d);scan.tick(2300,d);assert(!scan.busy() && scan.result()==-2 && d.restores==2);
    d.startResult=-1;d.completion=-1;scan.request(3000,d);scan.tick(3300,d);scan.tick(15000,d);
    assert(!scan.busy() && d.cancels==1 && d.restores==3);
    scan.request(0xffffff80U,d);scan.tick(0xabu,d);assert(scan.busy());scan.tick(0xacU,d);
    d.completion=0;scan.tick(0xadU,d);assert(!scan.busy() && scan.result()==0);
    puts("WiFi scan preparation, duplicate requests, retries, timeout, restore and millis rollover: PASS");
}

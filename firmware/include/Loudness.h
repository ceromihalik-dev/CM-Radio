#pragma once
namespace sound {
struct Tone {int bass,treble;};
inline Tone tone(int bass,int treble,bool loudness,int volume){
 int boost=loudness&&volume>0&&volume*21<750?(750-volume*21)*4/700:0;
 return {bass+boost>6?6:bass+boost,treble+boost/2>6?6:treble+boost/2};
}
}

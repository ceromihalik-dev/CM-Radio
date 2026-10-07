#include "WebUi.h"
const char WEB_UI[] PROGMEM = R"CMRADIO(
<!doctype html>
<html lang="de">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101722">
<title>CM-Radio</title>
<style>
:root{color-scheme:dark;font:16px system-ui;background:#101722;color:#edf4ff}*{box-sizing:border-box}body{margin:0;padding:24px 16px 48px}main{max-width:720px;margin:auto}h1{margin:0;font-size:2.4rem;letter-spacing:-.04em}h2{font-size:1.15rem;margin:0 0 16px}header{margin-bottom:24px}small,.muted{color:#acbdd4}section{background:#1a2535;padding:22px;border:1px solid #34455e;border-radius:18px;margin:18px 0}label{display:block;margin:14px 0 6px}input,button,select{font:inherit;border-radius:9px;padding:12px;border:1px solid #526682}input,select{width:100%;background:#111c2b;color:inherit}input[type=checkbox]{width:auto}input[type=range]{padding:0;accent-color:#67d6c7}button{background:#67d6c7;color:#082723;cursor:pointer;font-weight:650;min-height:46px}button.secondary{background:#293b51;color:#edf4ff}button:disabled{opacity:.5;cursor:wait}.row{display:flex;gap:10px;flex-wrap:wrap}.row button{flex:1}#station{font-size:1.3rem;margin:14px 0 8px;overflow-wrap:anywhere}#title{min-height:24px;overflow-wrap:anywhere}#notice{position:sticky;top:10px;background:#283e56;padding:12px;border-radius:10px;display:none;z-index:2;overflow-wrap:anywhere}.editor{border-top:1px solid #34455e;margin:18px 0;padding-top:8px}.editor button{margin-top:10px}summary{cursor:pointer;font-weight:650}code{overflow-wrap:anywhere}.tag{display:inline-block;padding:5px 10px;border-radius:20px;background:#294254;margin-top:12px}#details{line-height:1.7}a{color:#67d6c7}
</style>
<main>
<header><h1>CM-Radio<span style="color:#67d6c7">.</span></h1><small>Dein Radio. In deinem WLAN.</small><div><span class="tag" id="state">Verbinde …</span></div></header>
<div id="notice" role="status" aria-live="polite"></div>
<section><h2>Jetzt hören</h2><div id="station">—</div><div id="title" class="muted"></div><label for="stations">Sender</label><select id="stations"></select><div class="row" style="margin-top:16px"><button id="play" type="button">Abspielen</button><button id="stop" class="secondary" type="button">Stoppen</button></div><label for="volume">Lautstärke <output id="volumeValue">5 / 21</output></label><input id="volume" type="range" min="0" max="21" value="5"><label><input id="autoplay" type="checkbox" checked> Bei Stromzufuhr automatisch starten</label></section>
<section><details id="wifiDetails"><summary>WLAN einrichten</summary><p class="muted">2,4-GHz-WLAN auswählen. Nach dem Speichern verbindest du dein Handy wieder mit deinem Heimnetz.</p><form id="wifiForm"><label for="ssid">WLAN-Name</label><input id="ssid" maxlength="32" required autocomplete="off"><label for="password">WLAN-Passwort</label><input id="password" type="password" maxlength="63" autocomplete="new-password"><button style="margin-top:16px" type="submit">WLAN speichern und verbinden</button></form><p class="muted">Danach <a href="http://cm-radio.local">cm-radio.local</a> öffnen. Alternativ die IP-Adresse aus dem Router oder dem seriellen Monitor verwenden.</p></details></section>
<section><details><summary>Sender verwalten</summary><p class="muted">Bis zu 10 Sender. Benötigt wird die direkte MP3-/AAC-Stream-Adresse, keine Webseite.</p><div id="editors"></div><div class="row"><button id="add" class="secondary" type="button">Sender hinzufügen</button><button id="saveStations" type="button">Sender speichern</button></div></details></section>
<section><details><summary>Gerätestatus</summary><div id="details" class="muted"></div><p><small>Firmware V0.1 · Lokale Steuerung ohne Anmeldung.</small></p></details></section>
</main>
<script>
'use strict';
const $=id=>document.getElementById(id);
let list=[], editing=false, volumeBusy=false, volumeDesired=5, initialized=false, lastStatus=null;
function notice(message){$('notice').textContent=message;$('notice').style.display='block';}
async function api(path,method='GET',data){const options={method,cache:'no-store'};if(data!==undefined){options.headers={'Content-Type':'application/json'};options.body=JSON.stringify(data);}const response=await fetch('/api/v1/'+path,options);const result=await response.json();if(!response.ok)throw new Error(result.error||'Anfrage fehlgeschlagen');return result;}
async function action(fn){try{await fn();}catch(e){notice(e.message);}}
function selectStations(){const select=$('stations'),old=select.value;select.replaceChildren();list.forEach((s,i)=>{const o=document.createElement('option');o.value=String(i);o.textContent=s.name;select.append(o);});if(old!==''&&Number(old)<list.length)select.value=old;}
function editStations(){const container=$('editors');container.replaceChildren();list.forEach((s,i)=>{const row=document.createElement('div');row.className='editor';const name=document.createElement('input'),url=document.createElement('input');name.value=s.name;name.maxLength=63;name.setAttribute('aria-label','Sendername '+(i+1));url.value=s.url;url.maxLength=383;url.placeholder='http://…';url.setAttribute('aria-label','Stream-Adresse '+(i+1));name.oninput=()=>{s.name=name.value;editing=true;};url.oninput=()=>{s.url=url.value;editing=true;};const remove=document.createElement('button');remove.type='button';remove.className='secondary';remove.textContent='Entfernen';remove.onclick=()=>{if(list.length===1){notice('Mindestens ein Sender muss erhalten bleiben.');return;}list.splice(i,1);editing=true;editStations();};row.append(name,url,remove);container.append(row);});}
async function refresh(){const s=await api('status');lastStatus=s;$('state').textContent=!s.audioReady?'Audio prüfen':s.state==='streaming'?'Stream aktiv':s.state==='connecting'?'Verbinde Stream …':'Gestoppt';$('station').textContent=s.station;$('title').textContent=s.title||s.message||'';$('play').disabled=!s.audioReady;$('stop').disabled=!s.audioReady;if(document.activeElement!==$('volume')&&!volumeBusy){$('volume').value=s.volume;volumeDesired=s.volume;$('volumeValue').textContent=s.volume+' / 21';}if(document.activeElement!==$('autoplay'))$('autoplay').checked=s.autoplay;if(!initialized){$('stations').value=String(s.stationIndex);$('wifiDetails').open=s.setupActive;initialized=true;}const entries=[['Version',s.version],['Adresse',s.ip],['WLAN',s.wifiConnected?'Verbunden ('+s.rssi+' dBm)':'Offline'],['Flash',s.flashBytes+' Bytes'],['PSRAM',s.psramBytes+' Bytes'],['Freier Heap',s.freeHeap+' Bytes'],['Laufzeit',s.uptimeSeconds+' s'],['Einstellungen',s.settingsPending?'Speichern steht aus':'Gespeichert']];$('details').replaceChildren(...entries.map(([k,v])=>{const d=document.createElement('div');d.textContent=k+': '+v;return d;}));}
$('play').onclick=()=>action(async()=>{await api('play','POST',{station:Number($('stations').value)});await refresh();});
$('stop').onclick=()=>action(async()=>{await api('stop','POST',{});await refresh();});
$('volume').oninput=()=>{$('volumeValue').textContent=$('volume').value+' / 21';};
$('volume').onchange=()=>{volumeDesired=Number($('volume').value);if(volumeBusy)return;volumeBusy=true;action(async()=>{try{let sent;do{sent=volumeDesired;await api('volume','POST',{volume:sent});}while(sent!==volumeDesired);}finally{volumeBusy=false;}});};
$('autoplay').onchange=()=>action(async()=>{await api('config','POST',{autoplay:$('autoplay').checked});});
$('wifiForm').onsubmit=event=>{event.preventDefault();action(async()=>{await api('wifi','POST',{ssid:$('ssid').value,password:$('password').value});$('password').value='';notice('WLAN gespeichert. Verbinde dein Handy mit dem Heimnetz und öffne cm-radio.local.');});};
$('add').onclick=()=>{if(list.length>=10){notice('Maximal 10 Sender.');return;}list.push({name:'',url:''});editing=true;editStations();};
$('saveStations').onclick=()=>action(async()=>{await api('stations','PUT',{stations:list});editing=false;list=(await api('stations')).stations;selectStations();editStations();initialized=false;notice('Sender gespeichert.');await refresh();});
async function init(){try{list=(await api('stations')).stations;selectStations();editStations();const config=await api('config');$('ssid').value=config.ssid;await refresh();}catch(e){notice('Gerät nicht erreichbar: '+e.message);}}
init();setInterval(()=>action(refresh),2500);
</script>
</html>
)CMRADIO";

from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

s = s.replace(
    '<div id="audioMeta" class="meta">No song selected.</div></section>',
    '''<div id="audioMeta" class="meta">No song selected.</div>
<div id="clipBox" class="clipbox hidden"><div class="title" style="font-size:16px">Choose 30–50 seconds</div>
<div class="clipline"><span>Start point</span><strong id="startRead">0:00</strong></div><input id="clipStart" class="range" type="range" min="0" max="0" value="0" step="0.1">
<div class="clipline"><span>Clip length</span><strong id="lengthRead">50 sec</strong></div><input id="clipLength" class="range" type="range" min="30" max="50" value="50" step="0.1">
<div class="clipline"><span>Selected</span><strong id="clipRead">0:00 – 0:50</strong></div><div class="tiny">Every lyric video must be between 30 and 50 seconds. Move the start point to choose the verse, chorus or part you want.</div></div></section>''',
    1
)

s = s.replace(
    '.range{width:100%}video{',
    '.range{width:100%;accent-color:#8da2ff}.clipbox{background:#0e1221;border:1px solid #2d3554;border-radius:16px;padding:14px;margin-top:14px}.clipline{display:flex;justify-content:space-between;gap:12px;font-size:13px;margin:8px 0}video{',
    1
)

s = s.replace(
    "shareBtn=$('shareBtn');",
    "shareBtn=$('shareBtn'),clipBox=$('clipBox'),clipStartEl=$('clipStart'),clipLengthEl=$('clipLength'),startRead=$('startRead'),lengthRead=$('lengthRead'),clipRead=$('clipRead');",
    1
)

s = s.replace(
    "beatPulse=0,lastBeat=0;",
    "beatPulse=0,lastBeat=0,songDuration=0,clipStart=0,clipLength=50;",
    1
)

needle = "const fmt=s=>!isFinite(s)?'--:--':`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;const esc=s=>String(s).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));"
insert = needle + r'''
function updateClip(resetAI=true){
  if(!songDuration)return;
  const maxStart=Math.max(0,songDuration-30);
  clipStart=Math.min(maxStart,Math.max(0,Number(clipStartEl.value)||0));
  clipStartEl.max=String(maxStart);clipStartEl.value=String(clipStart);
  const remaining=songDuration-clipStart;
  const maxLen=Math.min(50,remaining);
  clipLengthEl.min='30';clipLengthEl.max=String(maxLen);
  clipLength=Math.min(maxLen,Math.max(30,Number(clipLengthEl.value)||Math.min(50,remaining)));
  clipLengthEl.value=String(clipLength);
  startRead.textContent=fmt(clipStart);lengthRead.textContent=`${clipLength.toFixed(clipLength%1?1:0)} sec`;clipRead.textContent=`${fmt(clipStart)} – ${fmt(clipStart+clipLength)}`;
  if(resetAI){words=[];scenes=[];aiStatus.textContent='Section changed — analyze this 30–50 sec clip with AI.'}
  draw(0);
}
function encodeAnalysisWav(buffer,startSec,durationSec){
  const targetRate=16000;
  const srcRate=buffer.sampleRate;
  const srcStart=Math.floor(startSec*srcRate);
  const outFrames=Math.max(1,Math.floor(durationSec*targetRate));
  const out=new ArrayBuffer(44+outFrames*2),v=new DataView(out);
  const str=(o,x)=>{for(let i=0;i<x.length;i++)v.setUint8(o+i,x.charCodeAt(i))};
  str(0,'RIFF');v.setUint32(4,36+outFrames*2,true);str(8,'WAVE');str(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,targetRate,true);v.setUint32(28,targetRate*2,true);v.setUint16(32,2,true);v.setUint16(34,16,true);str(36,'data');v.setUint32(40,outFrames*2,true);
  const channels=[];for(let c=0;c<buffer.numberOfChannels;c++)channels.push(buffer.getChannelData(c));
  for(let i=0;i<outFrames;i++){
    const srcPos=srcStart+(i*srcRate/targetRate),i0=Math.floor(srcPos),i1=Math.min(i0+1,buffer.length-1),f=srcPos-i0;
    let sample=0;
    for(const ch of channels){const a=ch[Math.min(i0,ch.length-1)]||0,b=ch[Math.min(i1,ch.length-1)]||0;sample+=a+(b-a)*f}
    sample/=Math.max(1,channels.length);sample=Math.max(-1,Math.min(1,sample));
    v.setInt16(44+i*2,sample<0?sample*32768:sample*32767,true);
  }
  return new Blob([out],{type:'audio/wav'});
}
async function selectedClipFile(){const tmp=new (window.AudioContext||window.webkitAudioContext)();try{const buf=await tmp.decodeAudioData(await songFile.arrayBuffer());const wav=encodeAnalysisWav(buf,clipStart,clipLength);return new File([wav],'reelwave-selected-clip-16k-mono.wav',{type:'audio/wav'})}finally{tmp.close()}}
'''
if needle not in s:
    raise SystemExit('Could not insert clip helper functions')
s = s.replace(needle, insert, 1)

old_audio = "audioInput.onchange=e=>{songFile=e.target.files[0];if(!songFile)return;audio.src=URL.createObjectURL(songFile);audioMeta.textContent='Loading…';audio.onloadedmetadata=()=>{audioMeta.innerHTML=`Loaded <strong>${esc(songFile.name)}</strong> · ${fmt(audio.duration)}`;aiBtn.disabled=previewBtn.disabled=exportBtn.disabled=false;aiStatus.textContent='Ready for AI lyric timing.';exportStatus.textContent='Ready to create a lyric video.'}};"
new_audio = "audioInput.onchange=e=>{songFile=e.target.files[0];if(!songFile)return;audio.src=URL.createObjectURL(songFile);audioMeta.textContent='Loading…';audio.onloadedmetadata=()=>{songDuration=audio.duration;if(songDuration<30){clipBox.classList.add('hidden');audioMeta.innerHTML=`Loaded <strong>${esc(songFile.name)}</strong> · ${fmt(songDuration)} · song is too short`;aiBtn.disabled=previewBtn.disabled=exportBtn.disabled=true;aiStatus.textContent='Reelwave lyric clips must be at least 30 seconds.';exportStatus.textContent='Choose an audio file at least 30 seconds long.';return}clipBox.classList.remove('hidden');clipStartEl.value='0';clipLengthEl.value=String(Math.min(50,songDuration));audioMeta.innerHTML=`Loaded <strong>${esc(songFile.name)}</strong> · ${fmt(songDuration)}`;aiBtn.disabled=previewBtn.disabled=exportBtn.disabled=false;aiStatus.textContent='Choose a 30–50 second section, then analyze it.';exportStatus.textContent='Ready to create the selected lyric video.';updateClip(false)}};clipStartEl.oninput=()=>updateClip(true);clipLengthEl.oninput=()=>updateClip(true);"
if old_audio not in s:
    raise SystemExit('Could not replace audio selection handler')
s = s.replace(old_audio,new_audio,1)

old_ai = "aiBtn.onclick=async()=>{if(!songFile)return;aiBtn.disabled=true;aiStatus.textContent='Listening to the song, timing words and planning scenes…';try{const fd=new FormData();fd.append('audio',songFile,songFile.name);fd.append('style',style);const r=await fetch(BACKEND+'/api/analyze',{method:'POST',body:fd});if(!r.ok)throw new Error(await r.text());const data=await r.json();words=Array.isArray(data.words)?data.words:[];scenes=Array.isArray(data.scenes)?data.scenes:[];aiStatus.innerHTML=`AI complete: <strong>${words.length}</strong> timed words · <strong>${scenes.length}</strong> scene ideas. Lyrics will be burned into the video.`;draw(audio.currentTime||0)}catch(err){aiStatus.textContent='AI analysis failed: '+err.message}finally{aiBtn.disabled=false}};"
new_ai = "aiBtn.onclick=async()=>{if(!songFile)return;aiBtn.disabled=true;aiStatus.textContent=`Preparing a compressed ${clipLength.toFixed(0)} sec analysis clip…`;try{const clip=await selectedClipFile();const fd=new FormData();fd.append('audio',clip,clip.name);fd.append('style',style);const r=await fetch(BACKEND+'/api/analyze',{method:'POST',body:fd});if(!r.ok)throw new Error(await r.text());const data=await r.json();words=Array.isArray(data.words)?data.words:[];scenes=Array.isArray(data.scenes)?data.scenes:[];aiStatus.innerHTML=`AI complete for ${fmt(clipStart)}–${fmt(clipStart+clipLength)}: <strong>${words.length}</strong> timed words · <strong>${scenes.length}</strong> scene ideas.`;draw(0)}catch(err){aiStatus.textContent='AI analysis failed: '+err.message}finally{aiBtn.disabled=false}};"
if old_ai not in s:
    raise SystemExit('Could not replace AI handler')
s=s.replace(old_ai,new_ai,1)

old_loop = "function loop(){const x=energy();draw(audio.currentTime||0,x.energy,x.bass);raf=requestAnimationFrame(loop)}"
new_loop = "function loop(){if(!audio.paused&&audio.currentTime>=clipStart+clipLength){audio.pause();cancelAnimationFrame(raf);draw(clipLength);return}const x=energy();draw(Math.max(0,(audio.currentTime||clipStart)-clipStart),x.energy,x.bass);raf=requestAnimationFrame(loop)}"
if old_loop not in s:
    raise SystemExit('Could not replace render loop')
s=s.replace(old_loop,new_loop,1)

old_preview = "previewBtn.onclick=async()=>{setupAudio();await ac.resume();if(audio.paused){if(audio.ended)audio.currentTime=0;await audio.play();previewBtn.textContent='⏸ Pause';cancelAnimationFrame(raf);loop()}else{audio.pause();previewBtn.textContent='▶ Preview'}};"
new_preview = "previewBtn.onclick=async()=>{setupAudio();await ac.resume();if(audio.paused){audio.currentTime=clipStart;await audio.play();previewBtn.textContent='⏸ Pause';cancelAnimationFrame(raf);loop()}else{audio.pause();previewBtn.textContent='▶ Preview selected section'}};"
if old_preview not in s:
    raise SystemExit('Could not replace preview handler')
s=s.replace(old_preview,new_preview,1)

s=s.replace("audio.currentTime=0;cancelAnimationFrame(raf);loop();rec.start(500);await audio.play();const dur=Math.max(1,audio.duration||30),start=performance.now();",
            "audio.currentTime=clipStart;cancelAnimationFrame(raf);loop();rec.start(500);await audio.play();const dur=clipLength,start=performance.now();",1)
s=s.replace("if(p>=1||audio.ended)return resolve();","if(p>=1||audio.currentTime>=clipStart+clipLength||audio.ended)return resolve();",1)
s=s.replace('Upload a song, let AI time the lyrics, then use generated skies or your own photo/GIF.', 'Upload a song, choose a 30–50 second section, let AI time the lyrics, then use generated skies or your own photo/GIF.', 1)
s=s.replace('✨ Analyze lyrics with AI','✨ Analyze selected clip with AI',1)
s=s.replace('▶ Preview','▶ Preview selected section',1)
s=s.replace('Export 9:16 lyric video','Export selected lyric video',1)

p.write_text(s,encoding='utf-8')
print('Applied Reelwave 30–50 second selector with compact 16 kHz mono AI clip.')

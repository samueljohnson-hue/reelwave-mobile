from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# Add textarea/control styles.
s = s.replace('.range{width:100%;accent-color:#8da2ff}', '.range{width:100%;accent-color:#8da2ff}.lyricsbox{width:100%;min-height:170px;background:#0b1020;color:#fff;border:1px solid #39405d;border-radius:15px;padding:13px;font:500 15px/1.5 system-ui;resize:vertical}.syncgrid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:10px}.syncnow{font-size:16px;background:#b7ff4a!important;color:#081006!important;border-color:#b7ff4a!important}.currentline{margin-top:10px;padding:12px;border-radius:14px;background:#0e1221;border:1px solid #2d3554;min-height:48px}.currentline strong{color:#b7ff4a}', 1)

old_section = '<section class="card"><div class="step">3 · AI lyrics</div><div class="title">Analyze & sync lyrics</div><button id="aiBtn" class="secondary" disabled>✨ Analyze selected clip with AI</button><div id="aiStatus" class="status">Upload a song first.</div><div class="title" style="font-size:16px;margin-top:16px">Lyric style</div>'
if old_section not in s:
    old_section = '<section class="card"><div class="step">3 · AI lyrics</div><div class="title">Analyze & sync lyrics</div><button id="aiBtn" class="secondary" disabled>✨ Analyze lyrics with AI</button><div id="aiStatus" class="status">Upload a song first.</div><div class="title" style="font-size:16px;margin-top:16px">Lyric style</div>'
new_section = '''<section class="card"><div class="step">3 · Lyrics</div><div class="title">Add your lyrics manually</div>
<textarea id="manualLyrics" class="lyricsbox" placeholder="Paste the lyrics for this 30–50 second section here.\n\nPut each lyric phrase on a new line, for example:\nwe don't have to\ndo this tonight\nlet's take it slow"></textarea>
<button id="aiBtn" class="hidden" disabled aria-hidden="true"></button>
<div class="syncgrid"><button id="startSyncBtn" class="secondary" disabled>▶ Start lyric sync</button><button id="tapSyncBtn" class="secondary syncnow" disabled>🎯 Tap next line</button></div>
<div class="syncgrid"><button id="undoSyncBtn" class="secondary" disabled>↶ Undo last tap</button><button id="finishSyncBtn" class="secondary" disabled>✓ Finish sync</button></div>
<div id="syncCurrent" class="currentline"><span class="meta">Paste your lyrics, then tap Start lyric sync.</span></div>
<div id="aiStatus" class="status">No AI needed — you control the lyric timing.</div>
<div class="tiny">While the selected song section plays, tap <strong>Tap next line</strong> exactly when each lyric line begins. Reelwave will save those timings and use them in the preview and exported video.</div>
<div class="title" style="font-size:16px;margin-top:16px">Lyric style</div>'''
if old_section not in s:
    raise SystemExit('Could not find lyric section')
s = s.replace(old_section, new_section, 1)

# Add DOM refs.
s = s.replace("shareBtn=$('shareBtn'),clipBox=$('clipBox')", "shareBtn=$('shareBtn'),manualLyrics=$('manualLyrics'),startSyncBtn=$('startSyncBtn'),tapSyncBtn=$('tapSyncBtn'),undoSyncBtn=$('undoSyncBtn'),finishSyncBtn=$('finishSyncBtn'),syncCurrent=$('syncCurrent'),clipBox=$('clipBox')", 1)

# Add state.
s = s.replace('songDuration=0,clipStart=0,clipLength=50;', 'songDuration=0,clipStart=0,clipLength=50,manualLines=[],syncMarks=[],syncIndex=0,syncing=false;', 1)

# Add manual sync helpers after selectedClipFile (or before media handler if function marker differs).
marker = "mediaInput.onchange=e=>{"
helpers = r'''
function cleanManualLines(){return manualLyrics.value.split(/\n+/).map(x=>x.trim()).filter(Boolean)}
function showSyncLine(){
  if(!manualLines.length){syncCurrent.innerHTML='<span class="meta">Paste your lyrics, then tap Start lyric sync.</span>';return}
  if(syncIndex>=manualLines.length){syncCurrent.innerHTML='<strong>All lines marked.</strong> Tap Finish sync.';return}
  syncCurrent.innerHTML=`<span class="meta">Next line ${syncIndex+1}/${manualLines.length}</span><br><strong>${esc(manualLines[syncIndex])}</strong>`;
}
function buildManualWords(){
  if(!manualLines.length||!syncMarks.length)return false;
  const marks=syncMarks.slice(0,manualLines.length);
  while(marks.length<manualLines.length){const prev=marks.length?marks[marks.length-1]:0;marks.push(Math.min(clipLength,prev+Math.max(.8,(clipLength-prev)/(manualLines.length-marks.length))))}
  words=[];
  for(let li=0;li<manualLines.length;li++){
    const start=Math.max(0,marks[li]);
    const next=li<manualLines.length-1?Math.max(start+.15,marks[li+1]):clipLength;
    const end=Math.min(clipLength,Math.max(start+.25,next));
    const parts=manualLines[li].split(/\s+/).filter(Boolean);
    const dur=Math.max(.2,end-start),step=dur/Math.max(1,parts.length);
    parts.forEach((word,i)=>words.push({word,start:start+i*step,end:Math.min(end,start+(i+1)*step),line:li}));
  }
  scenes=[];draw(Math.max(0,(audio.currentTime||clipStart)-clipStart);return true;
}
async function beginManualSync(){
  manualLines=cleanManualLines();
  if(!songFile){aiStatus.textContent='Upload a song first.';return}
  if(!manualLines.length){aiStatus.textContent='Paste your lyrics first, with each phrase on a new line.';return}
  syncMarks=[];syncIndex=0;syncing=true;words=[];scenes=[];
  startSyncBtn.disabled=true;tapSyncBtn.disabled=false;undoSyncBtn.disabled=false;finishSyncBtn.disabled=false;manualLyrics.disabled=true;
  showSyncLine();aiStatus.textContent='Syncing — tap each line when you hear it begin.';
  setupAudio();await ac.resume();audio.currentTime=clipStart;await audio.play();cancelAnimationFrame(raf);loop();
}
function markNextLine(){
  if(!syncing||syncIndex>=manualLines.length)return;
  const rel=Math.max(0,Math.min(clipLength,(audio.currentTime||clipStart)-clipStart));
  syncMarks[syncIndex]=rel;syncIndex++;
  if(syncIndex>=manualLines.length){tapSyncBtn.disabled=true;aiStatus.textContent='All lyric lines marked. Tap Finish sync.'}
  showSyncLine();
}
function undoSync(){
  if(!syncing||syncIndex<=0)return;syncIndex--;syncMarks=syncMarks.slice(0,syncIndex);tapSyncBtn.disabled=false;showSyncLine();aiStatus.textContent='Last timing removed — tap that line again.';
}
function finishManualSync(){
  if(!syncing)return;
  audio.pause();cancelAnimationFrame(raf);syncing=false;manualLyrics.disabled=false;startSyncBtn.disabled=false;tapSyncBtn.disabled=true;undoSyncBtn.disabled=true;finishSyncBtn.disabled=true;
  if(!syncMarks.length){aiStatus.textContent='No lyric timings were recorded.';showSyncLine();return}
  buildManualWords();aiStatus.innerHTML=`Lyrics synced manually: <strong>${manualLines.length}</strong> lines · <strong>${words.length}</strong> words. Ready to preview and export.`;
  syncCurrent.innerHTML='<strong>✓ Manual lyric sync complete</strong><br><span class="meta">You can preview it now, or start sync again to redo the timing.</span>';
}
startSyncBtn.onclick=beginManualSync;tapSyncBtn.onclick=markNextLine;undoSyncBtn.onclick=undoSync;finishSyncBtn.onclick=finishManualSync;
manualLyrics.oninput=()=>{manualLines=cleanManualLines();if(songFile&&!syncing)startSyncBtn.disabled=!manualLines.length;showSyncLine()};
'''
if marker not in s: raise SystemExit('Could not find media handler marker')
s = s.replace(marker, helpers + marker, 1)

# Enable manual sync when audio loads, and update messaging.
s = s.replace("aiBtn.disabled=previewBtn.disabled=exportBtn.disabled=false;aiStatus.textContent='Choose a 30–50 second section, then analyze it.';", "aiBtn.disabled=true;previewBtn.disabled=exportBtn.disabled=false;startSyncBtn.disabled=!cleanManualLines().length;aiStatus.textContent='Paste your lyrics and sync each line manually.';", 1)
s = s.replace("aiBtn.disabled=previewBtn.disabled=exportBtn.disabled=true;aiStatus.textContent='Reelwave lyric clips must be at least 30 seconds.';", "aiBtn.disabled=true;previewBtn.disabled=exportBtn.disabled=true;startSyncBtn.disabled=true;aiStatus.textContent='Reelwave lyric clips must be at least 30 seconds.';", 1)

# When clip range changes, clear manual timing instead of requesting AI.
s = s.replace("if(resetAI){words=[];scenes=[];aiStatus.textContent='Section changed — analyze this 30–50 sec clip with AI.'}", "if(resetAI){words=[];scenes=[];syncMarks=[];syncIndex=0;if(typeof manualLines!=='undefined')manualLines=cleanManualLines();aiStatus.textContent='Section changed — sync your lyric lines again for this clip.';if(typeof startSyncBtn!=='undefined')startSyncBtn.disabled=!songFile||!manualLines.length}", 1)

# Disable old AI handler by replacing it with harmless no-op if present.
start = s.find("aiBtn.onclick=async()=>")
if start != -1:
    end = s.find(";\npreviewBtn.onclick", start)
    if end != -1:
        s = s[:start] + "aiBtn.onclick=()=>{}" + s[end+1:]

# Make preview/export require synced lyrics, to avoid silent sky-only videos by accident.
s = s.replace("previewBtn.onclick=async()=>{setupAudio();", "previewBtn.onclick=async()=>{if(!words.length){aiStatus.textContent='Sync your manual lyrics first.';return}setupAudio();", 1)
s = s.replace("exportBtn.onclick=async()=>{if(!songFile)return;", "exportBtn.onclick=async()=>{if(!songFile)return;if(!words.length){exportStatus.textContent='Sync your manual lyrics first.';return}", 1)

# Update app description away from AI lyrics.
s = s.replace('Upload a song, choose a 30–50 second section, let AI time the lyrics, then use generated skies or your own photo/GIF.', 'Upload a song, choose a 30–50 second section, paste your lyrics, then tap along to sync each line. Use generated skies or your own photo/GIF and export the finished lyric video.', 1)
s = s.replace('Upload a song, let AI time the lyrics, then use generated skies or your own photo/GIF.', 'Upload a song, paste your lyrics and tap along to sync each line, then use generated skies or your own photo/GIF.', 1)

p.write_text(s, encoding='utf-8')
print('Added manual lyric entry with tap-to-sync timing; AI transcription is no longer required.')

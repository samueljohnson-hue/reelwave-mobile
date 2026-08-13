from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')

# Ensure manual-sync DOM refs exist.
old="shareBtn=$('shareBtn'),clipBox=$('clipBox')"
new="shareBtn=$('shareBtn'),manualLyrics=$('manualLyrics'),startSyncBtn=$('startSyncBtn'),tapSyncBtn=$('tapSyncBtn'),undoSyncBtn=$('undoSyncBtn'),finishSyncBtn=$('finishSyncBtn'),syncCurrent=$('syncCurrent'),clipBox=$('clipBox')"
if old in s:
    s=s.replace(old,new,1)

# Fix malformed playback loop introduced by the 30-50 second patch.
bad="function loop(){if(!audio.paused&&audio.currentTime>=clipStart+clipLength){audio.pause();cancelAnimationFrame(raf);draw(clipLength);return}const x=energy();draw(Math.max(0,(audio.currentTime||clipStart)-clipStart,x.energy,x.bass,x.mids,x.highs);raf=requestAnimationFrame(loop)}"
good="function loop(){if(!audio.paused&&audio.currentTime>=clipStart+clipLength){audio.pause();cancelAnimationFrame(raf);draw(clipLength);return}const x=energy();draw(Math.max(0,(audio.currentTime||clipStart)-clipStart),x.energy,x.bass,x.mids,x.highs);raf=requestAnimationFrame(loop)}"
if bad in s:
    s=s.replace(bad,good,1)

# Add a visible boot error rather than silently disabling all controls.
s=s.replace("(()=>{const $=id=>document.getElementById(id),", "(()=>{window.addEventListener('error',e=>{const el=document.getElementById('audioMeta');if(el)el.textContent='App error: '+e.message});const $=id=>document.getElementById(id),",1)

p.write_text(s,encoding='utf-8')
print('Applied UI refs + playback loop syntax fix.')
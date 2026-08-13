from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
# Manual sync patch accidentally referenced its new DOM variables before they existed,
# causing the entire script to stop and making file/sky controls appear dead.
old="shareBtn=$('shareBtn'),clipBox=$('clipBox')"
new="shareBtn=$('shareBtn'),manualLyrics=$('manualLyrics'),startSyncBtn=$('startSyncBtn'),tapSyncBtn=$('tapSyncBtn'),undoSyncBtn=$('undoSyncBtn'),finishSyncBtn=$('finishSyncBtn'),syncCurrent=$('syncCurrent'),clipBox=$('clipBox')"
if old in s:
    s=s.replace(old,new,1)
# If the previous patch already inserted refs, leave them intact.
# Add a visible boot error rather than silently disabling all controls.
s=s.replace("(()=>{const $=id=>document.getElementById(id),", "(()=>{window.addEventListener('error',e=>{const el=document.getElementById('audioMeta');if(el)el.textContent='App error: '+e.message});const $=id=>document.getElementById(id),",1)
p.write_text(s,encoding='utf-8')
print('Applied v12 UI boot/control fix.')
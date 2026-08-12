from pathlib import Path

p = Path('build-src/reelwave-mobile-v3/www/index.html')
s = p.read_text(encoding='utf-8')

s = s.replace("  let recorder = null, chunks = [];\n  let audioSourceFile = null;", "  let recorder = null, chunks = [];\n  let exportStopTimer = null;\n  let exportStartedAt = 0;\n  let audioSourceFile = null;")

s = s.replace("""    await new Promise(res=>{\n      if(audioEl.readyState >= 1) return res();\n      audioEl.addEventListener('loadedmetadata', res, {once:true});\n    });\n    if(!state.audioDuration) state.audioDuration = audioEl.duration || 0;\n\n    state.audioLoaded = true;\n""", """    await new Promise(res=>{\n      if(audioEl.readyState >= 1) return res();\n      audioEl.addEventListener('loadedmetadata', res, {once:true});\n    });\n\n    // Android WebView can occasionally return a bogus decoded duration (often ~1s).\n    // Prefer the longest sane duration reported by either Web Audio or the media element.\n    const elementDuration = Number.isFinite(audioEl.duration) && audioEl.duration > 0 ? audioEl.duration : 0;\n    state.audioDuration = Math.max(state.audioDuration || 0, elementDuration);\n    if(state.audioDuration <= 1.1){\n      try{\n        await new Promise((resolve)=>{\n          const done = ()=>resolve();\n          audioEl.addEventListener('durationchange', done, {once:true});\n          audioEl.addEventListener('canplay', done, {once:true});\n          setTimeout(done, 1200);\n        });\n        const retryDuration = Number.isFinite(audioEl.duration) && audioEl.duration > 0 ? audioEl.duration : 0;\n        state.audioDuration = Math.max(state.audioDuration || 0, retryDuration);\n      }catch(_){}\n    }\n\n    state.audioLoaded = true;\n""")

s = s.replace("""      if(state.isExporting && audioEl.currentTime >= state.trim.end - 0.03){\n        finishExport();\n      }\n""", """      // Android export completion is controlled by a wall-clock timer.\n""")

s = s.replace("""    if(recorder && recorder.state !== 'inactive') recorder.stop();\n    audioEl.pause();\n    state.isExporting = false;\n    setExportUIState(false);\n""", """    if(exportStopTimer){ clearTimeout(exportStopTimer); exportStopTimer = null; }\n    if(recorder && recorder.state !== 'inactive') recorder.stop();\n    audioEl.pause();\n    state.isExporting = false;\n    setExportUIState(false);\n""", 1)

old = """    state.isExporting = true;\n    setExportUIState(true);\n\n    audioEl.muted = false; audioEl.volume = 1;\n    audioEl.currentTime = state.trim.start;\n    await audioEl.play();\n    recorder.start(200);\n"""
new = """    state.isExporting = true;\n    setExportUIState(true);\n\n    audioEl.muted = false; audioEl.volume = 1;\n    audioEl.pause();\n    audioEl.currentTime = state.trim.start;\n    try{\n      await new Promise((resolve)=>{\n        if(Math.abs(audioEl.currentTime - state.trim.start) < 0.15 && audioEl.readyState >= 2) return resolve();\n        const done = ()=>resolve();\n        audioEl.addEventListener('seeked', done, {once:true});\n        setTimeout(done, 700);\n      });\n    }catch(_){}\n\n    // Start MediaRecorder first, then audio. Android WebView may otherwise create a tiny file.\n    recorder.start(250);\n    exportStartedAt = performance.now();\n    try{ await audioEl.play(); }catch(err){\n      if(recorder && recorder.state !== 'inactive') recorder.stop();\n      state.isExporting = false;\n      setExportUIState(false);\n      alert('Reelwave could not start the selected audio. Please choose the audio file again.');\n      return;\n    }\n\n    const exportMs = Math.max(1000, Math.round(totalDuration()*1000));\n    exportStopTimer = setTimeout(()=>finishExport(), exportMs + 250);\n"""
if old not in s:
    raise SystemExit('Could not find Android export start block')
s = s.replace(old, new)

s = s.replace("""  function finishExport(){\n    if(recorder && recorder.state !== 'inactive') recorder.stop();\n    audioEl.pause();\n    state.isExporting = false;\n  }\n""", """  function finishExport(){\n    if(exportStopTimer){ clearTimeout(exportStopTimer); exportStopTimer = null; }\n    if(recorder && recorder.state !== 'inactive') recorder.stop();\n    audioEl.pause();\n    state.isExporting = false;\n  }\n""")

s = s.replace("""    const t = clamp(audioEl.currentTime - state.trim.start, 0, totalDuration());\n    const pct = Math.round((t/totalDuration())*100);\n""", """    const elapsed = Math.max(0, (performance.now() - exportStartedAt) / 1000);\n    const pct = Math.round((Math.min(elapsed, totalDuration())/totalDuration())*100);\n""")

p.write_text(s, encoding='utf-8')
print('Applied Android duration/export fix')

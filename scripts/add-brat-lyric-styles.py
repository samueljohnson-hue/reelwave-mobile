from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
# Remove Brat buttons from sky selector if present after expanded-sky patch.
s=s.replace('<button class="chip" data-style="brat1">Brat 1</button><button class="chip" data-style="brat2">Brat 2</button>','')
# Add Brat 1/2 to lyric selector.
needle='<button class="chip" data-lyric="minimal">Minimal</button>'
if needle in s and 'data-lyric="brat1"' not in s:
    s=s.replace(needle, needle+'<button class="chip" data-lyric="brat1">Brat 1</button><button class="chip" data-lyric="brat2">Brat 2</button>',1)
# Extend lyric drawing: same reference-inspired narrow lowercase layout, black vs white.
old="ctx.font='700 46px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle='#fff';ctx.shadowColor='rgba(0,0,0,.65)';ctx.shadowBlur=12;"
new="const brat=lyricMode==='brat1'||lyricMode==='brat2';ctx.font=brat?'400 52px Arial Narrow, Arial, sans-serif':'700 46px Arial';ctx.textAlign=brat?'left':'center';ctx.textBaseline='middle';ctx.fillStyle=lyricMode==='brat1'?'#111': '#fff';ctx.shadowColor=lyricMode==='brat2'?'rgba(0,0,0,.5)':'rgba(255,255,255,.18)';ctx.shadowBlur=brat?5:12;"
if old in s:s=s.replace(old,new,1)
# If lyric renderer has centered x/y, introduce deterministic free placement for brat styles.
s=s.replace("ctx.fillText(line,360,1040);", "if(brat){const seed=Math.floor(t*1.7)%6;const pos=[[80,250],[390,330],[120,570],[370,690],[90,880],[330,1010]][seed];ctx.fillText(String(line).toLowerCase(),pos[0],pos[1]);}else ctx.fillText(line,360,1040);",1)
p.write_text(s,encoding='utf-8')
print('Moved Brat 1/2 to lyric styles: black and white reference-inspired variants.')

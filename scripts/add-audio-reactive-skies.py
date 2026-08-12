from pathlib import Path

p=Path('www/index.html')
s=p.read_text(encoding='utf-8')

old_energy="function energy(){if(!analyser)return{energy:.2,bass:.2};const b=new Uint8Array(analyser.frequencyBinCount);analyser.getByteFrequencyData(b);let s=0,bs=0;for(let i=0;i<b.length;i++){s+=b[i];if(i<40)bs+=b[i]}const e=s/b.length/255,bass=bs/40/255;history.push(e);if(history.length>42)history.shift();const avg=history.reduce((a,v)=>a+v,0)/history.length,now=performance.now();if(e>avg*1.25&&e>.15&&now-lastBeat>230){beatPulse=1;lastBeat=now}beatPulse*=.88;return{energy:e,bass}}"
new_energy="function energy(){if(!analyser)return{energy:.2,bass:.2,mids:.2,highs:.2};const f=new Uint8Array(analyser.frequencyBinCount);analyser.getByteFrequencyData(f);let total=0,lo=0,mid=0,hi=0;for(let i=0;i<f.length;i++){total+=f[i];if(i<36)lo+=f[i];else if(i<150)mid+=f[i];else hi+=f[i]}const e=total/f.length/255,bass=lo/36/255,mids=mid/114/255,highs=hi/Math.max(1,f.length-150)/255;history.push(e);if(history.length>48)history.shift();const avg=history.reduce((a,v)=>a+v,0)/history.length,now=performance.now();if((bass>0.34&&bass>e*1.05)||(e>avg*1.25&&e>.15)){if(now-lastBeat>210){beatPulse=1;lastBeat=now}}beatPulse*=.86;return{energy:e,bass,mids,highs}}"
if old_energy not in s: raise SystemExit('energy fn not found')
s=s.replace(old_energy,new_energy,1)

old_loop="function loop(){const x=energy();draw(audio.currentTime||0,x.energy,x.bass);raf=requestAnimationFrame(loop)}"
new_loop="function loop(){const x=energy();draw(audio.currentTime||0,x.energy,x.bass,x.mids,x.highs);raf=requestAnimationFrame(loop)}"
if old_loop in s:s=s.replace(old_loop,new_loop,1)

s=s.replace("function draw(t,e=.2,b=.2){if(mode!=='media')drawSky(t,e,b);else{ctx.fillStyle='#000';ctx.fillRect(0,0,720,1280)}drawMedia(t,e);drawLyrics(t)}",
"function draw(t,e=.2,b=.2,m=.2,h=.2){if(mode!=='media')drawSky(t,e,b,m,h);else{ctx.fillStyle='#000';ctx.fillRect(0,0,720,1280)}drawMedia(t,e,b,m,h);drawLyrics(t)}",1)

s=s.replace("function drawMedia(t,e){if(!mediaImg||mode==='sky')return;const r=coverRect(mediaImg),pulse=1+beatPulse*.055+e*.025,panX=Math.sin(t*.18)*22,panY=Math.cos(t*.13)*16;",
"function drawMedia(t,e,b=.2,m=.2,h=.2){if(!mediaImg||mode==='sky')return;const r=coverRect(mediaImg),pulse=1+beatPulse*.07+b*.05,panX=Math.sin(t*(.15+m*.55))*22*(.6+m),panY=Math.cos(t*(.11+h*.45))*16*(.6+h);",1)

s=s.replace("function drawSky(t,e,b){","function drawSky(t,e,b,m=.2,h=.2){",1)
s=s.replace("for(let i=0;i<7;i++){const x=((i*143+t*(40+i*5))%1000)-150,y=180+i*130+Math.sin(t*.25+i)*35;cloud(x,y,70+i*5,.07+e*.08)}",
"for(let i=0;i<7;i++){const speed=(28+i*5)*(1+m*1.7),x=((i*143+t*speed)%1000)-150,y=180+i*130+Math.sin(t*(.18+h*.6)+i)*35*(.7+h);cloud(x,y,(70+i*5)*(1+b*.12),.07+e*.08+m*.05)}",1)
s=s.replace("ctx.globalAlpha=.2+e*.3;ctx.fillStyle='#fff';for(let i=0;i<50;i++){ctx.fillRect((i*137.7)%720,(i*83.1+t*(10+i%5))%1280,2,2)}",
"ctx.globalAlpha=.16+e*.24+h*.28;ctx.fillStyle='#fff';for(let i=0;i<65;i++){const sz=1+(i%3)+(h>.55?1:0);ctx.fillRect((i*137.7+t*h*12)%720,(i*83.1+t*(8+i%5)*(1+h))%1280,sz,sz)}",1)
s=s.replace("if(style==='aurora'){for(let k=0;k<4;k++){ctx.beginPath();ctx.lineWidth=65+k*13;ctx.strokeStyle=`rgba(${80+k*35},255,${190+k*10},${.12+e*.12})`;for(let x=0;x<=720;x+=20){const y=260+k*95+Math.sin(x*.012+t*.7+k)*75; x===0?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke()}}",
"if(style==='aurora'){for(let k=0;k<4;k++){ctx.beginPath();ctx.lineWidth=(65+k*13)*(1+b*.08);ctx.strokeStyle=`rgba(${80+k*35},255,${190+k*10},${.10+e*.08+h*.22})`;for(let x=0;x<=720;x+=20){const y=260+k*95+Math.sin(x*.012+t*(.45+m*1.2)+k)*75*(.7+h*.65);x===0?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke()}}",1)
s=s.replace("if(style==='thunder'&&beatPulse>.35){","if(style==='thunder'&&(beatPulse>.35||h>.72)){",1)

p.write_text(s,encoding='utf-8')
print('Added multiband beat-reactive movement: bass, mids, highs, beat pulse.')

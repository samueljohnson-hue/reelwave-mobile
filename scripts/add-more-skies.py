from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# Add more visual preset buttons.
old_buttons = '<button class="chip active" data-style="dream">Dream Sky</button><button class="chip" data-style="storm">Storm</button><button class="chip" data-style="sunset">Sunset</button><button class="chip" data-style="brat1">Brat 1</button><button class="chip" data-style="brat2">Brat 2</button>'
new_buttons = '<button class="chip active" data-style="dream">Dream Sky</button><button class="chip" data-style="storm">Storm</button><button class="chip" data-style="sunset">Sunset</button><button class="chip" data-style="aurora">Aurora</button><button class="chip" data-style="galaxy">Galaxy</button><button class="chip" data-style="moon">Moonlight</button><button class="chip" data-style="heaven">Heaven</button><button class="chip" data-style="pink">Pink Clouds</button><button class="chip" data-style="thunder">Thunder</button><button class="chip" data-style="golden">Golden Hour</button><button class="chip" data-style="brat1">Brat 1</button><button class="chip" data-style="brat2">Brat 2</button>'
if old_buttons in s:
    s = s.replace(old_buttons, new_buttons, 1)

old_palettes = "const palettes={dream:['#090d2b','#3a2874','#df7dff','#8fd7ff'],storm:['#05070c','#172033','#53617a','#b7c8e8'],sunset:['#26102f','#812b50','#ff8359','#ffd57b'],brat1:['#081006','#16320c','#78a836','#b7ff4a'],brat2:['#050505','#324100','#93c230','#b7ff4a']};"
new_palettes = "const palettes={dream:['#090d2b','#3a2874','#df7dff','#8fd7ff'],storm:['#05070c','#172033','#53617a','#b7c8e8'],sunset:['#26102f','#812b50','#ff8359','#ffd57b'],aurora:['#02141c','#083f51','#16a58f','#79ffd2'],galaxy:['#050018','#1a0a4d','#67298b','#e57dff'],moon:['#02050e','#0e1b39','#5270a3','#c9ddff'],heaven:['#5e93c7','#9ed1ee','#eef9ff','#ffffff'],pink:['#3c123d','#9b3e79','#ff94c9','#ffd6ea'],thunder:['#020308','#111827','#344256','#d7e7ff'],golden:['#35130b','#9c4820','#f39b46','#ffe3a0'],brat1:['#081006','#16320c','#78a836','#b7ff4a'],brat2:['#050505','#324100','#93c230','#b7ff4a']};"
if old_palettes in s:
    s = s.replace(old_palettes, new_palettes, 1)

old_draw = "function drawSky(t,e,b){const p=palettes[style],g=ctx.createLinearGradient(0,0,0,1280);p.forEach((c,i)=>g.addColorStop(i/(p.length-1),c));ctx.fillStyle=g;ctx.fillRect(0,0,720,1280);for(let i=0;i<7;i++){const x=((i*143+t*(40+i*5))%1000)-150,y=180+i*130+Math.sin(t*.25+i)*35;cloud(x,y,70+i*5,.08+e*.08)}ctx.globalAlpha=.25+e*.3;ctx.fillStyle='#fff';for(let i=0;i<50;i++){ctx.fillRect((i*137.7)%720,(i*83.1+t*(10+i%5))%1280,2,2)}ctx.globalAlpha=1;if(style==='brat2'&&beatPulse>.35){ctx.fillStyle=`rgba(183,255,74,${beatPulse*.2})`;ctx.fillRect(0,0,720,1280)}}"
new_draw = r'''function drawSky(t,e,b){const p=palettes[style]||palettes.dream,g=ctx.createLinearGradient(0,0,0,1280);p.forEach((c,i)=>g.addColorStop(i/(p.length-1),c));ctx.fillStyle=g;ctx.fillRect(0,0,720,1280);
if(style==='aurora'){for(let k=0;k<4;k++){ctx.beginPath();ctx.lineWidth=65+k*13;ctx.strokeStyle=`rgba(${80+k*35},255,${190+k*10},${.12+e*.12})`;for(let x=0;x<=720;x+=20){const y=260+k*95+Math.sin(x*.012+t*.7+k)*75; x===0?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke()}}
if(style==='galaxy'){for(let i=0;i<80;i++){const a=i*.61+t*.025,r=40+(i%28)*11,x=360+Math.cos(a)*r,y=560+Math.sin(a)*r*.55;ctx.fillStyle=`rgba(255,${120+i%120},255,${.12+e*.25})`;ctx.fillRect(x,y,2+(i%3),2+(i%3))}}
if(style==='moon'){const mx=540+Math.sin(t*.05)*25,my=235;const rg=ctx.createRadialGradient(mx,my,10,mx,my,130);rg.addColorStop(0,'rgba(255,255,240,.95)');rg.addColorStop(.35,'rgba(210,230,255,.5)');rg.addColorStop(1,'rgba(190,220,255,0)');ctx.fillStyle=rg;ctx.beginPath();ctx.arc(mx,my,130,0,Math.PI*2);ctx.fill()}
if(style==='heaven'){ctx.globalAlpha=.24+e*.12;for(let i=0;i<9;i++)cloud(((i*157+t*22)%950)-110,240+i*95,95+i*4,.18);ctx.globalAlpha=1}
if(style==='thunder'&&beatPulse>.35){ctx.strokeStyle=`rgba(230,245,255,${.35+beatPulse*.55})`;ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(500,80);ctx.lineTo(430,360);ctx.lineTo(510,330);ctx.lineTo(395,660);ctx.stroke()}
for(let i=0;i<7;i++){const x=((i*143+t*(40+i*5))%1000)-150,y=180+i*130+Math.sin(t*.25+i)*35;cloud(x,y,70+i*5,.07+e*.08)}ctx.globalAlpha=.2+e*.3;ctx.fillStyle='#fff';for(let i=0;i<50;i++){ctx.fillRect((i*137.7)%720,(i*83.1+t*(10+i%5))%1280,2,2)}ctx.globalAlpha=1;if(style==='brat2'&&beatPulse>.35){ctx.fillStyle=`rgba(183,255,74,${beatPulse*.2})`;ctx.fillRect(0,0,720,1280)}if(style==='pink'&&beatPulse>.5){ctx.fillStyle=`rgba(255,160,215,${beatPulse*.1})`;ctx.fillRect(0,0,720,1280)}if(style==='golden'){const rg=ctx.createRadialGradient(530,250,20,530,250,260);rg.addColorStop(0,'rgba(255,245,190,.8)');rg.addColorStop(1,'rgba(255,170,70,0)');ctx.fillStyle=rg;ctx.fillRect(0,0,720,600)}}'''
if old_draw in s:
    s = s.replace(old_draw, new_draw, 1)

# Make failed API responses user-readable instead of generic fetch failures.
s = s.replace("if(!r.ok)throw new Error(await r.text());const data=await r.json();", "if(!r.ok){let msg='AI analysis failed';try{const er=await r.json();msg=er.error||msg}catch{try{msg=await r.text()||msg}catch{}}throw new Error(msg)}const data=await r.json();", 1)

p.write_text(s,encoding='utf-8')
print('Added expanded sky presets and clearer AI errors.')

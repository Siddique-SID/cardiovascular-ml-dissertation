from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math
root=Path(__file__).resolve().parents[1]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def f(size,path=font):return ImageFont.truetype(path,size)
frames=[]
for frame in range(24):
 im=Image.new('RGB',(1200,360),'#300c19');d=ImageDraw.Draw(im)
 d.rectangle((1,1,1198,358),outline='#82475c',width=2)
 d.text((45,28),'CARDIO  /  A STUDY IN COMPARISON',font=f(13),fill='#d3a3af')
 d.text((45,85),'Seven models.',font=f(56,bold),fill='#fff1df')
 d.text((45,154),'One shared test.',font=f(52,serif),fill='#f6b69a')
 d.text((47,244),'MSc RESEARCH  ·  SIDDIQUE SAYED  ·  LIVERPOOL 2026',font=f(13),fill='#d3a3af')
 d.text((47,291),'70,000 records  /  7 classifiers  /  5 evaluation metrics',font=f(15),fill='#fff1df')
 cx,cy=946,171
 for orbit in range(7):
  theta=orbit*math.pi/7+frame*math.pi/540
  pts=[]
  for i in range(121):
   t=2*math.pi*i/120
   x,y=166*math.cos(t),55*math.sin(t)
   pts.append((cx+x*math.cos(theta)-y*math.sin(theta),cy+x*math.sin(theta)+y*math.cos(theta)))
  d.line(pts,fill='#94586b',width=1)
  t=frame*2*math.pi/24+orbit*.8
  x,y=166*math.cos(t),55*math.sin(t)
  dx,dy=cx+x*math.cos(theta)-y*math.sin(theta),cy+x*math.sin(theta)+y*math.cos(theta)
  d.ellipse((dx-3,dy-3,dx+3,dy+3),fill='#f6b69a')
 d.ellipse((cx-70,cy-70,cx+70,cy+70),fill='#300c19',outline='#94586b')
 d.text((cx,cy-24),'7',anchor='mm',font=f(42,bold),fill='#fff1df')
 d.text((cx,cy+18),'PERSPECTIVES',anchor='mm',font=f(10),fill='#d3a3af')
 
 if frame == 0: palette = im.quantize(colors=32)
 frames.append(im.quantize(palette=palette))
frames[0].save(root/'docs/cover.gif',save_all=True,append_images=frames[1:],duration=150,loop=0,optimize=True,disposal=1)
frames[0].save(root/'docs/cover-preview.png')
print('Animated cover:',(root/'docs/cover.gif').stat().st_size,'bytes')

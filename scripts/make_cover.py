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
 im=Image.new('RGB',(1200,360),'#102f43');d=ImageDraw.Draw(im)
 d.rectangle((1,1,1198,358),outline='#2c6479',width=2)
 d.text((45,28),'CARDIO  /  A STUDY IN COMPARISON',font=f(13),fill='#9fc8d0')
 d.text((45,85),'Seven models.',font=f(56,bold),fill='#eff8f8')
 d.text((45,154),'One shared test.',font=f(52,serif),fill='#76d6c6')
 d.text((47,244),'MSc RESEARCH  ·  SIDDIQUE SAYED  ·  LIVERPOOL 2026',font=f(13),fill='#9fc8d0')
 d.text((47,291),'70,000 records  /  7 classifiers  /  5 evaluation metrics',font=f(15),fill='#eff8f8')
 cx,cy=946,171
 for orbit in range(7):
  theta=orbit*math.pi/7+frame*math.pi/540
  pts=[]
  for i in range(121):
   t=2*math.pi*i/120
   x,y=166*math.cos(t),55*math.sin(t)
   pts.append((cx+x*math.cos(theta)-y*math.sin(theta),cy+x*math.sin(theta)+y*math.cos(theta)))
  d.line(pts,fill='#36768a',width=1)
  t=frame*2*math.pi/24+orbit*.8
  x,y=166*math.cos(t),55*math.sin(t)
  dx,dy=cx+x*math.cos(theta)-y*math.sin(theta),cy+x*math.sin(theta)+y*math.cos(theta)
  d.ellipse((dx-3,dy-3,dx+3,dy+3),fill='#76d6c6')
 d.ellipse((cx-70,cy-70,cx+70,cy+70),fill='#102f43',outline='#36768a')
 d.text((cx,cy-24),'7',anchor='mm',font=f(42,bold),fill='#eff8f8')
 d.text((cx,cy+18),'PERSPECTIVES',anchor='mm',font=f(10),fill='#9fc8d0')
 
 if frame == 0: palette = im.quantize(colors=32)
 frames.append(im.quantize(palette=palette))
frames[0].save(root/'docs/cover.gif',save_all=True,append_images=frames[1:],duration=150,loop=0,optimize=True,disposal=1)
frames[0].save(root/'docs/cover-preview.png')
print('Animated cover:',(root/'docs/cover.gif').stat().st_size,'bytes')

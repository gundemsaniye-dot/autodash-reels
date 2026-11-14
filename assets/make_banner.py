# usage: python3 make_banner.py "LINE ONE" "LINE TWO"  -> writes banner_tall.png (1080x270)
import sys
from PIL import Image, ImageDraw, ImageFont
P='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
l1,l2=(sys.argv[1].upper(),sys.argv[2].upper())
b=Image.new('RGBA',(1080,270)); px=b.load()
for y in range(270):
    for x in range(1080):
        t=x/1079; px[x,y]=(int(12+30*t),int(14+8*t),int(30+60*t),255)
d=ImageDraw.Draw(b); d.rectangle((0,0,1079,8),fill=(48,209,88)); d.rectangle((0,261,1079,269),fill=(48,209,88))
def fit(txt,size):
    while size>34:
        f=ImageFont.truetype(P,size)
        if d.textlength(txt,font=f)<=880: return f
        size-=2
    return ImageFont.truetype(P,34)
for txt,size,y,col in [(l1,70,40,'white'),(l2,84,128,(48,224,98))]:
    f=fit(txt,size); w=d.textlength(txt,font=f); d.text(((1080-w)/2,y),txt,font=f,fill=col)
b.save('banner_tall.png')

# usage: python3 make_photo_reel.py OUT.mp4 "HOOK LINE 1" "HOOK LINE 2" AUDIO.mp3 img1.jpg img2.jpg ...
# Photo post -> 9:16 Reel: blurred bg of each photo, sharp photo fitted in the safe area, slim top banner,
# SAFE AREA (IG/TikTok/YouTube Shorts UI): all text, banner and card stay inside y=230..1480 and x=90..890 (see SAFE_AREA.md).
# AutoDash App Store card visible from the first second, whoosh on every slide change, post audio as music, ad appended.
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
out,l1,l2,audio=sys.argv[1:5]; imgs=sys.argv[5:]
P='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
# slim banner 1080x170
b=Image.new('RGBA',(1080,170)); px=b.load()
for y in range(170):
    for x in range(1080):
        t=x/1079; px[x,y]=(int(12+30*t),int(14+8*t),int(30+60*t),255)
d=ImageDraw.Draw(b); d.rectangle((0,0,1079,6),fill=(48,209,88)); d.rectangle((0,163,1079,169),fill=(48,209,88))
def fit(txt,size):
    while size>30:
        f=ImageFont.truetype(P,size)
        if d.textlength(txt,font=f)<=880: return f
        size-=2
    return ImageFont.truetype(P,30)
for txt,size,y,col in [(l1.upper(),46,20,'white'),(l2.upper(),58,78,(48,224,98))]:
    f=fit(txt,size); w=d.textlength(txt,font=f); d.text(((1080-w)/2,y),txt,font=f,fill=col)
b.save('banner_photo.png')
N=len(imgs); CL=3.0; X=0.4; step=CL-X; total=round(CL+(N-1)*step,2)
inp=[]
for im in imgs: inp+=["-loop","1","-framerate","30","-t",str(CL),"-i",im]
k=N
inp+=["-i","banner_photo.png","-i","lower.png","-i",audio,"-i","whoosh.wav","-i","pop.wav","-i","ad.mp4"]
ib,ic,ia,iw,ip,iad=N,N+1,N+2,N+3,N+4,N+5
fc=[]
for i in range(N):
    fc.append(f"[{i}:v]split[s{i}a][s{i}b];[s{i}a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.18[bg{i}];"
              f"[s{i}b]scale=-2:880[fg{i}];[bg{i}][fg{i}]overlay=x=(W-w)/2:y=420,fps=30,setsar=1,format=yuv420p[c{i}]")
cur="c0"
for i in range(1,N):
    off=round(i*step,2)
    fc.append(f"[{cur}][c{i}]xfade=transition=slideleft:duration={X}:offset={off}[x{i}]"); cur=f"x{i}"
fc.append(f"[{cur}][{ib}:v]overlay=x=0:y=240[t1]")
fc.append(f"[{ic}:v]format=rgba,scale=780:-2[cd]")
fc.append(f"[t1][cd]overlay=x=90:y='1310+620*exp(-12*(t-0.15))'[t2]")
fc.append(f"color=c=0x00E5FF:s=1080x14:r=30:d={total+1}[bar]")
fc.append(f"[t2][bar]overlay=x='-W+W*t/{total}':y=H-14:shortest=1,format=yuv420p[v]")
# audio
fc.append(f"[{ia}:a]aresample=48000,atrim=0:{total},afade=t=in:d=0.4,afade=t=out:st={total-1.5}:d=1.5,volume=0.8[mu]")
fc.append(f"[{iw}:a]asplit={N-1}"+"".join(f"[w{i}]" for i in range(1,N)) if N>2 else f"[{iw}:a]anull[w1]")
labs=["[mu]"]
for i in range(1,N):
    ms=int(max(0,i*step-0.05)*1000); fc.append(f"[w{i}]adelay={ms}|{ms},volume=0.7[wd{i}]"); labs.append(f"[wd{i}]")
fc.append(f"[{ip}:a]adelay=150|150,volume=0.8[pd]"); labs.append("[pd]")
fc.append(f"{''.join(labs)}amix=inputs={len(labs)}:duration=first:normalize=0,alimiter=limit=0.95[a]")
cmd=["ffmpeg","-v","error","-y"]+inp+["-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-t",str(total),"-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","160k","photo_body.mp4"]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.stderr[-1500:])
off=round(total-0.35,2)
cmd2=["ffmpeg","-v","error","-y","-i","photo_body.mp4","-i","ad.mp4","-filter_complex",
 f"[0:v]fps=30,format=yuv420p[a];[1:v]fps=30,format=yuv420p[b];[a][b]xfade=transition=smoothleft:duration=0.35:offset={off}[v];[0:a]aresample=48000[a0];[1:a]aresample=48000[a1];[a0][a1]acrossfade=d=0.35[ao]",
 "-map","[v]","-map","[ao]","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out]
r=subprocess.run(cmd2,capture_output=True,text=True); print(r.stderr[-800:])

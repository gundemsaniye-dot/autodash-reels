import subprocess,sys,json
src,out=sys.argv[1],sys.argv[2]
D=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]).decode())
D=round(D,2)
tc=0.15; tstar=round(min(D*0.45,6),2)
pulses=[1.2,tstar,round(D*0.5,2),tc]
z="1.03+0.03*sin(2*PI*t/9)+"+"+".join(f"if(gte(t,{p}),0.05*exp(-7*(t-{p})),0)" for p in pulses)
inputs=["-i",src]+sum([["-loop","1","-framerate","30","-t",str(D+1),"-i",f] for f in ["banner_tall.png","sticker_new.png","sticker_spark.png","lower.png"]],[])+["-i","music.wav","-i","whoosh.wav","-i","pop.wav"]
fc=[
 "[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=contrast=1.06:saturation=1.18,vignette=PI/5,fade=t=in:d=0.2[z]",
 "[1:v]format=rgba[ban]","[2:v]format=rgba[nw]",
 f"[3:v]format=rgba,scale=w=-2:h='max(4,230*pow(min(1,max(0,t-{tstar})/0.25),0.7))':eval=frame[st]","[4:v]format=rgba[cd]",
 "[z][ban]overlay=x=0:y=195:shortest=1[v1]",
 f"[v1][nw]overlay=x=600:y='500+330*exp(-9*(t-1.2))*cos(14*(t-1.2))+6*sin(8*t)':enable='between(t,1.2,3.2)'[v2]",
 f"[v2][st]overlay=x='80-w/2+90':y='1020-(t-{tstar})*40-h/2':enable='between(t,{tstar},{tstar+2.4})'[v3]",
 f"[v3][cd]overlay=x=40:y='1390+540*exp(-12*(t-{tc}))':enable='gte(t,{tc})'[v4]",
 f"color=c=0x00E5FF:s=1080x14:r=30:d={D+1}[bar]",
 f"[v4][bar]overlay=x='-W+W*t/{D}':y=H-14:shortest=1[v]",
 f"[0:a]aresample=48000,volume=1.0[a0]",
 f"[5:a]atrim=0:{D},afade=t=in:d=0.5,afade=t=out:st={D-1.5}:d=1.5,volume=0.12[mu]",
 "[6:a]asplit=2[w1][w2]","[7:a]asplit=2[p1][p2]",
 "[w1]adelay=30|30,volume=0.8[wa]",
 f"[w2]adelay=1200|1200,volume=0.8[wb]",
 f"[p1]adelay={int(tstar*1000)}|{int(tstar*1000)},volume=0.8[pa]",
 f"[p2]adelay={int(tc*1000)}|{int(tc*1000)},volume=0.8[pb]",
 f"[a0][mu][wa][wb][pa][pb]amix=inputs=6:duration=first:normalize=0,alimiter=limit=0.95[a]"]
cmd=["ffmpeg","-v","error","-y"]+inputs+["-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-t",str(D),"-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","160k","body.mp4"]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.stderr[-1200:])
off=round(D-0.35,2)
cmd2=["ffmpeg","-v","error","-y","-i","body.mp4","-i","ad.mp4","-filter_complex",
 f"[0:v]fps=30,format=yuv420p[a];[1:v]fps=30,format=yuv420p[b];[a][b]xfade=transition=smoothleft:duration=0.35:offset={off}[v];[0:a]aresample=48000[a0];[1:a]aresample=48000[a1];[a0][a1]acrossfade=d=0.35[ao]",
 "-map","[v]","-map","[ao]","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out]
r=subprocess.run(cmd2,capture_output=True,text=True); print(r.stderr[-800:])

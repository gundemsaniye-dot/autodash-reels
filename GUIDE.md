# car-widgets-autodash: daily Reel workflow
Instagram: next.gen.studio.app (Business) via Buffer channel id 6af841af62b70b94b02b77bb, org 6af8413f700167741ad07cb8.
Source: TikTok @car.widget. Goal: re-edit one NEW video per run, append the Car Widgets: AutoDash ad (assets/ad.mp4), publish as Instagram Reel.

## Rules
1. Never repost the original unedited. Never reuse an ID listed in posted.json.
2. Download with yt-dlp (no watermark): `pip install --break-system-packages yt-dlp`; list: `yt-dlp --flat-playlist --playlist-end 20 --print "%(id)s | %(upload_date)s | %(duration)s | %(title).80s" https://www.tiktok.com/@car.widget`. Pick the newest ID not in posted.json that downloads as a normal video (5-60 s). Skip photo posts.
3. Banner: look at 4 frames, find where the original burned-in caption sits, write a NEW 2-line English hook for the video topic: `cd assets && python3 make_banner.py "LINE ONE" "LINE TWO"`. The banner covers y=195..465 of the 1080x1920 frame; if the original text sits elsewhere, adjust y in make_reel.py (overlay y=195) so no original text leaks.
4. Render: `cd assets && python3 make_reel.py ../src.mp4 ../reel.mp4` (no zoom; bottom App Store card visible from the first second; NEW + star stickers; music 12 %; ad appended with a soft transition).
5. QC: ffprobe 1080x1920 h264+aac; extract 4-6 frames and look (no original text leaking, stickers/card inside frame); volumedetect max < -0.3 dB.
6. Caption (English, SEO): first ~125 chars = main keywords in a natural sentence, then 1-3 short sentences about what the video shows, then "Get Car Widgets: AutoDash on the App Store 👇", then a blank line and 4-5 hashtags: #carplay #ios27 #carwidgets #autodash + at most 1 topic tag. No credit, no permission wording, no @car.widget, do not name competitor apps.
7. Publish: copy reel.mp4 to `reels/<tiktok_id>.mp4`, commit and push to main of THIS repo only, verify `https://raw.githubusercontent.com/gundemsaniye-dot/autodash-reels/main/reels/<id>.mp4` returns 200, then Buffer create_post: channelId above, schedulingType automatic, mode shareNow, metadata.instagram {type: reel, shouldShareToFeed: true}, assets [{video:{url:<raw url>}}]. Check get_post until status is sent and report the externalLink.
8. Add the TikTok ID to posted.json, commit, push.
Touch only this repository. Never touch other repos.

# Safe area map (1080x1920 frame)
Measured from real phone screenshots of the published reel on TikTok and Instagram (video is shown at ~0.844 scale, so ~50 px are cropped on each side), plus YouTube Shorts UI.

| Zone | Pixels | What covers it |
|---|---|---|
| Top | y 0..230 | status bar, Following/For You tabs, search, back/+ buttons |
| Bottom | y 1480..1920 | username, caption, comment bar, nav bar, Shorts title |
| Right column | x 890..1080, y 900..1480 | like / comment / share / save buttons |
| Side crop | x 0..50 and x 1030..1080 | cut off on tall phones |

**Safe box: x 90..890, y 230..1480.** All text, banner hook, stickers, the photo and the App Store card must be inside it (banner text may run to x=990 because the right column starts at y=900).

Current layout: banner y 240..410, photo y 420..1300, App Store card x 90..870, y 1310..1474. Reference picture: assets/safe_area_map.png.

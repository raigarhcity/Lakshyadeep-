# नींद क्यों ज़रूरी है? (Why we sleep)

A 31-second Hindi motion-graphics explainer, 1080x1920 (9:16) at 30 fps, for Reels and Shorts.

Final video: `neend-kyon-zaroori.mp4`

## Scenes
1. 0–4.6s: We spend about a third of our life asleep (about 26 years over 79 years).
2. 4.6–9.8s: The brain doesn't switch off; brain waves slow down in deep sleep.
3. 9.8–15.8s: The brain washes out the day's waste (the glymphatic system).
4. 15.8–21.6s: Memories get stored.
5. 21.6–26.6s: Staying awake 24 hours impairs you about as much as being drunk; focus and immunity drop.
6. 26.6–31s: Sleep 7–9 hours a night.

## Rebuild
- `index.html` draws every frame from a pure `render(t)` on a canvas. Open it in a browser to preview it live.
- `audio.py` synthesizes the soundtrack (needs numpy): `python3 audio.py out/score.wav`
- `render.mjs` captures each frame with Playwright and encodes it with ffmpeg: `node render.mjs out/silent.mp4`
- Mux the two:
  `ffmpeg -i out/silent.mp4 -i out/score.wav -c:v copy -c:a aac -b:a 192k -af loudnorm=I=-16:TP=-1.5 -shortest neend-kyon-zaroori.mp4`

Fonts: Baloo 2 and Mukta (SIL Open Font License, see `assets/`).

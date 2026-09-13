# Petals

TouchDesigner audio reactive particle mask artwork. The final saved project is `petals_fifteen_masks_v30.toe`; the reusable component is `petals_fifteen_masks_v30.tox`.

The project contains fifteen front surface mask fields, a 72 BPM four-four choreography, combined X/Y/Z movement, restrained snare turns, the supplied title opening, and falling petals with crosswind. The soundtrack is intentionally not included. TouchDesigner will use the audio path saved in the project (`C:/Users/matts/Music/petals.wav`); update the `track` Audio File In CHOP if the file is elsewhere.

Open the `.toe` in TouchDesigner. The final output is `/project1/nine_mask_cloud/OUT`. Use the Ensemble Test controls to play from the beginning or render. Rendering writes a silent `.mov`; `export_fifteen_masks_v30.ps1` shows the ffmpeg command for adding the external soundtrack.

## Source layout

- `thirteen_mask_runtime_v30.py` — embedded runtime source for the final project.
- `petals_finish_v25.glsl` — title, falling-petal and wind compositing shader.
- `bake_4x4_choreography_v28.py`, `bake_snare_turns_v28.py` — audio-envelope choreography baking.
- `prepare_masks_v26.py`, `install_masks_v26.py` — mask preparation and installation helpers.
- `assets/pop/morph_front` and `assets/pop/new_masks_v26` — front-visible point geometry.
- `assets/title/petals_intro.png` — supplied opening image.

No video or audio files are tracked.

# GIF / MP4 Timing Lab

A small reproducible dataset and local GIF metadata inspector for checking how unequal picture holds map onto fixed-rate MP4 video.

## What is included

- `source.gif`: our generated three-picture GIF; stored holds read back as 100, 400 and 900 milliseconds, canvas 320 by 200.
- `fps15.mp4`, `fps24.mp4`, `fps30.mp4`: actual saved browser exports from the same source on October 19, 2026; no visitor files.
- `timing-results.csv`: one row per consecutive source-picture run in each output.
- `frame-timing.json`: every decoded output frame label and presentation timestamp, plus file hashes and measurement method.
- `inspect_gif.py`: a standard-library-only local GIF block inspector. Prints dimensions, picture count and stored graphic-control delays. No network calls.
- `checklist.md`: a reusable source/output verification checklist.

The browser tool and the experiment narrative are maintained at [VideoPromptFlow](https://videopromptflow.com/guides/animated-gif-to-mp4-frame-delays/).

## Run locally

```sh
python inspect_gif.py source.gif
```

Python 3 is required. There are no Python package dependencies. The inspector parses GIF block structure; it does not decode LZW pixels, establish full integrity, repair files or convert video. Malformed/truncated block structure exits with an error. Graphic-control delays are stored values, not predictions of every player's actual playback.

## Reproduce the saved-video measurements

Convert the unchanged source at original size with output rates 15, 24 and 30 fps. For these exports the converter used `-ignore_loop 1`, `scale=320:200:flags=lanczos,fps=FPS,format=yuv420p`, libx264, ultrafast, CRF 23, no audio and faststart.

Decode a saved output with your local FFmpeg:

```sh
ffmpeg -i fps15.mp4 -vf showinfo -vsync 0 -f rawvideo -pix_fmt rgb24 frames.rgb
```

Retain the `showinfo` log. Split raw output into 320*200*3-byte frames. Compare each frame's top-left RGB pixel to the generated source backgrounds (25,106,71), (171,82,26), (34,60,145), using minimum squared RGB distance. Group consecutive identical labels. This classifier is only for this deliberately solid-color sample, not arbitrary animations.

Hold seconds = consecutive frame count / selected output fps. Total seconds = decoded frame count / fps. The JSON retains the transition timestamps as a cross-check.

| fps | Output picture groups | Total frames | Total seconds |
|---|---|---|---|
| 15 | 2 / 6 / 13 | 21 | 1.4 |
| 24 | 2 / 10 / 22 | 34 | 34/24 |
| 30 | 3 / 12 / 27 | 42 | 1.4 |

At 15 fps, total duration matched the source while individual holds changed. At 30 fps the three holds matched this sample. This is not a universal best-frame-rate claim, benchmark of other tools, or browser compatibility guarantee. The download-event notification timed out during automation, but the saved files existed in Downloads and these exact copies were decoded afterward.

## License and scope

The original code, documentation, generated sample and dataset in this repository are MIT licensed. No FFmpeg binaries, WebAssembly engine, third-party source, website credentials, analytics exports or visitor media are distributed here. FFmpeg is a separately obtained external tool under its own license. This repository is a timing lab, not the complete converter website.

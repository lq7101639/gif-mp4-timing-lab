# GIF to MP4 verification checklist

## Before conversion
- Keep the unchanged source and record its SHA-256.
- Distinguish the filename, valid GIF header and actual image decode.
- Record canvas dimensions and stored frame delays; do not call a header check a full integrity test.

## After conversion
- Save the actual MP4 and record its hash; a Done badge alone is insufficient.
- Decode the saved file and inspect each picture transition and the final hold.
- Record selected fps, decoded frame count, timestamps, and the method used to identify pictures.
- Check total duration separately from individual holds.
- Distinguish encoded repetition from a player's loop setting.

## Report honestly
- Name the source sample, tool version/date and browser used.
- Mark facts, inferences and untested cases separately.
- Do not infer a universal best fps or file-size limit from one sample.
- A complete replacement file is not a repaired damaged file.
- Record failed download checks separately from successful file decoding.

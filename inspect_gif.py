"""Read GIF block metadata locally. Does not decode pixels or repair data."""
import argparse
import hashlib
import json
from pathlib import Path

def inspect(data):
    pos = 0
    def take(n):
        nonlocal pos
        end = pos + n
        if end > len(data):
            raise ValueError(f'Truncated GIF block at byte {pos}')
        result = data[pos:end]
        pos = end
        return result
    def blocks():
        while True:
            size = take(1)[0]
            if size == 0:
                return
            take(size)
    header = take(6)
    if header not in (b'GIF87a', b'GIF89a'):
        raise ValueError('Not a GIF signature')
    screen = take(7)
    width = int.from_bytes(screen[:2], 'little')
    height = int.from_bytes(screen[2:4], 'little')
    if not width or not height:
        raise ValueError('Invalid zero canvas dimension')
    if screen[4] & 128:
        take(3 * 2 ** ((screen[4] & 7) + 1))
    frames, delay = [], None
    while True:
        marker = take(1)[0]
        if marker == 0x3B:
            break
        if marker == 0x21:
            kind = take(1)[0]
            if kind == 0xF9:
                size = take(1)[0]
                if size != 4:
                    raise ValueError('Invalid graphic-control block size')
                control = take(4)
                delay = int.from_bytes(control[1:3], 'little') * 10
                if take(1) != b'\x00':
                    raise ValueError('Missing graphic-control terminator')
            else:
                blocks()
                if kind == 0x01:
                    delay = None  # a plain-text rendering block consumes its control
        elif marker == 0x2C:
            image = take(9)
            if image[8] & 128:
                take(3 * 2 ** ((image[8] & 7) + 1))
            take(1)  # LZW minimum code size; pixel validity is not checked
            blocks()
            frames.append({'picture': len(frames) + 1, 'stored_delay_ms': delay})
            delay = None
        else:
            raise ValueError(f'Unexpected GIF block marker {marker:#x} at {pos-1}')
    return {'canvas_width': width, 'canvas_height': height, 'pictures': frames,
            'trailing_bytes': len(data)-pos, 'sha256': hashlib.sha256(data).hexdigest(),
            'limitation': 'Block metadata only; no LZW pixel decode, repair or playback guarantee.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.file.read_bytes()), indent=2))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')

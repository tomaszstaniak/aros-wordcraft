#!/usr/bin/env python3
"""Compares two RGBA PNGs of the same size, as written by `WordCraft --screenshot`.

usage: imgdiff.py A.png B.png [DIFF.png]

Prints the number of differing pixels, the largest channel difference and
the bounding box of the differences; with DIFF.png, writes the differing
pixels in red on a dimmed copy of A. Exit status 0 when identical, 1 when not.
"""
import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from icons import decode_rgba  # noqa: E402


def size(path):
    data = Path(path).read_bytes()
    return struct.unpack(">II", data[16:24])


def encode(width, rows):
    raw = b"".join(b"\0" + bytes(r) for r in rows)
    def chunk(name, data):
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, len(rows), 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    a, b = sys.argv[1], sys.argv[2]
    if size(a) != size(b):
        print(f"sizes differ: {size(a)} vs {size(b)}")
        return 1
    ra, rb = decode_rgba(Path(a))[2], decode_rgba(Path(b))[2]
    w = size(a)[0]
    count, worst, box = 0, 0, None
    out = []
    for y, (pa, pb) in enumerate(zip(ra, rb)):
        row = bytearray()
        for x in range(w):
            ca, cb = pa[4 * x:4 * x + 4], pb[4 * x:4 * x + 4]
            d = max(abs(i - j) for i, j in zip(ca, cb))
            if d:
                count += 1
                worst = max(worst, d)
                box = (min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)) if box else (x, y, x, y)
                row += bytes((255, 0, 0, 255))
            else:
                row += bytes((ca[0] // 3 + 170, ca[1] // 3 + 170, ca[2] // 3 + 170, 255))
        out.append(row)
    print(f"{count} pixels differ, largest channel difference {worst}, box {box}")
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_bytes(encode(w, out))
    return 0 if count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

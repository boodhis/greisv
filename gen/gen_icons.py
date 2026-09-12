#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерирует icon-192.png и icon-512.png в корне сайта без внешних зависимостей.
Цвет — акцент сайта (#4fc3f7) с тёмным кантом. Запуск: python3 gen/gen_icons.py
"""
import os
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

def make_png(path, size, fg=(0x4f, 0xc3, 0xf7, 255), bg=(0x0d, 0x11, 0x17, 255)):
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            edge = 4
            r = bg if (x < edge or y < edge or x >= size - edge or y >= size - edge) else fg
            row += bytes(r[:3])
        rows.append(bytes(row))
    raw = b"".join(rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print("->", os.path.relpath(path, ROOT))

def main():
    for s in (192, 512):
        make_png(os.path.join(ROOT, f"icon-{s}.png"), s)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从预习网站/wordbank.js 提取全部单词，用微软 Jenny 女声逐词生成 MP3。
输出到 英语音频/单词音频/w001.mp3 ... 与网页编号顺序一致。
"""

import asyncio
import pathlib
import re

import edge_tts


ROOT = pathlib.Path(__file__).resolve().parent.parent
WORD_BANK_JS = ROOT / "预习网站" / "wordbank.js"
OUT_DIR = ROOT / "英语音频" / "单词音频"
VOICE = "en-US-JennyNeural"
RATE = "-15%"


def extract_words() -> list[str]:
    text = WORD_BANK_JS.read_text(encoding="utf-8")
    # 按文件出现顺序提取 {w:"..."}，与网页编号顺序一致
    return re.findall(r'\bw:"([^"]+)"', text)


async def main() -> None:
    words = extract_words()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"共 {len(words)} 个词/短语")
    for i, word in enumerate(words, 1):
        path = OUT_DIR / f"w{i:03d}.mp3"
        if path.exists() and path.stat().st_size > 1000:
            continue
        communicate = edge_tts.Communicate(word, VOICE, rate=RATE)
        await communicate.save(str(path))
        print(f"OK w{i:03d}: {word}")


if __name__ == "__main__":
    asyncio.run(main())

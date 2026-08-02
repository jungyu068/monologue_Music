#!/usr/bin/env python3
"""🎵 음악 웹사이트 빌더 — build_site.py
데타1의 앨범 커버 + 곡 목록 → 아름다운 음악 웹사이트 생성!
"""
import os, json, glob, unicodedata, shutil

DATA1 = "/Volumes/데타1"
OUT = os.path.expanduser("~/MusicWebsite")
os.makedirs(f"{OUT}/covers", exist_ok=True)

def nfc(p):
    return unicodedata.normalize("NFC", p)

# EP 영상 URL 매핑 (우리 채널 @jungyu068 업로드분 — 실장님 확정 2026-08!)
EP_MAP = {
    "Summer Stories": "iruZR25D2lk",
    "Starlight July": "E0Ivtq2Xt48",
    "Neon Heartbreak": "pcQmtGduAeM",
    "Beyond the Map": "AD8DtnNM_CM",
    "Wanderlight": "rr9ZHZMalz4",
    "소실점과 여백": "xuSj1sGEZMo",
    "여백의 온도": "9Obf99lKbzE",
    "따스한 햇살 아래": "nilaDJSedOk",
    "A Night Touched by Moonlight": "H8DSf38GUL4",
    "The Midnight_Silence": "OcOFcZjs2v0",
    "Walking Through Time": "Oqdrr9FHOrs",
}

# 앨범 수집 (커버 있는 폴더!)
albums = []
seen = set()
for wav in glob.glob(os.path.join(DATA1, "**", "*.wav"), recursive=True):
    base = os.path.basename(wav)
    if base.startswith("._") or "mastering_tmp" in base or "_master" in base or "_edit" in base:
        continue
    d = os.path.dirname(wav)
    if "/수정/" in nfc(wav) or "수정" == nfc(os.path.basename(d)):
        continue
    key = nfc(d)
    if key in seen:
        continue
    seen.add(key)
    # 커버 찾기
    cover = None
    for ext in (".jpg", ".jpeg", ".png"):
        for name in ("cover", "Cover", "COVER"):
            p = os.path.join(d, name + ext)
            if os.path.exists(p):
                cover = p
                break
        if cover:
            break
    songs = []
    for f in sorted(os.listdir(d)):
        if f.startswith("._") or not f.endswith(".wav") or "mastering_tmp" in f:
            continue
        songs.append({
            "title": nfc(os.path.splitext(f)[0]),
            "file": "/데타1" + nfc(os.path.join(d, f)).replace(DATA1, ""),
        })
    # 언어 판단 (한글 곡명 = Korean!)
    all_titles = " ".join(s["title"] for s in songs)
    has_ko = any('\uac00' <= ch <= '\ud7a3' for ch in all_titles)
    albums.append({
        "name": nfc(os.path.basename(d)),
        "cover": cover,
        "songs": songs,
        "lang": "ko" if has_ko else "en",
        "ep_url": EP_MAP.get(nfc(os.path.basename(d))),
    })

# 커버 복사 (안전한 파일명)
for i, a in enumerate(albums):
    if a["cover"]:
        ext = os.path.splitext(a["cover"])[1].lower()
        dest = f"{OUT}/covers/album_{i:03d}{ext}"
        try:
            shutil.copy2(a["cover"], dest)
            a["cover_file"] = f"covers/album_{i:03d}{ext}"
        except Exception:
            a["cover_file"] = None
    else:
        a["cover_file"] = None

with open(f"{OUT}/albums.json", "w", encoding="utf-8") as f:
    json.dump(albums, f, ensure_ascii=False, indent=1)

print(f"✅ {len(albums)}개 앨범 수집!")
for a in albums[:10]:
    print(f"  🎵 {a['name']} ({len(a['songs'])}곡) {'🖼️' if a['cover_file'] else ''}")

"""komi_instagram 素材台帳を作る（サイトには何も追加しない）。
出力: internal/media_ledger.csv
"""
import csv, json, re, subprocess
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\Users\hm60m\Documents\komi_instagram")
OUT = Path(__file__).with_name("media_ledger.csv")
site_codes = {c["code"] for c in json.loads((SRC / "_site_cases.json").read_text(encoding="utf-8"))}

PARTS = [("ヘアスカルプ", "頭皮"), ("頭皮", "頭皮"), ("ヘアライン", "ヘアライン"), ("アイライン", "アイライン"),
         ("リップ", "リップ"), ("アマラ", "アマラピンク"), ("パラメディカル", "パラメディカル"),
         ("傷", "パラメディカル"), ("乳輪", "パラメディカル"), ("眉", "眉")]

def part_of(cap):
    m = re.search(r"■メニュー[:：](.+)", cap)
    s = m.group(1) if m else cap[:300]
    for k, v in PARTS:
        if k in s:
            return v
    return ""

def ratio_label(w, h):
    r = w / h
    for lab, v in [("16:9", 16/9), ("4:3", 4/3), ("1:1", 1), ("4:5", 4/5), ("3:4", 3/4), ("9:16", 9/16)]:
        if abs(r - v) < 0.03:
            return lab
    return f"{r:.2f}"

def probe(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True).stdout
    j = json.loads(o or "{}")
    s = (j.get("streams") or [{}])[0]
    return s.get("width", 0), s.get("height", 0), float(j.get("format", {}).get("duration", 0) or 0)

rows = []
for d in sorted(SRC.iterdir()):
    if not d.is_dir() or "_" not in d.name:
        continue
    date, code = d.name.split("_", 1)
    capf = d / "caption.txt"
    cap = capf.read_text(encoding="utf-8", errors="ignore") if capf.exists() else ""
    part = part_of(cap)
    is_case = "ビフォー" in cap or "Before" in cap or "症例" in cap or "■メニュー" in cap
    for f in sorted(d.iterdir()):
        ext = f.suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png", ".mp4"):
            continue
        if ext == ".mp4":
            w, h, dur = probe(f); kind = "動画"
        else:
            with Image.open(f) as im:
                w, h = im.size
            dur = 0; kind = "静止画"
        if kind == "動画":
            use = "ヒーロー候補" if 5 <= dur <= 60 else "要確認"
        else:
            use = "症例" if is_case else "雰囲気/人物"
        rows.append({
            "path": str(f), "日付": date, "種類": kind, "用途候補": use, "施術部位": part,
            "人物あり": "要目視", "文字入り": "要目視", "縦横比": ratio_label(w, h),
            "解像度": f"{w}x{h}", "動画秒数": f"{dur:.1f}" if dur else "",
            "サイト掲載済": "済" if code in site_codes else "",
            "Instagram投稿URL": f"https://www.instagram.com/p/{code}/",
            "Web掲載確認": "済(既存症例ページ)" if code in site_codes else "要確認",
        })

with OUT.open("w", encoding="utf-8-sig", newline="") as fp:
    w = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows ->", OUT)

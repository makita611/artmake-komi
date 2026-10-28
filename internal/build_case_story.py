# -*- coding: utf-8 -*-
"""ヒーロー直下の「3症例ストーリー」を各ページに差し込む（再実行可）。

症例データは cases-*.html の CASE_DETAILS（gen系スクリプト管理）から読むだけで、そちらは編集しない。
差し込み先は <!-- CASE_STORY_START --> 〜 <!-- CASE_STORY_END -->。無ければヒーロー(.kv)の直後に作る。
選定方針（2026-10-03 masa）: 眉が主役。東京/トップ=男性眉+男性スカルプ、群馬=眉、リメイク系は出さない。
使い方: py internal/build_case_story.py   （sites/artmake で実行）
"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# code: (症例ページ, カバー画像番号, 読み物リンク)
CASES = {
    "DZKJKZ6Eqc3": ("cases-eyebrow", 3, ("column/am-mens", "メンズ眉のコラムを読む")),
    "DafKmt7kupz": ("cases-eyebrow", 4, ("column/am-mens", "メンズ眉のコラムを読む")),
    "DacrkSNEr5_": ("cases-scalp", 1, ("column/am-hairscalp-toha", "ヘアスカルプのコラムを読む")),
    "Dcf5N_YkkaV": ("cases-eyebrow", 3, ("column/am-eyebrow-type", "毛並み/パウダーの違いを読む")),
    "Dazv5vJErPt": ("cases-eyebrow", 3, ("column/am-eyebrow-type", "毛並み/パウダーの違いを読む")),
}
PAGES = {
    "index.html":    ["DZKJKZ6Eqc3", "DafKmt7kupz", "DacrkSNEr5_"],
    "tokyo.html":    ["DZKJKZ6Eqc3", "DafKmt7kupz", "DacrkSNEr5_"],
    "tsukuba.html":  ["Dcf5N_YkkaV", "DZKJKZ6Eqc3", "Dazv5vJErPt"],
    "ota.html":      ["Dazv5vJErPt", "Dcf5N_YkkaV", "DafKmt7kupz"],
    "takasaki.html": ["Dazv5vJErPt", "Dcf5N_YkkaV", "DafKmt7kupz"],
}
FIELDS = ["費用", "施術回数", "リスク・副作用", "ダウンタイム"]


def load_details():
    out = {}
    for page in {v[0] for v in CASES.values()}:
        s = (ROOT / f"{page}.html").read_text(encoding="utf-8")
        for art in re.findall(r'<article class="case-detail">(.*?)</article>', s, re.S):
            m = re.search(r'instagram\.com/p/([^/]+)/', art)
            if not m or m.group(1) not in CASES:
                continue
            d = {"title": re.search(r"<h3>(.*?)</h3>", art).group(1),
                 "meta": re.search(r'<p class="cd-meta">(.*?)</p>', art).group(1),
                 "imgs": re.findall(r'<img[^>]+src="([^"]+)"', art)}
            for dt, dd in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", art):
                d[dt] = dd
            out[m.group(1)] = d
    return out


def card(code, d):
    page, n, (col_href, col_label) = CASES[code]
    img = d["imgs"][n - 1] if len(d["imgs"]) >= n else d["imgs"][0]
    part, _, sub = d["title"].partition("｜")
    rows = "".join(f"<dt>{f}</dt><dd>{d[f]}</dd>" for f in FIELDS if f in d)
    alt = html.escape(f"{part} 症例写真（{d['meta'].split('・')[-1]}）")
    return f'''      <article class="cs-card">
        <div class="cs-img"><img loading="lazy" src="{img}" alt="{alt}" width="720" height="900"></div>
        <div class="cs-body">
          <p class="cs-tag">{part}</p>
          <h3 class="cs-title">{sub or part}</h3>
          <p class="cs-meta">{d["meta"]}</p>
          <dl class="cs-dl">{rows}</dl>
          <div class="cs-links">
            <a href="{page}">症例の詳細を見る →</a>
            <a href="{col_href}">{col_label} →</a>
          </div>
        </div>
      </article>'''


def section(codes, details):
    cards = "\n".join(card(c, details[c]) for c in codes)
    return f'''<!-- CASE_STORY_START（internal/build_case_story.py が生成。手編集しない） -->
<section class="cs-section" id="case-story" aria-labelledby="case-story-title">
  <div class="container">
    <div class="cs-head">
      <p class="section-label">Cases</p>
      <h2 class="section-title" id="case-story-title">症例を見る</h2>
      <p class="cs-note">写真はご本人の同意を得て掲載しています。施術直後の写真は色が濃く見え、仕上がりには個人差があります。</p>
    </div>
    <p class="cs-hint" aria-hidden="true">← 横にスワイプして見る →</p>
    <div class="cs-track">
{cards}
    </div>
    <div class="cs-foot">
      <a href="cases-eyebrow" class="btn btn-secondary">眉の症例をもっと見る</a>
      <a href="column/?part=mayu" class="cs-foot-link">部位別のコラム一覧 →</a>
    </div>
  </div>
</section>
<!-- CASE_STORY_END -->'''


def main():
    details = load_details()
    missing = [c for c in CASES if c not in details]
    assert not missing, f"症例ページに見つからない: {missing}"
    for fn, codes in PAGES.items():
        p = ROOT / fn
        s = p.read_text(encoding="utf-8")
        block = section(codes, details)
        if "<!-- CASE_STORY_START" in s:
            s = re.sub(r"<!-- CASE_STORY_START.*?<!-- CASE_STORY_END -->", lambda m: block, s, flags=re.S)
        else:
            i = s.index("data-kv>")
            j = s.index("</section>", i) + len("</section>")
            s = s[:j] + "\n\n" + block + s[j:]
        p.write_text(s, encoding="utf-8")
        print("updated", fn, codes)


if __name__ == "__main__":
    main()

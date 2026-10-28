# -*- coding: utf-8 -*-
"""症例ページ → 部位別コラムへの導線を差し込む（再実行可）。
- cases-*.html: ギャラリーの直後（CASE_DETAILS_START の手前）に「この部位について読む」
- cases.html  : 「部位で見る」の下に「部位別のコラム」行
CASE_DETAILS_START〜END の中には触らない。マーカー: <!-- CASE_COLUMNS_START/END -->
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
idx = (ROOT / "column" / "index.html").read_text(encoding="utf-8")
TITLES = {m.group(1).removesuffix(".html"): m.group(2) for m in re.finditer(
    r'<a href="([^"]+)" class="col-card-link">\s*<span class="col-cat">[^<]*</span>\s*<h2 class="col-title">([^<]*)</h2>', idx)}
COUNTS = {}
for parts in re.findall(r'data-parts="([^"]*)"', idx):
    for p in parts.split():
        COUNTS[p] = COUNTS.get(p, 0) + 1

PAGES = {
    "eyebrow":     ("眉", "mayu", ["am-eyebrow-type", "am-eyebrow-design", "am-mens", "am-eyebrow-color"]),
    "lip":         ("リップ", "lip", ["am-lip-color", "am-lip-downtime", "am-lip-herpes"]),
    "eyeliner":    ("アイライン", "eyeline", ["am-eyeliner", "am-megane-contact", "am-senior-eyemake"]),
    "hairline":    ("ヘアライン", "hair", ["am-hairline", "am-enkei-hairline", "am-hairscalp-toha"]),
    "scalp":       ("ヘアスカルプ", "hair", ["am-hairscalp-toha", "am-hairline", "am-enkei-hairline"]),
    "amarapink":   ("アマラピンク", "amara", ["am-amarapink", "am-yakuzai-jokyo"]),
    "paramedical": ("パラメディカル", "para", ["am-paramedical-kizuato", "am-hokuro", "am-nyurin-nyutou"]),
}
STYLE = ('<style>.case-cols{margin:48px 0 0;padding:24px;background:var(--beige-light);border:0.5px solid var(--border)}'
         '.case-cols h2{font-family:var(--font-serif-ja);font-weight:400;font-size:18px;color:var(--brown);margin:4px 0 14px}'
         '.case-cols ul{list-style:none;margin:0 0 14px;padding:0;display:grid;gap:8px}'
         '.case-cols li a{display:block;padding:12px 14px;background:var(--white);border:0.5px solid var(--border);font-size:13px;line-height:1.7;color:var(--brown);text-decoration:none}'
         '.case-cols li a:hover{border-color:var(--gold)}'
         '.case-cols-all{font-size:13px;color:var(--gold)}'
         '.part-nav-cols a{font-size:12px}</style>')


def put(s, block, anchor):
    block = f"<!-- CASE_COLUMNS_START（internal/add_case_column_links.py） -->\n{block}\n<!-- CASE_COLUMNS_END -->\n"
    if "<!-- CASE_COLUMNS_START" in s:
        return re.sub(r"<!-- CASE_COLUMNS_START.*?<!-- CASE_COLUMNS_END -->\n", lambda m: block, s, flags=re.S)
    assert s.count(anchor) == 1, anchor
    return s.replace(anchor, block + anchor)


for cat, (ja, part, slugs) in PAGES.items():
    fn = ROOT / f"cases-{cat}.html"
    s = fn.read_text(encoding="utf-8")
    lis = "\n".join(f'        <li><a href="column/{x}">{TITLES[x]}</a></li>' for x in slugs if x in TITLES)
    block = f'''{STYLE}
    <aside class="case-cols" aria-labelledby="case-cols-title">
      <span class="section-label">Column</span>
      <h2 id="case-cols-title">{ja}について読む</h2>
      <ul>
{lis}
      </ul>
      <a class="case-cols-all" href="column/?part={part}">{ja}のコラムをすべて見る（{COUNTS.get(part, 0)}件）→</a>
    </aside>'''
    anchor = "<!-- CASE_DETAILS_START -->" if "<!-- CASE_DETAILS_START -->" in s else         '    <p style="text-align:center;margin-top:40px;font-size:12px;color:var(--text-muted);font-weight:300">'
    fn.write_text(put(s, block, anchor), encoding="utf-8")
    print("updated", fn.name)

fn = ROOT / "cases.html"
s = fn.read_text(encoding="utf-8")
row = "\n".join(f'      <a href="column/?part={p}">{j}</a>' for j, p in
                [("眉", "mayu"), ("男性の眉", "mens"), ("リップ", "lip"), ("アイライン", "eyeline"),
                 ("ヘアライン・スカルプ", "hair"), ("アマラピンク", "amara"), ("パラメディカル", "para")])
block = f'''{STYLE}
    <nav class="part-nav part-nav-cols" aria-label="部位別のコラム">
      <span class="part-nav-label">部位のコラムを読む：</span>
{row}
    </nav>'''
fn.write_text(put(s, block, "    <!-- ギャラリー -->"), encoding="utf-8")
print("updated cases.html")

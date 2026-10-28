# -*- coding: utf-8 -*-
"""column/index.html の記事カードに data-parts（部位タグ）を付ける（再実行可）。
自動公開(publish-column.yml)で増えたタグ無しカードは、js/column-filter.js がタイトルから推定するので
ここに追記しなくても「部位で見る」に出る。精度を上げたい時だけ MAP に足して再実行する。
"""
import re
from pathlib import Path

IDX = Path(__file__).resolve().parent.parent / "column" / "index.html"
AREA = "area"
MAP = {
    "am-mito": AREA, "am-kensei": AREA, "am-tsuchiura": AREA, "artmake-gunma": AREA,
    "am-saitama-higashi": AREA, "am-tochigi": AREA, "am-tx-chiba": AREA, "am-takasaki": AREA,
    "am-ota": AREA, "am-tokyo-hanzomon": AREA, "am-tsukuba": AREA, "artmake-ibaraki": AREA,
    "am-yakuzai-jokyo": "fix lip", "am-hairscalp-toha": "hair", "am-mayuge-toha": "mayu",
    "am-megane-contact": "eyeline", "am-sports-suiei": "mayu eyeline", "am-kisetsu-kikou": "basic",
    "am-tojitsu-nagare": "basic", "am-shorai-sonae": "basic", "am-paramedical-kizuato": "para",
    "am-enkei-hairline": "hair", "am-hokuro": "para", "am-senior-eyemake": "mayu eyeline",
    "am-hairline": "hair", "am-koganzai-mayuge": "mayu para", "am-nyurin-nyutou": "para",
    "am-jitan-biyo-bijinesu": "basic", "am-koukai-shinai-erabikata": "basic",
    "am-artmake-toha": "basic mayu lip eyeline", "am-eyebrow-color": "mayu", "am-iryouhikoujo": "basic",
    "am-shusei": "mayu fix", "am-lip-color": "lip", "am-jokyo": "fix", "am-henshoku": "mayu fix",
    "am-eyebrow-design": "mayu", "am-clinic-vs-salon": "basic", "am-kaisu": "basic mayu lip",
    "am-amarapink": "amara", "am-mens": "mayu mens", "am-eyeliner": "eyeline", "am-price": "basic mayu lip",
    "am-mri-tattoo": "basic", "am-lip-downtime": "lip", "am-jizoku": "basic", "am-tekisei": "basic",
    "am-downtime": "basic", "am-eyebrow-type": "mayu", "am-kinki": "basic", "am-pigment": "basic",
    "am-supppin": "basic", "am-lip-herpes": "lip", "am-clinic-erabi": "basic", "am-itami": "basic",
}

s = IDX.read_text(encoding="utf-8")
miss = []

def repl(m):
    slug = m.group(2).removesuffix(".html")
    parts = MAP.get(slug)
    if not parts:
        miss.append(slug)
        return m.group(0)
    return f'<article class="col-card" data-parts="{parts}">{m.group(1)}<a href="{m.group(2)}"'

s = re.sub(r'<article class="col-card"(?: data-parts="[^"]*")?>(\s*)<a href="([^"]+)"', repl, s)
IDX.write_text(s, encoding="utf-8")
print("tagged", len(MAP), "/ untagged(JS推定):", miss)

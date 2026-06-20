# -*- coding: utf-8 -*-
"""部位別 症例ページ ジェネレータ。cases-eyebrow.html と同型のページを生成する。"""
import re

CFG = {
    "lip": dict(
        ja="リップ", term="リップアートメイク", en="Lip", tag="リップ", caption="リップ / Lip",
        hero="唇の血色・輪郭の仕上がり実例",
        lead="リップアートメイクは唇全体に色素を入れ、血色感・くすみ・輪郭のお悩みを補整する医療アートメイクです。すっぴんでも血色のある唇に見え、口紅の塗り直し負担を減らせます。単純ヘルペスの既往がある方は事前申告と予防薬の服用が必要です。ご希望の発色・形に合わせた仕上がり実例を掲載しています。",
        content="唇への色素注入による発色・輪郭の補整",
        kaisu="通常2回（初回＋1〜3ヶ月後の補色）。発色・定着具合により追加施術が必要な場合があります。",
        cost="¥55,000〜¥88,000程度", risk="腫れ・乾燥、単純ヘルペスの再発（既往歴のある方は事前申告・抗ヘルペス薬の服用が必要）、色ムラ・経年での退色",
        menu=("artmake.html", "リップのメニュー・料金"),
        cols=[("column/am-lip-herpes.html","リップとヘルペス"),("column/am-lip-downtime.html","リップのダウンタイム"),("column/am-itami.html","痛みについて")],
        imgs=["images/lartmake1.jpg","images/lartmake2.jpg","images/lartmake3.jpg","images/lartmake4.jpg"],
    ),
    "eyeliner": dict(
        ja="アイライン", term="アイラインアートメイク", en="Eyeliner", tag="アイライン", caption="アイライン / Eyeliner",
        hero="目元を引き締めるアイラインの仕上がり実例",
        lead="アイラインアートメイクは上下まぶたのキワに色素を定着させ、目元の印象を引き締める医療アートメイクです。にじみにくく、すっぴん・スポーツ・温泉でも目元の印象を保てます。ナチュラルからしっかりめまで濃さを調整でき、その仕上がり実例を掲載しています。",
        content="上下まぶたのキワへの色素定着",
        kaisu="通常2回（初回＋1〜3ヶ月後の補色）。定着具合により追加施術が必要な場合があります。",
        cost="¥23,000〜¥55,000程度", risk="腫れ・むくみ・内出血、色のにじみ、まれに感染やアレルギー反応",
        menu=("artmake.html", "アイラインのメニュー・料金"),
        cols=[("column/am-eyeliner.html","アイラインの基礎知識"),("column/am-itami.html","痛みについて"),("column/am-downtime.html","ダウンタイムの経過")],
        imgs=["images/eartmake1.jpg","images/eartmake2.jpg","images/eartmake3.jpg","images/eartmake4.jpg"],
    ),
    "hairline": dict(
        ja="ヘアライン", term="ヘアラインアートメイク", en="Hairline", tag="ヘアライン", caption="ヘアライン / Hairline",
        hero="生え際の輪郭を補整するヘアラインの仕上がり実例",
        lead="ヘアライン（生え際）アートメイクは、額の生え際に点状に色素を入れて輪郭を補整し、顔まわりの印象を整える医療アートメイクです。生え際の薄さ・後退・面長のお悩みに用いられます。その仕上がり実例を掲載しています。",
        content="生え際への点状の色素定着による輪郭の補整",
        kaisu="通常2回（初回＋1〜3ヶ月後の補色）。範囲・定着具合により追加施術が必要な場合があります。",
        cost="¥66,000〜¥82,500程度", risk="腫れ・赤み、色の定着差、まれに感染やアレルギー反応",
        menu=("artmake.html", "ヘアラインのメニュー・料金"),
        cols=[("column/am-itami.html","痛みについて"),("column/am-downtime.html","ダウンタイムの経過")],
        imgs=["images/artmake5.jpg"],
    ),
    "scalp": dict(
        ja="ヘアスカルプ", term="ヘアスカルプメディカルアートメイク", en="Scalp", tag="ヘアスカルプ", caption="ヘアスカルプ / Scalp",
        hero="地肌の透けを目立ちにくくする仕上がり実例",
        lead="ヘアスカルプメディカルアートメイクは、頭皮に微細な点を描き、地肌の透けや密度のお悩みを目立ちにくくする医療アートメイクです。範囲や状態により複数回に分けて施術します。その仕上がり実例を掲載しています。",
        content="ヘアスカルプメディカルアートメイク（頭皮への微細な点描による地肌の補整）",
        kaisu="範囲・状態により異なります（複数回必要な場合があります。カウンセリングでご案内します）。",
        cost="¥44,000〜¥176,000程度（範囲・回数により大きく変動）", risk="腫れ・赤み・かゆみ、色素の定着差・経年での退色、まれに感染やアレルギー反応",
        menu=("artmake.html", "ヘアスカルプのメニュー・料金"),
        cols=[("column/am-itami.html","痛みについて"),("column/am-downtime.html","ダウンタイムの経過")],
        imgs=["images/sartmake1.jpg","images/sartmake2.jpg","images/sartmake3.jpg","images/sartmake4.jpg","images/sartmake5.jpg"],
    ),
    "amarapink": dict(
        ja="アマラピンク", term="アマラピンク", en="Amarapink", tag="アマラピンク", caption="アマラピンク / Amarapink",
        hero="色素沈着・黒ずみのトーン補整の仕上がり実例",
        lead="アマラピンクは、色素沈着・黒ずみが気になる部位に医療アートメイクの技術でトーンを補整する施術です。デリケートな部位のくすみのお悩みに用いられます。施術部位・状態により回数や費用が変わります。その仕上がり実例を掲載しています。",
        content="アマラピンク（色素沈着・黒ずみ部位への医療アートメイク技術によるトーン補整）",
        kaisu="範囲・状態により異なります（複数回必要な場合があります。カウンセリングでご案内します）。",
        cost="¥65,000〜¥185,000程度（部位により異なる）", risk="腫れ・赤み・色ムラ、色の定着差・経年での退色、まれに感染やアレルギー反応",
        menu=("amarapink.html", "アマラピンクのメニュー・詳細"),
        cols=[("column/am-pigment.html","染料・色素の安全性"),("column/am-itami.html","痛みについて")],
        imgs=["images/amara7.jpg","images/amara8.jpg","images/amara9.jpg","images/amara10.jpg","images/amara11.jpg","images/amara12.jpg","images/amara0.jpg"],
    ),
    "paramedical": dict(
        ja="パラメディカル", term="パラメディカルアートメイク", en="Paramedical", tag="パラメディカル", caption="パラメディカル / Paramedical",
        hero="傷跡・白斑などのカモフラージュの仕上がり実例",
        lead="パラメディカルアートメイクは、白斑・傷跡・妊娠線などを周囲の肌色に近づけてカモフラージュする医療アートメイクです。見た目のお悩みの軽減を目的とし、状態により複数回の施術を行う場合があります。その仕上がり実例を掲載しています。",
        content="パラメディカルアートメイク（白斑・傷跡・妊娠線等のカモフラージュ）",
        kaisu="状態・範囲により異なります（複数回必要な場合があります。カウンセリングでご案内します）。",
        cost="¥28,000〜¥44,000程度", risk="腫れ・赤み、周囲の肌色との色調差・経年での退色、まれに感染やアレルギー反応",
        menu=("paramedical.html", "パラメディカルの詳細"),
        cols=[("column/am-itami.html","痛みについて"),("column/am-downtime.html","ダウンタイムの経過")],
        imgs=["images/para1.jpg","images/para2.jpg","images/para3.jpg","images/para4.jpg"],
    ),
}

# テンプレートは cases-eyebrow.html を読み、眉固有部分をプレースホルダに置換して再利用する
tpl = open("cases-eyebrow.html", encoding="utf-8").read()

def build(cat, c):
    items = []
    for src in c["imgs"]:
        items.append(
            '      <div class="gallery-item" data-category="%s" onclick="openLightbox(this)">\n'
            '        <img loading="lazy" src="%s" alt="%s 症例 ビフォーアフター｜東京・半蔵門 komi" data-caption="%s">\n'
            '        <div class="gallery-item-overlay"><span class="gallery-item-tag">%s</span></div>\n'
            '      </div>' % (cat, src, c["term"], c["caption"], c["tag"])
        )
    gallery = "\n".join(items)
    related = "\n".join(
        ['        <a href="%s">%s</a>' % (c["menu"][0], c["menu"][1]),
         '        <a href="cases.html">症例写真トップ（全部位）</a>'] +
        ['        <a href="%s">%s</a>' % (h, l) for h, l in c["cols"]]
    )
    out = """<!DOCTYPE html>
<html lang="ja">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-NRZMPVR9');</script>
<!-- End Google Tag Manager -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(term)s症例｜ビフォーアフター仕上がり実例｜KOMI ARTMAKE</title>
<meta name="description" content="%(term)sの症例写真集。仕上がり実例と、施術内容・費用目安・施術回数・主なリスク副作用を併記。東京・半蔵門のkomiが医療機関で施術します。">
<link rel="canonical" href="https://artmake-komi.com/cases-%(cat)s">
<meta property="og:title" content="%(term)s症例｜ビフォーアフター仕上がり実例｜KOMI ARTMAKE">
<meta property="og:description" content="%(term)sの症例写真集。施術内容・費用目安・施術回数・主なリスク副作用を併記。東京・半蔵門のkomiが医療機関で施術。">
<meta property="og:url" content="https://artmake-komi.com/cases-%(cat)s">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Noto+Serif+JP:wght@300;400&family=Noto+Sans+JP:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
%(style)s
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://artmake-komi.com/" },
    { "@type": "ListItem", "position": 2, "name": "症例写真", "item": "https://artmake-komi.com/cases" },
    { "@type": "ListItem", "position": 3, "name": "%(term)s症例", "item": "https://artmake-komi.com/cases-%(cat)s" }
  ]
}
</script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NRZMPVR9" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

%(header)s

<section class="page-hero" style="background-image:url('images/hero-cases.jpg')">
  <div class="page-hero-overlay"></div>
  <div class="page-hero-content">
    <p class="section-label">%(en)s Cases</p>
    <h1 class="page-hero-title">%(term)s症例</h1>
    <p class="page-hero-desc">%(hero)s</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <nav class="breadcrumb"><a href="/">ホーム</a> ＞ <a href="cases.html">症例写真</a> ＞ %(ja)s</nav>

    <p class="case-lead">%(lead)s</p>

    <!-- 医療広告ガイドライン 限定解除要件の併記（施術内容・費用・回数・リスク） -->
    <div class="req-box">
      <h2>%(term)sの施術概要（必ずお読みください）</h2>
      <dl>
        <dt>施術内容</dt>
        <dd>%(content)s。針のついた専用器具で皮膚に極細の傷をつけ、色素を定着させる医療行為です。麻酔クリームを使用します。</dd>
        <dt>施術回数</dt>
        <dd>%(kaisu)s</dd>
        <dt>費用目安</dt>
        <dd>%(cost)s（税込・クリニックにより異なります。詳細は<a href="clinics.html" style="color:var(--gold)">提携院ページ</a>）</dd>
        <dt>主なリスク・副作用</dt>
        <dd>%(risk)s。施術を受けられない方（禁忌）もあります。</dd>
      </dl>
      <p class="req-note">※掲載写真はご本人の同意をいただいた施術実例です。個人が特定されないよう配慮しています。施術結果には個人差があり、効果を保証するものではありません。施術の適否・リスクの詳細はカウンセリングでご説明します。</p>
    </div>

    <!--
      症例の追加方法（自動化対応）：
      1. 画像を images/incoming/ に入れる → Claudeが images/ へ移動・命名
      2. %(MARK)s_CASES_START マーカー直下に gallery-item を追加（最新を上に）
      data-category は "%(cat)s" 固定
    -->
    <div class="gallery-grid" id="galleryGrid">
      <!-- %(MARK)s_CASES_START -->
%(gallery)s
    </div>

    <p style="text-align:center;margin-top:40px;font-size:12px;color:var(--text-muted);font-weight:300">
      随時、%(ja)sの症例を追加しています。InstagramでもBefore/Afterをご覧いただけます。<br>
      <a href="https://www.instagram.com/artmake_komi/" target="_blank" rel="noopener" style="color:var(--gold)">→ Instagramはこちら</a>
    </p>

    <div style="margin-top:56px">
      <span class="section-label">Related</span>
      <h2 class="section-title" style="font-size:20px;margin:8px 0 20px">あわせて見る・読む</h2>
      <div class="related-links">
%(related)s
      </div>
    </div>
  </div>
</section>

<!-- Lightbox -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close" onclick="closeLightbox()">✕</button>
  <img loading="lazy" class="lightbox-img" id="lightboxImg" src="" alt="">
  <p class="lightbox-caption" id="lightboxCaption"></p>
  <dl class="lightbox-info" id="lightboxInfo"></dl>
</div>

%(reservation)s
<section class="cta-section">
  <div class="container">
    <div class="cta-inner">
      <span class="section-label">Contact</span>
      <h2 class="cta-title">%(ja)sのご相談はお気軽に</h2>
      <p class="cta-desc">症例やデザインについての質問もLINEよりどうぞ。</p>
      <div class="cta-btns">
        <a href="https://lin.ee/8AGmhyG" target="_blank" rel="noopener" class="btn btn-line">LINE公式で相談</a>
        <a href="https://www.instagram.com/artmake_komi/" target="_blank" rel="noopener" class="btn btn-insta">Instagramで相談</a>
      </div>
    </div>
  </div>
</section>

%(footer)s

<script src="js/main.js"></script>
<script>
const categoryInfo = {
  %(cat)s: { content: '%(content)s', cost: '%(cost)s', risk: '%(risk)s' }
};
function openLightbox(el) {
  const img = el.querySelector('img');
  const cat = el.dataset.category;
  const info = categoryInfo[cat];
  document.getElementById('lightboxImg').src = img.src;
  document.getElementById('lightboxImg').alt = img.alt;
  document.getElementById('lightboxCaption').textContent = img.dataset.caption || '';
  const infoEl = document.getElementById('lightboxInfo');
  if (info) {
    infoEl.innerHTML =
      '<dt>施術内容：</dt><dd>' + info.content + '</dd>' +
      '<dt>費用目安：</dt><dd>' + info.cost + '（税込・詳細は<a href="clinics.html" style="color:var(--gold)">提携院ページ</a>へ）</dd>' +
      '<dt>主なリスク・副作用：</dt><dd>' + info.risk + '</dd>';
  } else {
    infoEl.innerHTML = '';
  }
  document.getElementById('lightbox').classList.add('open');
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
}
document.addEventListener('keydown', e => { if(e.key === 'Escape') closeLightbox(); });
</script>
</body>
</html>
"""
    # 共通パーツ(style/header/reservation/footer)は eyebrow から抜き出して流用
    style = re.search(r'(<style>.*?</style>)', tpl, re.DOTALL).group(1)
    header_block = re.search(r'(<header class="site-header">.*?</header>\s*<div class="mobile-nav">.*?</div>)', tpl, re.DOTALL).group(1)
    reservation = re.search(r'(<section class="section" style="background:var\(--beige-light\)">.*?</section>)', tpl, re.DOTALL).group(1)
    footer = re.search(r'(<footer class="site-footer">.*?</footer>)', tpl, re.DOTALL).group(1)
    return out % dict(
        cat=cat, term=c["term"], en=c["en"], ja=c["ja"], hero=c["hero"], lead=c["lead"],
        content=c["content"], kaisu=c["kaisu"], cost=c["cost"], risk=c["risk"],
        MARK=cat.upper(), gallery=gallery, related=related,
        style=style, header=header_block, reservation=reservation, footer=footer,
    )

for cat, c in CFG.items():
    html = build(cat, c)
    fn = "cases-%s.html" % cat
    open(fn, "w", encoding="utf-8").write(html)
    print("wrote", fn, "(%d imgs)" % len(c["imgs"]))

# --- sitemap 更新 ---
sm = open("sitemap.xml", encoding="utf-8").read()
slugs = ["eyebrow"] + list(CFG.keys())
new_lines = "  <!-- 症例 部位別 -->\n" + "\n".join(
    '  <url><loc>https://artmake-komi.com/cases-%s</loc><lastmod>2026-06-21</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>' % s
    for s in slugs
) + "\n"
if "cases-eyebrow" not in sm:
    sm = sm.replace("</urlset>", new_lines + "</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("sitemap updated with", len(slugs), "case pages")
else:
    print("sitemap already has case pages, skipped")

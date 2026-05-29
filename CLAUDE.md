# KOMI ARTMAKE サイト — Claude作業ルール

## リポジトリ
- GitHub: `makita611/artmake-komi`
- 本番: https://artmake-komi.com
- デプロイ: Cloudflare Pages（push → 自動）

## 【最重要】画像・動画の見切れ防止ルール

**画像や動画を追加・変更するたびに必ず確認すること。指摘なしに自分で守ること。**

### 画像の種類と設定（必ず守る）

#### `<img>` タグの場合
| 用途 | object-fit | aspect-ratio | background |
|---|---|---|---|
| コンテンツ画像（content-img） | **contain** | なし（height:auto） | var(--beige) |
| メニュー画像（menu-img） | **contain** | 4/3（維持） | var(--beige) |
| ギャラリー画像 | **contain** | 1/1（維持） | var(--beige) |
| アーティスト写真 | **contain** | 3/4（維持） | var(--beige) |
| 動画（video要素） | **contain** | 固定しない | — |

#### `background-image` CSS の場合（divに背景画像を使うとき）
| 用途 | background-size | background-repeat | background-color |
|---|---|---|---|
| サービスカード（service-img） | **contain** | no-repeat | var(--beige) |
| その他コンテンツ背景 | **contain** | no-repeat | var(--beige) |
| ヒーロー背景（hero-slide, page-hero） | cover（意図的） | — | var(--brown) |

### 絶対に使わない設定
- `object-fit: cover` → コンテンツ画像には**禁止**
- `background-size: cover` → ヒーロー・装飾背景以外は**禁止**

### `cover` が許可される唯一の例外
- `.hero-slide`（トップページスライドショー背景）
- `.page-hero`（各ページのヒーロー背景）
- これ以外はすべて `contain` を使うこと

### 新しい画像エリアを作るときのテンプレート
```html
<!-- img タグの場合 -->
<img src="images/xxx.png" style="width:100%;height:auto;object-fit:contain;background:var(--beige);display:block;">

<!-- div background-image の場合 -->
<div style="aspect-ratio:4/3;background-image:url('images/xxx.png');background-size:contain;background-position:center;background-repeat:no-repeat;background-color:var(--beige);"></div>
```

---

## ファイル構成

```
artmake-komi.com/
├── index.html          トップ
├── artmake.html        アートメイク（画像: artmake1〜7.png）
├── amarapink.html      アマラピンク（画像: amara0〜6.png）
├── paramedical.html    パラメディカル
├── clinics.html        提携院
├── cases.html          症例写真
├── artists.html        アーティスト
├── contact.html        お問い合わせ
├── tokyo.html          東京エリアLP
├── column/
│   ├── index.html
│   ├── am-itami.html
│   ├── am-clinic-erabi.html
│   ├── am-lip-herpes.html
│   └── scheduled/      （月水金 10:00 JST 自動公開）
├── css/style.css       スタイル（rootのstyle.cssは旧版・使用しない）
├── js/main.js
└── images/
```

## CSS変数（主要）
```css
--gold: #c4a36e
--brown: #3d3028
--beige: #f0e8d8
--beige-light: #f7f3ec
--white: #fff
--text: #3d3028
--text-light: #6b5a4e
--text-muted: #9e8e84
--border: rgba(61,48,40,0.12)
```

## Git運用
- push前に `git pull --rebase origin main` が必要な場合がある（複数端末運用のため）
- コラム自動公開: `column/scheduled/` に置いてpushすると月水金10:00に自動公開

## コラム記事スコアリング
スコアリング結果: Obsidian `Projects/KOMI_ARTMAKE/2026-05-29_コラム記事スコアリング.md`
次の優先記事: 眉ワーキングvsパウダー / ダウンタイム×仕事 / エリアSEOつくば

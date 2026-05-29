# KOMI ARTMAKE サイト — Claude作業ルール

## リポジトリ
- GitHub: `makita611/artmake-komi`
- 本番: https://artmake-komi.com
- デプロイ: Cloudflare Pages（push → 自動）

## 画像・動画を変更・追加したときの必須確認

**画像や動画を追加・変更するたびに以下を必ず実施すること。**

### チェックリスト
- [ ] `object-fit` が `cover` になっていないか → **`contain` を使う**
- [ ] `aspect-ratio` が固定されている場合、画像の縦横比と一致しているか確認
- [ ] `<video>` に固定 `aspect-ratio` を設定しない（動画の自然サイズに従わせる）
- [ ] ギャラリー系画像（amara-gallery等）も `object-fit: contain` + `background: var(--beige)`

### 基本方針
| 用途 | aspect-ratio | object-fit | background |
|---|---|---|---|
| コンテンツ画像（content-img） | 4/3（維持） | contain | var(--beige) |
| メニュー画像（menu-img） | 4/3（維持） | contain | var(--beige) |
| ギャラリー画像 | 1/1（維持） | contain | var(--beige) |
| 動画（sejutsu-video） | 固定しない | contain | — |

`cover` は「意図的に中央トリミングしたい場合のみ」使用する。

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

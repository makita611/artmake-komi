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

---

## コラム記事の運用ルール（必ず守る）

### 記事追加時にやること（毎回必須）
1. `column/` に記事HTMLを作成する
2. `column/index.html` の `<!-- ARTICLES_START -->` の直下に新記事カードを**最新順（一番上）**に追加する
3. 新記事の「関連記事（Related Articles）」に既存コラムへのリンクを追加する
4. 既存コラムの「関連記事」に新記事へのリンクを追加する（相互リンク）

### 記事間の連携（内部リンク）ルール
コラム記事は以下のパターンで相互にリンクする：
- **クリニック選び** (`am-clinic-erabi.html`) → 染料安全性・リスク記事へリンク
- **染料安全性** (`am-pigment.html`) → クリニック選び・リスク記事へリンク
- **リスク・禁忌** (`am-kinki.html`) → クリニック選び・染料安全性へリンク
- **痛み** (`am-itami.html`) → クリニック選び・すっぴん記事へリンク
- **すっぴん・満足度** (`am-supppin.html`) → クリニック選び・痛み記事へリンク
- **リップ・ヘルペス** (`am-lip-herpes.html`) → 痛み・クリニック選びへリンク

### artmake.htmlとの連携
新しい「染料情報」「リスク情報」コラムは、artmake.htmlのFAQセクション下に「あわせて読みたいコラム」バナーを設置してリンクする。

### ファイル構成（更新済み）
```
column/
├── index.html
├── am-supppin.html    （すっぴん・アンケートデータ）
├── am-pigment.html    （染料・ピグメント安全性）← 作成予定
├── am-kinki.html      （施術禁忌・リスク情報）← 作成予定
├── am-clinic-erabi.html（クリニック選び）
├── am-itami.html      （痛み）
├── am-lip-herpes.html （リップ・ヘルペス）
└── scheduled/
```

## エリアLP
4ページ全て完成・稼働中:
- `tokyo.html`    東京・半蔵門（一番町まつりかクリニック）
- `tsukuba.html`  茨城・つくば（B-leafメディカル）
- `ota.html`      群馬・太田（シンシアガーデンクリニック太田院）
- `takasaki.html` 群馬・高崎（シンシアガーデンクリニック高崎院）
LP構成: Hero→実績バー→こんな方へ→アクセス→メニュー→Why Here→komi写真+プロフィール→選ばれる理由→MY STORY→OUR CONCEPT→動画→症例写真→SNSモニター→口コミ→ご予約の流れ→FAQ→CTA

---

## Claude作業スタイル（トークン節約）
- 大きいHTMLは全文ではなく必要箇所だけ読む（offset/limit、Grep優先）
- 同じファイルを編集した後、確認のために読み直さない（Edit/Writeが失敗すればエラーになる）
- 冗長な前置き・選択肢の羅列をしない。結論と根拠だけ述べる
- 自明な低リスク操作は確認を求めず実行する（.claude/settings.local.json の許可設定に従う）
- 危険操作（rm -rf / git push --force / reset --hard / .env・鍵の読取）は設定でdeny済み＝絶対にしない

# SEO URLメモ — 「.html と クリーンURLの重複」は“もう対策済み”

最終更新: 2026-08-15

## 結論（先に読む）
artmake-komi.com の「`/foo.html` と `/foo` が重複してる」問題は、**インフラ側で既に正しく処理されている**。
GSC/監査で「重複URLペア」が出ても、それは**過去インデックスの名残**であり、サイトが壊れているわけではない。
**新規で"修正"を作り込む必要はない。** 下の3点が保たれていればOK。

## 現状（2026-08-15 実測で確認）
1. **Cloudflare Pages が `.html` → クリーンURL へ 308 Permanent Redirect 済み**
   - 例: `curl -sI https://artmake-komi.com/column/am-itami.html` → `308` / `Location: /column/am-itami`
2. **canonical タグが全ページで正しくクリーンURLを指している**（root・column とも）
3. **sitemap.xml は .html を1件も含まない**（全部クリーンURL）

→ Google はいずれクリーンURLに評価を寄せる。放置で正しく収束する。

## 唯一の実害だった点（2026-08-15 修正済み・commit f920c28）
- サイト内で**唯一** `.html` を指していた内部リンク `column/index.html` の `am-amarapink.html` を
  クリーンURL `am-amarapink` に統一した。これで .html版へGoogleを誘導する内部リンクがゼロになった。

## 【今後のルール】同じ間違いを繰り返さないために
1. **内部リンクは必ずクリーンURL（拡張子なし）で書く。** `href="am-xxx.html"` は禁止 → `href="am-xxx"`。
   - ⚠️ 注意: この repo の CLAUDE.md 旧記述では例として `am-xxx.html` と書かれている箇所があるが、
     **実運用はクリーンURLに移行済み**。CLAUDE.md の `.html` 表記は「ファイル名の説明」であって
     「リンクの書き方」ではない。リンクはクリーンURLで。
2. **監査/GSCで「.html と クリーンの重複ペア」が出ても、いきなり"直そう"としない。** まず実測:
   ```bash
   curl -sI https://artmake-komi.com/<path>.html | grep -iE "^HTTP|^location"
   ```
   308 で Location がクリーンURLなら**対策済み＝作業不要**。新しいリダイレクト設定を足す必要はない。
3. 新規内部.htmlリンクの混入チェック（記事追加時に走らせると安全）:
   ```bash
   grep -rhoE 'href="[^"]+\.html"' *.html column/*.html column/scheduled/*.html | grep -v 'href="http'
   ```
   → 何も出なければOK（外部リンクの.htmlは無視して良い）。

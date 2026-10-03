/* KV: posterを先に見せ、条件が良いときだけ短い無音ループを重ねる。
   モーション低減 / 省データ / 2G / 自動再生拒否（iOS低電力モード等）では静止画のまま。 */
(function () {
  var kv = document.querySelector('[data-kv]');
  if (!kv) return;

  // 次回施術日：ページ内の日程チップ [data-next-session] の先頭を流用（手更新は日程側1か所で済む）
  var slot = kv.querySelector('[data-kv-next]');
  var chip = document.querySelector('[data-next-session]');
  if (slot && chip) slot.textContent = '次回施術日 ' + chip.textContent.trim();

  var v = kv.querySelector('.kv-video');
  if (!v) return;
  var mm = window.matchMedia;
  if (mm && mm('(prefers-reduced-motion: reduce)').matches) return;
  var c = navigator.connection;
  if (c && (c.saveData || /(^|-)2g$/.test(c.effectiveType || ''))) return;

  function start() {
    var pc = mm && mm('(min-width: 900px)').matches;
    var src = pc ? v.getAttribute('data-src-pc') : v.getAttribute('data-src-sp');
    if (!src) return;
    v.muted = true;
    v.src = src;
    v.addEventListener('playing', function () { kv.classList.add('is-playing'); }, { once: true });
    var p = v.play();
    if (p && p.catch) p.catch(function () {});
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        if (e[0].isIntersecting) { var q = v.play(); if (q && q.catch) q.catch(function () {}); }
        else v.pause();
      }).observe(kv);
    }
  }
  if (document.readyState === 'complete') setTimeout(start, 200);
  else window.addEventListener('load', function () { setTimeout(start, 200); });
})();

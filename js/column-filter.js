/* コラム一覧の「部位で見る」絞り込み。?part=mayu のようにURLで開ける（症例ページ等からのリンク用）。
   data-parts の無いカード（自動公開で追加された記事）はタイトルから部位を推定する。 */
(function () {
  var nav = document.querySelector('[data-col-filter]');
  var cards = [].slice.call(document.querySelectorAll('.col-card'));
  if (!nav || !cards.length) return;
  var status = document.querySelector('[data-col-status]');

  var GUESS = [
    ['mens', /メンズ|男性/], ['mayu', /眉/], ['eyeline', /アイライン|目元|アイメイク/],
    ['lip', /リップ|唇/], ['hair', /ヘアライン|スカルプ|頭皮|生え際|薄毛/],
    ['para', /パラメディカル|傷跡|ほくろ|乳輪|白斑/], ['amara', /アマラ/],
    ['fix', /除去|修正|やり直し|変色|消し/]
  ];
  cards.forEach(function (c) {
    if (c.getAttribute('data-parts')) return;
    var t = c.textContent, p = [];
    GUESS.forEach(function (g) { if (g[1].test(t)) p.push(g[0]); });
    var cat = (c.querySelector('.col-cat') || {}).textContent || '';
    if (/エリア/.test(cat)) p.push('area');
    if (!p.length) p.push('basic');
    c.setAttribute('data-parts', p.join(' '));
  });

  var links = [].slice.call(nav.querySelectorAll('a[data-part]'));
  function has(c, part) { return part === 'all' || (' ' + c.getAttribute('data-parts') + ' ').indexOf(' ' + part + ' ') > -1; }
  links.forEach(function (a) {
    var part = a.getAttribute('data-part');
    var n = cards.filter(function (c) { return has(c, part); }).length;
    var s = document.createElement('span'); s.className = 'col-filter-n'; s.textContent = n;
    a.appendChild(s);
  });

  function apply(part, push) {
    var ok = links.some(function (a) { return a.getAttribute('data-part') === part; });
    if (!ok) part = 'all';
    var n = 0;
    cards.forEach(function (c) { var on = has(c, part); c.hidden = !on; if (on) n++; });
    links.forEach(function (a) {
      var on = a.getAttribute('data-part') === part;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
    if (status) {
      var label = links.filter(function (a) { return a.getAttribute('data-part') === part; })[0];
      status.textContent = part === 'all' ? '' : '「' + label.firstChild.textContent.trim() + '」のコラム ' + n + '件';
    }
    if (push && window.history && history.replaceState) {
      history.replaceState(null, '', part === 'all' ? location.pathname : '?part=' + part);
    }
  }
  nav.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-part]');
    if (!a) return;
    e.preventDefault();
    apply(a.getAttribute('data-part'), true);
  });
  var q = (location.search.match(/[?&]part=([a-z]+)/) || [])[1];
  apply(q || 'all', false);
  if (q) { var g = document.querySelector('.col-grid'); if (g && nav.scrollIntoView) nav.scrollIntoView({ block: 'start' }); }
})();

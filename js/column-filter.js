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
  /* 地域: リンクのslugから判定。地域が分かる記事は自動で「地域から探す」にも入れる */
  var REGION = {
    tokyo: ['tokyo', 'hanzomon', 'chiyoda'], ibaraki: ['tsukuba', 'tsuchiura', 'ibaraki', 'mito'],
    tochigi: ['tochigi', 'utsunomiya', 'mibu', 'ashikaga', 'sano'], gunma: ['gunma', 'takasaki', 'ota', 'maebashi'],
    kagawa: ['kagawa', 'takamatsu'], nagano: ['nagano', 'saku', 'ueda', 'komoro', 'karuizawa']
  };
  function regionOf(c) {
    var a = c.querySelector('a[href]'); if (!a) return '';
    var toks = a.getAttribute('href').replace(/\.html$/, '').split('/').pop().split('-');
    for (var r in REGION) { for (var i = 0; i < REGION[r].length; i++) { if (toks.indexOf(REGION[r][i]) > -1) return r; } }
    return '';
  }
  cards.forEach(function (c) {
    var reg = regionOf(c);
    if (c.getAttribute('data-parts')) {
      if (reg) { var cur = ' ' + c.getAttribute('data-parts') + ' '; var add = (cur.indexOf(' area ') < 0 ? ' area' : '') + ' ' + reg; c.setAttribute('data-parts', (cur + add).trim().replace(/\s+/g, ' ')); }
      return;
    }
    var t = c.textContent, p = [];
    if (reg) p.push('area', reg);
    GUESS.forEach(function (g) { if (g[1].test(t)) p.push(g[0]); });
    var cat = (c.querySelector('.col-cat') || {}).textContent || '';
    if (/エリア/.test(cat)) p.push('area');
    if (!p.length) p.push('basic');
    if (reg && p.indexOf('basic') > -1) p.splice(p.indexOf('basic'), 1);
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

  var expanded = false, grid = document.querySelector('.col-grid'), more = null;
  if (grid) {
    more = document.createElement('p'); more.style.cssText = 'text-align:center;margin:28px 0';
    more.innerHTML = '<a href="#" class="col-more" style="display:inline-block;border:0.5px solid var(--border);padding:12px 28px;font-size:13px;color:var(--brown);text-decoration:none;background:var(--white)">さらに表示する（新しい順）</a>';
    grid.parentNode.insertBefore(more, grid.nextSibling);
    more.addEventListener('click', function (e) { e.preventDefault(); expanded = true; apply('all', false); });
  }
  function apply(part, push) {
    var ok = links.some(function (a) { return a.getAttribute('data-part') === part; });
    if (!ok) part = 'all';
    var n = 0;
    var LIMIT = 30, shown = 0;
    cards.forEach(function (c) {
      var on = has(c, part);
      if (on) n++;
      if (on && part === 'all' && !expanded && ++shown > LIMIT) on = false;
      c.hidden = !on;
    });
    if (more) more.hidden = !(part === 'all' && !expanded && n > LIMIT);
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

// Nav 現在地ハイライト（絶対パス統一に伴い、activeはJSで自動付与）
(function () {
  function norm(p) {
    p = (p || '').split('#')[0].split('?')[0];
    p = p.replace(/index\.html$/, '').replace(/\.html$/, '');
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    return p === '' ? '/' : p;
  }
  var here = norm(location.pathname);
  document.querySelectorAll('.global-nav a, .mobile-nav a').forEach(function (a) {
    var href = norm(a.getAttribute('href'));
    if (href === '/') return;
    if (here === href || (href === '/column' && here.indexOf('/column') === 0)) {
      a.classList.add('active');
    }
  });
  var dd = document.querySelector('.global-nav .has-dropdown');
  if (dd && dd.querySelector('.dropdown-menu a.active')) {
    var parent = dd.querySelector('.nav-parent');
    if (parent) parent.classList.add('active');
  }
})();

// Hamburger menu
const hamburger = document.querySelector('.hamburger');
const mobileNav = document.querySelector('.mobile-nav');
if (hamburger && mobileNav) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileNav.classList.toggle('open');
  });
  mobileNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      mobileNav.classList.remove('open');
    });
  });
}

// Hero slideshow
const slides = document.querySelectorAll('.hero-slide');
if (slides.length > 1) {
  let current = 0;
  setInterval(() => {
    slides[current].classList.remove('active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('active');
  }, 5000);
}

// Reviews toggle
function toggleReviews() {
  const hidden = document.querySelectorAll('.hidden-review');
  const btn = document.getElementById('reviewsMoreBtn');
  const isShowing = hidden[0] && hidden[0].style.display === 'block';
  hidden.forEach(el => { el.style.display = isShowing ? 'none' : 'block'; });
  if (btn) btn.textContent = isShowing ? '口コミをもっと見る' : '閉じる';
}

// Scroll fade-in
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.service-card, .review-card, .case-img-wrap, .artist-inner, .fade-in').forEach(el => {
  observer.observe(el);
});


// 施術動画 再生・一時停止（モバイル対応版）
const videoOverlay = document.getElementById('videoOverlay');
const sejutsuVideo = document.getElementById('sejutsuVideo');
// iOSは同時に1本しか再生できないためhero動画を取得
const bgVideo = document.querySelector('.lp-hero-video') || document.querySelector('.hero-video');

if (videoOverlay && sejutsuVideo) {
  function tryPlay() {
    // hero動画を先に停止（iOS制限対応）
    if (bgVideo && !bgVideo.paused) { bgVideo.pause(); }
    const p = sejutsuVideo.play();
    if (p !== undefined) {
      p.then(function() {
        videoOverlay.classList.add('hidden');
      }).catch(function(err) {
        // autoplay制限の場合、mutedで再試行
        sejutsuVideo.muted = true;
        sejutsuVideo.play().then(function() {
          videoOverlay.classList.add('hidden');
        }).catch(function() {});
      });
    } else {
      videoOverlay.classList.add('hidden');
    }
  }
  function doPause() {
    sejutsuVideo.pause();
    videoOverlay.classList.remove('hidden');
    // hero動画を再開
    if (bgVideo) { bgVideo.play().catch(function(){}); }
  }
  videoOverlay.addEventListener('click', tryPlay);
  sejutsuVideo.addEventListener('click', function() {
    if (sejutsuVideo.paused) { tryPlay(); } else { doPause(); }
  });
  sejutsuVideo.addEventListener('ended', function() {
    videoOverlay.classList.remove('hidden');
    if (bgVideo) { bgVideo.play().catch(function(){}); }
  });
}

// FAQ アコーディオン
function toggleFaq(btn) {
  const answer = btn.nextElementSibling;
  const isOpen = btn.classList.contains('open');
  document.querySelectorAll('.faq-question').forEach(b => { b.classList.remove('open'); b.nextElementSibling.classList.remove('open'); });
  if (!isOpen) { btn.classList.add('open'); answer.classList.add('open'); }
}

/* ===== CTAクリック計測（GA4へ cta_click を送る。item_label=ボタン位置 / link_url=遷移先 / cta_type=種類）=====
   dataLayerにcta_clickイベントを積み、GTM(カスタムイベント cta_click のトリガー+GA4イベントタグ)がGA4へ送る。既存の line_click / instagram_click は別途GTM側が送る。 */
(function () {
  window.dataLayer = window.dataLayer || [];

  function ctaType(a) {
    var href = a.getAttribute('href') || '';
    var txt = (a.textContent || '').replace(/\s+/g, '');
    if (/lin\.ee|line\.me/.test(href)) return 'line';
    if (/instagram\.com/.test(href)) return 'instagram';
    if (/^tel:/.test(href)) return 'tel';
    if (/#price|料金/.test(href) || /料金|総額|費用/.test(txt)) return 'price';
    if (/case|#cases|#case-story/.test(href) || /症例/.test(txt)) return 'cases';
    if (/(^|\/)contact(\.html)?(\?|#|$)/.test(href) || /お問い合わせ|お問合せ/.test(txt)) return 'contact';
    if (/(^|\/)clinics?(\.html)?(\?|#|$)/.test(href)) return 'clinics';
    return '';
  }

  function position(a) {
    if (a.closest('.float-line-btn, .float-insta-btn, [class*="float-"]')) return 'floating';
    if (a.closest('.kv')) return 'hero';
    if (a.closest('.site-header, .mobile-nav')) return 'header';
    if (a.closest('footer, .site-footer')) return 'footer';
    if (a.closest('.cta-section')) return 'bottom_cta';
    if (a.closest('.faq-section')) return 'faq';
    if (a.closest('.cs-section')) return 'case_story';
    if (a.closest('.quick-nav, [data-quick-nav]')) return 'quick_nav';
    if (a.closest('.col-start')) return 'column_start';
    if (a.closest('.col-grid, .col-card')) return 'column_list';
    if (a.closest('article, .article-body, .column-body')) return 'article';
    var sec = a.closest('section');
    if (sec) return (sec.id || (sec.className || '').split(/\s+/)[0] || 'section').slice(0, 40);
    return 'other';
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var type = ctaType(a);
    if (!type) return;
    var href = a.href || '';
    window.dataLayer.push({
      event: 'cta_click',
      cta_type: type,
      item_label: position(a),
      link_url: href.slice(0, 100),
      click_text: (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50),
      page_path: location.pathname
    });
  }, true);
})();

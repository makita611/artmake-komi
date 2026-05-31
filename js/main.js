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

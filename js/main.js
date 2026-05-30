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


// 施術動画 再生・一時停止
const videoOverlay = document.getElementById('videoOverlay');
const sejutsuVideo = document.getElementById('sejutsuVideo');
if (videoOverlay && sejutsuVideo) {
  videoOverlay.addEventListener('click', () => {
    sejutsuVideo.play();
    videoOverlay.classList.add('hidden');
  });
  sejutsuVideo.addEventListener('click', () => {
    if (sejutsuVideo.paused) {
      sejutsuVideo.play();
      videoOverlay.classList.add('hidden');
    } else {
      sejutsuVideo.pause();
      videoOverlay.classList.remove('hidden');
    }
  });
  sejutsuVideo.addEventListener('ended', () => {
    videoOverlay.classList.remove('hidden');
  });
}

// FAQ アコーディオン
function toggleFaq(btn) {
  const answer = btn.nextElementSibling;
  const isOpen = btn.classList.contains('open');
  document.querySelectorAll('.faq-question').forEach(b => { b.classList.remove('open'); b.nextElementSibling.classList.remove('open'); });
  if (!isOpen) { btn.classList.add('open'); answer.classList.add('open'); }
}

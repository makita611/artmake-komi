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

document.querySelectorAll('.service-card, .review-card, .case-img-wrap, .artist-inner').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

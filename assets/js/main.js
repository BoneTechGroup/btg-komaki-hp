// ===== スクロール出現アニメーション =====
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// ===== FAQ アコーディオン =====
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
});

// ===== モバイルメニュー =====
const mnav = document.getElementById('mnav');
document.getElementById('burger')?.addEventListener('click', () => mnav.classList.add('show'));
document.getElementById('mclose')?.addEventListener('click', () => mnav.classList.remove('show'));
mnav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mnav.classList.remove('show')));

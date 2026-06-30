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

// ===== ギャラリー ライトボックス =====
const lb = document.getElementById('lightbox');
if (lb) {
  const lbImg = lb.querySelector('img');
  document.querySelectorAll('.gallery-grid figure img').forEach(img => {
    img.addEventListener('click', () => { lbImg.src = img.src; lbImg.alt = img.alt; lb.classList.add('show'); });
  });
  lb.addEventListener('click', () => lb.classList.remove('show'));
}

// ===== モバイルメニュー =====
const mnav = document.getElementById('mnav');
document.getElementById('burger')?.addEventListener('click', () => mnav.classList.add('show'));
document.getElementById('mclose')?.addEventListener('click', () => mnav.classList.remove('show'));
mnav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mnav.classList.remove('show')));

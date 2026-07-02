// ===== スクロール進捗バー =====
const progress = document.getElementById('progress');
const onScroll = () => {
  const h = document.documentElement;
  const p = (h.scrollTop) / (h.scrollHeight - h.clientHeight);
  if (progress) progress.style.width = (p * 100) + '%';
};
document.addEventListener('scroll', onScroll, { passive: true }); onScroll();

// ===== スクロール出現アニメーション =====
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
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

// ===== トップへ戻るボタン =====
const totop = document.getElementById('totop');
if (totop) {
  const toggleTop = () => totop.classList.toggle('show', window.scrollY > 600);
  document.addEventListener('scroll', toggleTop, { passive: true }); toggleTop();
  totop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// ===== 慰謝料 計算シミュレーター =====
(() => {
  const total = document.getElementById('simTotal');
  const totalN = document.getElementById('simTotalN');
  const visit = document.getElementById('simVisit');
  const visitN = document.getElementById('simVisitN');
  const yenEl = document.getElementById('simYen');
  const calcEl = document.getElementById('simCalc');
  if (!total) return;
  const DAILY = 4300;
  const fmt = n => n.toLocaleString('ja-JP');
  let cur = 0;

  function animateTo(target) {
    cancelAnimationFrame(animateTo._r);
    yenEl.textContent = fmt(target); // 確実に最終値を表示（環境非依存）
    if (!('requestAnimationFrame' in window)) { cur = target; return; }
    const start = cur, t0 = performance.now(), dur = 500;
    const step = (t) => {
      const k = Math.min(1, (t - t0) / dur);
      const val = Math.round(start + (target - start) * (1 - Math.pow(1 - k, 3)));
      yenEl.textContent = fmt(val);
      if (k < 1) animateTo._r = requestAnimationFrame(step); else { cur = target; yenEl.textContent = fmt(target); }
    };
    animateTo._r = requestAnimationFrame(step);
  }

  function calc() {
    let t = Math.max(1, Math.min(180, +total.value || 1));
    let v = Math.max(1, Math.min(120, +visit.value || 1));
    // 対象日数 = min(実通院日数×2, 通院期間の日数)
    const target = Math.min(v * 2, t);
    const yen = target * DAILY;
    calcEl.innerHTML = `4,300円 × <b>${fmt(target)}日</b>（実通院${v}日×2=${fmt(v*2)}日 と 通院期間${t}日 の少ない方）`;
    animateTo(yen);
  }
  // レンジと数値入力の同期
  const sync = (a, b) => a.addEventListener('input', () => { b.value = a.value; calc(); });
  sync(total, totalN); sync(totalN, total);
  sync(visit, visitN); sync(visitN, visit);
  calc();
})();

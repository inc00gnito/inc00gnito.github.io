document.documentElement.classList.add('js');
document.getElementById('year').textContent = new Date().getFullYear();

const motionOK = matchMedia('(prefers-reduced-motion: no-preference)').matches;
const nav = document.querySelector('.nav');
const bar = document.querySelector('.progress');
const timeline = document.querySelector('.timeline');
let lastY = scrollY, ticking = false;

function onScroll() {
  const y = scrollY;
  const max = document.documentElement.scrollHeight - innerHeight;
  bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
  nav.classList.toggle('hide', y > lastY && y > 120);
  lastY = y;
  if (motionOK && timeline) {
    const r = timeline.getBoundingClientRect();
    const p = (innerHeight * 0.75 - r.top) / r.height;
    timeline.style.setProperty('--p', Math.min(Math.max(p, 0.04), 1));
  }
  ticking = false;
}
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
onScroll();

const counters = document.querySelectorAll('[data-count]');
if (motionOK && 'IntersectionObserver' in window) {
  const reveal = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      reveal.unobserve(e.target);
      e.target.classList.add('in');
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('section:not(.hero) h2, .stat, .card, .timeline > li, .contact > *').forEach((el, i) => {
    el.classList.add('reveal');
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    reveal.observe(el);
  });

  const count = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      count.unobserve(e.target);
      const el = e.target;
      const end = +el.dataset.count;
      const pre = el.dataset.prefix || '';
      const suf = el.dataset.suffix || '';
      const t0 = performance.now();
      const tick = (t) => {
        const p = Math.min((t - t0) / 1100, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + Math.round(end * eased).toLocaleString('en-US') + suf;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.6 });
  counters.forEach((el) => count.observe(el));
}

if (motionOK && matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.querySelectorAll('.btn').forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const r = btn.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width / 2) * 0.25;
      const y = (e.clientY - r.top - r.height / 2) * 0.35;
      btn.style.transform = `translate(${x}px, ${y}px)`;
    });
    btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
  });
}

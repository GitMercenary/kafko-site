/* Kafko — site behaviour. No dependencies. */
(function () {
  'use strict';

  /* reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window)) {
    rv.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    rv.forEach(function (el) { io.observe(el); });
  }

  /* smooth in-page scroll (Lenis-free, respects reduced motion) */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      var t = document.querySelector(id);
      if (!t) return;
      e.preventDefault();
      t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  });

  /* TODO(BAT): ordering destination. Awaiting the client's platform or WhatsApp number. */
  var ORDER_URL = '';
  var btn = document.getElementById('orderBtn');
  if (btn) {
    btn.addEventListener('click', function (e) {
      if (!ORDER_URL) { e.preventDefault(); }
      else { btn.setAttribute('href', ORDER_URL); }
    });
  }

  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();

/* sticky nav state — appended after visual QA */
(function () {
  var nav = document.querySelector('.nav');
  if (!nav) return;
  var f = function () { nav.classList.toggle('is-stuck', window.scrollY > 80); };
  f(); window.addEventListener('scroll', f, { passive: true });
})();

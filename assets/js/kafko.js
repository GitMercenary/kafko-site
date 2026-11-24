/* ============================================================================
   KAFKO — motion.
   Native reimplementation of escape.cafe's motion system (see study.md M1–M9).
   The original ships GSAP + ScrollTrigger + Lenis + Splitting + Swiper ≈ 310KB.
   This is ~7KB and behaviourally equivalent.
   ============================================================================ */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function randomInRange(min, max) { return Math.random() * (max - min) + min; }

  /* ---- viewport vars, as the original sets them on <html> ---------------- */
  function setViewportVars() {
    var d = document.documentElement;
    d.style.setProperty('--viewport-height', window.innerHeight + 'px');
    d.style.setProperty('--scrollbar-width', Math.max(window.innerWidth - d.clientWidth, 0) + 'px');
  }
  setViewportVars();
  window.addEventListener('resize', setViewportVars);

  /* =======================================================================
     M3 — .js-anim-big-title : split by chars, then scatter-in.
     Original: every 3rd char xPercent ±50, others yPercent ±70, each char its
     own random 0.1–0.6s stagger; expo.out, transform 1.4s / opacity 0.8s.
     ======================================================================= */
  function splitChars(el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach(function (w, wi) {
      var wEl = document.createElement('span');
      wEl.className = 'word';
      w.split('').forEach(function (c) {
        var cEl = document.createElement('span');
        cEl.className = 'char';
        cEl.textContent = c;
        wEl.appendChild(cEl);
      });
      el.appendChild(wEl);
      if (wi < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    return $$('.word', el);
  }

  function prepBigTitle(title) {
    var words = splitChars(title);
    var animI = 0, xIndex = 0, yIndex = 0;
    words.forEach(function (word, index) {
      animI = index % 2 ? 1 : 0;
      Array.prototype.slice.call(word.children).forEach(function (char, subindex) {
        if ((subindex + animI) % 3 === 0) {
          char.style.setProperty('--cx', (xIndex % 2 ? 50 : -50) + '%');
          xIndex++;
        } else if (animI % 2 === 0) {
          char.style.setProperty('--cy', (yIndex % 2 ? -70 : 70) + '%');
          yIndex++;
        }
        char.style.setProperty('--cd', randomInRange(0.1, 0.6).toFixed(3) + 's');
        animI++;
      });
    });
  }

  /* =======================================================================
     M4 — .js-anim-lines : split into REAL visual lines (measured after layout),
     then rise from 50% with a 0.15s-per-line stagger.
     ======================================================================= */
  function splitLines(el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    var probes = words.map(function (w, i) {
      var s = document.createElement('span');
      s.style.display = 'inline-block';
      s.textContent = w;
      el.appendChild(s);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
      return s;
    });
    var lines = [], top = null, cur = null;
    probes.forEach(function (p) {
      var t = Math.round(p.getBoundingClientRect().top);
      if (top === null || Math.abs(t - top) > 4) { top = t; cur = []; lines.push(cur); }
      cur.push(p.textContent);
    });
    el.textContent = '';
    lines.forEach(function (ws, i) {
      var line = document.createElement('span');
      line.className = 'line';
      line.style.setProperty('--line-index', i);
      var inner = document.createElement('span');
      inner.textContent = ws.join(' ');
      line.appendChild(inner);
      el.appendChild(line);
    });
  }

  /* =======================================================================
     M5 — parallax through --yPercent, scrubbed to scroll.
       .js-parallax-in / .js-parallax : -1 → 1  over "top bottom" → "bottom top"
       .js-parallax-header            :  0 → 1  over "top top"    → "bottom top"
     ======================================================================= */
  var parallaxEls = [];
  function collectParallax() {
    parallaxEls = $$('.js-parallax-in, .js-parallax').map(function (el) {
      return { el: el, from: -1, to: 1, header: false };
    }).concat($$('.js-parallax-header').map(function (el) {
      return { el: el, from: 0, to: 1, header: true };
    }));
  }

  var ticking = false;
  function updateParallax() {
    var vh = window.innerHeight;
    parallaxEls.forEach(function (p) {
      var r = p.el.getBoundingClientRect();
      var start = p.header ? 0 : vh;      // "top top" vs "top bottom"
      var end = -r.height;                // "bottom top"
      var prog = (start - r.top) / (start - end);
      prog = prog < 0 ? 0 : prog > 1 ? 1 : prog;
      p.el.style.setProperty('--yPercent', (p.from + (p.to - p.from) * prog).toFixed(4));
    });
    ticking = false;
  }
  function onScroll() {
    if (!ticking && !reduce) { ticking = true; requestAnimationFrame(updateParallax); }
  }

  /* =======================================================================
     M2 — per-section theme flip.
     ScrollTrigger start:"top top" end:"bottom top" → whichever section is
     crossing the top of the viewport owns document.body[data-theme].
     ======================================================================= */
  var sections = [];
  function updateTheme() {
    if (!sections.length) return;
    var active = sections[0];
    sections.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top <= 1 && r.bottom > 1) active = s;
    });
    var atEnd = window.innerHeight + window.scrollY >= document.body.scrollHeight - 2;
    if (atEnd) active = sections[sections.length - 1];
    var t = active.dataset.theme || 'light';
    if (document.body.dataset.theme !== t) document.body.dataset.theme = t;
  }

  /* ---- deterministic reveal sweep — the safety net under the observers ---- */
  var revealEls = [];
  function collectReveals() {
    revealEls = $$('.js-anim-big-title, .js-anim-lines, .js-anim-in, .mobile-lines');
  }
  function sweepReveals() {
    var vh = window.innerHeight, i = revealEls.length;
    while (i--) {
      var el = revealEls[i];
      if (el.classList.contains('-active')) { revealEls.splice(i, 1); continue; }
      var r = el.getBoundingClientRect();
      // once-only reveal: if the top has passed the trigger line it has been
      // reached, even if the element is now scrolled above the viewport.
      if (r.top < vh * 0.85) {
        el.classList.add('-active');
        revealEls.splice(i, 1);
      }
    }
  }

  /* ---- reveal triggers (IntersectionObserver stands in for ScrollTrigger) -- */
  function observe(els, opts) {
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('-active'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('-active'); io.unobserve(e.target); }
      });
    }, opts);
    els.forEach(function (e) { io.observe(e); });
  }

  /* =======================================================================
     M7 — the collections carousel.
     Swiper config recovered: { speed:600, slidesPerView:1, grabCursor:true,
                                navigation:{ nextEl:'.next-btn', prevEl:'.prev-btn' } }
     ======================================================================= */
  function initCarousel() {
    var root = document.querySelector('[data-carousel]');
    if (!root) return;
    var track = root.querySelector('.homeCollections__slides');
    var slides = $$('.homeCollections__slide', root);
    var infos = $$('[data-info]', root);
    var lines = $$('.homeCollections__productsLine');
    var scope = root.closest('.homeCollections') || document;
    var prev = scope.querySelector('[data-prev]');
    var next = scope.querySelector('[data-next]');
    if (!track || !slides.length) return;
    var i = 0;

    function go(n) {
      i = (n + slides.length) % slides.length;
      track.style.transform = 'translate3d(' + (-100 * i) + '%,0,0)';
      slides.forEach(function (s, k) { s.classList.toggle('-active', k === i); });
      lines.forEach(function (l, k) { l.classList.toggle('-active', k === i); });
      infos.forEach(function (el, k) { el.hidden = k !== i; });
    }
    if (prev) prev.addEventListener('click', function () { go(i - 1); });
    if (next) next.addEventListener('click', function () { go(i + 1); });

    var x0 = null;
    root.addEventListener('pointerdown', function (e) { x0 = e.clientX; root.style.cursor = 'grabbing'; });
    window.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0;
      if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1));
      x0 = null; root.style.cursor = 'grab';
    });
    root.style.cursor = 'grab';
    go(0);
  }

  /* ---- order CTA — awaiting the client's ordering platform --------------- */
  function initOrder() {
    var ORDER_URL = '';
    $$('[data-order]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        if (!ORDER_URL) e.preventDefault(); else btn.setAttribute('href', ORDER_URL);
      });
    });
  }

  /* ---- boot -------------------------------------------------------------- */
  function init() {
    var bigTitles = $$('.js-anim-big-title');
    var lineEls = $$('.js-anim-lines');
    var animIns = $$('.js-anim-in');

    bigTitles.forEach(prepBigTitle);
    lineEls.forEach(splitLines);
    collectParallax();

    sections = $$('.js-section');
    if (sections.length) document.body.dataset.theme = sections[0].dataset.theme || 'light';

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        document.documentElement.classList.add('is-ready');
        observe(bigTitles, { threshold: 0 });                              // ST default "top bottom"
        observe(lineEls, { rootMargin: '0px 0px -20% 0px', threshold: 0 }); // "top 80%"
        observe(animIns, { rootMargin: '0px 0px -20% 0px', threshold: 0 }); // "top 80%"
        observe($$('.mobile-lines'), { threshold: 0 });
        collectReveals();
        sweepReveals();
        updateParallax();
        updateTheme();
      });
    });

    window.addEventListener('scroll', function () {
      onScroll(); updateTheme(); sweepReveals();
    }, { passive: true });
    window.addEventListener('resize', function () {
      collectParallax(); onScroll(); sweepReveals();
    }, { passive: true });
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  ready(function () {
    init();
    initCarousel();
    initOrder();
    var yr = document.getElementById('yr');
    if (yr) yr.textContent = new Date().getFullYear();
  });
})();

/* newsletter — not wired to a list yet; validate and acknowledge in place */
(function () {
  var f = document.getElementById('newsletter');
  if (!f) return;
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var note = f.parentElement.querySelector('.note');
    var v = f.querySelector('input').value.trim();
    if (!note) return;
    note.textContent = /.+@.+\..+/.test(v)
      ? 'Thanks — we’ll be in touch. (Not yet connected to a mailing list.)'
      : '⚠ Please enter a valid email address.';
  });
})();

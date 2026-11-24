#!/usr/bin/env python3
"""
Kafko — page generator.

Structure follows escape.cafe section-for-section (see
webforge/projects/kafko-escape/study.md). The real class names are kept so the
build can be diffed against the original.

Usage: python build.py
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WM = io.open(os.path.join(HERE, "_wm.svg"), encoding="utf-8").read()
KM = io.open(os.path.join(HERE, "_km.svg"), encoding="utf-8").read()


def img(slug, w, h, alt, sizes="100vw", widths=(500, 900)):
    srcset = ", ".join("assets/img/%s-%d.webp %dw" % (slug, x, x) for x in widths)
    return ('<img src="assets/img/%s-%d.webp" srcset="%s" sizes="%s" '
            'width="%d" height="%d" alt="%s" loading="lazy">'
            % (slug, widths[-1], srcset, sizes, w, h, alt))


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kafko — Specialty Coffee, Done Right</title>
<meta name="description" content="Kafko — specialty coffee and quick bites in under ten minutes. Find us on 100 Feet Road, Indiranagar, Bengaluru. Open 7am to 11pm, daily.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#FF4637">
<link rel="icon" href="assets/svg/kafko-favicon-k.svg">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/RobotoCondensed-800-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/Barlow-500-latin.woff2" crossorigin>
<link rel="stylesheet" href="assets/css/kafko.css">
</head>
<body data-theme="red">

<a href="#main" class="sr-only">Skip to content</a>

<!-- fixed 90px right rail — escape.cafe deducts this from --col on desktop -->
<aside class="rail" aria-hidden="true">
  <span class="rail__txt">Under 10 minutes &middot; Micro-format outlets &middot; Bengaluru</span>
</aside>

<header class="header">
  <a href="#top" aria-label="Kafko — home"><span class="header__logo">%s</span></a>
  <nav class="header__nav" aria-label="Primary">
    <a href="#collections">Coffee</a>
    <a href="#mission">Ritual</a>
    <a href="#visit">Visit</a>
    <a href="#visit">Visit us</a>
  </nav>
</header>

<main id="main">
""" % KM

# --------------------------------------------------------------- 1 · HERO
HERO = """
<!-- ===================== 1 · homeHero ===================== -->
<section class="homeHero js-section" data-theme="red" id="top">
  <div class="homeHero__media js-parallax-header">
    <img src="assets/img/hero-baristas-1600.webp"
         srcset="assets/img/hero-baristas-900.webp 900w, assets/img/hero-baristas-1600.webp 1600w"
         sizes="100vw" width="1600" height="900" fetchpriority="high"
         alt="Baristas serving espresso and cappuccino across the counter">
  </div>

  <div class="homeHero__wrapper pad-x">
    <div class="homeHero__wm">%s</div>
    <h1 class="homeHero__tagline t-h1 js-anim-big-title">We do not believe in shit coffee.</h1>
    <p class="homeHero__description t-h4 js-anim-lines">Specialty coffee and quick bites in under ten minutes, engineered for speed, precision and consistency.</p>
    <div class="homeHero__btnWrapper">
      <a class="btn btn--dark" href="#visit">Find us</a>
      <a class="btn btn--light" href="#collections">See the menu</a>
    </div>

    <div class="homeHero__push">
      <p class="homeHero__mood t-narrow">Effortless<br>Fearless<br>Seamless</p>
      <div class="homeHero__products">
        <ul class="homeHero__list">
          <li class="homeHero__product">
            <h3>Espresso</h3>
            <table><tr><td>Type</td><td>Single origin</td></tr><tr><td>Serve</td><td>Hot</td></tr><tr><td>Time</td><td>Under 10</td></tr></table>
          </li>
          <li class="homeHero__product">
            <h3>Cold brew</h3>
            <table><tr><td>Type</td><td>Slow steep</td></tr><tr><td>Serve</td><td>Iced</td></tr><tr><td>Time</td><td>Under 10</td></tr></table>
          </li>
          <li class="homeHero__product">
            <h3>Beans</h3>
            <table><tr><td>Type</td><td>Roasted fresh</td></tr><tr><td>Serve</td><td>Take home</td></tr><tr><td>Grind</td><td>To order</td></tr></table>
          </li>
        </ul>
      </div>
      <p class="homeHero__pushTagline t-narrow">For urban hustlers chasing momentum. Day in, day out.</p>
    </div>
  </div>
</section>

<!-- marquee is MOBILE-ONLY on the original (.mobile-lines) -->
<div class="mobile-lines">
  <p class="line">
    <span>Let's raise a roast &#10037;</span><span>Your daily ritual &#10037;</span>
    <span>Under 10 minutes &#10037;</span><span>Craft over compromise &#10037;</span>
    <span aria-hidden="true">Let's raise a roast &#10037;</span><span aria-hidden="true">Your daily ritual &#10037;</span>
    <span aria-hidden="true">Under 10 minutes &#10037;</span><span aria-hidden="true">Craft over compromise &#10037;</span>
  </p>
</div>
""" % WM

# --------------------------------------------------------------- 2 · COLLECTIONS
SLIDES = [
    ("espresso-pour", "Espresso bar", "Let's raise a roast.",
     "Single-origin and blends, pulled to spec. Flat white, cortado, filter — every cup built the same way, every time.",
     ["hands-cappuccino", "cappuccino-art", "flat-white-teal", "table-warm"]),
    ("cold-brew", "Cold &amp; iced", "In and out in ten.",
     "Cold brew and iced pours for the walk back to your desk. No queue, no fuss, no compromise on the coffee.",
     ["table-warm", "flat-white-teal", "hands-cappuccino", "cappuccino-art"]),
    ("grinder-beans", "Retail", "Take the beans home.",
     "The same coffee we serve, bagged fresh and ground to your brew method. Your daily ritual, at your kitchen counter.",
     ["cappuccino-art", "hands-cappuccino", "table-warm", "flat-white-teal"]),
]

vis, infos, lines = [], [], []
for n, (slug, kicker, title, body, prods) in enumerate(SLIDES):
    vis.append(
        '      <div class="homeCollections__slide%s">\n'
        '        <div class="media-filter homeCollections__visualWrapper js-parallax-in">%s</div>\n'
        '        <span class="brand">%s</span>\n'
        '      </div>'
        % (" -active" if n == 0 else "",
           img(slug, 600, 450, title, "(max-width:1023px) 100vw, 50vw", (600, 1000)),
           kicker.replace("&amp;", "&")))
    infos.append(
        '      <div data-info%s>\n'
        '        <p class="t-narrow">%s</p>\n'
        '        <h3 class="t-h2 js-anim-big-title mt-2">%s</h3>\n'
        '        <p class="body mt-2">%s</p>\n'
        '        <div class="homeCollections__buttons">\n'
        '          <a class="btn btn--dark" href="#visit">Visit us</a>\n'
        '          <a class="btn btn--light" href="#mission">Learn more</a>\n'
        '        </div>\n'
        '      </div>' % ("" if n == 0 else " hidden", kicker, title, body))
    media = "\n".join(
        '        <div class="product-media">%s</div>'
        % img(p, 500, 500, "Kafko coffee", "(max-width:1023px) 25vw, 20vw", (500, 900))
        for p in prods)
    lines.append(
        '    <div class="homeCollections__productsLine%s">\n%s\n    </div>'
        % (" -active" if n == 0 else "", media))

COLLECTIONS = """
<!-- ===================== 2 · homeCollections ===================== -->
<section class="homeCollections js-section" data-theme="beige" id="collections">
  <div class="pad-x">
    <div class="homeCollections__head">
      <h2 class="t-h2">The menu</h2>
      <div class="homeCollections__nav">
        <button type="button" data-prev aria-label="Previous">&larr;</button>
        <button type="button" data-next aria-label="Next">&rarr;</button>
      </div>
    </div>

    <div class="homeCollections__inner" data-carousel>
      <div class="homeCollections__visuals">
        <div class="homeCollections__slides">
%s
        </div>
      </div>
      <div class="homeCollections__infos">
%s
      </div>
    </div>

    <div class="homeCollections__productsWrapper">
%s
    </div>
  </div>
</section>
""" % ("\n".join(vis), "\n".join(infos), "\n".join(lines))

# --------------------------------------------------------------- 3 · MISSION
MISSION = """
<!-- ===================== 3 · homeMission ===================== -->
<section class="homeMission js-section" data-theme="red" id="mission">
  <div class="media-filter homeMission__bg js-parallax-in">
    <img src="assets/img/urban-hustler-1600.webp"
         srcset="assets/img/urban-hustler-900.webp 900w, assets/img/urban-hustler-1600.webp 1600w"
         sizes="100vw" width="1600" height="900" loading="lazy"
         alt="Working from a cafe table">
  </div>

  <div class="homeMission__manifest">
    <p class="homeMission__tagline t-narrow">Our ritual</p>
    <div>
      <p class="homeMission__text t-h5 js-anim-lines">We deliver specialty coffee and quick bites in under ten minutes through micro-format outlets engineered for speed, precision and consistency. Because the best coffee shouldn't cost you your morning.</p>
      <a class="homeMission__btn btn btn--light btn--blend" href="#visit">Find the outlet</a>
    </div>
  </div>

  <div class="homeMission__visual">
    <div class="homeMission__img media-filter js-parallax-in">%s</div>
  </div>
  <p class="homeMission__imageTagline t-narrow js-anim-in">We are the daily ritual of the creators, the dreamers and the doers.</p>
</section>
""" % img("cafe-interior-warm", 500, 667, "Warm cafe interior with sunlight across the seating",
          "(max-width:1023px) 60vw, 420px", (500, 900))

# --------------------------------------------------------------- 4 · MANIFEST
MANIFEST = """
<!-- ===================== 4 · homeManifest ===================== -->
<section class="homeManifest js-section" data-theme="beige" id="visit">
  <div class="homeManifest__list pad-x">
    <h2 class="homeManifest__line2 t-h1 js-anim-big-title">Come</h2>
    <div class="media-filter homeManifest__image js-parallax-in">%s</div>
    <a class="homeManifest__btn btn btn--dark js-anim-in" href="#visit">Get directions</a>
    <h2 class="homeManifest__line3 t-h1 js-anim-big-title">Say hi.</h2>
    <div class="homeManifest__subscribe js-anim-in">
      <div class="visitCard">
        <dl>
          <dt>Where</dt><dd>Kafko, 100 Feet Road, Indiranagar,<br>Bengaluru, Karnataka 560038</dd>
          <dt>Hours</dt><dd>7:00am &ndash; 11:00pm, all week</dd>
          <dt>Call</dt><dd><a href="tel:+918660023218">+91 86600 23218</a></dd>
          <dt>Email</dt><dd><a href="mailto:hello@kafko.in">hello@kafko.in</a></dd>
        </dl>
        <a class="btn btn--red" href="https://maps.google.com/?q=100+Feet+Road+Indiranagar+Bengaluru" target="_blank" rel="noopener">Open in Maps</a>
        <p class="t-narrow" style="opacity:.55;margin-top:14px">&#9888; Placeholder details &mdash; to be replaced with the real outlet.</p>
      </div>
    </div>
  </div>
</section>
""" % img("espresso-pour", 600, 450, "Espresso pouring into a cup",
          "(max-width:1023px) 38vw, 420px", (600, 1000))

# --------------------------------------------------------------- FOOTER
FOOTER = """
</main>

<footer class="footer js-section" data-theme="dark">
  <div class="pad-x">

    <div class="footer__top">
      <nav class="footer__mainMenu" aria-label="Footer">
        <h4>Kafko</h4>
        <ul>
          <li><a href="#collections">The menu</a></li>
          <li><a href="#mission">Our ritual</a></li>
          <li><a href="#visit">Visit</a></li>
          <li><a href="#visit">Find us</a></li>
          <li><a href="credits.html">Image credits</a></li>
        </ul>
      </nav>

      <div class="footer__productsMenu">
        <h4>Our coffee</h4>
        <ul>
          <li><a href="#collections">Espresso bar</a></li>
          <li><a href="#collections">Cold &amp; iced</a></li>
          <li><a href="#collections">Beans to take home</a></li>
          <li><a href="#collections">Quick bites</a></li>
        </ul>
      </div>

      <div class="footer__newsletter">
        <h4>Stay in the loop</h4>
        <h2>New roasts, new outlets. Nothing else.</h2>
        <form id="newsletter" novalidate>
          <input type="email" name="email" placeholder="Email" aria-label="Email address" autocomplete="email" required>
          <button type="submit" aria-label="Subscribe">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path d="M4 12h15M13 6l6 6-6 6"/>
            </svg>
          </button>
        </form>
        <p class="note">&#9888; Placeholder &mdash; not connected to a mailing list yet.</p>

        <div class="footer__socials">
          <a href="#" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>
            </svg>
          </a>
          <a href="#" aria-label="Facebook">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path d="M15 3h-3a4 4 0 0 0-4 4v3H5v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
            </svg>
          </a>
          
        </div>
      </div>
    </div>

    <div class="footer__visual media-filter js-parallax-in">%s</div>

    <div class="footer__lastRow">
      <div class="footer__logo">%s</div>
      <h2 class="footer__close t-h2 js-anim-big-title">And you? How do you Kafko?</h2>
    </div>

    <div class="footer__footer">
      <div class="inner">
        <span>&copy; <span id="yr">2026</span> Kafko &middot; Bengaluru</span>
        <a class="center" href="#top">
          <span class="arrows"><span>&uarr;</span><span>&uarr;</span><span>&uarr;</span><span>&uarr;</span><span>&uarr;</span></span>
          <span>Kafko back to top</span>
          <span class="arrows"><span>&uarr;</span><span>&uarr;</span><span>&uarr;</span><span>&uarr;</span><span>&uarr;</span></span>
        </a>
        <span>Site by Black Arrow Technologies</span>
      </div>
    </div>

  </div>
</footer>

<script src="assets/js/kafko.js" defer></script>
</body>
</html>
""" % (img("hands-cappuccino", 500, 500, "A Kafko cup in hand", "260px", (500, 900)), WM)

io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="").write(
    HEAD + HERO + COLLECTIONS + MISSION + MANIFEST + FOOTER)
print("index.html written")

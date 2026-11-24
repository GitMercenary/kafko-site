# Kafko — build

Internal. Built by Black Arrow Technologies, 30-Aug-2026.

One-page brand site. Custom-coded, no framework, no build step, no dependencies.
Total CSS + JS is ~20KB uncompressed. Deploys as static files anywhere.

## The governing rule

> **escape.cafe decides structure and motion. The styleguide decides colour, type, shape and voice.
> Where they conflict, the styleguide wins.**

escape.cafe and Kafko are aesthetic opposites — escape is cold, desaturated, near-monochrome and
hard-edged; Kafko is warm, loud, red/cream and rounded. So "replica" means the **skeleton**, not the
mood. Concretely:

| escape.cafe | Kafko |
|---|---|
| square boxed buttons | rounded mono pills (styleguide p.15) |
| hard-edged panels | ~28px soft radii (styleguide "Online" p.28) |
| near-monochrome + photography does the colour | the four brand colours do the work |
| Shopify commerce sections | brand sections — **no cart, no checkout** |

Two alignments made this land better than it sounds: escape's headline style is heavy condensed
caps, which is exactly **Roboto Condensed ExtraBold**; and escape labels everything in mono, which
is exactly **IBM Plex Mono Medium**. Direct swaps.

## Structure (escape.cafe, section for section)

```
edge rail + minimal nav
1 · hero — full-bleed colour, giant wordmark, headline, CTA
2 · marquee ticker → spec boxes with mono labels → proposition split
3 · the menu — three cards (escape's "Collections")
4 · mission / manifesto over a colour block
5 · the outlet — editorial panel, corner mono captions, coordinates
6 · order — giant display word-scroll + numbered 01/02/03 list
closing marquee → black footer → oversized closing line
```

Six content sections, as contracted. **No e-commerce** — escape.cafe is a Shopify store, and
"clone escape.cafe" quietly implies subscriptions, cart and wholesale. Those are Phase 2 and are
deliberately not built. Hold this line.

## Brand implementation

**The wordmark is the real thing.** `assets/svg/kafko-wordmark.svg` was extracted as vector paths
directly out of the styleguide PDF — not traced, not approximated. Also extracted:
`kafko-vertical.svg` and `kafko-favicon-k.svg` (used as the nav mark and favicon).

```
--red    #FF4637   Kombucha Red
--beige  #FFF0C8   Toasty Beige
--black  #000000
--white  #FFFFFF
```
Only the six approved colour combos from styleguide p.12 are used. No other colours exist in the CSS.

**Type** (styleguide p.15 fallback stack, all self-hosted — no Google Fonts requests):
Headlines **Roboto Condensed ExtraBold** · Sub-heads **Barlow Medium** · Body **Barlow Regular** ·
Captions **IBM Plex Mono Medium**.

**Voice** used verbatim: *"We do not believe in shit coffee."* · *"Let's raise a roast."* ·
*"Your daily ritual."* · *Effortless. Fearless. Seamless.*

## Photography — licensed placeholders, in place

Kafko has no photography of its own (the styleguide's image pages are all *"Reference Only — WIP"*),
so the site currently runs on **10 Creative Commons images** sourced through
[Openverse](https://openverse.org) — CC0 and CC-BY only, no rights-managed stock, nothing with
third-party branding visible.

They are not dropped in raw. Each one is **cropped to the layout's aspect and put through one shared
warm grade** (+6% saturation, +8% contrast, reds up / blues down) so they read as a single shoot
rather than ten unrelated photos. The hero additionally runs **greyscale + Kombucha Red multiply** —
that duotone is what makes stock look art-directed rather than borrowed.

**Attribution is handled**: `credits.html` lists every image with creator, licence and source link,
and is linked from the footer. `IMAGE-CREDITS.json` holds the machine-readable version.
CC-BY requires this — do not remove the credits page while these images are in use.

⚠️ **These are still placeholders.** Get Kafko's own shoot — product, outlet interior, and people.
Swap the files in `assets/img/` (same filenames, same aspects) and delete `credits.html`
and its footer link. Nothing else needs to change.

## Also pending

- **Ordering destination** — `ORDER_URL` in `assets/js/kafko.js` is empty; the button is inert and
  labelled as pending on the page. Needs the client's platform or a WhatsApp number.
- **Address, hours, phone, email, social links** — marked `⚠️ pending` in the footer.
- **Prices** — cards show `From ₹—`.

## Deploying

Static, no build step. `vercel.json` and `netlify.toml` are included — security headers and
immutable caching on fonts and images.

```
cd "_build"
python -m http.server 8080
# → http://localhost:8080
```

Copy the folder to any host.

⚠️ **kafko.in is currently on GoDaddy Website Builder**, a closed SaaS — you cannot drop files into
it. The domain has to be repointed (Vercel/Netlify/any static host), and his Website Builder
subscription becomes redundant. Flag that to him so he can cancel it.

Remove `<meta name="robots" content="noindex,nofollow">` before go-live.

## QA done (30-Aug-2026)

Chromium at 1440px and 390px, served over HTTP: no horizontal overflow · no console errors ·
no failed requests · all four font families loading · every image/placeholder labelled ·
one `<h1>` · meta description present · reduced-motion disables the marquee and reveals ·
visible focus rings.

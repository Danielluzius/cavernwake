<p align="center">
  <img src="https://img.shields.io/badge/English-000000?style=for-the-badge&color=ffffff" alt="English" />
  <a href="README.de.md"><img src="https://img.shields.io/badge/Deutsch-6e7781?style=for-the-badge&color=ffffff" alt="Deutsch" /></a>
</p>

# Cavernwake

A pixel-art exploration game in side view, built entirely with **HTML and CSS** — not a single line of JavaScript.

You wake up in a cave system after a fall, separated from your backpack and its light. Tunnels, ladders and elevators connect the rooms. Find your gear, work through the obstacles, and look for a way out.

<p align="center">
  <img src="docs/title-screen.png" alt="Cavernwake title screen" width="960" />
</p>

## Play

Play it live: [cavernwake.danielluzius.dev](https://cavernwake.danielluzius.dev)

Or open `index.html` in a browser. No install, no build, no server.

- **Move** with the direction pads at the edge of the vision field (walk, climb, ride lifts).
- **Advance dialogue** with *Next* / *Weiter*.
- **Inventory** is the bag in the top-left. Inspect items and use them on barriers.
- **Settings** is the gear in the top-right: hints, language, imprint, restart.
- **Language** (English / Deutsch) can already be chosen on the title screen.

Nothing is stored on a server. No cookies, no tracking. Progress lives only in the open page; a reload starts over.

A modern browser with CSS Grid, Flexbox and `:checked` is enough.

## HTML and CSS only

The whole game is markup and stylesheets:

- Hidden **radios and checkboxes** hold the state (position, intro/outro, inventory, puzzles).
- **Labels** are the clicks (movement, dialogue, items, settings).
- **Sibling selectors** (`:checked`, `~`, `:is()`) switch the camera, sprite, HUD and obstacles.
- **Keyframes** play walk, climb, idle and cutscene cycles.

Ship `index.html`, `css/main.css` and `assets/` — that is the game. Opening the file is enough to play; you do not need the source tree or npm.

## Architecture

Hidden radios and checkboxes sit as siblings **before** `.game`. Labels check them. CSS sibling combinators (`:checked ~`) switch camera, sprite, HUD and obstacles. Source order in `scss/main.scss` is load-bearing: later partials win same-specificity ties (obstacles after player, intro after the position graph, responsive last).

`html/` and `scss/` are the source. `index.html` and `css/main.css` are generated — never edit those two by hand.

## Develop

```bash
npm install
npm run watch:html
npm run watch:css
```

Or one-shot: `npm run build:html` and `npm run build:css`. Sass 1.103+ is the only runtime build dependency. `scripts/extract_positions.py` is a one-off map tool (Pillow); it is not on the npm pipeline.

## What's in it

- Title screen, then an opening cutscene
- A cave graph of **36 stands**, linked by walking, ladders and four elevator shafts
- A lamp vision field around the character (pixel art stays sharp)
- Tools and barriers you pick up and use
- Optional one-shot hint sparks
- An ending once the way out is open

## Layout

```
index.html              generated — play this
css/main.css            generated from scss/
html/                   source markup + partials
scss/                   source styles (Sass modules)
scripts/build_html.js   HTML assembler
assets/
  characters/           character sprite frames
  objects/              inventory icons
  world/                backgrounds, obstacles, UI
  fonts/                Fusion Pixel (SIL Open Font License)
docs/
  title-screen.png
```

## Credits

- Game and pixel art: **Daniel Luzius**
- UI font: [Fusion Pixel](https://takwolf.com) by TakWolf, [SIL OFL 1.1](https://openfontlicense.org)

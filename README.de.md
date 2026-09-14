<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge&color=ffffff" alt="English" /></a>
  <img src="https://img.shields.io/badge/Deutsch-000000?style=for-the-badge&color=ffffff" alt="Deutsch" />
</p>

# Cavernwake

Ein Pixel-Art-Erkundungsspiel in der Seitenansicht, gebaut nur mit **HTML und CSS** — ohne eine Zeile JavaScript.

Du wachst nach einem Sturz in einem Höhlensystem auf, getrennt von deinem Rucksack und deiner Lichtquelle. Gänge, Leitern und Aufzüge verbinden die Räume. Finde deine Ausrüstung, arbeite dich durch die Hindernisse und suche einen Ausweg.

<p align="center">
  <img src="docs/title-screen.png" alt="Cavernwake Title Screen" width="960" />
</p>

## Spielen

`index.html` im Browser öffnen. Keine Installation, kein Build, kein Server.

- **Bewegen** über die Richtungspads am Rand des Sichtfelds (Gehen, Klettern, Aufzüge).
- **Dialoge** mit *Weiter* / *Next* fortschalten.
- **Inventar** ist die Tasche oben links. Gegenstände ansehen und an Hindernissen einsetzen.
- **Einstellungen** ist das Zahnrad oben rechts: Hinweise, Sprache, Impressum, Neustart.
- **Sprache** (Deutsch / English) lässt sich schon auf dem Title Screen wählen.

Es wird nichts auf einem Server gespeichert. Keine Cookies, kein Tracking. Fortschritt lebt nur in der offenen Seite; ein Neuladen setzt zurück.

Ein moderner Browser mit CSS Grid, Flexbox und `:checked` reicht aus.

## Nur HTML und CSS

Das ganze Spiel ist Markup und Stylesheets:

- Versteckte **Radios und Checkboxen** halten den Zustand (Position, Intro/Outro, Inventar, Rätsel).
- **Labels** sind die Klicks (Bewegung, Dialoge, Items, Settings).
- **Geschwister-Selektoren** (`:checked`, `~`, `:is()`) schalten Kamera, Sprite, HUD und Hindernisse.
- **Keyframes** spielen Walk-, Kletter-, Idle- und Cutscene-Zyklen.

`index.html`, `css/main.css` und `assets/` — das ist das Spiel. Die Datei öffnen reicht zum Spielen; Quelle und npm braucht man dafür nicht.

## Architektur

Versteckte Radios und Checkboxen sitzen als Geschwister **vor** `.game`. Labels checken sie. CSS-Geschwister-Selektoren (`:checked ~`) schalten Kamera, Sprite, HUD und Hindernisse. Die Reihenfolge in `scss/main.scss` ist lasttragend: spätere Partials gewinnen bei gleicher Spezifität (Obstacles nach Player, Intro nach dem Positionsgraphen, Responsive zuletzt).

`html/` und `scss/` sind die Quelle. `index.html` und `css/main.css` werden generiert — diese beiden nie per Hand editieren.

## Entwickeln

```bash
npm install
npm run watch:html
npm run watch:css
```

Oder einmalig: `npm run build:html` und `npm run build:css`. Sass 1.103+ ist die einzige Build-Abhängigkeit zur Laufzeit. `scripts/extract_positions.py` ist ein einmaliges Karten-Tool (Pillow) und hängt nicht an der npm-Pipeline.

## Was drinsteckt

- Title Screen, danach die Eröffnungs-Cutscene
- Eine Höhlenkarte aus **36 Standpunkten**, verbunden durch Gehen, Leitern und vier Aufzugschächte
- Ein Lampen-Sichtfeld um den Charakter (Pixel-Art bleibt scharf)
- Werkzeuge und Barrieren, die du aufhebst und einsetzt
- Optionale, einmalige Hinweis-Sparks
- Ein Ende, sobald der Weg hinaus offen ist

## Aufbau

```
index.html              generiert — diese Datei spielen
css/main.css            generiert aus scss/
html/                   Quell-Markup + Partials
scss/                   Quell-Styles (Sass-Module)
scripts/build_html.js   HTML-Assembler
assets/
  characters/           Charakter-Sprite-Frames
  objects/              Inventar-Icons
  world/                Hintergründe, Hindernisse, UI
  fonts/                Fusion Pixel (SIL Open Font License)
docs/
  title-screen.png
```

## Credits

- Spiel und Pixel-Art: **Daniel Luzius**
- UI-Schrift: [Fusion Pixel](https://takwolf.com) von TakWolf, [SIL OFL 1.1](https://openfontlicense.org)

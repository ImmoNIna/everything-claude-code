---
name: nina-reel-style
description: Fester Schnitt- und Layout-Stil fuer Nina Kleins Instagram Reels (Ranking-Videos, Untertitel, Hook, Ranking-Tabelle). Verwenden, wann immer ein Reel fuer Nina geschnitten oder gerendert wird.
---

# Nina Reel Style

Alle Reels von Nina sollen immer gleich aussehen. Diese Werte nicht ohne ausdruecklichen Wunsch aendern.

## When to Use

- Rohvideo aus Google Drive "Videos für Claude" schneiden
- Ranking-Videos (Platz N bis 1) mit Tabelle
- Ausgabe in Google Drive "videos für Nina" (Ordner-ID 1H0We6nzPkjm99OW-85jJ644WNU4o9PTY)

## How It Works

Format: 1080x1920, 30 fps, H.264, AAC 48 kHz, Lautheit -14 LUFS, Tempo 1,1 (Stimme ohne Tonhoehenaenderung).

Schnitt:
- Beste Aufnahme pro Satz waehlen, Wiederholungen, Versprecher, Fuellwoerter und Pausen > 0,28 s raus
- Kalter Einstieg: 2 bis 3 starke Saetze als Teaser
- Bild nach oben verschoben: Grundzoom 1,12 / 1,20 im Wechsel, Straßenname und "Platz X" 1,30; Crop-Y = (ih-1920)*0,85
- Straßenname / Ueberbegriff: Telefonstimme (highpass 350 Hz, lowpass 3200 Hz, Kompressor 8:1)

Schrift: Montserrat Bold ueberall.

Hook (erste 3,2 s): schwarze Schrift 66 px auf weißem Kasten, oben, MarginV 150.

Untertitel: weiß 82 px, schwarze Kontur 7, aktives Wort gelb #FFE600, max. 3 Woerter, unten ausgerichtet mit MarginV 700 (sitzt direkt ueber der Tabelle).

"PLATZ X": gelb 96 px, gleiche Position wie Untertitel.

Ranking-Tabelle (ganzes Video sichtbar, ueber dem Video, kein schwarzer Hintergrund):
- Breite 690 px, zentriert, Zeilenhoehe 58, Abstand 8, Unterkante bei y=1620
- Nummernblock links 70 px, 22 % dunkler als die Balkenfarbe, Ziffer weiß 42 px
- Farben Platz 1 bis 6: #22B55A, #8BCB4A, #F4C63D, #F08A3E, #EE5A28, #B71C1C
- Ecken abgerundet 12 px

Ueberschrift (Straßenname): waehrend der Bewertung groß 112 px, weiß, Kontur 7, bei y=960 zentriert, lange Namen zweizeilig. Bei "Platz X" gleitet der Name einzeilig in 0,55 s in seinen Balken und bleibt dort bis zum Ende.

## Examples

Referenz: "Ranking lauteste Straßen Hamburg v4" im Ordner "videos für Nina".

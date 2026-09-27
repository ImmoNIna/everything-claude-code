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
- Gesicht in jedem Schnitt gleich positioniert: Gesichtserkennung (OpenCV YuNet) pro Schnitt, Ausschnitt so, dass die Gesichtsmitte bei x=540, y=600 liegt
- Zoom pro Schnitt: Grundzoom 1,00 / 1,08 im Wechsel, Straßenname und "Platz X" 1,15; hoeher nur falls noetig, damit das Gesicht auf y=600 kommt (Mindestzoom 1320/(1920-Gesicht_y)), maximal 1,15
- Pruefung vor Upload: Gesichtskasten in jedem Schnitt vollstaendig im Bild, oben mindestens 150 px Abstand
- Straßenname / Ueberbegriff: Telefonstimme (highpass 350 Hz, lowpass 3200 Hz, Kompressor 8:1)

Schrift: Montserrat Bold ueberall.

Hook (erste 3,2 s): schwarze Schrift 66 px auf weißem Kasten, oben, MarginV 150.

Untertitel: weiß 82 px, schwarze Kontur 7, aktives Wort gelb #FFE600, max. 3 Woerter, unten ausgerichtet mit MarginV 870 (Unterkante y=1050, zwischen Gesicht und Straßennamen).

"PLATZ X": gelb 96 px, Großbuchstaben, gleiche Position wie Untertitel.

Ranking-Tabelle (ganzes Video sichtbar, ueber dem Video, kein schwarzer Hintergrund):
- Breite 600 px, zentriert, Zeilenhoehe 78, Abstand 8, Unterkante bei y=1680 (Oberkante y=1172)
- Nummernblock links 80 px, 22 % dunkler als die Balkenfarbe, Ziffer weiß 56 px
- Straßenname im Balken: weiß 46 px, Kontur 3, normale Groß-/Kleinschreibung, zentriert im Farbbereich, bei langen Namen nur horizontal gestaucht
- Farben Platz 1 bis 6: #22B55A, #8BCB4A, #F4C63D, #F08A3E, #EE5A28, #B71C1C
- Ecken abgerundet 12 px

Ueberschrift (Straßenname): waehrend der Bewertung schwarze Schrift 72 px auf weißem Kasten (hebt sich von den Untertiteln ab), einzeilig, bei y=1112 zentriert direkt ueber der Tabelle, normale Groß-/Kleinschreibung. Bei "Platz X" wird daraus weiße Schrift, die in 0,55 s einzeilig in ihren Balken gleitet und dort bis zum Ende bleibt.

## Examples

Referenz: "Ranking lauteste Straßen Hamburg v6" im Ordner "videos für Nina".

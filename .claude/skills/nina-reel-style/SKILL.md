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
- Straßenname im Balken: weiß 56 px (ca. 11 px Luft oben/unten), Kontur 3, normale Groß-/Kleinschreibung, zentriert im Farbbereich, bei langen Namen nur horizontal gestaucht
- Farben Platz 1 bis 6: #B71C1C (dunkelrot), #EE5A28, #F08A3E, #F4C63D, #8BCB4A, #22B55A (gruen)
- Ecken abgerundet 12 px

Ueberschrift (Straßenname): waehrend der Bewertung schwarze Schrift 72 px auf weißem Kasten (hebt sich von den Untertiteln ab), einzeilig, bei y=1112 zentriert direkt ueber der Tabelle, normale Groß-/Kleinschreibung. Bei "Platz X" wird daraus weiße Schrift, die in 0,55 s einzeilig in ihren Balken gleitet und dort bis zum Ende bleibt.

## Ablauf (Skripte in scripts/, Composio Sandbox: 1 CPU, 1 GB RAM)

1. Rohvideo per Composio GOOGLEDRIVE_DOWNLOAD_FILE holen (s3url), in ~/work/raw.mp4 laden (Ordner per Bash anlegen, nicht per Workbench: die laeuft als root)
2. Transkript mit Wort-Zeitstempeln: Rohvideo per opusclip_create_upload_link zu OpusClip, submit_project (skipSlicing), opusclip_get_transcript
3. projects/<name>.json anlegen: words, plan (t/n/p Abschnitte, beste Takes), fix, hook, places
4. Skripte per raw.githubusercontent.com vom Branch holen, `bash setup.sh`, `python3 build.py`, `python3 faces.py`, `python3 render.py`, `bash finish.sh` (lange Schritte mit nohup im Hintergrund; jeder Aufruf unter 60 s halten, sonst wird die Sandbox zurueckgesetzt und alle Dateien sind weg)
5. final.mp4 per upload_local_file + GOOGLEDRIVE_RESUMABLE_UPLOAD in "videos für Nina"

## Examples

Referenz: "Ranking lauteste Straßen Hamburg v7" im Ordner "videos für Nina".

# 🧮 rechnify.at

Kostenlose Online-Rechner für Österreich & Deutschland. Über 50 Präzisionsrechner für Finanzen, Steuern, Arbeitszeit, Familie und Alltag. Alle Berechnungen laufen lokal im Browser – 100 % Datenschutz.

## 🌐 Live

**URL:** <https://rechnify.at>

## ✨ Features

- 📊 **Über 50 Rechner** – Brutto-Netto, Überstunden, MwSt, Krypto-Steuern, Pensionsrechner, ETF-Sparplan, Kreditrechner und mehr
- 🇦🇹🇩🇪 **Zwei Länder** – Vollständige Unterstützung für Österreich und Deutschland mit korrekten Steuersätzen 2026
- 🔒 **100 % Datenschutz** – Alle Berechnungen erfolgen lokal im Browser, keine Datenweitergabe
- ⚡ **Live-Berechnung** – Ergebnisse aktualisieren sich beim Tippen (kein Button-Klick nötig)
- 📱 **PWA** – Installierbar als App, funktioniert offline
- 🎨 **Modernes Design** – Space Grotesk + Inter, Cobalt-Akzent, Dark Mode
- 📝 **Blog & Ratgeber** – Steuer-Tipps, Gehaltsverhandlung, Mindestlohn-Updates

## 🛠️ Technologie-Stack

- **Frontend:** HTML5, CSS3 (Custom Properties / OKLCH), Vanilla JavaScript
- **Hosting:** Firebase Hosting
- **Fonts:** Google Fonts (Space Grotesk, Inter)
- **Monetarisierung:** Google AdSense
- **Deployment:** `firebase deploy`

## 📁 Projektstruktur

```
rechnify.at/
├── index.html              # Homepage (Bento Grid)
├── finanzen/               # Finanz-Rechner (AT)
│   ├── gehaltsrechner.html # Brutto-Netto AT (Flagship)
│   ├── brutto-netto/       # pSEO-Hub (Brutto→Netto Beträge)
│   └── ...
├── de/                     # Deutschland-Version
│   └── finanzen/
│       └── ...
├── arbeitszeit/            # Arbeitszeit-Rechner
├── familie/                # Familien-Rechner
├── alltag/                 # Alltag & Gesundheit
├── mathematik/             # Mathematik
├── blog/                   # Ratgeber-Artikel
├── assets/
│   ├── css/                # Global, Premium, UX-Enhancements
│   ├── js/                 # Core, UI, Tools, Analytics
│   └── images/             # Logos, OG-Images, Favicons
├── tokens.css              # Design-Tokens (OKLCH)
├── firebase.json           # Firebase Hosting Config
├── sitemap.xml             # Sitemap (218 URLs)
└── robots.txt              # Crawl-Regeln
```

## 🚀 Erste Schritte

### Voraussetzungen

- Node.js (für optionale Build-Scripts)
- Firebase CLI (`npm install -g firebase-tools`)

### Lokal starten

```bash
# Repository klonen
git clone https://github.com/bayrakf/rechnify-at.git
cd rechnify-at

# Lokalen Server starten
python3 -m http.server 8000
# oder
npx serve .

# Im Browser öffnen
http://localhost:8000
```

### Deployen

```bash
firebase login
firebase deploy
```

## 📊 Rechner-Kategorien

| Kategorie | Anzahl | Beispiele |
| ----------- | -------- | ----------- |
| 💶 Finanzen & Steuern | 20+ | Gehaltsrechner, MwSt, Krypto-Steuer, Pensionsrechner, Kreditrechner |
| ⏰ Arbeitszeit | 10+ | Überstunden, Stundenlohn, Urlaubstage, Schichtplan, Brückentage |
| 👶 Familie | 4 | Kinderbetreuungsgeld, Elterngeld, Schwangerschaft, Studienbeitrag |
| 📐 Mathematik | 3 | Prozentrechner, Dreisatz, Taschenrechner |
| ⚖️ Alltag & Gesundheit | 8+ | BMI, Kalorien, Stromkosten, Währungsumrechner, Schulnoten |

## 📝 Lizenz

MIT-Lizenz

## 👤 Autor

[bayrakf](https://github.com/bayrakf)

## 📧 Kontakt

- Website: <https://rechnify.at/kontakt.html>
- GitHub Issues: <https://github.com/bayrakf/rechnify-at/issues>

---

**Hinweis:** Alle Rechner sind für Österreich und Deutschland optimiert. Steuerwerte Stand 2026.

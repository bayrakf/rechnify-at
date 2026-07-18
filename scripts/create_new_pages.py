#!/usr/bin/env python3
"""Create new pages: Währungsumrechner, Arbeitszeit Hub, Embed page, PWA prompt."""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# 1. WÄHRUNGSUMRECHNER
waehrung = '''<!DOCTYPE html>
<html lang="de-AT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Währungsumrechner – Live Wechselkurse | rechnify.at</title>
  <meta name="description" content="Kostenloser Währungsumrechner: EUR, USD, CHF, GBP und mehr. Live-Kurse, einfach Betrag eingeben und umrechnen. Lokal im Browser." />
  <link rel="canonical" href="https://rechnify.at/alltag/waehrungsumrechner.html" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="alternate" hreflang="de-AT" href="https://rechnify.at/alltag/waehrungsumrechner.html" />
  <link rel="alternate" hreflang="x-default" href="https://rechnify.at/alltag/waehrungsumrechner.html" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Währungsumrechner – Live Wechselkurse | rechnify.at" />
  <meta property="og:description" content="Kostenloser Währungsumrechner: EUR, USD, CHF, GBP und mehr." />
  <meta property="og:url" content="https://rechnify.at/alltag/waehrungsumrechner.html" />
  <meta property="og:image" content="https://rechnify.at/assets/images/og-share.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="og:locale" content="de_AT" />
  <meta property="og:site_name" content="rechnify.at" />
  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" /></noscript>
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="/assets/css/global.css?v=3.1" /></noscript>
  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Währungsumrechner", "operatingSystem": "All", "applicationCategory": "FinanceApplication", "offers": { "@type": "Offer", "price": "0.00", "priceCurrency": "EUR" } }
  </script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="rechnify.at">
        <picture><source srcset="/assets/images/logo-72.webp" type="image/webp" /><img src="/assets/images/logo-72.jpg" alt="rechnify Logo" width="36" height="36" decoding="async" /></picture>
        <span class="site-logo-text">rechnify<span>.at</span></span>
      </a>
      <nav class="site-nav" id="siteNav">
        <a href="/">🏠 Start</a>
        <a href="/#finanzen">💶 Finanzen</a>
        <a href="/#arbeitszeit">⏰ Arbeitszeit</a>
        <a href="/#familie">👶 Familie</a>
        <a href="/#mathematik">📐 Mathematik</a>
        <a href="/#alltag">⚖️ Alltag</a>
      </nav>
      <div class="header-actions">
        <button class="btn-icon" id="darkModeToggle" aria-label="Dunkelmodus" type="button">🌙</button>
      </div>
    </div>
  </header>
  <nav class="breadcrumb" aria-label="Brotkrumen">
    <a href="/">Start</a><span class="breadcrumb-sep">/</span>
    <a href="/#alltag">Alltag</a><span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-current">Währungsumrechner</span>
  </nav>
  <main class="site-main">
    <div class="calculator-container">
      <div class="calculator-card">
        <div class="calc-header">
          <div class="calc-icon">💱</div>
          <h1 style="margin-bottom:8px;">Währungsumrechner</h1>
          <p>Rechne Beträge zwischen Währungen um. Live-Kurse von der Europäischen Zentralbank.</p>
        </div>
        <div class="calc-body">
          <div class="input-group">
            <label for="amount">Betrag</label>
            <div class="input-suffix">
              <input type="number" id="amount" value="100" min="0" step="0.01">
              <span class="suffix" id="fromCurrency">EUR</span>
            </div>
          </div>
          <div class="input-group">
            <label for="from">Von</label>
            <select id="from">
              <option value="EUR" selected>EUR – Euro</option>
              <option value="USD">USD – US-Dollar</option>
              <option value="CHF">CHF – Schweizer Franken</option>
              <option value="GBP">GBP – Britisches Pfund</option>
              <option value="JPY">JPY – Japanischer Yen</option>
              <option value="CNY">CNY – Chinesischer Yuan</option>
              <option value="CAD">CAD – Kanadischer Dollar</option>
              <option value="AUD">AUD – Australischer Dollar</option>
              <option value="SEK">SEK – Schwedische Krone</option>
              <option value="NOK">NOK – Norwegische Krone</option>
              <option value="DKK">DKK – Dänische Krone</option>
              <option value="PLN">PLN – Polnischer Zloty</option>
              <option value="CZK">CZK – Tschechische Krone</option>
              <option value="HUF">HUF – Ungarischer Forint</option>
              <option value="TRY">TRY – Türkische Lira</option>
            </select>
          </div>
          <div class="input-group">
            <label for="to">Nach</label>
            <select id="to">
              <option value="EUR">EUR – Euro</option>
              <option value="USD" selected>USD – US-Dollar</option>
              <option value="CHF">CHF – Schweizer Franken</option>
              <option value="GBP">GBP – Britisches Pfund</option>
              <option value="JPY">JPY – Japanischer Yen</option>
              <option value="CNY">CNY – Chinesischer Yuan</option>
              <option value="CAD">CAD – Kanadischer Dollar</option>
              <option value="AUD">AUD – Australischer Dollar</option>
              <option value="SEK">SEK – Schwedische Krone</option>
              <option value="NOK">NOK – Norwegische Krone</option>
              <option value="DKK">DKK – Dänische Krone</option>
              <option value="PLN">PLN – Polnischer Zloty</option>
              <option value="CZK">CZK – Tschechische Krone</option>
              <option value="HUF">HUF – Ungarischer Forint</option>
              <option value="TRY">TRY – Türkische Lira</option>
            </select>
          </div>
          <button class="btn" id="calculate" style="width: 100%; margin-top: 10px;">Umrechnen</button>
          <div id="result" class="result-box hidden">
            <h3>Ergebnis</h3>
            <div class="result-grid">
              <div class="result-card">
                <div class="text-sm text-muted">Umgerechnet</div>
                <div class="big-number text-success" id="resConverted">--</div>
                <div class="sub-number" id="resRate">--</div>
              </div>
            </div>
            <div style="margin-top: 16px; font-size: 12px; color: var(--text-muted);" id="resUpdated">Kurse werden geladen...</div>
          </div>
        </div>
        <div class="help">
          <strong>Wie wird berechnet?</strong><br />
          Kurse von der Europäischen Zentralbank (EZB). Werden täglich aktualisiert. Lokal im Browser berechnet — keine Datenweitergabe.
        </div>
      </div>
      <section class="content-section" style="margin-top: 32px;">
        <h2>Wie funktioniert der Währungsumrechner?</h2>
        <p>Unser Währungsumrechner verwendet die offiziellen Wechselkurse der <strong>Europäischen Zentralbank (EZB)</strong>. Diese werden jeden Werktag um 16:00 Uhr MEZ aktualisiert.</p>
        <h3>Unterstützte Währungen</h3>
        <p>Der Rechner unterstützt 15 wichtige Währungen: Euro (EUR), US-Dollar (USD), Schweizer Franken (CHF), Britisches Pfund (GBP), Japanischer Yen (JPY), Chinesischer Yuan (CNY) und viele mehr.</p>
        <h3>Tipps für Reisende</h3>
        <ul>
          <li><strong>Vor der Reise umrechnen:</strong> So weißt du, wie viel Budget dir im Zielland zur Verfügung steht</li>
          <li><strong>Karten-Gebühren:</strong> Viele Banken verlangen 1-2% Auslandseinsatzgebühr</li>
          <li><strong>Bargeld vs. Karte:</strong> Karten haben oft bessere Kurse als Wechselstuben am Flughafen</li>
        </ul>
      </section>
    </div>
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="site-logo-text">rechnify<span>.at</span></span>
          <p>Kostenlose Online-Rechner für Österreich & Deutschland.</p>
        </div>
        <div class="footer-col">
          <h3>Alltag</h3>
          <ul>
            <li><a href="/alltag/waehrungsumrechner.html">Währungsumrechner</a></li>
            <li><a href="/alltag/kalorienrechner.html">Kalorienrechner</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>Info</h3>
          <ul>
            <li><a href="/ueber-uns.html">Über uns</a></li>
            <li><a href="/kontakt.html">Kontakt</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
  <script src="/assets/js/global.js?v=3.1"></script>
  <script>
    'use strict';
    let rates = {};
    let lastUpdate = '';
    async function loadRates() {
      try {
        const res = await fetch('https://api.frankfurter.app/latest?from=EUR');
        const data = await res.json();
        rates = data.rates;
        rates['EUR'] = 1;
        lastUpdate = data.date;
        document.getElementById('resUpdated').textContent = 'Kurse vom ' + lastUpdate + ' (EZB)';
      } catch(e) {
        rates = {EUR:1, USD:1.08, CHF:0.95, GBP:0.85, JPY:162, CNY:7.8, CAD:1.47, AUD:1.65, SEK:11.4, NOK:11.7, DKK:7.46, PLN:4.3, CZK:25.2, HUF:385, TRY:34.5};
        lastUpdate = 'geschätzt';
        document.getElementById('resUpdated').textContent = 'Kurse: ' + lastUpdate + ' (Fallback)';
      }
    }
    function convert() {
      const amount = parseFloat(document.getElementById('amount').value) || 0;
      const from = document.getElementById('from').value;
      const to = document.getElementById('to').value;
      if (Object.keys(rates).length === 0) return;
      const inEUR = from === 'EUR' ? amount : amount / rates[from];
      const result = to === 'EUR' ? inEUR : inEUR * rates[to];
      const rate = to === 'EUR' ? 1/rates[from] : (from === 'EUR' ? rates[to] : rates[to] / rates[from]);
      document.getElementById('resConverted').textContent = result.toLocaleString('de-AT', {minimumFractionDigits:2, maximumFractionDigits:2}) + ' ' + to;
      document.getElementById('resRate').textContent = '1 ' + from + ' = ' + rate.toFixed(4) + ' ' + to;
      document.getElementById('fromCurrency').textContent = from;
      document.getElementById('result').classList.remove('hidden');
    }
    document.getElementById('calculate').addEventListener('click', convert);
    document.getElementById('from').addEventListener('change', () => { document.getElementById('fromCurrency').textContent = document.getElementById('from').value; });
    document.getElementById('to').addEventListener('change', convert);
    document.getElementById('amount').addEventListener('input', convert);
    loadRates().then(() => { convert(); });
  </script>
</body>
</html>'''
(BASE / "alltag" / "waehrungsumrechner.html").write_text(waehrung, encoding='utf-8')
print("Created: waehrungsumrechner.html")

# 2. ARBEITSZEIT HUB
arbeitszeit = '''<!DOCTYPE html>
<html lang="de-AT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Arbeitszeit & Personal Rechner Österreich 2026 | rechnify.at</title>
  <meta name="description" content="Kostenlose Arbeitszeitrechner: Überstunden, Urlaubstage, Stundenlohn, Teilzeit, Brückentage und mehr. Für Österreich und Deutschland." />
  <link rel="canonical" href="https://rechnify.at/arbeitszeit/" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="alternate" hreflang="de-AT" href="https://rechnify.at/arbeitszeit/" />
  <link rel="alternate" hreflang="x-default" href="https://rechnify.at/arbeitszeit/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Arbeitszeit & Personal Rechner Österreich 2026 | rechnify.at" />
  <meta property="og:description" content="Kostenlose Arbeitszeitrechner: Überstunden, Urlaubstage, Stundenlohn und mehr." />
  <meta property="og:url" content="https://rechnify.at/arbeitszeit/" />
  <meta property="og:image" content="https://rechnify.at/assets/images/og-share.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="og:locale" content="de_AT" />
  <meta property="og:site_name" content="rechnify.at" />
  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" /></noscript>
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="/assets/css/global.css?v=3.1" /></noscript>
  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "CollectionPage", "name": "Arbeitszeit & Personal Rechner Österreich 2026", "url": "https://rechnify.at/arbeitszeit/", "description": "Kostenlose Arbeitszeitrechner für Österreich und Deutschland.", "isPartOf": { "@type": "WebSite", "name": "rechnify.at", "url": "https://rechnify.at/" } }
  </script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="rechnify.at">
        <picture><source srcset="/assets/images/logo-72.webp" type="image/webp" /><img src="/assets/images/logo-72.jpg" alt="rechnify Logo" width="36" height="36" decoding="async" /></picture>
        <span class="site-logo-text">rechnify<span>.at</span></span>
      </a>
      <nav class="site-nav" id="siteNav">
        <a href="/">🏠 Start</a>
        <a href="/#finanzen">💶 Finanzen</a>
        <a href="/#arbeitszeit">⏰ Arbeitszeit</a>
        <a href="/#familie">👶 Familie</a>
        <a href="/#mathematik">📐 Mathematik</a>
        <a href="/#alltag">⚖️ Alltag</a>
      </nav>
      <div class="header-actions">
        <button class="btn-icon" id="darkModeToggle" aria-label="Dunkelmodus" type="button">🌙</button>
      </div>
    </div>
  </header>
  <nav class="breadcrumb" aria-label="Brotkrumen">
    <a href="/">Start</a><span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-current">Arbeitszeit</span>
  </nav>
  <main class="site-main">
    <article class="content-section">
      <h1>Arbeitszeit & Personal Rechner Österreich 2026</h1>
      <p class="subtitle">Kostenlose Arbeitszeitrechner für Österreich und Deutschland. Alle Berechnungen laufen lokal in deinem Browser — keine Datenweitergabe, 100% Datenschutz.</p>
      <h2>Zeiterfassung & Überstunden</h2>
      <p>Erfasse deine Arbeitszeit, berechne Überstunden mit Zuschlägen oder plane deine Schichten. Unsere Rechner berücksichtigen Pausen, gesetzliche Ruhezeiten und tarifliche Zuschlagssätze.</p>
      <ul class="hub-list">
        <li><a href="/arbeitszeit/kommen-gehen-rechner.html">Kommen-Gehen Rechner</a></li>
        <li><a href="/arbeitszeit/ueberstundenrechner.html">Überstundenrechner</a></li>
        <li><a href="/arbeitszeit/ueberstunden-auszahlen-oesterreich.html">Überstunden auszahlen Österreich</a></li>
        <li><a href="/arbeitszeit/schichtplan-rechner.html">Schichtplan-Rechner</a></li>
      </ul>
      <h2>Gehalt & Lohn</h2>
      <p>Berechne deinen Stundenlohn, vergleiche Teilzeit-Varianten oder prüfe, wie sich eine Gehaltserhöhung auswirkt.</p>
      <ul class="hub-list">
        <li><a href="/arbeitszeit/stundenlohn-rechner.html">Stundenlohnrechner AT</a></li>
        <li><a href="/de/arbeitszeit/stundenlohn-rechner.html">Stundenlohnrechner DE</a></li>
        <li><a href="/arbeitszeit/teilzeitrechner.html">Teilzeitrechner</a></li>
      </ul>
      <h2>Urlaub & Feiertage</h2>
      <p>Plane deinen Urlaub optimal: Berechne deinen Urlaubsanspruch, finde die besten Brückentage-Kombinationen.</p>
      <ul class="hub-list">
        <li><a href="/arbeitszeit/urlaubstage-rechner.html">Urlaubstage-Rechner</a></li>
        <li><a href="/arbeitszeit/brueckentage-planer.html">Brückentage-Planer</a></li>
        <li><a href="/arbeitszeit/arbeitstage-rechner.html">Arbeitstage-Rechner</a></li>
      </ul>
      <h2>Warum rechnify.at für Arbeitszeit?</h2>
      <ul>
        <li><strong>100% kostenlos</strong> — keine Registrierung</li>
        <li><strong>Datenschutz zuerst</strong> — alle Berechnungen lokal im Browser</li>
        <li><strong>AT & DE</strong> — beide Arbeitsrechtssysteme</li>
        <li><strong>Aktuell 2026</strong> — gesetzliche Regelungen berücksichtigt</li>
      </ul>
      <p class="help" style="margin-top:24px;">Alle Berechnungen sind Orientierungswerte und ersetzen keine Rechtsberatung. Stand: 2026.</p>
    </article>
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="site-logo-text">rechnify<span>.at</span></span>
          <p>Kostenlose Online-Rechner für Österreich & Deutschland.</p>
        </div>
        <div class="footer-col">
          <h3>Arbeitszeit</h3>
          <ul>
            <li><a href="/arbeitszeit/kommen-gehen-rechner.html">Kommen-Gehen</a></li>
            <li><a href="/arbeitszeit/ueberstundenrechner.html">Überstunden</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>Info</h3>
          <ul>
            <li><a href="/ueber-uns.html">Über uns</a></li>
            <li><a href="/kontakt.html">Kontakt</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
  <script src="/assets/js/global.js?v=3.1"></script>
</body>
</html>'''
(BASE / "arbeitszeit" / "index.html").write_text(arbeitszeit, encoding='utf-8')
print("Created: arbeitszeit/index.html")

# 3. EMBED PAGE
embed = '''<!DOCTYPE html>
<html lang="de-AT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Rechner einbinden – Kostenlos für deine Website | rechnify.at</title>
  <meta name="description" content="Binde rechnify.at Rechner kostenlos auf deiner Website ein: iframe-Embed, Widget. Für HR-Blogs, Steuerberater, Personalvermittler." />
  <link rel="canonical" href="https://rechnify.at/embed.html" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="alternate" hreflang="de-AT" href="https://rechnify.at/embed.html" />
  <link rel="alternate" hreflang="x-default" href="https://rechnify.at/embed.html" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Rechner einbinden – Kostenlos für deine Website | rechnify.at" />
  <meta property="og:description" content="Binde rechnify.at Rechner kostenlos auf deiner Website ein." />
  <meta property="og:url" content="https://rechnify.at/embed.html" />
  <meta property="og:image" content="https://rechnify.at/assets/images/og-share.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="og:locale" content="de_AT" />
  <meta property="og:site_name" content="rechnify.at" />
  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" /></noscript>
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="/assets/css/global.css?v=3.1" /></noscript>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="rechnify.at">
        <picture><source srcset="/assets/images/logo-72.webp" type="image/webp" /><img src="/assets/images/logo-72.jpg" alt="rechnify Logo" width="36" height="36" decoding="async" /></picture>
        <span class="site-logo-text">rechnify<span>.at</span></span>
      </a>
      <nav class="site-nav" id="siteNav">
        <a href="/">🏠 Start</a>
        <a href="/#finanzen">💶 Finanzen</a>
        <a href="/#arbeitszeit">⏰ Arbeitszeit</a>
        <a href="/#familie">👶 Familie</a>
        <a href="/#mathematik">📐 Mathematik</a>
        <a href="/#alltag">⚖️ Alltag</a>
      </nav>
      <div class="header-actions">
        <button class="btn-icon" id="darkModeToggle" aria-label="Dunkelmodus" type="button">🌙</button>
      </div>
    </div>
  </header>
  <nav class="breadcrumb" aria-label="Brotkrumen">
    <a href="/">Start</a><span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-current">Rechner einbinden</span>
  </nav>
  <main class="site-main">
    <article class="content-section">
      <h1>Rechner kostenlos auf deiner Website einbinden</h1>
      <p class="subtitle">Binde jeden rechnify.at-Rechner kostenlos per iframe auf deiner Website ein. Perfekt für HR-Blogs, Steuerberater, Personalvermittler und Finanz-Websites.</p>
      <h2>So funktioniert's</h2>
      <p>Kopiere einfach den iframe-Code des gewünschten Rechners und füge ihn in deine Website ein. Der Rechner läuft komplett auf rechnify.at — du brauchst kein Backend, keine Wartung, keine Updates.</p>
      <h2>Verfügbare Rechner zum Einbinden</h2>
      <p>Alle Rechner können mit dem Parameter <code>?widget=true</code> eingebunden werden. Beispiele:</p>
      <h3>Brutto-Netto Gehaltsrechner</h3>
      <textarea readonly style="width:100%;height:80px;font-family:monospace;font-size:12px;padding:12px;border-radius:6px;border:1px solid var(--border);resize:none;" onclick="this.select()"><iframe src="https://rechnify.at/finanzen/gehaltsrechner.html?widget=true" width="100%" height="600" style="border:none; border-radius:12px;"></iframe></textarea>
      <h3>MwSt-Rechner</h3>
      <textarea readonly style="width:100%;height:80px;font-family:monospace;font-size:12px;padding:12px;border-radius:6px;border:1px solid var(--border);resize:none;" onclick="this.select()"><iframe src="https://rechnify.at/finanzen/mwst-rechner.html?widget=true" width="100%" height="500" style="border:none; border-radius:12px;"></iframe></textarea>
      <h3>Überstundenrechner</h3>
      <textarea readonly style="width:100%;height:80px;font-family:monospace;font-size:12px;padding:12px;border-radius:6px;border:1px solid var(--border);resize:none;" onclick="this.select()"><iframe src="https://rechnify.at/arbeitszeit/ueberstundenrechner.html?widget=true" width="100%" height="600" style="border:none; border-radius:12px;"></iframe></textarea>
      <h3>Kalorienrechner</h3>
      <textarea readonly style="width:100%;height:80px;font-family:monospace;font-size:12px;padding:12px;border-radius:6px;border:1px solid var(--border);resize:none;" onclick="this.select()"><iframe src="https://rechnify.at/alltag/kalorienrechner.html?widget=true" width="100%" height="600" style="border:none; border-radius:12px;"></iframe></textarea>
      <h2>Vorteile für Website-Betreiber</h2>
      <ul>
        <li><strong>100% kostenlos</strong> — keine Kosten, keine Anmeldung</li>
        <li><strong>Kein Backend nötig</strong> — iframe reicht, alles läuft auf rechnify.at</li>
        <li><strong>Keine Wartung</strong> — Updates und neue Features automatisch</li>
        <li><strong>Keine Daten</strong> — alle Berechnungen im Browser, DSGVO-konform</li>
        <li><strong>Branding-frei</strong> — Rechner sind werbefrei im Widget-Modus</li>
        <li><strong>Mobil-optimiert</strong> — funktioniert auf allen Geräten</li>
      </ul>
      <h2>Für wen geeignet?</h2>
      <ul>
        <li><strong>HR-Blogs & Personal-Websites</strong> — Gehaltsrechner für Bewerber</li>
        <li><strong>Steuerberater</strong> — MwSt- und Steuerrechner für Mandanten</li>
        <li><strong>Personalvermittler</strong> — Stundenlohn- und Gehaltsrechner</li>
        <li><strong>Finanz-Blogs</strong> — Kredit-, Zins- und ETF-Rechner</li>
        <li><strong>Gewerkschaften</strong> — Überstunden- und Urlaubsrechner</li>
        <li><strong>Unternehmen</strong> — Sachbezugs- und Pendlerrechner für Mitarbeiter</li>
      </ul>
      <h2>Partner werden</h2>
      <p>Bist du an einer Partnerschaft interessiert? Wir bieten:</p>
      <ul>
        <li>Custom-Branding (dein Logo im Rechner)</li>
        <li>White-Label-Lösungen (eigene Domain)</li>
        <li>Affiliate-Programm für Finanz-Produkte</li>
        <li>API-Zugriff für eigene Apps</li>
      </ul>
      <p><a href="/kontakt.html" class="btn" style="display:inline-block;margin-top:16px;">Kontakt aufnehmen →</a></p>
      <p class="help" style="margin-top:24px;">Die Einbindung ist kostenlos. Bei hoher Traffic-Belastung behalten wir uns vor, Widget-Zugriffe zu limitieren.</p>
    </article>
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="site-logo-text">rechnify<span>.at</span></span>
          <p>Kostenlose Online-Rechner für Österreich & Deutschland.</p>
        </div>
        <div class="footer-col">
          <h3>Info</h3>
          <ul>
            <li><a href="/embed.html">Rechner einbinden</a></li>
            <li><a href="/ueber-uns.html">Über uns</a></li>
            <li><a href="/kontakt.html">Kontakt</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
  <script src="/assets/js/global.js?v=3.1"></script>
</body>
</html>'''
(BASE / "embed.html").write_text(embed, encoding='utf-8')
print("Created: embed.html")

# 4. PWA INSTALL PROMPT in global.js
with open(BASE / "assets" / "js" / "global.js", 'r') as f:
    js = f.read()

pwa_code = """

// --- PWA Install Prompt ---
let deferredPrompt = null;
function initPWAInstall() {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (localStorage.getItem('rechnify.pwaDismissed') === '1') return;
    setTimeout(showPWAInstallBanner, 3000);
  });
  window.addEventListener('appinstalled', () => {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) banner.remove();
    deferredPrompt = null;
  });
}
function showPWAInstallBanner() {
  if (document.getElementById('pwa-install-banner')) return;
  if (window.matchMedia('(display-mode: standalone)').matches) return;
  const banner = document.createElement('div');
  banner.id = 'pwa-install-banner';
  banner.style.cssText = 'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:300;background:var(--color-accent);color:var(--color-accent-ink);padding:12px 20px;border-radius:var(--radius-pill);box-shadow:var(--shadow-lg);display:flex;align-items:center;gap:12px;max-width:90vw;font-size:14px;font-family:var(--font-display);font-weight:600;';
  banner.innerHTML = '<span>📱 rechnify.at installieren</span>';
  const installBtn = document.createElement('button');
  installBtn.textContent = 'Installieren';
  installBtn.style.cssText = 'background:rgba(255,255,255,0.2);border:none;color:inherit;padding:6px 14px;border-radius:var(--radius-pill);cursor:pointer;font-weight:700;font-size:13px;';
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === 'dismissed') localStorage.setItem('rechnify.pwaDismissed', '1');
    deferredPrompt = null;
    banner.remove();
  });
  banner.appendChild(installBtn);
  const closeBtn = document.createElement('button');
  closeBtn.textContent = '✕';
  closeBtn.style.cssText = 'background:none;border:none;color:inherit;cursor:pointer;font-size:18px;opacity:0.7;';
  closeBtn.addEventListener('click', () => {
    localStorage.setItem('rechnify.pwaDismissed', '1');
    banner.remove();
  });
  banner.appendChild(closeBtn);
  document.body.appendChild(banner);
  setTimeout(() => { if (banner.parentNode) banner.remove(); }, 15000);
}
"""

if 'initPWAInstall' not in js:
    js = js.rstrip() + '\n' + pwa_code + '\n'
    js = js.replace('registerServiceWorker();', 'registerServiceWorker();\n  initPWAInstall();')
    with open(BASE / "assets" / "js" / "global.js", 'w') as f:
        f.write(js)
    print("Updated: global.js with PWA install prompt")

print("All pages created!")
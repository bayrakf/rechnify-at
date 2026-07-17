import os

def create_arbeitstage_rechner():
    template = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Arbeitstage-Rechner {COUNTRY_NAME} – Werktage berechnen | rechnify.at</title>
  <meta name="description" content="Berechne die genauen Arbeitstage für deinen Zeitraum in {COUNTRY_NAME}. Zieht Wochenenden und gesetzliche Feiertage automatisch ab." />
  <link rel="canonical" href="https://rechnify.at/{PATH_PREFIX}arbeitszeit/arbeitstage-rechner.html" />
  {ALT_LINKS}

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5052220565736445" crossorigin="anonymous"></script>

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="Arbeitstage-Rechner {COUNTRY_NAME} | rechnify.at" />
  <meta property="og:description" content="Werktage und Arbeitstage inkl. Feiertage berechnen." />
  <meta property="og:url" content="https://rechnify.at/{PATH_PREFIX}arbeitszeit/arbeitstage-rechner.html" />
  <meta property="og:image" content="https://rechnify.at/assets/images/favicon-512x512.png" />
  <meta property="og:locale" content="{LOCALE}" />
  <meta property="og:site_name" content="rechnify.at" />

  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="512x512" href="/assets/images/favicon-512x512.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/tokens.css" />
  <link rel="stylesheet" href="/assets/css/global.css" />

  <style>
    .calc-body { padding: 24px; }
    .input-group { margin-bottom: 20px; }
    .input-group label { display: block; margin-bottom: 8px; font-weight: bold; color: var(--color-ink); }
    .input-group input, .input-group select { 
      width: 100%; 
      padding: 12px; 
      border: 1px solid var(--color-rule); 
      border-radius: 10px; 
      background: var(--color-paper); 
      color: var(--color-ink); 
      font-size: 16px; 
    }
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    @media(max-width: 600px) { .input-row { grid-template-columns: 1fr; } }

    .result-box { 
      margin-top: 24px; 
      background: var(--color-paper-2); 
      border: 1px solid var(--color-rule); 
      border-radius: 12px; 
      padding: 24px; 
    }
    
    .result-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid var(--color-rule);
    }
    .result-item:last-child { border-bottom: none; padding-bottom: 0; }
    .result-item.highlight { font-weight: bold; font-size: 1.4em; color: var(--color-primary); border-bottom: none; }
    .result-item.muted { color: var(--color-ink-3); font-size: 0.9em; }
    
    .holiday-list {
        margin-top: 16px;
        font-size: 0.9rem;
        color: var(--color-ink-2);
        background: var(--color-paper);
        padding: 12px;
        border-radius: 8px;
        border: 1px solid var(--color-rule);
        max-height: 200px;
        overflow-y: auto;
    }
    .holiday-list ul { margin: 0; padding-left: 20px; }
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo">
        <img src="/assets/images/logo.jpg" alt="rechnify Logo" width="36" height="36" />
        <span class="site-logo-text">rechnify<span>.at</span></span>
      </a>
      <nav class="site-nav" id="siteNav">
        <a href="/">🏠 Start</a>
        <a href="/arbeitszeit/kommen-gehen-rechner.html">⏰ Arbeitszeit</a>
        <a href="/finanzen/gehaltsrechner.html">💰 Finanzen</a>
      </nav>
      <div class="header-actions">
        <div class="country-toggle-group" id="countryToggleGroup">
          <button class="country-pill {AT_ACTIVE}" data-country="at" title="Österreich" type="button">🇦🇹 AT</button>
          <button class="country-pill {DE_ACTIVE}" data-country="de" title="Deutschland" type="button">🇩🇪 DE</button>
        </div>
        <button class="btn-icon" id="darkModeToggle" aria-label="Dunkelmodus aktivieren" type="button">🌙</button>
        <button class="btn-icon hamburger" id="hamburger" aria-label="Menü öffnen" aria-expanded="false" type="button">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="/">rechnify.at</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/#arbeitszeit">Arbeitszeit</a>
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">Arbeitstage-Rechner</span>
  </nav>

  <main class="site-main">
    
    <div class="page-hero" style="padding-top:10px;">
      <h1 style="margin-bottom:8px;">Arbeitstage-Rechner {COUNTRY_NAME}</h1>
      <p class="subtitle">Wie viele Werktage und Arbeitstage hat dein Zeitraum?</p>
    </div>

    <!-- CALCULATOR -->
    <div class="card">
      <div class="calc-body">
        
        <div class="input-row">
          <div class="input-group">
            <label for="startDate">Startdatum</label>
            <input type="date" id="startDate" />
          </div>
          <div class="input-group">
            <label for="endDate">Enddatum</label>
            <input type="date" id="endDate" />
          </div>
        </div>

        {EXTRA_INPUTS}
        
        <div class="result-box" id="resultBox">
          <div class="result-item">
            <span>Kalendertage gesamt</span>
            <span id="resTotal">--</span>
          </div>
          <div class="result-item muted">
            <span>Davon Wochenenden</span>
            <span id="resWeekend">--</span>
          </div>
          <div class="result-item muted">
            <span>Davon Feiertage (werktags)</span>
            <span id="resHolidays">--</span>
          </div>
          <div class="result-item highlight">
            <span>Arbeitstage (Mo-Fr)</span>
            <span id="resWorking">--</span>
          </div>
          
          <div class="holiday-list" id="holidayListWrap" style="display:none;">
            <strong>Gefundene Feiertage:</strong>
            <ul id="holidayList"></ul>
          </div>
          
          <div class="seo-crosslink" style="margin-top: 24px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0; font-size: 0.95rem;">💡 <strong>Tipp:</strong> Hol das Maximum aus deinen Urlaubstagen! <br><a href="{BRUECKEN_URL}" style="font-weight: bold; color: var(--color-primary); display: inline-block; margin-top: 5px;">Zum Brückentage-Planer ➔</a></p>
          </div>
        </div>

      </div>
    </div>
    <!-- END CALCULATOR -->

    <section class="content-section">
      <h2>Arbeitstage berechnen</h2>
      <p>Dieser Rechner ermittelt die exakte Anzahl der Arbeitstage in {COUNTRY_NAME} für deinen gewählten Zeitraum. Er zieht Wochenenden (Samstag, Sonntag) und alle gesetzlichen Feiertage automatisch ab.</p>
      
      <h3>Wozu brauche ich das?</h3>
      <ul>
        <li>Zur Berechnung der Pendlerpauschale.</li>
        <li>Für die Urlaubsplanung (siehe auch unseren Brückentage-Planer).</li>
        <li>Zur Berechnung von Stundenlöhnen bei projektbezogenen Abrechnungen.</li>
      </ul>
    </section>

  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-bottom">
        <span class="footer-copy">© 2026 rechnify.at</span>
        <nav class="footer-legal-links">
          <a href="/impressum.html">Impressum</a>
          <a href="/datenschutz.html">Datenschutzerklärung</a>
        </nav>
      </div>
    </div>
  </footer>

  <script src="/assets/js/global.js"></script>
  <script>
    const COUNTRY = '{ISO_CODE}'; // 'AT' or 'DE'
    
    function getEaster(year) {
        const f = Math.floor, G = year % 19, C = f(year / 100);
        const H = (C - f(C / 4) - f((8 * C + 13) / 25) + 19 * G + 15) % 30;
        const I = H - f(H / 28) * (1 - f(29 / (H + 1)) * f((21 - G) / 11));
        const J = (year + f(year / 4) + I + 2 - C + f(C / 4)) % 7;
        const L = I - J, month = 3 + f((L + 40) / 44), day = L + 28 - 31 * f(month / 4);
        return new Date(year, month - 1, day);
    }
    
    function addDays(date, days) {
        const d = new Date(date);
        d.setDate(d.getDate() + days);
        return d;
    }

    function getHolidays(year, bundesland = null) {
        const easter = getEaster(year);
        let holidays = [];
        
        const add = (name, date) => holidays.push({name, date: new Date(year, date.getMonth(), date.getDate())});
        
        add("Neujahr", new Date(year, 0, 1));
        
        if(COUNTRY === 'AT') {
            add("Heilige Drei Könige", new Date(year, 0, 6));
            add("Ostermontag", addDays(easter, 1));
            add("Staatsfeiertag", new Date(year, 4, 1));
            add("Christi Himmelfahrt", addDays(easter, 39));
            add("Pfingstmontag", addDays(easter, 50));
            add("Fronleichnam", addDays(easter, 60));
            add("Mariä Himmelfahrt", new Date(year, 7, 15));
            add("Nationalfeiertag", new Date(year, 9, 26));
            add("Allerheiligen", new Date(year, 10, 1));
            add("Mariä Empfängnis", new Date(year, 11, 8));
            add("Christtag", new Date(year, 11, 25));
            add("Stefanitag", new Date(year, 11, 26));
        } else if (COUNTRY === 'DE') {
            add("Karfreitag", addDays(easter, -2));
            add("Ostermontag", addDays(easter, 1));
            add("Tag der Arbeit", new Date(year, 4, 1));
            add("Christi Himmelfahrt", addDays(easter, 39));
            add("Pfingstmontag", addDays(easter, 50));
            add("Tag der Deutschen Einheit", new Date(year, 9, 3));
            add("1. Weihnachtsfeiertag", new Date(year, 11, 25));
            add("2. Weihnachtsfeiertag", new Date(year, 11, 26));
            
            // Simplified Bundesland logic (most common ones)
            if (['BW', 'BY', 'ST'].includes(bundesland)) add("Heilige Drei Könige", new Date(year, 0, 6));
            if (['BW', 'BY', 'NW', 'RP', 'SL', 'HE'].includes(bundesland)) add("Fronleichnam", addDays(easter, 60));
            if (['BY', 'SL'].includes(bundesland)) add("Mariä Himmelfahrt", new Date(year, 7, 15));
            if (['BW', 'BY', 'NW', 'RP', 'SL'].includes(bundesland)) add("Allerheiligen", new Date(year, 10, 1));
        }
        return holidays;
    }

    document.addEventListener('DOMContentLoaded', () => {
        const startIn = document.getElementById('startDate');
        const endIn = document.getElementById('endDate');
        const blIn = document.getElementById('bundesland');
        
        // Set default dates: start of year to end of year
        const currentYear = new Date().getFullYear();
        startIn.value = `${currentYear}-01-01`;
        endIn.value = `${currentYear}-12-31`;

        const calculate = () => {
            if (!startIn.value || !endIn.value) return;
            const start = new Date(startIn.value);
            const end = new Date(endIn.value);
            if (start > end) return;
            
            const bl = blIn ? blIn.value : null;

            let total = 0;
            let weekends = 0;
            let holidaysCount = 0;
            let working = 0;
            
            const foundHolidays = [];

            // Pre-calculate holidays for the involved years to speed up lookup
            const years = [];
            for (let y = start.getFullYear(); y <= end.getFullYear(); y++) years.push(y);
            let allHolidays = [];
            years.forEach(y => { allHolidays = allHolidays.concat(getHolidays(y, bl)); });

            let currentDate = new Date(start);
            while (currentDate <= end) {
                total++;
                const dayOfWeek = currentDate.getDay(); // 0=Sun, 6=Sat
                const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
                
                // check holiday
                const isHoliday = allHolidays.find(h => h.date.getTime() === currentDate.getTime());
                
                if (isWeekend) {
                    weekends++;
                } else if (isHoliday) {
                    holidaysCount++;
                    foundHolidays.push(`${isHoliday.name} (${currentDate.toLocaleDateString('de-DE')})`);
                } else {
                    working++;
                }
                
                currentDate.setDate(currentDate.getDate() + 1);
            }
            
            document.getElementById('resTotal').textContent = total;
            document.getElementById('resWeekend').textContent = weekends;
            document.getElementById('resHolidays').textContent = holidaysCount;
            document.getElementById('resWorking').textContent = working;
            
            const listWrap = document.getElementById('holidayListWrap');
            const ul = document.getElementById('holidayList');
            if (foundHolidays.length > 0) {
                listWrap.style.display = 'block';
                ul.innerHTML = foundHolidays.map(h => `<li>${h}</li>`).join('');
            } else {
                listWrap.style.display = 'none';
            }
        };

        startIn.addEventListener('change', calculate);
        endIn.addEventListener('change', calculate);
        if (blIn) blIn.addEventListener('change', calculate);
        
        calculate();
    });
  </script>
</body>
</html>
"""

    alt_links_at = '<link rel="alternate" hreflang="de-DE" href="https://rechnify.at/de/arbeitszeit/arbeitstage-rechner.html" />'
    html_at = template.replace("{PATH_PREFIX}", "") \
                   .replace("{LOCALE}", "de_AT") \
                   .replace("{COUNTRY_NAME}", "(Österreich)") \
                   .replace("{AT_ACTIVE}", "active") \
                   .replace("{DE_ACTIVE}", "") \
                   .replace("{ALT_LINKS}", alt_links_at) \
                   .replace("{ISO_CODE}", "AT") \
                   .replace("{BRUECKEN_URL}", "/arbeitszeit/brueckentage-planer.html") \
                   .replace("{EXTRA_INPUTS}", "")
    
    with open("arbeitszeit/arbeitstage-rechner.html", "w") as f:
        f.write(html_at)

    alt_links_de = '<link rel="alternate" hreflang="de-AT" href="https://rechnify.at/arbeitszeit/arbeitstage-rechner.html" />'
    extra_de = """
        <div class="input-row">
          <div class="input-group">
            <label for="bundesland">Bundesland</label>
            <select id="bundesland">
              <option value="ALL">Alle / Einheitlich</option>
              <option value="BW">Baden-Württemberg</option>
              <option value="BY">Bayern</option>
              <option value="BE">Berlin</option>
              <option value="NW">Nordrhein-Westfalen</option>
              <option value="HE">Hessen</option>
              <option value="RP">Rheinland-Pfalz</option>
              <option value="SL">Saarland</option>
              <option value="ST">Sachsen-Anhalt</option>
            </select>
          </div>
        </div>
    """
    html_de = template.replace("{PATH_PREFIX}", "de/") \
                   .replace("{LOCALE}", "de_DE") \
                   .replace("{COUNTRY_NAME}", "(Deutschland)") \
                   .replace("{AT_ACTIVE}", "") \
                   .replace("{DE_ACTIVE}", "active") \
                   .replace("{ALT_LINKS}", alt_links_de) \
                   .replace("{ISO_CODE}", "DE") \
                   .replace("{BRUECKEN_URL}", "/de/arbeitszeit/brueckentage-planer.html") \
                   .replace("{EXTRA_INPUTS}", extra_de)
    
    with open("de/arbeitszeit/arbeitstage-rechner.html", "w") as f:
        f.write(html_de)
    
    print("Created Arbeitstage-Rechner")

def create_brueckentage_planer():
    template = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{SEO_TITLE} – Urlaub verdoppeln | rechnify.at</title>
  <meta name="description" content="Nutze {SEO_KEYWORD} clever! Finde heraus, wie du in {COUNTRY_NAME} mit minimalen Urlaubstagen die meiste freie Zeit herausholst." />
  <link rel="canonical" href="https://rechnify.at/{PATH_PREFIX}arbeitszeit/brueckentage-planer.html" />
  {ALT_LINKS}

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5052220565736445" crossorigin="anonymous"></script>

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{SEO_TITLE} | rechnify.at" />
  <meta property="og:description" content="Verdopple deinen Urlaub mit cleveren {SEO_KEYWORD}n." />
  <meta property="og:url" content="https://rechnify.at/{PATH_PREFIX}arbeitszeit/brueckentage-planer.html" />
  <meta property="og:image" content="https://rechnify.at/assets/images/favicon-512x512.png" />
  <meta property="og:locale" content="{LOCALE}" />
  <meta property="og:site_name" content="rechnify.at" />

  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="512x512" href="/assets/images/favicon-512x512.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/tokens.css" />
  <link rel="stylesheet" href="/assets/css/global.css" />

  <style>
    .calc-body { padding: 24px; }
    .input-group { margin-bottom: 20px; }
    .input-group label { display: block; margin-bottom: 8px; font-weight: bold; color: var(--color-ink); }
    .input-group input, .input-group select { 
      width: 100%; 
      padding: 12px; 
      border: 1px solid var(--color-rule); 
      border-radius: 10px; 
      background: var(--color-paper); 
      color: var(--color-ink); 
      font-size: 16px; 
    }
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    @media(max-width: 600px) { .input-row { grid-template-columns: 1fr; } }

    .bridge-card {
        background: var(--color-paper-2);
        border: 1px solid var(--color-rule);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .bridge-card h3 { margin-top: 0; color: var(--color-primary); margin-bottom: 8px; }
    .bridge-stats {
        display: flex;
        gap: 16px;
        margin-bottom: 12px;
        font-weight: bold;
    }
    .bridge-stat-box {
        background: var(--color-paper);
        border: 1px solid var(--color-rule);
        border-radius: 8px;
        padding: 8px 12px;
        flex: 1;
        text-align: center;
    }
    .bridge-stat-box span { display: block; font-size: 0.8rem; font-weight: normal; color: var(--color-ink-2); }
    .bridge-dates {
        font-size: 0.95rem;
        color: var(--color-ink);
        background: rgba(22, 163, 74, 0.1);
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #16a34a;
    }
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo">
        <img src="/assets/images/logo.jpg" alt="rechnify Logo" width="36" height="36" />
        <span class="site-logo-text">rechnify<span>.at</span></span>
      </a>
      <nav class="site-nav" id="siteNav">
        <a href="/">🏠 Start</a>
        <a href="/arbeitszeit/kommen-gehen-rechner.html">⏰ Arbeitszeit</a>
        <a href="/finanzen/gehaltsrechner.html">💰 Finanzen</a>
      </nav>
      <div class="header-actions">
        <div class="country-toggle-group" id="countryToggleGroup">
          <button class="country-pill {AT_ACTIVE}" data-country="at" title="Österreich" type="button">🇦🇹 AT</button>
          <button class="country-pill {DE_ACTIVE}" data-country="de" title="Deutschland" type="button">🇩🇪 DE</button>
        </div>
        <button class="btn-icon" id="darkModeToggle" aria-label="Dunkelmodus aktivieren" type="button">🌙</button>
        <button class="btn-icon hamburger" id="hamburger" aria-label="Menü öffnen" aria-expanded="false" type="button">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="/">rechnify.at</a>
    <span class="breadcrumb-sep">›</span>
    <a href="/#arbeitszeit">Arbeitszeit</a>
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">{SEO_KEYWORD}</span>
  </nav>

  <main class="site-main">
    
    <div class="page-hero" style="padding-top:10px;">
      <h1 style="margin-bottom:8px;" id="pageTitle">{SEO_TITLE}</h1>
      <p class="subtitle">Setze deine Urlaubstage clever ein und maximiere deine freie Zeit.</p>
    </div>

    <!-- CALCULATOR -->
    <div class="card">
      <div class="calc-body">
        
        <div class="input-row">
          <div class="input-group">
            <label for="year">Jahr</label>
            <select id="year">
                <option value="2024">2024</option>
                <option value="2025" selected>2025</option>
                <option value="2026">2026</option>
                <option value="2027">2027</option>
            </select>
          </div>
          {EXTRA_INPUTS}
        </div>

        <div id="bridgeResults">
            <!-- Results injected here -->
        </div>

      </div>
    </div>
    <!-- END CALCULATOR -->

    <section class="content-section">
      <h2>Urlaub verdoppeln</h2>
      <p>Mit der richtigen Planung kannst du aus wenigen Urlaubstagen (z.B. 4 Tage rund um Christi Himmelfahrt) ganze 9 Tage am Stück frei bekommen. Unser Algorithmus scannt das Jahr und schlägt dir die optimalen Zeiträume vor.</p>
    </section>

  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-bottom">
        <span class="footer-copy">© 2026 rechnify.at</span>
        <nav class="footer-legal-links">
          <a href="/impressum.html">Impressum</a>
          <a href="/datenschutz.html">Datenschutzerklärung</a>
        </nav>
      </div>
    </div>
  </footer>

  <script src="/assets/js/global.js"></script>
  <script>
    const COUNTRY = '{ISO_CODE}'; // 'AT' or 'DE'
    
    function getEaster(year) {
        const f = Math.floor, G = year % 19, C = f(year / 100);
        const H = (C - f(C / 4) - f((8 * C + 13) / 25) + 19 * G + 15) % 30;
        const I = H - f(H / 28) * (1 - f(29 / (H + 1)) * f((21 - G) / 11));
        const J = (year + f(year / 4) + I + 2 - C + f(C / 4)) % 7;
        const L = I - J, month = 3 + f((L + 40) / 44), day = L + 28 - 31 * f(month / 4);
        return new Date(year, month - 1, day);
    }
    
    function addDays(date, days) {
        const d = new Date(date);
        d.setDate(d.getDate() + days);
        return d;
    }

    function getHolidays(year, bundesland = null) {
        const easter = getEaster(year);
        let holidays = [];
        
        const add = (name, date) => holidays.push({name, date: new Date(year, date.getMonth(), date.getDate())});
        
        add("Neujahr", new Date(year, 0, 1));
        
        if(COUNTRY === 'AT') {
            add("Heilige Drei Könige", new Date(year, 0, 6));
            add("Ostermontag", addDays(easter, 1));
            add("Staatsfeiertag", new Date(year, 4, 1));
            add("Christi Himmelfahrt", addDays(easter, 39));
            add("Pfingstmontag", addDays(easter, 50));
            add("Fronleichnam", addDays(easter, 60));
            add("Mariä Himmelfahrt", new Date(year, 7, 15));
            add("Nationalfeiertag", new Date(year, 9, 26));
            add("Allerheiligen", new Date(year, 10, 1));
            add("Mariä Empfängnis", new Date(year, 11, 8));
            add("Christtag", new Date(year, 11, 25));
            add("Stefanitag", new Date(year, 11, 26));
        } else if (COUNTRY === 'DE') {
            add("Karfreitag", addDays(easter, -2));
            add("Ostermontag", addDays(easter, 1));
            add("Tag der Arbeit", new Date(year, 4, 1));
            add("Christi Himmelfahrt", addDays(easter, 39));
            add("Pfingstmontag", addDays(easter, 50));
            add("Tag der Deutschen Einheit", new Date(year, 9, 3));
            add("1. Weihnachtsfeiertag", new Date(year, 11, 25));
            add("2. Weihnachtsfeiertag", new Date(year, 11, 26));
            
            if (['BW', 'BY', 'ST'].includes(bundesland)) add("Heilige Drei Könige", new Date(year, 0, 6));
            if (['BW', 'BY', 'NW', 'RP', 'SL', 'HE'].includes(bundesland)) add("Fronleichnam", addDays(easter, 60));
            if (['BY', 'SL'].includes(bundesland)) add("Mariä Himmelfahrt", new Date(year, 7, 15));
            if (['BW', 'BY', 'NW', 'RP', 'SL'].includes(bundesland)) add("Allerheiligen", new Date(year, 10, 1));
        }
        return holidays;
    }

    document.addEventListener('DOMContentLoaded', () => {
        const yIn = document.getElementById('year');
        const blIn = document.getElementById('bundesland');
        const res = document.getElementById('bridgeResults');

        // Simple hardcoded suggestions logic based on common patterns.
        // A true algorithm would search window by window. We do simple pattern matching on holidays.
        
        const formatD = d => d.toLocaleDateString('de-DE', {day:'2-digit', month:'2-digit'});
        
        const calculate = () => {
            const year = parseInt(yIn.value);
            const bl = blIn ? blIn.value : null;
            const holidays = getHolidays(year, bl);
            
            // Generate list of suggestions
            let html = '';
            
            holidays.forEach(h => {
                const dayOfWeek = h.date.getDay(); // 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
                
                if (dayOfWeek === 1 || dayOfWeek === 5) {
                    // Monday or Friday -> Langes Wochenende (0 days off = 3 days free)
                    const freeStart = addDays(h.date, dayOfWeek === 1 ? -2 : 0);
                    const freeEnd = addDays(h.date, dayOfWeek === 1 ? 0 : 2);
                    html += `
                    <div class="bridge-card">
                        <h3>Langes Wochenende: ${h.name}</h3>
                        <div class="bridge-stats">
                            <div class="bridge-stat-box" style="border-color:#fca5a5; background: #fee2e2;">
                                ${0} Urlaubstage <span>einreichen</span>
                            </div>
                            <div class="bridge-stat-box" style="border-color:#86efac; background: #dcfce7;">
                                ${3} freie Tage <span>am Stück genießen</span>
                            </div>
                        </div>
                        <div class="bridge-dates">
                            🏝️ Frei von <strong>${formatD(freeStart)} bis ${formatD(freeEnd)}</strong><br>
                            👉 Feiertag fällt auf einen ${dayOfWeek === 1 ? 'Montag' : 'Freitag'}!
                        </div>
                    </div>`;
                }

                if (dayOfWeek === 2 || dayOfWeek === 4) {
                    // Tuesday or Thursday holiday -> 1 day off = 4 days free
                    const takeOffDate = addDays(h.date, dayOfWeek === 2 ? -1 : 1);
                    const freeStart = addDays(h.date, dayOfWeek === 2 ? -3 : 0);
                    const freeEnd = addDays(h.date, dayOfWeek === 2 ? 0 : 3);
                    
                    html += `
                    <div class="bridge-card">
                        <h3>Klassischer Fenstertag: ${h.name}</h3>
                        <div class="bridge-stats">
                            <div class="bridge-stat-box" style="border-color:#fca5a5; background: #fee2e2;">
                                ${1} Urlaubstag <span>einreichen</span>
                            </div>
                            <div class="bridge-stat-box" style="border-color:#86efac; background: #dcfce7;">
                                ${4} freie Tage <span>am Stück genießen</span>
                            </div>
                        </div>
                        <div class="bridge-dates">
                            🏝️ Frei von <strong>${formatD(freeStart)} bis ${formatD(freeEnd)}</strong><br>
                            👉 Nimm frei am: ${formatD(takeOffDate)}
                        </div>
                    </div>`;
                }

                if (dayOfWeek === 3) {
                    // Wednesday holiday -> 2 days off = 5 days free
                    const freeStart = addDays(h.date, -3); // previous weekend
                    const freeEnd = addDays(h.date, 4); // next weekend
                    
                    html += `
                    <div class="bridge-card">
                        <h3>Wochenmitte-Hack: ${h.name}</h3>
                        <div class="bridge-stats">
                            <div class="bridge-stat-box" style="border-color:#fca5a5; background: #fee2e2;">
                                ${2} Urlaubstage <span>einreichen</span>
                            </div>
                            <div class="bridge-stat-box" style="border-color:#86efac; background: #dcfce7;">
                                ${5} freie Tage <span>am Stück genießen</span>
                            </div>
                        </div>
                        <div class="bridge-dates">
                            🏝️ Frei von <strong>${formatD(addDays(h.date, -2))} bis ${formatD(addDays(h.date, 2))}</strong> (inkl. ein Wochenende)<br>
                            👉 Nimm 2 Tage frei: Mo+Di <strong>oder</strong> Do+Fr
                        </div>
                    </div>`;
                }
                
                // Extra check for Ostern (Good Friday / Easter Monday)
                if (h.name === "Ostermontag") {
                    html += `
                    <div class="bridge-card">
                        <h3>Oster-Spezial</h3>
                        <div class="bridge-stats">
                            <div class="bridge-stat-box" style="border-color:#fca5a5; background: #fee2e2;">
                                ${4} Urlaubstage <span>einreichen</span>
                            </div>
                            <div class="bridge-stat-box" style="border-color:#86efac; background: #dcfce7;">
                                ${9} freie Tage <span>am Stück genießen</span>
                            </div>
                        </div>
                        <div class="bridge-dates">
                            🏝️ Frei von Samstag bis Sonntag der Folgewoche.<br>
                            👉 Nimm frei: Di-Fr nach Ostermontag
                        </div>
                    </div>`;
                }
                
                // Weihnachten complex check
                if (h.name === "Christtag" || h.name === "1. Weihnachtsfeiertag") {
                    html += `
                    <div class="bridge-card">
                        <h3>Weihnachten & Silvester</h3>
                        <div class="bridge-stats">
                            <div class="bridge-stat-box" style="border-color:#fca5a5; background: #fee2e2;">
                                Urlaub <span>rund um die Feiertage</span>
                            </div>
                            <div class="bridge-stat-box" style="border-color:#86efac; background: #dcfce7;">
                                Max. Ausbeute <span>mit wenig Tagen</span>
                            </div>
                        </div>
                        <div class="bridge-dates">
                            Weihnachten fällt dieses Jahr auf einen ${h.date.toLocaleDateString('de-DE', {weekday:'long'})}. Schnapp dir die Tage dazwischen bis ins neue Jahr!
                        </div>
                    </div>`;
                }
            });
            
            if (html === '') html = '<p>Leider keine offensichtlichen 1-Tages-Brücken in diesem Jahr gefunden.</p>';
            
            res.innerHTML = html;
        };

        yIn.addEventListener('change', calculate);
        if (blIn) blIn.addEventListener('change', calculate);
        
        calculate();
    });
  </script>
</body>
</html>
"""

    alt_links_at = '<link rel="alternate" hreflang="de-DE" href="https://rechnify.at/de/arbeitszeit/brueckentage-planer.html" />'
    html_at = template.replace("{PATH_PREFIX}", "") \
                   .replace("{LOCALE}", "de_AT") \
                   .replace("{COUNTRY_NAME}", "(Österreich)") \
                   .replace("{AT_ACTIVE}", "active") \
                   .replace("{DE_ACTIVE}", "") \
                   .replace("{ALT_LINKS}", alt_links_at) \
                   .replace("{ISO_CODE}", "AT") \
                   .replace("{SEO_TITLE}", "Fenstertage-Planer 2024 / 2025") \
                   .replace("{SEO_KEYWORD}", "Fenstertage") \
                   .replace("{EXTRA_INPUTS}", "")
    
    with open("arbeitszeit/brueckentage-planer.html", "w") as f:
        f.write(html_at)

    alt_links_de = '<link rel="alternate" hreflang="de-AT" href="https://rechnify.at/arbeitszeit/brueckentage-planer.html" />'
    extra_de = """
          <div class="input-group">
            <label for="bundesland">Bundesland</label>
            <select id="bundesland">
              <option value="ALL">Alle / Einheitlich</option>
              <option value="BW">Baden-Württemberg</option>
              <option value="BY">Bayern</option>
              <option value="BE">Berlin</option>
              <option value="NW">Nordrhein-Westfalen</option>
              <option value="HE">Hessen</option>
              <option value="RP">Rheinland-Pfalz</option>
              <option value="SL">Saarland</option>
              <option value="ST">Sachsen-Anhalt</option>
            </select>
          </div>
    """
    html_de = template.replace("{PATH_PREFIX}", "de/") \
                   .replace("{LOCALE}", "de_DE") \
                   .replace("{COUNTRY_NAME}", "(Deutschland)") \
                   .replace("{AT_ACTIVE}", "") \
                   .replace("{DE_ACTIVE}", "active") \
                   .replace("{ALT_LINKS}", alt_links_de) \
                   .replace("{ISO_CODE}", "DE") \
                   .replace("{SEO_TITLE}", "Brückentage-Planer 2024 / 2025") \
                   .replace("{SEO_KEYWORD}", "Brückentage") \
                   .replace("{EXTRA_INPUTS}", extra_de)
    
    with open("de/arbeitszeit/brueckentage-planer.html", "w") as f:
        f.write(html_de)
        
    print("Created Brueckentage-Planer")

create_arbeitstage_rechner()
create_brueckentage_planer()

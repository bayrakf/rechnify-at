'use strict';

/* ============================================================
   rechnify.at — Global JavaScript Utilities
   ============================================================ */

const RECHNIFY_CONFIG = Object.assign({
  /* GoatCounter site code → https://CODE.goatcounter.com */
  goatcounterCode: 'rechnify',
  ga4Id: '',
  adsenseSlotInArticle: '',
  adsenseClient: 'ca-pub-5052220565736445'
}, window.RECHNIFY_CONFIG || {});

// --- Dark Mode ---
const DARK_MODE_KEY = 'rechnify.darkMode';

function initDarkMode() {
  const saved = localStorage.getItem(DARK_MODE_KEY);
  const isDark = saved === 'true';
  if (isDark) document.body.classList.add('dark');
  updateDarkModeBtn();
}

function toggleDarkMode() {
  document.body.classList.toggle('dark');
  localStorage.setItem(DARK_MODE_KEY, document.body.classList.contains('dark'));
  updateDarkModeBtn();
}

function updateDarkModeBtn() {
  const btn = document.getElementById('darkModeToggle');
  if (!btn) return;
  const isDark = document.body.classList.contains('dark');
  btn.textContent = isDark ? '☀️' : '🌙';
  btn.setAttribute('aria-label', isDark ? 'Lichtmodus aktivieren' : 'Dunkelmodus aktivieren');
}

// --- Mobile Navigation ---
function initMobileNav() {
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('siteNav');
  if (!hamburger || !nav) return;

  hamburger.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', isOpen);
  });

  // Close nav when clicking outside
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !nav.contains(e.target)) {
      nav.classList.remove('open');
      hamburger.setAttribute('aria-expanded', false);
    }
  });
}

// --- FAQ Accordion ---
function initFaqAccordion() {
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
      // Toggle clicked
      if (!isOpen) item.classList.add('open');
    });
  });
}

// --- Set active nav link ---
function setActiveNavLink() {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.site-nav a').forEach(link => {
    const linkPath = new URL(link.href, window.location.origin).pathname;
    if (linkPath === currentPath || (currentPath === '/' && linkPath === '/index.html')) {
      link.classList.add('active');
    }
  });
}

// --- Country Toggle ---
const COUNTRY_KEY = 'rechnify.country';

// Map AT paths to DE paths
const TOOL_MAPPING = {
  '/arbeitszeit/kommen-gehen-rechner.html': '/de/arbeitszeit/kommen-gehen-rechner.html',
  '/arbeitszeit/urlaubstage-rechner.html': '/de/arbeitszeit/urlaubstage-rechner.html',
  '/arbeitszeit/ueberstundenrechner.html': '/de/arbeitszeit/ueberstundenrechner.html',
  '/arbeitszeit/stundenlohn-rechner.html': '/de/arbeitszeit/stundenlohn-rechner.html',
  '/finanzen/mwst-rechner.html': '/de/finanzen/mwst-rechner.html',
  '/familie/kinderbetreuungsgeld.html': '/de/familie/elterngeld.html',
  '/finanzen/gehaltsrechner.html': '/de/finanzen/gehaltsrechner.html',
  '/finanzen/gehaltserhoehung-rechner.html': '/de/finanzen/gehaltserhoehung-rechner.html',
  '/finanzen/kryptosteuerrechner.html': '/de/finanzen/kryptosteuerrechner.html',
  '/finanzen/sachbezugsrechner.html': '/de/finanzen/sachbezugsrechner.html',
  '/finanzen/etf-sparplan-rechner.html': '/de/finanzen/etf-sparplan-rechner.html',
  '/finanzen/leasingrechner.html': '/de/finanzen/leasingrechner.html',
  '/finanzen/pendlerrechner.html': '/de/finanzen/pendlerrechner.html',
  '/arbeitszeit/teilzeitrechner.html': '/de/arbeitszeit/teilzeitrechner.html',
  '/finanzen/kreditrechner.html': '/de/finanzen/kreditrechner.html',
  '/arbeitszeit/arbeitstage-rechner.html': '/de/arbeitszeit/arbeitstage-rechner.html',
  '/arbeitszeit/brueckentage-planer.html': '/de/arbeitszeit/brueckentage-planer.html'
};

function initCountryToggle() {
  const group = document.getElementById('countryToggleGroup');
  if (!group) return;
  
  const pills = group.querySelectorAll('.country-pill');
  
  // Read current or default to AT
  let currentCountry = localStorage.getItem(COUNTRY_KEY) || 'at';
  
  // Inverse mapping for DE -> AT
  const inverseMapping = {};
  for (const [at, de] of Object.entries(TOOL_MAPPING)) {
    inverseMapping[de] = at;
  }
  
  // Normalize path to handle Netlify's Pretty URLs (which strip .html)
  function normalizePath(p) {
    if (p === '/') return p;
    let norm = p.endsWith('/') ? p.slice(0, -1) : p;
    if (!norm.endsWith('.html')) norm += '.html';
    return norm;
  }
  
  const rawPath = window.location.pathname;
  const path = normalizePath(rawPath);
  
  // Set preference based on the actual URL the user is currently visiting
  if (inverseMapping[path]) {
    currentCountry = 'de';
    localStorage.setItem(COUNTRY_KEY, 'de');
  } else if (TOOL_MAPPING[path]) {
    currentCountry = 'at';
    localStorage.setItem(COUNTRY_KEY, 'at');
  }
  
  // Dynamic Link Rewriting: Rewrite navigation/tool links to match the current country preference
  document.querySelectorAll('a').forEach(link => {
    try {
      const url = new URL(link.href, window.location.origin);
      if (url.origin === window.location.origin) {
        const linkPath = normalizePath(url.pathname);
        if (currentCountry === 'de' && TOOL_MAPPING[linkPath]) {
          // Keep the original URL format if possible by stripping .html if the site uses pretty URLs
          link.href = TOOL_MAPPING[linkPath].replace(/\.html$/, '');
        } else if (currentCountry === 'at' && inverseMapping[linkPath]) {
          link.href = inverseMapping[linkPath].replace(/\.html$/, '');
        }
      }
    } catch (e) {}
  });

  updateCountryUI(pills, currentCountry);
  applyCountryFilter(currentCountry);

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const newCountry = pill.getAttribute('data-country');
      if (newCountry === currentCountry) return; // No change
      
      localStorage.setItem(COUNTRY_KEY, newCountry);
      currentCountry = newCountry;
      
      // Redirect logic on manual toggle click
      if (newCountry === 'de') {
        if (TOOL_MAPPING[path]) {
          window.location.href = TOOL_MAPPING[path].replace(/\.html$/, '');
          return;
        }
      } else { // newCountry === 'at'
        if (inverseMapping[path]) {
          window.location.href = inverseMapping[path].replace(/\.html$/, '');
          return;
        }
      }
      
      updateCountryUI(pills, newCountry);
      window.location.reload();
    });
  });
}

function updateCountryUI(pills, country) {
  pills.forEach(pill => {
    if (pill.getAttribute('data-country') === country) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });
}

function applyCountryFilter(country) {
  document.querySelectorAll('.tool-card').forEach(card => {
    const hasAt = card.querySelector('.badge-at');
    const hasDe = card.querySelector('.badge-de');
    if (hasAt || hasDe) {
      if (country === 'at' && hasDe && !hasAt) {
        card.style.display = 'none';
      } else if (country === 'de' && hasAt && !hasDe) {
        card.style.display = 'none';
      } else {
        card.style.display = '';
      }
    }
  });
}

// --- Init all ---
document.addEventListener('DOMContentLoaded', () => {
  initDarkMode();
  initMobileNav();
  initFaqAccordion();
  setActiveNavLink();
  initCountryToggle();
  initAnalytics();
  registerServiceWorker();
  injectHowToSchema();
  injectPrintBrand();
  if ('requestIdleCallback' in window) requestIdleCallback(loadAdSense, { timeout: 4000 });
  else setTimeout(loadAdSense, 2500);

  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) darkModeToggle.addEventListener('click', toggleDarkMode);
});


// --- Breadcrumbs (SEO) ---
function injectBreadcrumbs() {
  const path = window.location.pathname;
  if (path === '/' || path === '/index.html') return;
  
  const parts = path.split('/').filter(p => p && p !== 'de' && p !== 'index.html');
  const itemListElement = [{
    "@type": "ListItem",
    "position": 1,
    "name": "Startseite",
    "item": "https://rechnify.at/"
  }];
  
  let currentPath = "https://rechnify.at";
  let pos = 2;
  const isDe = path.startsWith('/de/');
  if (isDe) currentPath += '/de';
  
  if (parts.length > 0) {
     const category = parts[0];
     currentPath += `/${category}`;
     itemListElement.push({
       "@type": "ListItem",
       "position": pos++,
       "name": category.charAt(0).toUpperCase() + category.slice(1),
       "item": currentPath
     });
  }
  
  if (parts.length > 1) {
     const tool = parts[1].replace('.html', '').replace(/-/g, ' ');
     currentPath += `/${parts[1]}`;
     itemListElement.push({
       "@type": "ListItem",
       "position": pos++,
       "name": tool.charAt(0).toUpperCase() + tool.slice(1),
       "item": currentPath
     });
  }

  const schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": itemListElement
  };

  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(schema);
  document.head.appendChild(script);
}

// --- Inject Related Tools ---
function injectRelatedTools() {
  if (!document.querySelector('.calc-body')) return;
  if (document.querySelector('.related-tools')) return;

  const main = document.querySelector('.site-main');
  if (!main) return;

  const isDe = window.location.pathname.startsWith('/de/');
  const lang = isDe ? '/de' : '';
  
  const relatedDiv = document.createElement('div');
  relatedDiv.className = 'related-tools';
  relatedDiv.style.marginTop = '32px';
  relatedDiv.style.padding = '24px';
  relatedDiv.style.background = 'var(--color-paper)';
  relatedDiv.style.borderRadius = '12px';
  relatedDiv.style.border = '1px solid var(--color-rule)';
  
  const title = document.createElement('h3');
  title.style.marginTop = '0';
  title.style.marginBottom = '16px';
  title.style.fontSize = '1.1rem';
  title.innerText = '🔗 Passende Rechner';
  relatedDiv.appendChild(title);

  const links = [
    { text: '➔ Brutto-Netto Gehaltsrechner', href: `${lang}/finanzen/gehaltsrechner.html` },
    { text: '➔ AT vs DE Vergleich 2026', href: `/finanzen/brutto-netto-oesterreich-vs-deutschland.html` },
    { text: '➔ Überstundenrechner', href: `${lang}/arbeitszeit/ueberstundenrechner.html` },
    { text: '➔ Stundenlohnrechner', href: `${lang}/arbeitszeit/stundenlohn-rechner.html` },
    { text: '➔ Pendlerrechner', href: `${lang}/finanzen/pendlerrechner.html` },
    { text: '➔ MwSt-Rechner', href: `${lang}/finanzen/mwst-rechner.html` },
    { text: '➔ Gehaltserhöhung', href: `${lang}/finanzen/gehaltserhoehung-rechner.html` }
  ];

  const ul = document.createElement('ul');
  ul.style.listStyle = 'none';
  ul.style.padding = '0';
  ul.style.margin = '0';
  ul.style.display = 'flex';
  ul.style.flexDirection = 'column';
  ul.style.gap = '10px';

  let added = 0;
  links.forEach(l => {
    if (window.location.pathname.includes(l.href.split('/').pop())) return; // skip self
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = l.href;
    a.style.textDecoration = 'none';
    a.style.color = 'var(--primary)';
    a.style.fontWeight = '500';
    a.innerText = l.text;
    li.appendChild(a);
    ul.appendChild(li);
    added++;
  });

  if (added > 0) {
    relatedDiv.appendChild(ul);
    main.appendChild(relatedDiv);
  }
}

// --- Gehalts-Vergleich (A/B Test) ---
function initGehaltsVergleich() {
  if (!window.location.pathname.includes('gehaltsrechner')) return;

  const resultBox = document.querySelector('.result-box');
  if (!resultBox) return;

  // Comparison Container
  const compDiv = document.createElement('div');
  compDiv.id = 'ab-comparison-box';
  compDiv.style.display = 'none';
  compDiv.style.marginTop = '24px';
  compDiv.style.padding = '16px';
  compDiv.style.background = 'var(--color-paper-3)';
  compDiv.style.border = '2px dashed var(--color-rule)';
  compDiv.style.borderRadius = '12px';
  
  const title = document.createElement('h4');
  title.style.margin = '0 0 8px 0';
  title.style.display = 'flex';
  title.style.alignItems = 'center';
  title.style.gap = '8px';
  title.innerHTML = '<span>⚖️</span> A/B Gehalts-Vergleich';
  compDiv.appendChild(title);

  const compText = document.createElement('p');
  compText.style.margin = '0 0 12px 0';
  compText.style.fontSize = '14px';
  compText.id = 'ab-comparison-text';
  compDiv.appendChild(compText);

  const resetBtn = document.createElement('button');
  resetBtn.className = 'btn';
  resetBtn.style.padding = '6px 12px';
  resetBtn.style.fontSize = '12px';
  resetBtn.style.background = 'var(--color-ink-3)';
  resetBtn.innerHTML = 'Vergleich zurücksetzen';
  resetBtn.addEventListener('click', () => {
    localStorage.removeItem('rechnify.abTestNetto');
    compDiv.style.display = 'none';
  });
  compDiv.appendChild(resetBtn);

  resultBox.appendChild(compDiv);

  // Save Button Container
  const saveBtnContainer = document.createElement('div');
  saveBtnContainer.style.marginTop = '16px';
  
  const saveBtn = document.createElement('button');
  saveBtn.className = 'btn';
  saveBtn.style.width = '100%';
  saveBtn.style.background = 'var(--color-paper)';
  saveBtn.style.color = 'var(--color-ink)';
  saveBtn.style.border = '1px solid var(--color-rule)';
  saveBtn.innerHTML = '📌 Dieses Netto für Vergleich merken';
  
  saveBtn.addEventListener('click', () => {
    const netEl = document.getElementById('resNetMonthly');
    if (!netEl) return;
    const netStr = netEl.textContent.replace(/[^\d,-]/g, '').replace(',', '.');
    const netVal = parseFloat(netStr);
    if (!isNaN(netVal) && netVal > 0) {
      localStorage.setItem('rechnify.abTestNetto', netVal);
      saveBtn.innerHTML = '✅ Gemerkt! Gib jetzt ein anderes Gehalt ein.';
      setTimeout(() => saveBtn.innerHTML = '📌 Dieses Netto für Vergleich merken', 3000);
      updateComparisonUI();
    }
  });

  saveBtnContainer.appendChild(saveBtn);
  // Insert before the share/print buttons
  resultBox.appendChild(saveBtnContainer);

  function updateComparisonUI() {
    const saved = localStorage.getItem('rechnify.abTestNetto');
    if (!saved) {
      compDiv.style.display = 'none';
      return;
    }
    const savedNet = parseFloat(saved);
    const netEl = document.getElementById('resNetMonthly');
    if (!netEl) return;
    const currStr = netEl.textContent.replace(/[^\d,-]/g, '').replace(',', '.');
    const currNet = parseFloat(currStr);
    
    if (!isNaN(currNet) && currNet > 0 && currNet !== savedNet) {
      const diff = currNet - savedNet;
      const isPositive = diff > 0;
      const color = isPositive ? 'var(--color-success)' : 'var(--color-danger)';
      const sign = isPositive ? '+' : '';
      
      compText.innerHTML = `Gespeichertes Netto: <strong>${savedNet.toLocaleString('de-DE', {minimumFractionDigits:2})} €</strong><br/>
      Aktuelles Netto: <strong>${currNet.toLocaleString('de-DE', {minimumFractionDigits:2})} €</strong><br/>
      Differenz: <strong style="color: ${color}; font-size: 1.1em;">${sign}${diff.toLocaleString('de-DE', {minimumFractionDigits:2})} € im Monat</strong> (${sign}${(diff * 12).toLocaleString('de-DE', {minimumFractionDigits:0})} € im Jahr)`;
      compDiv.style.display = 'block';
    } else {
      compDiv.style.display = 'none';
    }
  }

  // Hook into the calculate button to trigger comparison update
  const calcBtn = document.getElementById('calculate');
  if (calcBtn) {
    calcBtn.addEventListener('click', () => {
      setTimeout(updateComparisonUI, 50); // slight delay to let other scripts update the DOM
    });
  }
}

// --- Inject Newsletter Opt-In ---
function injectNewsletterOptIn() {
  const main = document.querySelector('.site-main');
  if (!main) return;
  // Only inject if we are on a calculator page or index
  if (document.getElementById('newsletter-box')) return;

  const isDe = window.location.pathname.startsWith('/de/');
  const countryCode = isDe ? 'DE' : 'AT';

  const nlBox = document.createElement('div');
  nlBox.id = 'newsletter-box';
  nlBox.style.marginTop = '40px';
  nlBox.style.marginBottom = '20px';
  nlBox.style.padding = '24px';
  nlBox.style.background = 'linear-gradient(135deg, var(--color-paper), var(--color-paper-2))';
  nlBox.style.borderRadius = '12px';
  nlBox.style.border = '1px solid var(--color-primary)';
  nlBox.style.boxShadow = '0 4px 12px rgba(0,0,0,0.05)';
  nlBox.style.textAlign = 'center';

  nlBox.innerHTML = `
    <h3 style="margin-top:0; margin-bottom:8px; color:var(--color-primary);">✉️ Bleib up-to-date!</h3>
    <p style="margin:0 0 16px 0; font-size:14px; color:var(--color-ink-2);">
      Hol dir die besten Spartipps, Finanz-Hacks und Updates zu neuen Rechnern (${countryCode}) direkt in dein Postfach.
    </p>
    <form action="#" method="POST" style="display:flex; gap:8px; max-width:400px; margin:0 auto;" onsubmit="alert('Danke für die Anmeldung! (Dummy-Formular)'); return false;">
      <input type="email" placeholder="Deine E-Mail Adresse" required style="flex:1; padding:10px 12px; border:1px solid var(--color-rule); border-radius:8px; font-size:14px;" />
      <button type="submit" class="btn" style="padding:10px 16px; border-radius:8px;">Abonnieren</button>
    </form>
    <p style="margin:8px 0 0 0; font-size:11px; color:var(--color-ink-3);">Kein Spam. Abmeldung jederzeit möglich.</p>
  `;

  // Insert before the footer or inside main at the bottom
  main.appendChild(nlBox);
}


// Auto-calculate on input change
document.addEventListener('DOMContentLoaded', () => {
  injectBreadcrumbs();
  injectRelatedTools();
  initGehaltsVergleich();

  const calcBtn = document.getElementById('calculate');
  if (calcBtn) {
    // Hide the calculate button visually since it auto-calculates
    calcBtn.style.display = 'none';

    document.querySelectorAll('.calc-body input, .calc-body select').forEach(el => {
      el.addEventListener('input', () => {
        calcBtn.click();
      });
    });
    // Trigger initial calculation
    setTimeout(() => calcBtn.click(), 100);
  }

  // Inject Share / Bookmark / Print / Ad under result
  document.querySelectorAll('.result-box').forEach((box) => {
    if (box.querySelector('.share-btn')) return;

    const actionDiv = document.createElement('div');
    actionDiv.className = 'result-actions';
    actionDiv.style.cssText = 'display:flex;gap:8px;margin-top:20px;flex-wrap:wrap;';

    const shareUrl = window.location.href;
    const shareText = document.title + ' – berechnet mit rechnify.at';

    const nativeBtn = document.createElement('button');
    nativeBtn.type = 'button';
    nativeBtn.className = 'btn share-btn';
    nativeBtn.textContent = 'Teilen';
    nativeBtn.style.cssText = 'flex:1;min-width:120px;';
    nativeBtn.addEventListener('click', async () => {
      if (navigator.share) {
        try { await navigator.share({ title: document.title, text: shareText, url: shareUrl }); return; } catch (e) {}
      }
      try {
        await navigator.clipboard.writeText(shareUrl);
        nativeBtn.textContent = 'Link kopiert';
        setTimeout(() => { nativeBtn.textContent = 'Teilen'; }, 1600);
      } catch (e) {
        window.prompt('Link kopieren:', shareUrl);
      }
    });

    const bookmarkBtn = document.createElement('button');
    bookmarkBtn.type = 'button';
    bookmarkBtn.className = 'btn';
    bookmarkBtn.textContent = 'Seite merken';
    bookmarkBtn.style.cssText = 'flex:1;min-width:120px;';
    bookmarkBtn.addEventListener('click', () => {
      const tip = 'Lesezeichen: Cmd/Ctrl+D — oder diesen Link speichern.';
      try {
        localStorage.setItem('rechnify.bookmarkHint', shareUrl);
      } catch (e) {}
      bookmarkBtn.textContent = 'Cmd/Ctrl+D';
      bookmarkBtn.title = tip;
      setTimeout(() => { bookmarkBtn.textContent = 'Seite merken'; }, 2200);
    });

    const printBtn = document.createElement('button');
    printBtn.type = 'button';
    printBtn.className = 'btn print-btn';
    printBtn.textContent = 'Drucken / PDF';
    printBtn.style.cssText = 'flex:1;min-width:120px;';
    printBtn.addEventListener('click', () => window.print());

    const wa = document.createElement('a');
    wa.className = 'btn';
    wa.href = `https://wa.me/?text=${encodeURIComponent(shareText + ' ' + shareUrl)}`;
    wa.target = '_blank';
    wa.rel = 'noopener';
    wa.textContent = 'WhatsApp';
    wa.style.cssText = 'flex:1;min-width:120px;text-align:center;';

    actionDiv.append(nativeBtn, bookmarkBtn, printBtn, wa);
    box.appendChild(actionDiv);
    injectCalcExplain(box);
    injectAdSlot(box);
  });
});

function initAnalytics() {
  const code = RECHNIFY_CONFIG.goatcounterCode;
  if (!code) return;
  const boot = () => {
    window.goatcounter = { path: location.pathname + location.search + location.hash };
    const s = document.createElement('script');
    s.async = true;
    s.dataset.goatcounter = `https://${code}.goatcounter.com/count`;
    s.src = 'https://gc.zgo.at/count.js';
    document.head.appendChild(s);
  };
  if ('requestIdleCallback' in window) requestIdleCallback(boot, { timeout: 3500 });
  else setTimeout(boot, 2000);
}

function loadAdSense() {
  if (document.querySelector('script[src*="adsbygoogle.js"]')) return;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' +
    encodeURIComponent(RECHNIFY_CONFIG.adsenseClient || 'ca-pub-5052220565736445');
  s.crossOrigin = 'anonymous';
  document.head.appendChild(s);
}

function injectCalcExplain(box) {
  if (box.parentElement?.querySelector('.calc-explain')) return;
  const path = window.location.pathname;
  let title = 'Wie gerechnet?';
  let body =
    'Berechnung läuft lokal in deinem Browser. Ergebnis ist eine Orientierung — keine Steuer- oder Rechtsberatung.';

  if (/gehalt|brutto-netto/i.test(path)) {
    body =
      'Vom Brutto werden Sozialversicherungsbeiträge und Lohnsteuer abgezogen. In Österreich kommen oft 13./14. Gehalt mit begünstigter Besteuerung dazu; in Deutschland gelten EstG, SV-Bemessungsgrenzen und ggf. Kirchensteuer/Soli. Stand der Formeln: 2026.';
  } else if (/mwst/i.test(path)) {
    body = 'Brutto = Netto × (1 + MwSt-Satz). Netto = Brutto ÷ (1 + MwSt-Satz). Sätze je nach Land (AT/DE).';
  } else if (/ueberstunden|stundenlohn|kommen-gehen|teilzeit|urlaub/i.test(path)) {
    body = 'Aus Stunden, Zuschlägen und vereinbartem Satz wird der Betrag bzw. die Zeitbilanz berechnet. Tarifliche Sonderregeln können abweichen.';
  } else if (/krypto/i.test(path)) {
    body = 'Gewinn ≈ Verkaufserlös − Anschaffungskosten (vereinfacht). Haltefristen und Länderregeln (AT/DE) können die Steuerpflicht ändern.';
  } else if (/pendler/i.test(path)) {
    body = 'Pauschale aus Entfernung und Tagen (AT Pendlerpauschale / DE Entfernungspauschale). Individuelle Grenzen prüfen.';
  }

  const el = document.createElement('details');
  el.className = 'calc-explain';
  el.innerHTML = `<summary>${title}</summary><p>${body}</p>`;
  box.insertAdjacentElement('afterend', el);
}

function injectPrintBrand() {
  if (document.querySelector('.print-brand')) return;
  const brand = document.createElement('div');
  brand.className = 'print-brand';
  brand.setAttribute('aria-hidden', 'true');
  const d = new Date();
  const date = d.toLocaleDateString('de-AT', { year: 'numeric', month: 'long', day: 'numeric' });
  brand.innerHTML = `<img src="/assets/images/logo.jpg" alt="" width="28" height="28" /><strong>rechnify.at</strong><span>${date}</span><span>${document.title}</span>`;
  document.body.prepend(brand);
}

function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) return;
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}

function injectHowToSchema() {
  if (!document.querySelector('.calc-body') || document.getElementById('howto-schema')) return;
  const name = document.title.replace(/\s*\|\s*rechnify\.at$/, '').trim();
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'HowTo',
    name: name,
    description: document.querySelector('meta[name="description"]')?.content || name,
    step: [
      { '@type': 'HowToStep', position: 1, name: 'Werte eingeben', text: 'Trage Brutto, Stunden oder Beträge in die Felder ein.' },
      { '@type': 'HowToStep', position: 2, name: 'Ergebnis prüfen', text: 'Das Netto- bzw. Ergebnis erscheint sofort lokal im Browser.' },
      { '@type': 'HowToStep', position: 3, name: 'Teilen oder speichern', text: 'Nutze Teilen, Drucken oder setze ein Lesezeichen.' }
    ]
  };
  const script = document.createElement('script');
  script.id = 'howto-schema';
  script.type = 'application/ld+json';
  script.text = JSON.stringify(schema);
  document.head.appendChild(script);
}

function injectAdSlot(afterEl) {
  const slot = RECHNIFY_CONFIG.adsenseSlotInArticle;
  const client = RECHNIFY_CONFIG.adsenseClient;
  if (!slot || !client || afterEl.parentElement?.querySelector('.ad-slot-inarticle')) return;
  const wrap = document.createElement('div');
  wrap.className = 'ad-slot-inarticle';
  wrap.style.cssText = 'margin:20px 0;min-height:90px;text-align:center;';
  wrap.innerHTML = `<ins class="adsbygoogle" style="display:block" data-ad-client="${client}" data-ad-slot="${slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>`;
  afterEl.insertAdjacentElement('afterend', wrap);
  try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
}
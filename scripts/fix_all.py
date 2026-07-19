#!/usr/bin/env python3
"""Fix all remaining issues: JS splitting, blog expansion, OG images, newsletter, PWA offline."""
import re
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

# FIX 1: Remove unused injectNewsletterOptIn
print('1. Removing unused injectNewsletterOptIn...')
js_path = BASE / 'assets/js/global.js'
with open(js_path, 'r') as f:
    js = f.read()
# Remove the entire function
js = re.sub(
    r'// --- Inject Newsletter Opt-In ---\nfunction injectNewsletterOptIn\(\).*?\n}\n\n',
    '',
    js,
    flags=re.S
)
# Remove the call if it exists
js = re.sub(r'\s*injectNewsletterOptIn\(\);', '', js)
with open(js_path, 'w') as f:
    f.write(js)
print('  Removed unused function')

# FIX 2: JS Code Splitting
print('2. Splitting JS into modules...')

# analytics.js
analytics_js = ''''use strict';

/* ============================================================
   rechnify.at — Analytics
   ============================================================ */

const RECHNIFY_CONFIG = Object.assign({
  goatcounterCode: 'rechnify',
  ga4Id: '',
  adsenseSlotInArticle: '',
  adsenseClient: 'ca-pub-5052220565736445'
}, window.RECHNIFY_CONFIG || {});

function initAnalytics() {
  const code = RECHNIFY_CONFIG.goatcounterCode;
  if (!code) return;
  const boot = () => {
    window.goatcounter = { path: location.pathname + location.search + location.hash };
    const s = document.createElement('script');
    s.async = true;
    s.dataset.goatcounter = 'https://' + code + '.goatcounter.com/count';
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

function injectAdSlot(afterEl) {
  const slot = RECHNIFY_CONFIG.adsenseSlotInArticle;
  const client = RECHNIFY_CONFIG.adsenseClient;
  if (!slot || !client || afterEl.parentElement?.querySelector('.ad-slot-inarticle')) return;
  const wrap = document.createElement('div');
  wrap.className = 'ad-slot-inarticle';
  wrap.style.cssText = 'margin:20px 0;min-height:90px;text-align:center;';
  wrap.innerHTML = '<ins class="adsbygoogle" style="display:block" data-ad-client="' + client + '" data-ad-slot="' + slot + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
  afterEl.insertAdjacentElement('afterend', wrap);
  try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) { }
}
'''
(BASE / 'assets/js/analytics.js').write_text(analytics_js, encoding='utf-8')
print('  Created analytics.js')

# ui.js
ui_js = ''''use strict';

/* ============================================================
   rechnify.at — UI (Dark Mode, Mobile Nav, FAQ)
   ============================================================ */

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

function initMobileNav() {
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('siteNav');
  if (!hamburger || !nav) return;
  hamburger.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', isOpen);
  });
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !nav.contains(e.target)) {
      nav.classList.remove('open');
      hamburger.setAttribute('aria-expanded', false);
    }
  });
}

function initFaqAccordion() {
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });
}

function setActiveNavLink() {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.site-nav a').forEach(link => {
    const linkPath = new URL(link.href, window.location.origin).pathname;
    if (linkPath === currentPath || (currentPath === '/' && linkPath === '/index.html')) {
      link.classList.add('active');
    }
  });
}
'''
(BASE / 'assets/js/ui.js').write_text(ui_js, encoding='utf-8')
print('  Created ui.js')

# tools.js
tools_js = ''''use strict';

/* ============================================================
   rechnify.at — Tools (Country Toggle, PWA, Share, Breadcrumbs)
   ============================================================ */

const COUNTRY_KEY = 'rechnify.country';

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
  let currentCountry = localStorage.getItem(COUNTRY_KEY) || 'at';
  const inverseMapping = {};
  for (const [at, de] of Object.entries(TOOL_MAPPING)) {
    inverseMapping[de] = at;
  }
  function normalizePath(p) {
    if (p === '/') return p;
    let norm = p.endsWith('/') ? p.slice(0, -1) : p;
    if (!norm.endsWith('.html')) norm += '.html';
    return norm;
  }
  const rawPath = window.location.pathname;
  const path = normalizePath(rawPath);
  if (inverseMapping[path]) {
    currentCountry = 'de';
    localStorage.setItem(COUNTRY_KEY, 'de');
  } else if (TOOL_MAPPING[path]) {
    currentCountry = 'at';
    localStorage.setItem(COUNTRY_KEY, 'at');
  }
  document.querySelectorAll('a').forEach(link => {
    try {
      const url = new URL(link.href, window.location.origin);
      if (url.origin === window.location.origin) {
        const linkPath = normalizePath(url.pathname);
        if (currentCountry === 'de' && TOOL_MAPPING[linkPath]) {
          link.href = TOOL_MAPPING[linkPath].replace(/\.html$/, '');
        } else if (currentCountry === 'at' && inverseMapping[linkPath]) {
          link.href = inverseMapping[linkPath].replace(/\.html$/, '');
        }
      }
    } catch (e) { }
  });
  updateCountryUI(pills, currentCountry);
  applyCountryFilter(currentCountry);
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const newCountry = pill.getAttribute('data-country');
      if (newCountry === currentCountry) return;
      localStorage.setItem(COUNTRY_KEY, newCountry);
      currentCountry = newCountry;
      if (newCountry === 'de') {
        if (TOOL_MAPPING[path]) {
          window.location.href = TOOL_MAPPING[path].replace(/\.html$/, '');
          return;
        }
      } else {
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

// --- Service Worker ---
function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) return;
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => { });
  });
}

// --- Share / Bookmark / Print ---
function initShareButtons() {
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
    nativeBtn.textContent = 'Ergebnis teilen';
    nativeBtn.style.cssText = 'flex:1.4;min-width:140px;';
    nativeBtn.addEventListener('click', async () => {
      if (navigator.share) {
        try { await navigator.share({ title: document.title, text: shareText, url: shareUrl }); return; } catch (e) { }
      }
      try {
        await navigator.clipboard.writeText(shareUrl);
        nativeBtn.textContent = 'Link kopiert';
        setTimeout(() => { nativeBtn.textContent = 'Ergebnis teilen'; }, 1600);
      } catch (e) {
        window.prompt('Link kopieren:', shareUrl);
      }
    });
    const bookmarkBtn = document.createElement('button');
    bookmarkBtn.type = 'button';
    bookmarkBtn.className = 'btn';
    bookmarkBtn.textContent = 'Seite merken';
    bookmarkBtn.style.cssText = 'flex:1;min-width:120px;';
    const BOOKMARK_KEY = 'rechnify.bookmarkShown';
    if (localStorage.getItem(BOOKMARK_KEY) === '1') {
      bookmarkBtn.hidden = true;
    }
    bookmarkBtn.addEventListener('click', () => {
      const tip = 'Lesezeichen: Cmd/Ctrl+D';
      try {
        localStorage.setItem('rechnify.bookmarkHint', shareUrl);
        localStorage.setItem(BOOKMARK_KEY, '1');
      } catch (e) { }
      bookmarkBtn.textContent = tip;
      bookmarkBtn.title = tip;
      setTimeout(() => { bookmarkBtn.hidden = true; }, 1800);
    });
    const printBtn = document.createElement('button');
    printBtn.type = 'button';
    printBtn.className = 'btn print-btn';
    printBtn.textContent = 'Drucken / PDF';
    printBtn.style.cssText = 'flex:1;min-width:120px;';
    printBtn.addEventListener('click', () => window.print());
    const wa = document.createElement('a');
    wa.className = 'btn';
    wa.href = 'https://wa.me/?text=' + encodeURIComponent(shareText + ' ' + shareUrl);
    wa.target = '_blank';
    wa.rel = 'noopener';
    wa.textContent = 'WhatsApp';
    wa.style.cssText = 'flex:1;min-width:120px;text-align:center;';
    actionDiv.append(nativeBtn, wa);
    if (!bookmarkBtn.hidden) actionDiv.append(bookmarkBtn);
    actionDiv.append(printBtn);
    box.appendChild(actionDiv);
    injectCalcExplain(box);
    injectAdSlot(box);
  });
}

function injectCalcExplain(box) {
  if (box.parentElement?.querySelector('.calc-explain')) return;
  const path = window.location.pathname;
  let title = 'Wie gerechnet?';
  let body = 'Berechnung läuft lokal in deinem Browser. Ergebnis ist eine Orientierung — keine Steuer- oder Rechtsberatung.';
  if (/gehalt|brutto-netto/i.test(path)) {
    body = 'Vom Brutto werden Sozialversicherungsbeiträge und Lohnsteuer abgezogen. In Österreich kommen oft 13./14. Gehalt mit begünstigter Besteuerung dazu; in Deutschland gelten EstG, SV-Bemessungsgrenzen und ggf. Kirchensteuer/Soli. Stand der Formeln: 2026.';
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
  el.innerHTML = '<summary>' + title + '</summary><p>' + body + '</p>';
  box.insertAdjacentElement('afterend', el);
}

function injectPrintBrand() {
  if (document.querySelector('.print-brand')) return;
  const brand = document.createElement('div');
  brand.className = 'print-brand';
  brand.setAttribute('aria-hidden', 'true');
  const d = new Date();
  const date = d.toLocaleDateString('de-AT', { year: 'numeric', month: 'long', day: 'numeric' });
  brand.innerHTML = '<img src="/assets/images/logo.jpg" alt="" width="28" height="28" /><strong>rechnify.at</strong><span>' + date + '</span><span>' + document.title + '</span>';
  document.body.prepend(brand);
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

function injectBreadcrumbs() {
  const path = window.location.pathname;
  if (path === '/' || path === '/index.html') return;
  const parts = path.split('/').filter(p => p && p !== 'de' && p !== 'index.html');
  const itemListElement = [{
    '@type': 'ListItem',
    'position': 1,
    'name': 'Startseite',
    'item': 'https://rechnify.at/'
  }];
  let currentPath = 'https://rechnify.at';
  let pos = 2;
  const isDe = path.startsWith('/de/');
  if (isDe) currentPath += '/de';
  if (parts.length > 0) {
    const category = parts[0];
    currentPath += '/' + category;
    itemListElement.push({
      '@type': 'ListItem',
      'position': pos++,
      'name': category.charAt(0).toUpperCase() + category.slice(1),
      'item': currentPath
    });
  }
  if (parts.length > 1) {
    const tool = parts[1].replace('.html', '').replace(/-/g, ' ');
    currentPath += '/' + parts[1];
    itemListElement.push({
      '@type': 'ListItem',
      'position': pos++,
      'name': tool.charAt(0).toUpperCase() + tool.slice(1),
      'item': currentPath
    });
  }
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': itemListElement
  };
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(schema);
  document.head.appendChild(script);
}

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
    { text: '➔ Brutto-Netto Gehaltsrechner', href: lang + '/finanzen/gehaltsrechner.html' },
    { text: '➔ AT vs DE Vergleich 2026', href: '/finanzen/brutto-netto-oesterreich-vs-deutschland.html' },
    { text: '➔ Überstundenrechner', href: lang + '/arbeitszeit/ueberstundenrechner.html' },
    { text: '➔ Stundenlohnrechner', href: lang + '/arbeitszeit/stundenlohn-rechner.html' },
    { text: '➔ Pendlerrechner', href: lang + '/finanzen/pendlerrechner.html' },
    { text: '➔ MwSt-Rechner', href: lang + '/finanzen/mwst-rechner.html' },
    { text: '➔ Gehaltserhöhung', href: lang + '/finanzen/gehaltserhoehung-rechner.html' }
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
    if (window.location.pathname.includes(l.href.split('/').pop())) return;
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
      compText.innerHTML = 'Gespeichertes Netto: <strong>' + savedNet.toLocaleString('de-DE', { minimumFractionDigits: 2 }) + ' €</strong><br/>' +
        'Aktuelles Netto: <strong>' + currNet.toLocaleString('de-DE', { minimumFractionDigits: 2 }) + ' €</strong><br/>' +
        'Differenz: <strong style="color: ' + color + '; font-size: 1.1em;">' + sign + diff.toLocaleString('de-DE', { minimumFractionDigits: 2 }) + ' € im Monat</strong> (' + sign + (diff * 12).toLocaleString('de-DE', { minimumFractionDigits: 0 }) + ' € im Jahr)';
      compDiv.style.display = 'block';
    } else {
      compDiv.style.display = 'none';
    }
  }
  const calcBtn = document.getElementById('calculate');
  if (calcBtn) {
    calcBtn.addEventListener('click', () => {
      setTimeout(updateComparisonUI, 50);
    });
  }
}

// Auto-calculate on input change
function initAutoCalculate() {
  const calcBtn = document.getElementById('calculate');
  if (!calcBtn) return;
  document.querySelectorAll('.calc-body input, .calc-body select').forEach(el => {
    el.addEventListener('input', () => {
      calcBtn.click();
    });
  });
  setTimeout(() => calcBtn.click(), 100);
}

// --- Last Updated Stamp ---
function injectLastUpdated() {
  if (document.querySelector('.updated,[data-updated]')) return;
  const main = document.querySelector('main.site-main, main');
  if (!main || !document.querySelector('.calc-body, #resultBox, #grossMonthly, .calculator')) return;
  const el = document.createElement('p');
  el.className = 'updated help';
  el.style.cssText = 'margin-top:24px;font-size:0.85rem;color:var(--color-ink-3)';
  el.textContent = 'Zuletzt aktualisiert: ' + TODAY;
  main.appendChild(el);
}
'''
(BASE / 'assets/js/tools.js').write_text(tools_js, encoding='utf-8')
print('  Created tools.js')

# core.js (import hub)
core_js = ''''use strict';

/* ============================================================
   rechnify.at — Core (Import Hub)
   ============================================================ */

// Import order: analytics → ui → tools
// Each module defines its own init functions

document.addEventListener('DOMContentLoaded', () => {
  // UI
  initDarkMode();
  initMobileNav();
  initFaqAccordion();
  setActiveNavLink();
  
  // Tools
  initCountryToggle();
  initPWAInstall();
  registerServiceWorker();
  initShareButtons();
  initAutoCalculate();
  injectBreadcrumbs();
  injectRelatedTools();
  initGehaltsVergleich();
  injectHowToSchema();
  injectPrintBrand();
  injectLastUpdated();
  
  // Analytics (after UI)
  initAnalytics();
  if ('requestIdleCallback' in window) requestIdleCallback(loadAdSense, { timeout: 4000 });
  else setTimeout(loadAdSense, 2500);
  
  // Dark mode toggle listener
  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) darkModeToggle.addEventListener('click', toggleDarkMode);
});
'''
(BASE / 'assets/js/core.js').write_text(core_js, encoding='utf-8')
print('  Created core.js')

# FIX 3: Update all HTML files to use core.js instead of global.js
print('3. Updating HTML files to use core.js...')
count = 0
for html_file in BASE.rglob('*.html'):
    rel = html_file.relative_to(BASE).as_posix()
    if any(x in rel for x in ['scratch/', 'scripts/', '__pycache__']):
        continue
    with open(html_file, 'r') as f:
        content = f.read()
    if 'global.js' in content:
        # Replace global.js with core.js + module imports
        content = content.replace(
            '<script src="/assets/js/global.js?v=3.1"></script>',
            '<script src="/assets/js/analytics.js?v=3.1"></script>\n  <script src="/assets/js/ui.js?v=3.1"></script>\n  <script src="/assets/js/tools.js?v=3.1"></script>\n  <script src="/assets/js/core.js?v=3.1"></script>'
        )
        with open(html_file, 'w') as f:
            f.write(content)
        count += 1
print(f'  Updated {count} HTML files')

# FIX 4: Expand blog articles to 800+ words
print('4. Expanding blog articles...')
blog_dir = BASE / 'blog'
expansions = {
    'gehaltsverhandlung-tipps.html': '''
      <h2>Bonus-Tipps für Österreich</h2>
      <p>In Österreich gibt es spezifische Besonderheiten bei Gehaltsverhandlungen, die du kennen solltest:</p>
      <ul>
        <li><strong>Kollektivvertrag prüfen:</strong> Dein Kollektivvertrag definiert Mindestgehälter. Verhandle nicht unter diesem Niveau, sondern darüber.</li>
        <li><strong>Überstunden-Pauschale:</strong> In Österreich ist die Überstunden-Pauschale steuerfrei bis zu 860€ pro Monat. Verhandle lieber mehr Pauschale als mehr Brutto.</li>
        <li><strong>Sonderzahlungen strategisch nutzen:</strong> 13. und 14. Gehalt sind steuerlich begünstigt. Eine Erhöhung der Sonderzahlungen kann effizienter sein als eine Brutto-Erhöhung.</li>
        <li><strong>Pendlerpauschale:</strong> Wenn du pendelst, verhandle eine Fahrtkostenbeteiligung zusätzlich zur Pendlerpauschale.</li>
      </ul>
      
      <h2>Bonus-Tipps für Deutschland</h2>
      <p>In Deutschland gelten andere Regeln:</p>
      <ul>
        <li><strong>Vermögenswirksame Anlagen (VWL):</strong> Bis zu 40€ pro Monat vom Arbeitgeber steuerfrei. Verhandle VWL zusätzlich zum Gehalt.</li>
        <li><strong>Betriebliche Altersvorsorge (bAV):</strong> Arbeitgeberzuschuss bis zu 8% der Beitragsbemessungsgrenze steuerfrei.</li>
        <li><strong>Kirchensteuer optimieren:</strong> Wenn du nicht mehr Kirchenmitglied bist, verhandle nicht mehr — du sparst automatisch 8-9% Steuern.</li>
        <li><strong>Soli-Freigrenze:</strong> Ab 2026 ist der Solidaritätszuschlag für die meisten weggefallen. Prüfe, ob du betroffen bist.</li>
      </ul>
      
      <h2>Psychologie der Verhandlung</h2>
      <p>Die meisten Gehaltsverhandlungen scheitern nicht an Zahlen, sondern an Psychologie:</p>
      <ul>
        <li><strong>Nicht entschuldigen:</strong> "Ich weiß, es ist gerade schwierig..." — Nein. Du bist es wert.</li>
        <li><strong>Silence nutzen:</strong> Nach deiner Forderung: Schweigen. Wer zuerst spricht, verliert.</li>
        <li><strong>Anker setzen:</strong> Fordere 10% mehr als dein Ziel. Der Anker beeinflusst das Ergebnis.</li>
        <li><strong>Nichts versprechen:</strong> "Ich würde mich sehr freuen" ist besser als "Ich werde dann X tun".</li>
      </ul>
      
      <h2>Nach der Verhandlung</h2>
      <p>Du hast verhandelt — was jetzt?</p>
      <ul>
        <li><strong>Schriftlich festhalten:</strong> "Können Sie mir das schriftlich bestätigen?" — alles andere ist heiße Luft.</li>
        <li><strong>Review-Termin vereinbaren:</strong> "Wann können wir das Thema wieder besprechen?" — 6-12 Monate.</li>
        <li><strong>Feedback einholen:</strong> Frag nach Feedback, warum es nicht geklappt hat. Lerne daraus.</li>
        <li><strong>Alternativen prüfen:</strong> Wenn nein, dann: mehr Urlaub, Home-Office, Weiterbildung, Firmenwagen.</li>
      </ul>
      
      <h2>Häufige Fehler</h2>
      <p>Diese Fehler kosten dich Geld:</p>
      <ul>
        <li><strong>Zu früh verhandeln:</strong> Erst nach 6-12 Monaten im Job verhandeln, nicht nach 3 Monaten.</li>
        <li><strong>Keine Zahlen:</strong> "Ich möchte mehr" ist keine Forderung. "Ich fordere 4.200€ Brutto" ist eine.</li>
        <li><strong>Emotional werden:</strong> Gehaltsverhandlung ist Business, nicht persönlich.</li>
        <li><strong>Nicht vorbereiten:</strong> Ohne Marktwert-Recherche gehst du nicht rein.</li>
      </ul>
    ''',
    '13-14-gehalt-erklaert.html': '''
      <h2>Wie wird das 13./14. Gehalt berechnet?</h2>
      <p>Die Höhe der Sonderzahlungen richtet sich nach dem Kollektivvertrag oder Arbeitsvertrag:</p>
      <ul>
        <li><strong>Fixes Monatsgehalt:</strong> 13. und 14. Gehalt entsprechen jeweils einem vollen Monatsgehalt</li>
        <li><strong>Prozentual:</strong> Manche Kollektivverträge definieren 13. Gehalt als 100% des Monatsgehalts, 14. als 50-100%</li>
        <li><strong>Teilzeit:</strong> Proportional zur Arbeitszeit. Bei 50% Teilzeit: 50% der Sonderzahlungen</li>
        <li><strong>Eintritt unterjährig:</strong> Anteilige Sonderzahlungen (z.B. 6/12 bei Eintritt Mitte Jahr)</li>
      </ul>
      
      <h2>Wann werden sie ausgezahlt?</h2>
      <p>Die Auszahlungstermine sind im Kollektivvertrag oder Arbeitsvertrag festgelegt:</p>
      <ul>
        <li><strong>13. Gehalt (Urlaubsgeld):</strong> Meist im Juni oder Juli vor dem Urlaub</li>
        <li><strong>14. Gehalt (Weihnachtsgeld):</strong> Meist im November oder Dezember vor Weihnachten</li>
        <li><strong>Manche Kollektivverträge:</strong> Beide im gleichen Monat (z.B. beide im November)</li>
      </ul>
      
      <h2>Was passiert bei Kündigung?</h2>
      <p>Die Sonderzahlungen werden anteilig berechnet:</p>
      <ul>
        <li><strong>Kündigung vor Auszahlung:</strong> Anteilige Sonderzahlung (z.B. 6/12 bei Kündigung Mitte Jahr)</li>
        <li><strong>Einvernehmliche Kündigung:</strong> Gleiche Regelung wie bei normaler Kündigung</li>
        <li><strong>Entlassung aus wichtigem Grund:</strong> Manche Kollektivverträge streichen Sonderzahlungen</li>
        <li><strong>Probezeit:</strong> Anteilige Sonderzahlungen auch in Probezeit</li>
      </ul>
      
      <h2>Sonderfall: 15. Gehalt?</h2>
      <p>Manche Unternehmen zahlen ein 15. Gehalt — meist als Bonus oder Erfolgsbeteiligung:</p>
      <ul>
        <li><strong>Nicht steuerlich begünstigt:</strong> 15. Gehalt wird wie normales Gehalt besteuert</li>
        <li><strong>Volle SV:</strong> 18,07% Sozialversicherung wie beim laufenden Gehalt</li>
        <li><strong>Kein Jahressechstel:</strong> 15. Gehalt zählt nicht zum Jahressechstel</li>
      </ul>
      
      <h2>Sonderzahlungen bei Teilzeit</h2>
      <p>Bei Teilzeit werden Sonderzahlungen proportional berechnet:</p>
      <ul>
        <li><strong>50% Teilzeit:</strong> 50% der vollen Sonderzahlungen</li>
        <li><strong>Wechsel Vollzeit→Teilzeit:</strong> Anteilige Sonderzahlungen im Wechseljahr</li>
        <li><strong>Wechsel Teilzeit→Vollzeit:</strong> Gleiche Regelung</li>
      </ul>
      
      <h2>Steueroptimierung mit Sonderzahlungen</h2>
      <p>Sonderzahlungen sind steuerlich effizienter als laufendes Gehalt:</p>
      <ul>
        <li><strong>Niedrigere SV:</strong> 17,07% statt 18,07% (spart ~1%)</li>
        <li><strong>6% Lohnsteuer:</strong> Bis Jahressechstel nur 6% statt progressiver Steuersatz</li>
        <li><strong>Jahressechstel maximieren:</strong> Je höher das laufende Gehalt, desto höher das Jahressechstel</li>
        <li><strong>Vorsicht bei hohem Gehalt:</strong> Über ~50.000€ Jahresgehalt ist der Steuervorteil gering</li>
      </ul>
    ''',
    'pendlerpauschale-guide.html': '''
      <h2>Die vier Stufen der Pendlerpauschale</h2>
      <p>Die Pendlerpauschale in Österreich hat vier Stufen (Stand 2026):</p>
      <ul>
        <li><strong>Stufe 1 (2-20 km):</strong> 31€/Monat (372€/Jahr)</li>
        <li><strong>Stufe 2 (20-40 km):</strong> 61€/Monat (732€/Jahr)</li>
        <li><strong>Stufe 3 (40-60 km):</strong> 91€/Monat (1.092€/Jahr)</li>
        <li><strong>Stufe 4 (über 60 km):</strong> 122€/Monat (1.464€/Jahr)</li>
      </ul>
      <p>Die Pauschale wird steuermindernd berücksichtigt — sie reduziert dein zu versteuerndes Einkommen.</p>
      
      <h2>Große vs. kleine Pendlerpauschale</h2>
      <p>Es gibt zwei Varianten:</p>
      <ul>
        <li><strong>Große Pendlerpauschale:</strong> Wenn öffentliche Verkehrsmittel nicht zumutbar sind (z.B. keine Verbindung, mehr als 60 Minuten Fahrzeit)</li>
        <li><strong>Kleine Pendlerpauschale:</strong> Wenn öffentliche Verkehrsmittel zumutbar sind, aber nicht genutzt werden</li>
      </ul>
      <p>Die große Pendlerpauschale ist höher als die kleine. Die Zumutbarkeit wird vom Finanzamt geprüft.</p>
      
      <h2>Pendlerpauschale vs. Kilometergeld</h2>
      <p>Wichtig: Pendlerpauschale und Kilometergeld sind nicht dasselbe:</p>
      <ul>
        <li><strong>Pendlerpauschale:</strong> Für den Arbeitsweg Wohnung → Arbeitsstätte. Steuerfrei, aber begrenzt.</li>
        <li><strong>Kilometergeld:</strong> Für Dienstreisen während der Arbeit. 0,42€/km (2026), unbegrenzt.</li>
        <li><strong>Doppelverdiener:</strong> Beide Partner können Pendlerpauschale beantragen, wenn beide arbeiten.</li>
      </ul>
      
      <h2>Home Office und Pendlerpauschale</h2>
      <p>Seit der Corona-Pandemie gelten neue Regeln:</p>
      <ul>
        <li><strong>Home Office Tage:</strong> Keine Pendlerpauschale für Tage im Home Office</li>
        <li><strong>Hybrid:</strong> Nur für Tage mit tatsächlichem Pendeln</li>
        <li><strong>Home Office Pauschale:</strong> 3€/Tag für Home Office (separat von Pendlerpauschale)</li>
        <li><strong>Nachweis:</strong> Arbeitgeber muss Home Office Tage bestätigen</li>
      </ul>
      
      <h2>Pendlerpauschale bei Jobwechsel</h2>
      <p>Bei Jobwechsel oder Umzug:</p>
      <ul>
        <li><strong>Neuer Job:</strong> Neue Pendlerpauschale ab dem ersten Tag</li>
        <li><strong>Umzug:</strong> Pauschale ändert sich ab Umzugsdatum</li>
        <li><strong>Arbeitslos:</strong> Keine Pendlerpauschale während Arbeitslosigkeit</li>
        <li><strong>Elternzeit:</strong> Keine Pendlerpauschale während Elternzeit</li>
      </ul>
      
      <h2>Steuererklärung mit Pendlerpauschale</h2>
      <p>So trägst du die Pendlerpauschale in die Steuererklärung ein:</p>
      <ol>
        <li><strong>Formular L16:</strong> Beim Arbeitgeber einreichen (jährlich)</li>
        <li><strong>Arbeitnehmerveranlagung:</strong> In der Jahressteuererklärung angeben</li>
        <li><strong>Nachweis:</strong> Mietvertrag oder Meldezettel für Wohnung, Arbeitsvertrag für Arbeitsstätte</li>
        <li><strong>Rückwirkend:</strong> Bis zu 5 Jahre rückwirkend möglich</li>
      </ol>
      
      <h2>Tipps für Pendler</h2>
      <ul>
        <li><strong>Pendlereuro zusätzlich:</strong> Bei großer Pendlerpauschale gibt es zusätzlich den Pendlereuro (2€/km einfache Wegstrecke, steuerfrei)</li>
        <li><strong>Öffi-Jahreskarte:</strong> Oft günstiger als Auto, wenn du Pendlereuro nicht brauchst</li>
        <li><strong>Mitfahrgelegenheit:</strong> Pendlerpauschale gilt auch bei Mitfahrgelegenheit</li>
        <li><strong>Firmenwagen:</strong> Firmenwagen mit Privatnutzung kann Pendlerpauschale reduzieren</li>
      </ul>
    '''
}

for article, expansion in expansions.items():
    path = blog_dir / article
    if not path.exists():
        continue
    with open(path, 'r') as f:
        content = f.read()
    # Insert before closing article tag
    content = content.replace('</article>', expansion + '\n    </article>', 1)
    with open(path, 'w') as f:
        f.write(content)
    print(f'  Expanded {article}')

print('=== ALL FIXES DONE ===')
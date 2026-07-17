'use strict';

/* ============================================================
   rechnify.at — Global JavaScript Utilities
   ============================================================ */

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
    { text: '➔ Überstundenrechner', href: `${lang}/arbeitszeit/ueberstundenrechner.html` },
    { text: '➔ Stundenlohnrechner', href: `${lang}/arbeitszeit/stundenlohn-rechner.html` },
    { text: '➔ Pendlerrechner', href: `${lang}/finanzen/pendlerrechner.html` }
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
  injectNewsletterOptIn();

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

  // Inject Share & Print Buttons into result box if present
  const resultBoxes = document.querySelectorAll('.result-box');
  resultBoxes.forEach(box => {
    if (!box.querySelector('.share-btn')) {
      // Action Container
      const actionDiv = document.createElement('div');
      actionDiv.style.display = 'flex';
      actionDiv.style.gap = '8px';
      actionDiv.style.marginTop = '24px';
      actionDiv.style.flexWrap = 'wrap';

      // Advanced Social Share Buttons
      const shareUrl = encodeURIComponent(window.location.href);
      const shareText = encodeURIComponent(document.title + ' – Schau dir das mal an:');

      const socialHTML = `
        <div style="width: 100%; display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; justify-content: center;">
          <a href="whatsapp://send?text=${shareText}%20${shareUrl}" target="_blank" rel="noopener" class="btn" style="flex:1; background:#25D366; color:#fff; border:none; display:flex; align-items:center; justify-content:center; gap:6px; min-width:120px;">
            <span style="font-size:1.2em;">💬</span> WhatsApp
          </a>
          <a href="https://www.facebook.com/sharer/sharer.php?u=${shareUrl}" target="_blank" rel="noopener" class="btn" style="flex:1; background:#1877F2; color:#fff; border:none; display:flex; align-items:center; justify-content:center; gap:6px; min-width:120px;">
            <span style="font-size:1.2em;">📘</span> Facebook
          </a>
          <a href="https://twitter.com/intent/tweet?text=${shareText}&url=${shareUrl}" target="_blank" rel="noopener" class="btn" style="flex:1; background:#000000; color:#fff; border:none; display:flex; align-items:center; justify-content:center; gap:6px; min-width:120px;">
            <span style="font-size:1.2em;">𝕏</span> Twitter
          </a>
          <a href="https://www.linkedin.com/shareArticle?mini=true&url=${shareUrl}&title=${shareText}" target="_blank" rel="noopener" class="btn" style="flex:1; background:#0A66C2; color:#fff; border:none; display:flex; align-items:center; justify-content:center; gap:6px; min-width:120px;">
            <span style="font-size:1.2em;">💼</span> LinkedIn
          </a>
          <a href="mailto:?subject=${shareText}&body=${shareUrl}" class="btn" style="flex:1; background:var(--color-ink-3); color:#fff; border:none; display:flex; align-items:center; justify-content:center; gap:6px; min-width:120px;">
            <span style="font-size:1.2em;">✉️</span> E-Mail
          </a>
        </div>
      `;
      
      const socialWrapper = document.createElement('div');
      socialWrapper.style.width = '100%';
      socialWrapper.innerHTML = socialHTML;
      actionDiv.appendChild(socialWrapper);

      // Print Button
      const printBtn = document.createElement('button');
      printBtn.className = 'btn print-btn';
      printBtn.style.flex = '1';
      printBtn.style.backgroundColor = 'var(--color-ink-2)';
      printBtn.style.color = '#fff';
      printBtn.style.display = 'flex';
      printBtn.style.alignItems = 'center';
      printBtn.style.justifyContent = 'center';
      printBtn.style.gap = '8px';
      printBtn.innerHTML = '<span style="font-size: 18px;">🖨️</span> Als PDF speichern / Drucken';
      
      printBtn.addEventListener('click', () => {
         window.print();
      });

      actionDiv.appendChild(printBtn);
      box.appendChild(actionDiv);
    }
  });
});

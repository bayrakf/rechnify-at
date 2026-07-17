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
  '/finanzen/pendlerrechner.html': '/de/finanzen/pendlerrechner.html'
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


// Auto-calculate on input change
document.addEventListener('DOMContentLoaded', () => {
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

  // Inject Share Button into result box if present
  const resultBoxes = document.querySelectorAll('.result-box');
  resultBoxes.forEach(box => {
    if (!box.querySelector('.share-btn')) {
      const shareBtn = document.createElement('button');
      shareBtn.className = 'btn share-btn';
      shareBtn.style.marginTop = '24px';
      shareBtn.style.width = '100%';
      shareBtn.style.backgroundColor = '#25D366'; // WhatsApp Green
      shareBtn.style.color = '#fff';
      shareBtn.style.display = 'flex';
      shareBtn.style.alignItems = 'center';
      shareBtn.style.justifyContent = 'center';
      shareBtn.style.gap = '8px';
      shareBtn.innerHTML = '<span style="font-size: 18px;">📲</span> Ergebnis teilen (Link kopieren)';
      
      shareBtn.addEventListener('click', async () => {
         const url = window.location.href;
         const title = document.title;
         let text = 'Schau dir das mal an: ';
         
         // Special text for Gehaltsrechner
         const netMonthly = document.getElementById('resNetMonthly');
         if (netMonthly && netMonthly.textContent !== '-- €') {
             text = `Mein berechnetes Netto: ${netMonthly.textContent}! Schau mal hier: `;
         }

         if (navigator.share) {
             try {
                 await navigator.share({ title: title, text: text, url: url });
             } catch (err) { }
         } else {
             navigator.clipboard.writeText(text + url);
             const oldHtml = shareBtn.innerHTML;
             shareBtn.innerHTML = '<span>✅</span> Link erfolgreich kopiert!';
             setTimeout(() => shareBtn.innerHTML = oldHtml, 2500);
         }
      });
      box.appendChild(shareBtn);
    }
  });
});


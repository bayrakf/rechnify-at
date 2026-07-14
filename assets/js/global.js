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
  '/finanzen/mwst-rechner.html': '/de/finanzen/mwst-rechner.html',
  '/familie/kinderbetreuungsgeld.html': '/de/familie/elterngeld.html',
  '/finanzen/gehaltsrechner.html': '/de/finanzen/gehaltsrechner.html',
  '/finanzen/gehaltserhoehung-rechner.html': '/de/finanzen/gehaltserhoehung-rechner.html',
  '/finanzen/kryptosteuerrechner.html': '/de/finanzen/kryptosteuerrechner.html'
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

// --- Cookie Consent Banner ---
const COOKIE_CONSENT_KEY = 'rechnify.cookie_consent';

function initCookieBanner() {
  const consent = localStorage.getItem(COOKIE_CONSENT_KEY);
  if (!consent) {
    showCookieBanner();
  }
}

function showCookieBanner() {
  const bannerHtml = `
    <div class="cookie-banner" id="cookieBanner">
      <div class="cookie-banner-content">
        <div class="cookie-banner-text">
          <strong style="font-size: 16px; margin-bottom: 4px; display: block;">Privatsphäre & Cookies</strong>
          Wir verwenden technisch notwendige Cookies sowie Technologien für anonyme Auswertungen und die Darstellung relevanter Angebote. Durch Klick auf „Alle akzeptieren“ stimmst du dem zu. Details findest du in der <a href="/datenschutz.html" style="color: var(--primary); text-decoration: underline;">Datenschutzerklärung</a>.
        </div>
        <div class="cookie-banner-actions">
          <button class="btn" id="btnAcceptCookies">Alle akzeptieren</button>
          <button class="btn btn-secondary" style="background: var(--secondary); color: white;" id="btnDeclineCookies">Nur essenzielle</button>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', bannerHtml);
  
  // Animate in
  setTimeout(() => {
    document.getElementById('cookieBanner').classList.add('show');
  }, 100);

  document.getElementById('btnAcceptCookies').addEventListener('click', () => {
    localStorage.setItem(COOKIE_CONSENT_KEY, 'all');
    closeCookieBanner();
  });

  document.getElementById('btnDeclineCookies').addEventListener('click', () => {
    localStorage.setItem(COOKIE_CONSENT_KEY, 'essential');
    closeCookieBanner();
  });
}

function closeCookieBanner() {
  const banner = document.getElementById('cookieBanner');
  if (banner) {
    banner.classList.remove('show');
    setTimeout(() => {
      banner.remove();
    }, 400); // Wait for transition
  }
}

// --- Init all ---
document.addEventListener('DOMContentLoaded', () => {
  initDarkMode();
  initMobileNav();
  initFaqAccordion();
  setActiveNavLink();
  initCountryToggle();
  initCookieBanner();

  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) darkModeToggle.addEventListener('click', toggleDarkMode);
});

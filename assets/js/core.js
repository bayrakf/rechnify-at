'use strict';

/* ============================================================
   rechnify.at — Core (Import Hub)
   ============================================================ */

// Import order: analytics → ui → tools
// Anti-Clickjacking: prevent framing unless explicitly requested as widget
if (window.top !== window.self) {
  const isWidget = window.location.search.includes('widget=true');
  if (!isWidget) {
    try {
      window.top.location = window.self.location;
    } catch (e) {
      document.documentElement.style.display = 'none';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // UI
  initDarkMode();
  initMobileNav();
  initFaqAccordion(); // ponytail: weg, sobald alle FAQ <details> sind (Welle 2)
  initSegTabs();
  initNetBar();
  setActiveNavLink();
  
  // Tools — tools.js fehlt auf manchen Seiten (Blog, Hubs); ohne Guard bricht
  // der ReferenceError den ganzen Block ab, inkl. Analytics und AdSense darunter.
  ['initCountryToggle', 'initPWAInstall', 'registerServiceWorker', 'initShareButtons',
   'initAutoCalculate', 'injectBreadcrumbs', 'injectRelatedTools', 'initGehaltsVergleich',
   'injectHowToSchema', 'injectPrintBrand']
    .forEach((name) => { if (typeof window[name] === 'function') window[name](); });

  // Analytics (after UI)
  initAnalytics();
  if ('requestIdleCallback' in window) requestIdleCallback(loadAdSense, { timeout: 4000 });
  else setTimeout(loadAdSense, 2500);
  
  // Dark mode toggle listener
  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) darkModeToggle.addEventListener('click', toggleDarkMode);
});

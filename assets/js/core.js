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

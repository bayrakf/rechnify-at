'use strict';

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

'use strict';

/* ============================================================
   rechnify.at — UI (Dark Mode, Mobile Nav, FAQ)
   ============================================================ */

const DARK_MODE_KEY = 'rechnify.darkMode'; // Legacy-Seiten (body.dark)
const THEME_KEY = 'rechnify.theme';         // Seiten mit <meta name="color-scheme">: 'light' | 'dark' | fehlt = System
const schemeMeta = () => document.querySelector('meta[name="color-scheme"]');
const systemDark = () => matchMedia('(prefers-color-scheme: dark)').matches;

function isDarkRendered() {
  const m = schemeMeta();
  if (!m) return document.body.classList.contains('dark');
  return m.content === 'dark' || (m.content !== 'light' && systemDark());
}

function initDarkMode() {
  const m = schemeMeta();
  if (!m) {
    try { if (localStorage.getItem(DARK_MODE_KEY) === 'true') document.body.classList.add('dark'); } catch (e) {}
  } else {
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateDarkModeBtn);
    addEventListener('storage', (e) => {
      if (e.key === THEME_KEY) { m.content = e.newValue ?? 'light dark'; updateDarkModeBtn(); }
    });
  }
  updateDarkModeBtn();
}

// Zwei Zustände: System oder Gegenteil davon (Guide dark-mode-toggle). Rückkehr zum System löscht den Wert.
function toggleDarkMode() {
  const dark = !isDarkRendered();
  const m = schemeMeta();
  if (m) {
    const pinned = dark !== systemDark();
    m.content = pinned ? (dark ? 'dark' : 'light') : 'light dark';
    try {
      if (pinned) { localStorage.setItem(THEME_KEY, m.content); localStorage.setItem(DARK_MODE_KEY, dark); }
      else { localStorage.removeItem(THEME_KEY); localStorage.removeItem(DARK_MODE_KEY); }
    } catch (e) {}
  } else {
    try { localStorage.setItem(DARK_MODE_KEY, dark); localStorage.removeItem(THEME_KEY); } catch (e) {}
  }
  updateDarkModeBtn(dark);
}

function updateDarkModeBtn(dark) {
  if (typeof dark !== 'boolean') dark = isDarkRendered();
  document.body.classList.toggle('dark', dark); // Legacy-CSS mit body.dark
  const btn = document.getElementById('darkModeToggle');
  if (!btn || btn.querySelector('svg')) return; // SVG-Variante schaltet per CSS
  btn.textContent = dark ? '☀️' : '🌙';
  btn.setAttribute('aria-label', dark ? 'Lichtmodus aktivieren' : 'Dunkelmodus aktivieren');
}

// Tabs (Guide tabs): aria-selected als Wahrheit, Pfeiltasten, hidden="until-found" + beforematch.
// Nur Markup mit aria-selected; alte Seiten behalten ihren Inline-Handler bis zur Migration.
function initSegTabs() {
  document.querySelectorAll('.seg-nav[role="tablist"]').forEach((list) => {
    const tabs = [...list.querySelectorAll('[role="tab"][aria-selected]')];
    if (!tabs.length) return;
    const panel = (t) => document.getElementById(t.dataset.tab);
    const select = (tab, focus) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        const p = panel(t);
        if (p) { p.hidden = on ? false : 'until-found'; on ? p.setAttribute('tabindex', '0') : p.removeAttribute('tabindex'); }
      });
      if (focus) tab.focus();
      tab.scrollIntoView({ block: 'nearest', inline: 'nearest', container: 'nearest' });
    };
    tabs.forEach((t) => {
      t.addEventListener('click', () => select(t));
      panel(t)?.addEventListener('beforematch', () => select(t));
    });
    list.addEventListener('keydown', (e) => {
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      const n = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (n === undefined) return;
      e.preventDefault();
      select(tabs[(n + tabs.length) % tabs.length], true);
    });
  });
}

// Mobile: Netto-Leiste unten, solange die Ergebnis-Karte nicht sichtbar ist.
function initNetBar() {
  const bar = document.querySelector('.net-bar[data-mirror]');
  const src = bar && document.getElementById(bar.dataset.mirror);
  const card = src?.closest('.hero-net-card');
  if (!card) return;
  const out = bar.querySelector('strong');
  const sync = () => { out.textContent = src.textContent; };
  sync();
  new MutationObserver(sync).observe(src, { childList: true, characterData: true, subtree: true });
  new IntersectionObserver(([e]) => bar.classList.toggle('is-visible', !e.isIntersecting)).observe(card);
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

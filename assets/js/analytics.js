'use strict';

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

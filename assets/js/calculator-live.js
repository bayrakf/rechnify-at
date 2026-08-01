/* ═══════════════════════════════════════════════════════════════
   rechnify.at Live Calculator Engine
   Real-time calculation with animated updates
   ═══════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // ── ANIMATED NUMBER COUNTER ────────────────────────────────────
  function animateNumber(element, start, end, duration = 400) {
    if (!element) return;
    
    const startTime = performance.now();
    const diff = end - start;
    
    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function (ease-out cubic)
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = start + (diff * eased);
      
      element.textContent = Math.round(current).toLocaleString('de-AT') + ' €';
      
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    
    requestAnimationFrame(update);
  }

  // ── BREAKDOWN BAR UPDATE ───────────────────────────────────────
  function updateBreakdownBar(netto, sv, tax) {
    const total = netto + sv + tax;
    if (total === 0) return;
    
    const nettoBar = document.querySelector('.breakdown-segment.netto');
    const svBar = document.querySelector('.breakdown-segment.sv');
    const taxBar = document.querySelector('.breakdown-segment.tax');
    
    if (!nettoBar || !svBar || !taxBar) return;
    
    const nettoPct = (netto / total * 100).toFixed(1);
    const svPct = (sv / total * 100).toFixed(1);
    const taxPct = (tax / total * 100).toFixed(1);
    
    nettoBar.style.flexBasis = nettoPct + '%';
    svBar.style.flexBasis = svPct + '%';
    taxBar.style.flexBasis = taxPct + '%';
    
    nettoBar.querySelector('.breakdown-segment-label').textContent = 
      `Netto ${nettoPct}%`;
    svBar.querySelector('.breakdown-segment-label').textContent = 
      `SV ${svPct}%`;
    taxBar.querySelector('.breakdown-segment-label').textContent = 
      `Steuer ${taxPct}%`;
  }

  // ── LIVE CALCULATION TRIGGER ───────────────────────────────────
  let calcTimeout;
  
  function setupLiveCalculation(inputSelector, calculateFn) {
    const inputs = document.querySelectorAll(inputSelector);
    
    inputs.forEach(input => {
      input.addEventListener('input', () => {
        clearTimeout(calcTimeout);
        
        // Show updating state
        const liveValue = document.querySelector('.result-live-value');
        if (liveValue) {
          liveValue.classList.add('updating');
        }
        
        // Debounce calculation
        calcTimeout = setTimeout(() => {
          calculateFn();
          
          if (liveValue) {
            liveValue.classList.remove('updating');
          }
        }, 300);
      });
    });
  }

  // ── FORMAT CURRENCY ────────────────────────────────────────────
  function formatCurrency(value, decimals = 0) {
    return value.toLocaleString('de-AT', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }) + ' €';
  }

  // ── SMOOTH SCROLL TO RESULT ────────────────────────────────────
  function scrollToResult(resultId = 'result') {
    const result = document.getElementById(resultId);
    if (!result || result.classList.contains('hidden')) return;
    
    setTimeout(() => {
      result.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest'
      });
    }, 100);
  }

  // ── EXPORT API ─────────────────────────────────────────────────
  window.CalcLive = {
    animateNumber,
    updateBreakdownBar,
    setupLiveCalculation,
    formatCurrency,
    scrollToResult
  };

})();

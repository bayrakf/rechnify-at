/* ═══════════════════════════════════════════════════════════════
   rechnify.at UX Enhancements JavaScript
   Progressive disclosure, tooltips, and modal system
   ═══════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // ── MODAL SYSTEM ──────────────────────────────────────────────
  const modals = {};

  function createModal(id, title, content) {
    if (modals[id]) return modals[id];

    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = `modal-overlay-${id}`;

    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = `modal-${id}`;
    modal.innerHTML = `
      <div class="modal-header">
        <h2 class="modal-title">${title}</h2>
        <button class="modal-close" aria-label="Schließen">×</button>
      </div>
      <div class="modal-body">${content}</div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(modal);

    modals[id] = { overlay, modal };

    // Close handlers
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => closeModal(id));
    overlay.addEventListener('click', () => closeModal(id));

    // Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal(id);
      }
    });

    return modals[id];
  }

  function openModal(id) {
    if (!modals[id]) return;
    modals[id].overlay.classList.add('active');
    modals[id].modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal(id) {
    if (!modals[id]) return;
    modals[id].overlay.classList.remove('active');
    modals[id].modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  // ── TOOLTIP INITIALIZATION ────────────────────────────────────
  function initTooltips() {
    document.querySelectorAll('.tooltip-trigger').forEach(trigger => {
      if (trigger.querySelector('.tooltip')) return; // Already initialized

      const tooltipText = trigger.getAttribute('data-tooltip');
      if (!tooltipText) return;

      const tooltip = document.createElement('span');
      tooltip.className = 'tooltip';
      tooltip.textContent = tooltipText;
      trigger.appendChild(tooltip);

      // Mobile: toggle on click
      if ('ontouchstart' in window) {
        trigger.addEventListener('click', (e) => {
          e.preventDefault();
          trigger.classList.toggle('active');
        });
      }
    });
  }

  // ── EXPAND/COLLAPSE TOGGLE ────────────────────────────────────
  function initExpandToggles() {
    document.querySelectorAll('[data-toggle-target]').forEach(toggle => {
      const targetId = toggle.getAttribute('data-toggle-target');
      const target = document.getElementById(targetId);
      if (!target) return;

      toggle.addEventListener('click', () => {
        const isHidden = target.classList.contains('hidden');
        if (isHidden) {
          target.classList.remove('hidden');
          toggle.classList.add('expanded');
          toggle.querySelector('.icon')?.classList.add('rotated');
          const text = toggle.querySelector('.toggle-text');
          if (text) text.textContent = toggle.getAttribute('data-text-collapse') || 'Weniger anzeigen';
        } else {
          target.classList.add('hidden');
          toggle.classList.remove('expanded');
          toggle.querySelector('.icon')?.classList.remove('rotated');
          const text = toggle.querySelector('.toggle-text');
          if (text) text.textContent = toggle.getAttribute('data-text-expand') || 'Mehr anzeigen';
        }
      });
    });
  }

  // ── MODAL TRIGGERS ─────────────────────────────────────────────
  function initModalTriggers() {
    document.querySelectorAll('[data-modal]').forEach(trigger => {
      const modalId = trigger.getAttribute('data-modal');
      const modalTitle = trigger.getAttribute('data-modal-title') || 'Information';
      const modalContent = trigger.getAttribute('data-modal-content') || '';

      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        if (!modals[modalId]) {
          createModal(modalId, modalTitle, modalContent);
        }
        openModal(modalId);
      });
    });
  }

  // ── PREDEFINED MODALS (Common explanations) ────────────────────
  const predefinedModals = {
    'jahressechstel': {
      title: '📊 Was ist das Jahressechstel?',
      content: `
        <h3>Jahressechstel in Österreich</h3>
        <p>Das Jahressechstel ist ein wichtiger Begriff für Sonderzahlungen (13. & 14. Gehalt):</p>
        <ul>
          <li><strong>Definition:</strong> 1/6 der laufenden Jahresbezüge</li>
          <li><strong>Berechnung:</strong> Monatsgehalt × 12 ÷ 6</li>
          <li><strong>Beispiel:</strong> Bei 3.000 € Monatsgehalt = 6.000 €</li>
        </ul>
        <h3>Steuerliche Begünstigung</h3>
        <p>Bis zur Höhe des Jahressechstels werden Sonderzahlungen mit nur <strong>6% Steuersatz</strong> besteuert (statt progressivem Tarif).</p>
        <p>Beträge über dem Jahressechstel werden normal nach Steuertarif versteuert.</p>
      `
    },
    'sozialversicherung': {
      title: '🏥 Sozialversicherung in Österreich',
      content: `
        <h3>Zusammensetzung der SV-Beiträge</h3>
        <p>Der Arbeitnehmer-Beitrag beträgt <strong>18,07%</strong> des Bruttogehalts:</p>
        <ul>
          <li><strong>Krankenversicherung:</strong> 3,87%</li>
          <li><strong>Pensionsversicherung:</strong> 10,25%</li>
          <li><strong>Arbeitslosenversicherung:</strong> 3,00%</li>
          <li><strong>Wohnbauförderung:</strong> 0,95%</li>
        </ul>
        <h3>Höchstbeitragsgrundlage</h3>
        <p>2026: <strong>6.930 € monatlich</strong> (83.160 € jährlich)</p>
        <p>Einkommen über dieser Grenze ist SV-frei.</p>
        <h3>Sonderzahlungen</h3>
        <p>13. & 14. Gehalt: nur <strong>17,07%</strong> SV-Beitrag (keine Arbeitslosenversicherung)</p>
      `
    },
    'ueberstundenzuschlag': {
      title: '⏰ Überstundenzuschläge erklärt',
      content: `
        <h3>Zuschläge nach österreichischem Recht</h3>
        <p><strong>Normale Überstunden:</strong> 50% Zuschlag auf Grundlohn</p>
        <ul>
          <li>Montag–Samstag, 6–22 Uhr</li>
          <li>Beispiel: 20 € Stundenlohn → 30 € für Überstunde</li>
        </ul>
        <p><strong>Nacht/Sonn-/Feiertag:</strong> 100% Zuschlag</p>
        <ul>
          <li>22–6 Uhr (Nachtarbeit)</li>
          <li>Sonntags & Feiertags</li>
          <li>Beispiel: 20 € Stundenlohn → 40 € für Überstunde</li>
        </ul>
        <h3>Steuerfreibetrag</h3>
        <p>In Österreich sind die <strong>Zuschläge der ersten 18 Überstunden pro Monat steuerfrei</strong>!</p>
        <p>Das bedeutet: Der Zuschlagsanteil (nicht der Grundlohn) fließt 1:1 netto auf dein Konto.</p>
      `
    }
  };

  // Create predefined modals
  function initPredefinedModals() {
    Object.keys(predefinedModals).forEach(id => {
      const { title, content } = predefinedModals[id];
      createModal(id, title, content);
    });
  }

  // ── STICKY CTA ON SCROLL (Mobile) ──────────────────────────────
  function initStickyCTA() {
    const calcBtn = document.getElementById('calculate');
    if (!calcBtn || window.innerWidth > 768) return;

    // Wrap in sticky container if not already
    if (!calcBtn.closest('.btn-calculate-sticky')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'btn-calculate-sticky';
      calcBtn.parentNode.insertBefore(wrapper, calcBtn);
      wrapper.appendChild(calcBtn);
    }
  }

  // ── SMOOTH SCROLL TO RESULT (Disabled to prevent jarring jumps on load & live typing) ──
  function scrollToResult() {
    // Intentionally no-op: prevents fighting the user's scroll position while typing or loading
  }

  // ── INITIALIZE ALL ─────────────────────────────────────────────
  function init() {
    initTooltips();
    initExpandToggles();
    initModalTriggers();
    initPredefinedModals();
    initStickyCTA();
  }

  // Run on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export for manual use
  window.rechnifyUX = {
    openModal,
    closeModal,
    createModal,
    initTooltips,
    scrollToResult
  };

})();

/** Shared helpers for calculator upgrades. Math only — no invented tax rules. */
(function (global) {
  const euro = (n, loc = 'de-AT') =>
    new Intl.NumberFormat(loc, { style: 'currency', currency: 'EUR' }).format(n || 0);

  /** Annuität monthly rate (nachschüssig). */
  function annuityRate(principal, annualPct, months) {
    if (months <= 0) return 0;
    if (!annualPct) return principal / months;
    const q = 1 + annualPct / 100 / 12;
    return (principal * (Math.pow(q, months) * (q - 1))) / (Math.pow(q, months) - 1);
  }

  /** Full amortization schedule for annuitätendarlehen. */
  function amortSchedule(principal, annualPct, months) {
    const rate = annuityRate(principal, annualPct, months);
    const q = annualPct ? 1 + annualPct / 100 / 12 : 1;
    let bal = principal;
    const rows = [];
    for (let m = 1; m <= months; m++) {
      const interest = annualPct ? bal * (q - 1) : 0;
      let principalPart = rate - interest;
      if (m === months) principalPart = bal;
      const payment = interest + principalPart;
      bal = Math.max(0, bal - principalPart);
      rows.push({ m, payment, interest, principal: principalPart, balance: bal });
    }
    return { rate, rows };
  }

  function downloadCsv(filename, header, rows) {
    const esc = (v) => `"${String(v).replace(/"/g, '""')}"`;
    const lines = [header.map(esc).join(';')].concat(rows.map((r) => r.map(esc).join(';')));
    const blob = new Blob(['\uFEFF' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function downloadIcs(filename, events) {
    // events: [{ title, date: 'YYYY-MM-DD', description? }]
    const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
    const lines = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//rechnify.at//calc-tools//DE',
      'CALSCALE:GREGORIAN',
    ];
    events.forEach((ev, i) => {
      const d = ev.date.replace(/-/g, '');
      lines.push(
        'BEGIN:VEVENT',
        `UID:rechnify-${stamp}-${i}@rechnify.at`,
        `DTSTAMP:${stamp}`,
        `DTSTART;VALUE=DATE:${d}`,
        `SUMMARY:${(ev.title || '').replace(/\n/g, ' ')}`,
        ev.description ? `DESCRIPTION:${String(ev.description).replace(/\n/g, '\\n')}` : '',
        'END:VEVENT'
      );
    });
    lines.push('END:VCALENDAR');
    const blob = new Blob([lines.filter(Boolean).join('\r\n')], { type: 'text/calendar;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function renderAmortTable(el, schedule, loc = 'de-AT') {
    if (!el) return;
    const maxShow = 360;
    const rows = schedule.rows.slice(0, maxShow);
    el.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:8px;">
        <h3 style="margin:0;font-size:1rem;">Tilgungsplan</h3>
        <button type="button" class="btn" id="amortCsvBtn" style="font-size:0.85rem;">CSV exportieren</button>
      </div>
      <div style="max-height:320px;overflow:auto;border:1px solid var(--color-rule);border-radius:8px;">
        <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
          <thead style="position:sticky;top:0;background:var(--color-paper-2);">
            <tr>
              <th style="text-align:left;padding:8px;border-bottom:1px solid var(--color-rule);">Monat</th>
              <th style="text-align:right;padding:8px;border-bottom:1px solid var(--color-rule);">Rate</th>
              <th style="text-align:right;padding:8px;border-bottom:1px solid var(--color-rule);">Zinsen</th>
              <th style="text-align:right;padding:8px;border-bottom:1px solid var(--color-rule);">Tilgung</th>
              <th style="text-align:right;padding:8px;border-bottom:1px solid var(--color-rule);">Restschuld</th>
            </tr>
          </thead>
          <tbody>
            ${rows
              .map(
                (r) => `<tr>
              <td style="padding:6px 8px;border-bottom:1px solid var(--color-rule);">${r.m}</td>
              <td style="padding:6px 8px;border-bottom:1px solid var(--color-rule);text-align:right;">${euro(r.payment, loc)}</td>
              <td style="padding:6px 8px;border-bottom:1px solid var(--color-rule);text-align:right;">${euro(r.interest, loc)}</td>
              <td style="padding:6px 8px;border-bottom:1px solid var(--color-rule);text-align:right;">${euro(r.principal, loc)}</td>
              <td style="padding:6px 8px;border-bottom:1px solid var(--color-rule);text-align:right;">${euro(r.balance, loc)}</td>
            </tr>`
              )
              .join('')}
          </tbody>
        </table>
      </div>`;
    const btn = el.querySelector('#amortCsvBtn');
    if (btn) {
      btn.onclick = () =>
        downloadCsv(
          'tilgungsplan.csv',
          ['Monat', 'Rate', 'Zinsen', 'Tilgung', 'Restschuld'],
          schedule.rows.map((r) => [
            r.m,
            r.payment.toFixed(2),
            r.interest.toFixed(2),
            r.principal.toFixed(2),
            r.balance.toFixed(2),
          ])
        );
    }
  }

  // Self-check
  if (typeof assert !== 'undefined') {
    /* noop in browser */
  } else {
    const s = amortSchedule(12000, 0, 12);
    if (Math.abs(s.rate - 1000) > 0.01) console.warn('calc-tools: zero-interest amort check failed');
  }

  global.CalcTools = { euro, annuityRate, amortSchedule, downloadCsv, downloadIcs, renderAmortTable };
})(typeof window !== 'undefined' ? window : globalThis);

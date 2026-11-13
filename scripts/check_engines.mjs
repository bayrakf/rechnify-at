// Regression check for the reference net-pay engines (copied into ~870 pages).
// Run: node scripts/check_engines.mjs   — fails loudly if a value drifts.
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

const slice = (file, from, to) => {
  const s = readFileSync(new URL(`../${file}`, import.meta.url), 'utf8');
  const a = s.indexOf(from), e = s.indexOf(to, a);
  return s.slice(a, s.indexOf('\n    }', e) + 6);
};
const document = { getElementById: () => null };

const de = new Function('document', slice('de/finanzen/gehaltsrechner.html', 'function est2026', 'return { netMonthly') + '; return calcTaxesDE;')(document);
const at = new Function(slice('finanzen/gehaltsrechner.html', 'const AT2026', 'return {') + '; return calcTaxes;')();

const near = (x, y, msg) => assert.ok(Math.abs(x - y) < 0.01, `${msg}: ${x.toFixed(2)} != ${y}`);
// DE 2026, Steuerklasse 1, kinderlos: Minijob, Uebergangsbereich, regulär
near(de(500).netMonthly, 482.00, 'DE 500 Minijob');
near(de(1500).svMonthly, 279.31, 'DE 1500 SV Uebergangsbereich');
near(de(1500).netMonthly, 1207.27, 'DE 1500 netto');
near(de(1999.99).agSvMonthly, de(2000).agSvMonthly, 'DE AG-SV stetig an 2000');
near(de(3000).netMonthly, 2054.42, 'DE 3000 netto');
// AT 2026, 14 Gehälter (Geringfuegigkeit, AV-Staffel, regulär)
near(at(500, true).netMonthly, 500.00, 'AT 500 geringfuegig');
near(at(2000, true).netMonthly, 1627.26, 'AT 2000 netto');
near(at(3000, true).netMonthly, 2174.08, 'AT 3000 netto');
near(at(5000, true).netMonthly, 3216.37, 'AT 5000 netto');
console.log('ok');

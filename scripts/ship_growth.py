#!/usr/bin/env python3
"""Ship recommended growth items: new tools, pillar, changelog, wiring."""
from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCRIPTS = """  <script src="/assets/js/analytics.js?v=3.1"></script>
  <script src="/assets/js/ui.js?v=3.1"></script>
  <script src="/assets/js/tools.js?v=3.1"></script>
  <script src="/assets/js/core.js?v=3.1"></script>
  <script src="/assets/js/calc-tools.js"></script>"""

CSS = """  <style>
    .calc-body{padding:24px}
    .input-group{margin-bottom:16px}
    .input-group label{display:block;margin-bottom:6px;font-weight:600}
    .input-group input,.input-group select{width:100%;padding:12px;border:1px solid var(--color-rule);border-radius:10px;background:var(--color-paper);color:var(--color-ink);font-size:16px}
    .input-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
    @media(max-width:600px){.input-row{grid-template-columns:1fr}}
    .result-box{margin-top:20px;padding:20px;border:1px solid var(--color-rule);border-radius:12px;background:var(--color-paper-2)}
    .result-item{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--color-rule)}
    .result-item:last-child{border-bottom:0}
    .result-item.highlight{font-weight:700;font-size:1.15em;color:var(--color-primary)}
    .help{font-size:.9rem;color:var(--color-ink-3);margin-top:12px}
    .ext-links a{margin-right:12px}
  </style>"""


def page(path: str, *, title: str, desc: str, lang: str, canon: str, h1: str, body: str, og_locale: str = "de_AT"):
    hreflang = f'  <link rel="alternate" hreflang="{lang}" href="{canon}" />\n  <link rel="alternate" hreflang="x-default" href="{canon}" />'
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | rechnify.at</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canon}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{hreflang}
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="https://rechnify.at/assets/images/og-share.png" />
  <meta property="og:locale" content="{og_locale}" />
  <meta property="og:site_name" content="rechnify.at" />
  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" />
{CSS}
</head>
<body>
  <header class="site-header"><div class="header-inner">
    <a href="/" class="site-logo"><span class="site-logo-text">rechnify<span>.at</span></span></a>
  </div></header>
  <main class="site-main">
    <div class="page-hero" style="padding-top:10px"><h1 style="margin-bottom:8px">{h1}</h1>
    <p class="subtitle">{desc}</p></div>
    <div class="card"><div class="calc-body">
{body}
    </div></div>
  </main>
{SCRIPTS}
</body>
</html>
"""
    out = BASE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", path)


def main():
    # --- Abfertigung AT ---
    page(
        "finanzen/abfertigungsrechner.html",
        title="Abfertigungsrechner Österreich 2026",
        desc="Abfertigung alt (Staffel) und neu (1,53 % BMSVG) schätzen. Orientierungswerte, keine Rechtsberatung.",
        lang="de-AT",
        canon="https://rechnify.at/finanzen/abfertigungsrechner.html",
        h1="Abfertigungsrechner Österreich",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="sys">System</label>
            <select id="sys"><option value="neu">Abfertigung NEU (Beginn ab 1.1.2003)</option><option value="alt">Abfertigung ALT (Beginn vor 2003)</option></select>
          </div>
          <div class="input-group"><label for="brutto">Monatsbrutto (€)</label>
            <input type="number" id="brutto" min="0" step="50" value="3000" /></div>
        </div>
        <div class="input-row">
          <div class="input-group"><label for="jahre">Dienstjahre</label>
            <input type="number" id="jahre" min="0" max="45" step="1" value="8" /></div>
          <div class="input-group"><label for="sz">Sonderzahlungen/Jahr (Monatsgehälter)</label>
            <input type="number" id="sz" min="0" max="14" step="1" value="2" title="AT oft 13.+14. = 2" /></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item highlight"><span>Schätzung</span><span id="res">—</span></div>
          <div class="result-item"><span>Details</span><span id="det">—</span></div>
          <p class="help">NEU: AG zahlt laufend <strong>1,53&nbsp;%</strong> des Entgelts (inkl. Sonderzahlungen) in eine BV-Kasse (BMSVG). Hier: grobe Summe Beiträge ohne Verzinsung/Verwaltungskosten. ALT: gesetzliche Staffel in Monatsentgelten (ab 3/5/10/15/20/25 Jahren → 2/3/4/6/9/12). Anspruch ALT hängt von Beendigungsart ab. Quellen: <a href="https://www.usp.gv.at/themen/mitarbeiter-und-gesundheit/beendigung-des-arbeitsverhaeltnisses/abfertigung.html" rel="noopener" target="_blank">USP.gv.at</a>, <a href="https://ris.bka.gv.at/" rel="noopener" target="_blank">RIS</a>.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const euro=n=>CalcTools.euro(n,'de-AT');
          const altMonths=y=>{if(y>=25)return 12;if(y>=20)return 9;if(y>=15)return 6;if(y>=10)return 4;if(y>=5)return 3;if(y>=3)return 2;return 0;};
          const calc=()=>{
            const b=+brutto.value||0, y=+jahre.value||0, sz=+szEl.value||0, sys=sysEl.value;
            if(sys==='alt'){
              const m=altMonths(y);
              res.textContent=euro(b*m);
              det.textContent=m?`${m} Monatsentgelte × ${euro(b)}`:'unter 3 Dienstjahren: kein ALT-Anspruch (Staffel)';
            }else{
              const months=Math.max(0,y*12-1); // ab 2. Monat
              const yearly=b*(12+sz);
              const sum=yearly/12*months*0.0153;
              res.textContent=euro(sum);
              det.textContent=`1,53% × ~${months} Beitragsmonate (ohne Zinsen)`;
            }
          };
          const brutto=document.getElementById('brutto'), jahre=document.getElementById('jahre'), szEl=document.getElementById('sz'), sysEl=document.getElementById('sys');
          const res=document.getElementById('res'), det=document.getElementById('det');
          [brutto,jahre,szEl,sysEl].forEach(e=>e.addEventListener('input',calc));
          sysEl.addEventListener('change',calc); calc();
        });
        </script>
""",
    )

    # --- Kündigung AT ---
    page(
        "arbeitszeit/kuendigungsfrist-rechner.html",
        title="Kündigungsfrist Rechner Österreich 2026",
        desc="Gesetzliche Mindestfristen nach AngG §20 / ABGB-Angleichung. KV/Vertrag können abweichen.",
        lang="de-AT",
        canon="https://rechnify.at/arbeitszeit/kuendigungsfrist-rechner.html",
        h1="Kündigungsfrist Rechner Österreich",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="who">Wer kündigt?</label>
            <select id="who"><option value="ag">Arbeitgeber</option><option value="an">Arbeitnehmer</option></select></div>
          <div class="input-group"><label for="jahre">Vollendete Dienstjahre</label>
            <input type="number" id="jahre" min="0" max="45" value="4" /></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item highlight"><span>Gesetzliche Frist</span><span id="res">—</span></div>
          <div class="result-item"><span>Hinweis Termin</span><span id="term">—</span></div>
          <p class="help">AG (AngG §20 Abs. 2): 6 Wochen (1.–2. DJ), 2 Monate (ab 3.), 3 Monate (ab 6.), 4 Monate (ab 16.), 5 Monate (ab 26.); typisch zum <strong>Kalendervierteljahr</strong>, sofern nichts anderes vereinbart (§20 Abs. 3: 15. oder Monatsende möglich). AN: 1 Monat zum Monatsende (§20 Abs. 4), vertraglich verlängerbar. Arbeiter:innen seit Angleichung ähnliche Mindestfristen — KV kann abweichen. <a href="https://www.wko.at/arbeitsrecht/kuendigungsfristen" rel="noopener" target="_blank">WKO</a>, <a href="https://www.ris.bka.gv.at/" rel="noopener" target="_blank">RIS AngG §20</a>.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const ag=(y)=>y>=25?'5 Monate':y>=15?'4 Monate':y>=5?'3 Monate':y>=2?'2 Monate':'6 Wochen';
          const calc=()=>{
            const y=+jahre.value||0;
            if(who.value==='ag'){res.textContent=ag(y);term.textContent='i.d.R. zum Quartalsende (vertraglich oft Monatsende/15.)';}
            else{res.textContent='1 Monat';term.textContent='zum letzten Tag des Kalendermonats';}
          };
          const who=document.getElementById('who'),jahre=document.getElementById('jahre'),res=document.getElementById('res'),term=document.getElementById('term');
          [who,jahre].forEach(e=>e.addEventListener('input',calc));who.addEventListener('change',calc);calc();
        });
        </script>
""",
    )

    # --- Kündigung DE ---
    page(
        "de/arbeitszeit/kuendigungsfrist-rechner.html",
        title="Kündigungsfrist Rechner Deutschland 2026",
        desc="Gesetzliche Fristen nach BGB §622. Vertrag/Tarif können länger sein.",
        lang="de-DE",
        og_locale="de_DE",
        canon="https://rechnify.at/de/arbeitszeit/kuendigungsfrist-rechner.html",
        h1="Kündigungsfrist Rechner Deutschland",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="who">Wer kündigt?</label>
            <select id="who"><option value="ag">Arbeitgeber</option><option value="an">Arbeitnehmer</option></select></div>
          <div class="input-group"><label for="jahre">Betriebszugehörigkeit (Jahre)</label>
            <input type="number" id="jahre" min="0" max="45" value="6" /></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item highlight"><span>Gesetzliche Frist</span><span id="res">—</span></div>
          <div class="result-item"><span>Zum</span><span id="term">—</span></div>
          <p class="help">BGB §622: AG-Fristen nach Betriebszugehörigkeit (ab 2/5/8/10/12/15/20 Jahren: 1–7 Monate zum Monatsende; darunter 4 Wochen zum 15. oder Monatsende). AN: 4 Wochen zum 15. oder Monatsende. Probezeit/besondere Vereinbarungen möglich. <a href="https://www.gesetze-im-internet.de/bgb/__622.html" rel="noopener" target="_blank">gesetze-im-internet.de §622</a>.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const ag=(y)=>{if(y>=20)return[7,'Monatsende'];if(y>=15)return[6,'Monatsende'];if(y>=12)return[5,'Monatsende'];if(y>=10)return[4,'Monatsende'];if(y>=8)return[3,'Monatsende'];if(y>=5)return[2,'Monatsende'];if(y>=2)return[1,'Monatsende'];return[0,'15. oder Monatsende'];};
          const calc=()=>{
            const y=+jahre.value||0;
            if(who.value==='an'){res.textContent='4 Wochen';term.textContent='15. oder Letzter des Kalendermonats';return;}
            const [m,t]=ag(y);res.textContent=m?`${m} Monat(e)`:'4 Wochen';term.textContent=t;
          };
          const who=document.getElementById('who'),jahre=document.getElementById('jahre'),res=document.getElementById('res'),term=document.getElementById('term');
          [who,jahre].forEach(e=>e.addEventListener('input',calc));who.addEventListener('change',calc);calc();
        });
        </script>
""",
    )

    # --- Jobwechsel Netto ---
    page(
        "finanzen/jobwechsel-netto-vergleich.html",
        title="Jobwechsel Netto-Vergleich Österreich",
        desc="Altes vs neues Brutto grob vergleichen (AT-Richtwert). Für exakte Netto: Gehaltsrechner.",
        lang="de-AT",
        canon="https://rechnify.at/finanzen/jobwechsel-netto-vergleich.html",
        h1="Jobwechsel: Netto alt vs neu",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="alt">Aktuelles Brutto (€/Monat)</label><input type="number" id="alt" value="3200" min="0" step="50" /></div>
          <div class="input-group"><label for="neu">Neues Brutto (€/Monat)</label><input type="number" id="neu" value="3800" min="0" step="50" /></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item"><span>Δ Brutto</span><span id="dB">—</span></div>
          <div class="result-item highlight"><span>Δ Netto (Schätzung AT)</span><span id="dN">—</span></div>
          <div class="result-item"><span>Δ Jahr (×14)</span><span id="dY">—</span></div>
          <p class="help">Schätzung: Netto ≈ Brutto − SV 18,07% (gedeckelt) − grobe Lohnsteuer. Kein Ersatz für den <a href="/finanzen/gehaltsrechner.html">Gehaltsrechner</a>. Auch <a href="/arbeitszeit/kuendigungsfrist-rechner.html">Kündigungsfrist</a> und <a href="/finanzen/abfertigungsrechner.html">Abfertigung</a> prüfen.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const approx=b=>{const sv=Math.min(b,6930)*0.1807;const base=(b-sv)*12;let t=0;if(base>13539)t=Math.min(base,21992)-13539;t*=0.2;if(base>21992)t+=(Math.min(base,36458)-21992)*0.3;if(base>36458)t+=(Math.min(base,70365)-36458)*0.4;if(base>70365)t+=(Math.min(base,104859)-70365)*0.48;if(base>104859)t+=(base-104859)*0.5;return b-sv-t/12;};
          const euro=n=>CalcTools.euro(n,'de-AT');
          const calc=()=>{const a=+alt.value||0,n=+neu.value||0;const na=approx(a),nn=approx(n);dB.textContent=euro(n-a);dN.textContent=euro(nn-na);dY.textContent=euro((nn-na)*14);};
          const alt=document.getElementById('alt'),neu=document.getElementById('neu'),dB=document.getElementById('dB'),dN=document.getElementById('dN'),dY=document.getElementById('dY');
          [alt,neu].forEach(e=>e.addEventListener('input',calc));calc();
        });
        </script>
""",
    )

    # --- Strom ---
    page(
        "alltag/stromkosten-rechner.html",
        title="Stromkosten Rechner",
        desc="Jahresstromkosten aus Verbrauch (kWh) und Arbeitspreis (€/kWh) plus Grundgebühr. Keine erfundenen Tarife.",
        lang="de-AT",
        canon="https://rechnify.at/alltag/stromkosten-rechner.html",
        h1="Stromkosten Rechner",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="kwh">Verbrauch kWh/Jahr</label><input type="number" id="kwh" value="3500" min="0" step="10" /></div>
          <div class="input-group"><label for="preis">Arbeitspreis €/kWh</label><input type="number" id="preis" value="0.28" min="0" step="0.01" /></div>
        </div>
        <div class="input-row">
          <div class="input-group"><label for="grund">Grundgebühr €/Jahr</label><input type="number" id="grund" value="120" min="0" step="1" /></div>
          <div class="input-group"><label for="pers">Personen (optional, nur Info)</label><input type="number" id="pers" value="2" min="1" step="1" /></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item highlight"><span>Kosten / Jahr</span><span id="jahr">—</span></div>
          <div class="result-item"><span>Kosten / Monat</span><span id="mon">—</span></div>
          <div class="result-item"><span>pro Person / Monat</span><span id="pp">—</span></div>
          <p class="help">Du trägst Preis & Verbrauch selbst ein (Rechnung/Tarifblatt). Keine Standard-Tarife erfunden.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const euro=n=>CalcTools.euro(n,'de-AT');
          const calc=()=>{const j=(+kwh.value||0)*(+preis.value||0)+(+grund.value||0);jahr.textContent=euro(j);mon.textContent=euro(j/12);pp.textContent=euro(j/12/Math.max(1,+pers.value||1));};
          ['kwh','preis','grund','pers'].forEach(id=>document.getElementById(id).addEventListener('input',calc));
          const kwh=document.getElementById('kwh'),preis=document.getElementById('preis'),grund=document.getElementById('grund'),pers=document.getElementById('pers');
          const jahr=document.getElementById('jahr'),mon=document.getElementById('mon'),pp=document.getElementById('pp');calc();
        });
        </script>
""",
    )

    # --- Mietkauf vs Miete ---
    page(
        "finanzen/mietkauf-vs-miete.html",
        title="Mietkauf vs Miete Rechner",
        desc="Vergleiche laufende Miete mit Kauf/Kredit über dieselbe Laufzeit. Mathe only — keine Förderungen erfunden.",
        lang="de-AT",
        canon="https://rechnify.at/finanzen/mietkauf-vs-miete.html",
        h1="Miete vs Kauf (Kredit)",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="miete">Monatsmiete (€)</label><input type="number" id="miete" value="900" min="0" step="10" /></div>
          <div class="input-group"><label for="preis">Kaufpreis (€)</label><input type="number" id="preis" value="280000" min="0" step="1000" /></div>
        </div>
        <div class="input-row">
          <div class="input-group"><label for="ek">Eigenkapital (€)</label><input type="number" id="ek" value="40000" min="0" step="1000" /></div>
          <div class="input-group"><label for="zins">Kreditzins p.a. (%)</label><input type="number" id="zins" value="3.5" min="0" step="0.1" /></div>
        </div>
        <div class="input-row">
          <div class="input-group"><label for="jahre">Vergleichszeitraum (Jahre)</label><input type="number" id="jahre" value="20" min="1" max="40" /></div>
          <div class="input-group"><label for="nk">Nebenkosten Kauf einmalig (€)</label><input type="number" id="nk" value="25000" min="0" step="500" title="GrESt, Notar etc. — selbst eintragen" /></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item"><span>Miete gesamt (Zeitraum)</span><span id="mSum">—</span></div>
          <div class="result-item"><span>Kreditrate / Monat</span><span id="rate">—</span></div>
          <div class="result-item"><span>Kauf Cash-out (EK+NK+Raten)</span><span id="kSum">—</span></div>
          <div class="result-item highlight"><span>Differenz (Miete − Kauf Cash)</span><span id="diff">—</span></div>
          <p class="help">Kauf lässt Eigentum übrig (Restschuld am Ende nicht abgezogen — Annuität tilgt bei voller Laufzeit). Keine Instandhaltung/Steuer/Förderung modelliert. Tilgungsplan: <a href="/finanzen/kreditrechner.html">Kreditrechner</a>.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const euro=n=>CalcTools.euro(n,'de-AT');
          const calc=()=>{
            const mon=(+jahre.value||0)*12; const mSumV=(+miete.value||0)*mon;
            const loan=Math.max(0,(+preis.value||0)-(+ek.value||0));
            const r=CalcTools.annuityRate(loan,+zins.value||0,mon);
            const kSumV=(+ek.value||0)+(+nk.value||0)+r*mon;
            mSum.textContent=euro(mSumV); rate.textContent=euro(r); kSum.textContent=euro(kSumV); diff.textContent=euro(mSumV-kSumV);
          };
          ['miete','preis','ek','zins','jahre','nk'].forEach(id=>document.getElementById(id).addEventListener('input',calc));
          const miete=document.getElementById('miete'),preis=document.getElementById('preis'),ek=document.getElementById('ek'),zins=document.getElementById('zins'),jahre=document.getElementById('jahre'),nk=document.getElementById('nk');
          const mSum=document.getElementById('mSum'),rate=document.getElementById('rate'),kSum=document.getElementById('kSum'),diff=document.getElementById('diff');calc();
        });
        </script>
""",
    )

    # --- Studienbeitrag AT ---
    page(
        "familie/studienbeitrag-rechner.html",
        title="Studienbeitrag & ÖH-Beitrag Rechner Österreich",
        desc="ÖH-Beitrag und Studienbeitrag (Drittstaat / Überschreitung) selbst mit offiziellen Sätzen eintragen — keine erfundenen Unitarife.",
        lang="de-AT",
        canon="https://rechnify.at/familie/studienbeitrag-rechner.html",
        h1="Studienbeitrag Österreich",
        body=r"""
        <div class="input-row">
          <div class="input-group"><label for="oeh">ÖH-Beitrag € / Semester</label><input type="number" id="oeh" value="24.70" min="0" step="0.01" /></div>
          <div class="input-group"><label for="sb">Studienbeitrag € / Semester</label><input type="number" id="sb" value="0" min="0" step="0.01" /></div>
        </div>
        <div class="input-row">
          <div class="input-group"><label for="sem">Semester</label><input type="number" id="sem" value="6" min="1" max="20" /></div>
          <div class="input-group"><label for="typ">Hinweis Tarif</label>
            <select id="typ"><option>AT/EU oft 0 € Studienbeitrag + ÖH</option><option>Drittstaat: oft 726,72 € / Sem. (selbst prüfen)</option><option>Überschreitung Toleranz: oft 363,36 € / Sem.</option></select></div>
        </div>
        <div class="result-box" id="resultBox">
          <div class="result-item highlight"><span>Gesamt Zeitraum</span><span id="tot">—</span></div>
          <div class="result-item"><span>pro Semester</span><span id="ps">—</span></div>
          <p class="help">Sätze ändern sich — trage den Betrag deiner Uni/FH ein. Infos: <a href="https://www.oesterreich.gv.at/" rel="noopener" target="_blank">oesterreich.gv.at</a>, ÖH deiner Hochschule.</p>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded',()=>{
          const euro=n=>CalcTools.euro(n,'de-AT');
          const calc=()=>{const p=(+oeh.value||0)+(+sb.value||0);ps.textContent=euro(p);tot.textContent=euro(p*(+sem.value||0));};
          ['oeh','sb','sem'].forEach(id=>document.getElementById(id).addEventListener('input',calc));
          const oeh=document.getElementById('oeh'),sb=document.getElementById('sb'),sem=document.getElementById('sem'),tot=document.getElementById('tot'),ps=document.getElementById('ps');calc();
        });
        </script>
""",
    )

    # --- Pillar Pendler ---
    (BASE / "blog/pendlerpauschale-oesterreich-2026.html").write_text(
        f"""<!DOCTYPE html>
<html lang="de-AT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pendlerpauschale Österreich 2026 – Komplett-Guide | rechnify.at</title>
  <meta name="description" content="Pendlerpauschale & Pendlereuro 2026: kleine/große Pauschale, Teilarbeitstage, Homeoffice. Mit Rechner und Quellen." />
  <link rel="canonical" href="https://rechnify.at/blog/pendlerpauschale-oesterreich-2026.html" />
  <meta name="robots" content="index, follow" />
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" />
</head>
<body>
<header class="site-header"><div class="header-inner"><a href="/" class="site-logo"><span class="site-logo-text">rechnify<span>.at</span></span></a></div></header>
<main class="site-main"><article class="content-section">
  <h1>Pendlerpauschale Österreich 2026 – Komplett-Guide</h1>
  <p class="updated">Stand: 2026-07-21</p>
  <p>Die Pendlerpauschale mindert die Lohnsteuer; der <strong>Pendlereuro</strong> ist ein zusätzlicher Absetzbetrag (2&nbsp;€ je Kilometer einfacher Fahrtstrecke und Jahr, aliquotiert). Höhe der Pauschale hängt von Distanz und Zumutbarkeit öffentlicher Verkehrsmittel ab (kleine vs. große Pendlerpauschale).</p>
  <h2>Schnell berechnen</h2>
  <p><a class="btn" href="/finanzen/pendlerrechner.html">Zum Pendlerrechner AT ➔</a> · <a href="/finanzen/pendler-oesterreich-vs-deutschland.html">AT vs DE</a> · <a href="/de/finanzen/pendlerrechner.html">Pendler DE</a></p>
  <h2>Was du brauchst</h2>
  <ul>
    <li>Einfache Fahrtstrecke Wohnsitz ↔ Arbeitsstätte (km)</li>
    <li>Ob Öffis zumutbar sind</li>
    <li>Anwesenheitstage (volle / 2/3 / 1/3 Pauschale)</li>
  </ul>
  <h2>Offizielle Quellen</h2>
  <p class="ext-links">
    <a href="https://www.bmf.gv.at/" rel="noopener" target="_blank">BMF</a>
    <a href="https://www.finanz.at/" rel="noopener" target="_blank">FinanzOnline / finanz.at</a>
    <a href="https://www.usp.gv.at/" rel="noopener" target="_blank">USP.gv.at</a>
  </p>
  <p class="help">Keine Rechtsberatung. Beträge im Rechner entsprechen den in der App hinterlegten Jahrestabellen.</p>
</article></main>
{SCRIPTS}
</body></html>
""",
        encoding="utf-8",
    )
    print("wrote blog/pendlerpauschale-oesterreich-2026.html")

    # --- Changelog ---
    (BASE / "changelog.html").write_text(
        """<!DOCTYPE html>
<html lang="de-AT">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Changelog & Tarif-Updates | rechnify.at</title>
  <meta name="description" content="Was ist neu auf rechnify.at: Rechner, Tarifstand 2026, SEO und Fixes." />
  <link rel="canonical" href="https://rechnify.at/changelog.html" />
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" />
</head>
<body>
<header class="site-header"><div class="header-inner"><a href="/" class="site-logo"><span class="site-logo-text">rechnify<span>.at</span></span></a></div></header>
<main class="site-main"><article class="content-section">
  <h1>Changelog & Tarif-Updates</h1>
  <p>Transparenz für Nutzer und Crawler. Rechtliche Sätze nur nach offiziellen Quellen.</p>
  <h2>2026-07-21</h2>
  <ul>
    <li>Neu: Abfertigungsrechner AT, Kündigungsfrist AT/DE, Jobwechsel-Netto, Stromkosten, Mietkauf vs Miete, Studienbeitrag</li>
    <li>Pillar: Pendlerpauschale Österreich 2026</li>
    <li>Embed & interne Verlinkung verstärkt</li>
  </ul>
  <h2>2026-07-18</h2>
  <ul>
    <li>AT Brutto-Netto 10er-Schritte, DE Hubs, Städte-Seiten, Sitemap-Scan</li>
    <li>Leasing: Barkauf/Kredit/Leasing + Verdict</li>
    <li>Rechner-Upgrades: Tilgung, ICS, MwSt-Positionen</li>
  </ul>
  <p><a href="/embed.html">Rechner einbinden</a> · <a href="/blog/">Blog</a></p>
</article></main>
</body></html>
""",
        encoding="utf-8",
    )
    print("wrote changelog.html")

    # Patch embed with more tools
    emb = BASE / "embed.html"
    if emb.exists():
        t = emb.read_text(encoding="utf-8")
        if "abfertigungsrechner" not in t:
            t = t.replace(
                "</article>",
                """
      <h2>Beliebte Embeds</h2>
      <ul class="hub-list">
        <li><code>&lt;iframe src="https://rechnify.at/finanzen/gehaltsrechner.html" width="100%" height="720" loading="lazy"&gt;&lt;/iframe&gt;</code></li>
        <li><code>&lt;iframe src="https://rechnify.at/finanzen/abfertigungsrechner.html" ...&gt;</code></li>
        <li><code>&lt;iframe src="https://rechnify.at/arbeitszeit/kuendigungsfrist-rechner.html" ...&gt;</code></li>
        <li><code>&lt;iframe src="https://rechnify.at/alltag/kalorienrechner.html" ...&gt;</code></li>
      </ul>
      <p>Mehr Tools: <a href="/changelog.html">Changelog</a></p>
</article>""",
                1,
            )
            emb.write_text(t, encoding="utf-8")
            print("patched embed.html")

    print("DONE pages")


if __name__ == "__main__":
    main()

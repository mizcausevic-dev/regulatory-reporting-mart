# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    for script in [
        WAREHOUSE / "schema.sql",
        WAREHOUSE / "seed.sql",
        WAREHOUSE / "marts" / "mart_reporting_readiness.sql",
        WAREHOUSE / "marts" / "mart_deadline_pressure.sql",
    ]:
        conn.executescript(script.read_text(encoding="utf-8"))
    return conn


def rows(conn: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql).fetchall()]


def build_dashboard() -> dict[str, Any]:
    conn = connect()
    readiness = rows(
        conn,
        """
        SELECT *
        FROM mart_reporting_readiness
        ORDER BY readiness_score DESC, late_risk DESC
        """,
    )
    pressure = rows(conn, "SELECT * FROM mart_deadline_pressure")
    summary = {
        "generated_on": str(date.today()),
        "docket_count": len(readiness),
        "high_severity": sum(1 for row in readiness if row["severity"] == "high"),
        "blocked_packets": sum(row["blocked_or_draft_packets"] for row in readiness),
        "avg_readiness": round(sum(row["readiness_score"] for row in readiness) / len(readiness), 1),
        "max_late_risk": max(row["late_risk"] for row in readiness),
        "readiness_rows": readiness,
        "pressure_rows": pressure,
    }
    return summary


def status_badge(status: str) -> str:
    palette = {"green": "green", "yellow": "warn", "red": "bad"}
    tone = palette.get(status, "cyan")
    return f'<span class="status {tone}">{status.upper()}</span>'


def base_css() -> str:
    return """
    :root{
      --bg:#070a0f; --panel:#0b1220; --panel2:#0a1426;
      --line:rgba(120,255,170,.18); --line2:rgba(120,255,170,.10);
      --text:#e9f3ff; --muted:rgba(233,243,255,.72); --muted2:rgba(233,243,255,.55);
      --bert:#37ff8b; --bert2:#19c7ff; --warn:#ffcc66; --bad:#ff5c7a; --plum:#b88cff;
      --shadow:0 18px 60px rgba(0,0,0,.55);
      --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Courier New",monospace;
      --sans:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
    }
    *{box-sizing:border-box} html,body{height:100%}
    body{margin:0;font-family:var(--sans);color:var(--text);background:
      radial-gradient(1200px 600px at 20% -10%, rgba(55,255,139,.18), transparent 60%),
      radial-gradient(900px 520px at 90% 0%, rgba(25,199,255,.16), transparent 55%),
      radial-gradient(1000px 600px at 50% 110%, rgba(55,255,139,.10), transparent 60%),
      linear-gradient(180deg,#05070c 0%,#070a0f 35%,#05070c 100%);}
    .grid-bg{position:fixed;inset:0;pointer-events:none;opacity:.12;z-index:-1;background-image:
      linear-gradient(to right, rgba(55,255,139,.14) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(55,255,139,.10) 1px, transparent 1px);
      background-size:46px 46px;mask-image: radial-gradient(900px 600px at 40% 10%, #000 60%, transparent 100%);}
    .wrap{max-width:1280px;margin:0 auto;padding:24px 22px 80px}
    .topbar{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;border-bottom:1px solid var(--line2);padding-bottom:14px;margin-bottom:22px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase}
    .topbar .left{color:var(--bert)}
    .hero,.panel,.tablewrap{background:linear-gradient(180deg, rgba(11,18,32,.95), rgba(8,14,26,.92));border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow)}
    .herorow{display:grid;grid-template-columns:1.45fr .85fr;gap:18px} @media (max-width:1000px){.herorow{grid-template-columns:1fr}}
    .hero{padding:28px 28px 24px;border-top:2px solid var(--bert2)}
    .hero h1{font-size:64px;line-height:.95;margin:0 0 18px;font-weight:800;letter-spacing:-.5px}
    @media (max-width:700px){.hero h1{font-size:42px}}
    .hero p,.panel p{color:var(--muted);font-size:15px;line-height:1.55}
    .chiprow{display:flex;flex-wrap:wrap;gap:8px}
    .chip,.status,.notepill{font-family:var(--mono);font-size:11px;padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:rgba(6,10,18,.4);color:var(--muted)}
    .side{display:flex;flex-direction:column;gap:14px}
    .panel{padding:18px}
    .panel .lbl,.section-note{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--bert2)}
    .panel h3{margin:8px 0 6px;font-size:28px;line-height:1.02}
    .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px} @media (max-width:900px){.kpis{grid-template-columns:repeat(2,1fr)}} @media (max-width:640px){.kpis{grid-template-columns:1fr}}
    .kpi,.card{border:1px solid var(--line);border-radius:16px;padding:16px;background:linear-gradient(180deg, rgba(11,18,32,.85), rgba(8,14,26,.65))}
    .kpi .v{font-family:var(--mono);font-size:28px;font-weight:700}
    .kpi .lbl{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-top:6px}
    .kpi .h{font-size:12px;color:var(--muted);line-height:1.45;margin-top:8px}
    .green{color:var(--bert)} .cyan{color:var(--bert2)} .warn{color:var(--warn)} .plum{color:var(--plum)} .bad{color:var(--bad)}
    .section{margin-top:34px}
    .sh{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding-bottom:10px;border-bottom:1px solid var(--line2);margin-bottom:14px}
    .sh h2{margin:0;font-size:24px;font-weight:600}
    .sh .note{font-family:var(--mono);font-size:11px;color:var(--muted2);letter-spacing:.16em;text-transform:uppercase}
    .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px} @media (max-width:1000px){.cards{grid-template-columns:1fr}}
    .card h3{margin:8px 0 8px;font-size:22px}
    .card .eyebrow{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--bert)}
    table{width:100%;border-collapse:collapse} th,td{padding:13px 14px;text-align:left;font-size:13.5px;vertical-align:top}
    thead th{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted2);border-bottom:1px solid var(--line);background:rgba(11,18,32,.5)}
    tbody td{color:var(--muted);border-bottom:1px solid var(--line2)} tbody tr:hover{background:rgba(55,255,139,.03)}
    .tablewrap{padding:0;overflow:hidden}
    .status{display:inline-block;padding:4px 9px;border-radius:6px;border:1px solid currentColor}
    .quote{margin-top:34px;border:1px solid rgba(55,255,139,.22);background:radial-gradient(700px 200px at 0% 0%, rgba(55,255,139,.10), transparent 60%),linear-gradient(180deg, rgba(11,18,32,.92), rgba(8,14,26,.88));border-radius:18px;padding:24px 26px}
    .quote .lbl{font-family:var(--mono);font-size:11px;color:var(--bert);letter-spacing:.22em;text-transform:uppercase}
    .quote .q{margin-top:12px;font-size:32px;line-height:1.25;font-weight:600;max-width:1000px}
    footer{margin-top:30px;padding-top:14px;border-top:1px dashed var(--line2);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-family:var(--mono);font-size:11px;color:var(--muted2);letter-spacing:.08em}
    a{color:var(--bert2);text-decoration:none}
    """


def page(title: str, description: str, content: str, canonical: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}">
  <style>{base_css()}</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="wrap">{content}</div>
</body>
</html>"""


def overview_html(data: dict[str, Any]) -> str:
    readiness_rows = "".join(
        f"""
        <tr>
          <td><b>{row['title']}</b><br><span class="section-note">{row['docket_id']} · {row['agency_label']}</span></td>
          <td>{row['readiness_score']}</td>
          <td>{row['blockers']}</td>
          <td>{row['late_risk']}</td>
          <td>{status_badge('green' if row['readiness_score'] >= 80 else 'yellow' if row['readiness_score'] >= 70 else 'red')}</td>
        </tr>
        """
        for row in data["readiness_rows"]
    )

    pressure_cards = "".join(
        f"""
        <div class="card">
          <div class="eyebrow">{row['docket_id']}</div>
          <h3>{row['title']}</h3>
          <p>Due {row['due_date']} with late-risk {row['late_risk']} and {row['blockers']} blockers still open across the reporting packet.</p>
          <p>{status_badge(row['pressure_status'])}</p>
        </div>
        """
        for row in data["pressure_rows"]
    )

    return f"""
    <div class="topbar">
      <div class="left">reporting mart · sql + python operator surface</div>
      <div class="right">
        <div>reporting.kineticgain.com</div>
        <div>generated {data['generated_on']} · regulated reporting posture</div>
      </div>
    </div>
    <div class="herorow">
      <section class="hero">
        <div class="chiprow">
          <span class="chip">Regulatory mart</span>
          <span class="chip">deadline pressure</span>
          <span class="chip">evidence posture</span>
          <span class="chip">operator reporting</span>
        </div>
        <h1>Make reporting readiness visible before deadline pressure leaks into executive risk.</h1>
        <p>A warehouse-style reference implementation for Kinetic Gain OS: model dockets, evidence packets, blockers, and submission posture in SQL, then publish a crawlable operator surface from the same mart output.</p>
        <div class="chiprow">
          <span class="notepill">/reporting-lane/</span>
          <span class="notepill">/deadline-pressure/</span>
          <span class="notepill">/evidence-posture/</span>
        </div>
      </section>
      <aside class="side">
        <div class="panel">
          <div class="lbl">dockets</div>
          <h3 class="green">{data['docket_count']}</h3>
          <p>Active reporting and disclosure packets represented in the mart output.</p>
        </div>
        <div class="panel">
          <div class="lbl">avg readiness</div>
          <h3 class="cyan">{data['avg_readiness']}</h3>
          <p>Average submission readiness across the current docket portfolio.</p>
        </div>
        <div class="panel">
          <div class="lbl">blocked packets</div>
          <h3 class="warn">{data['blocked_packets']}</h3>
          <p>Evidence packets still in draft or blocked state before submission closeout.</p>
        </div>
      </aside>
    </div>
    <section class="section">
      <div class="sh"><h2>Mart KPIs</h2><div class="note">operator snapshot</div></div>
      <div class="kpis">
        <div class="kpi"><div class="v green">{data['docket_count']}</div><div class="lbl">tracked dockets</div><div class="h">Warehouse rows grouped into one reporting portfolio.</div></div>
        <div class="kpi"><div class="v warn">{data['high_severity']}</div><div class="lbl">high severity</div><div class="h">Packets with material regulatory or commercial risk if delayed.</div></div>
        <div class="kpi"><div class="v plum">{data['blocked_packets']}</div><div class="lbl">blocked evidence</div><div class="h">Packets still not clean enough for release-safe reporting.</div></div>
        <div class="kpi"><div class="v bad">{data['max_late_risk']}</div><div class="lbl">max late risk</div><div class="h">Highest late-risk score across current submissions.</div></div>
      </div>
    </section>
    <section class="section">
      <div class="sh"><h2>Deadline pressure</h2><div class="note">what needs intervention</div></div>
      <div class="cards">{pressure_cards}</div>
    </section>
    <section class="section">
      <div class="sh"><h2>Reporting readiness</h2><div class="note">mart output</div></div>
      <div class="tablewrap">
        <table>
          <thead><tr><th>Docket</th><th>Readiness</th><th>Blockers</th><th>Late risk</th><th>Status</th></tr></thead>
          <tbody>{readiness_rows}</tbody>
        </table>
      </div>
    </section>
    <section class="quote">
      <div class="lbl">why this matters</div>
      <div class="q">Kinetic Gain Embedded tie-back: this repo proves the portfolio can publish warehouse-style reporting surfaces where SQL models, deadlines, evidence packets, and operator posture stay legible in one place.</div>
    </section>
    <footer>
      <span>regulatory-reporting-mart · SQL mart + Python publisher</span>
      <span><a href="/docs/">Docs</a> · <a href="/verification/">Verification</a></span>
    </footer>
    """


def generic_html(title: str, note: str, bullets: list[str]) -> str:
    items = "".join(f"<li>{bullet}</li>" for bullet in bullets)
    return f"""
    <div class="topbar">
      <div class="left">reporting mart · regulated workflow</div>
      <div class="right"><div>{title}</div></div>
    </div>
    <section class="hero">
      <div class="section-note">{note}</div>
      <h1>{title}</h1>
      <p>{" ".join(bullets)}</p>
      <ul style="color:var(--muted);line-height:1.8">{items}</ul>
      <p><a href="/">Return to overview</a></p>
    </section>
    """


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_site(out_dir: str | Path | None = None, domain: str = "reporting.kineticgain.com") -> Path:
    data = build_dashboard()
    out = ROOT / "site" if out_dir is None else ROOT / Path(out_dir)
    out.mkdir(exist_ok=True)
    write(out / "index.html", page(
        "Regulatory Reporting Mart",
        "Warehouse-style reporting mart for docket readiness, evidence packets, and deadline pressure.",
        overview_html(data),
        f"https://{domain}/",
    ))
    write(out / "reporting-lane" / "index.html", page(
        "Reporting Lane",
        "Lane view for docket reporting and submission readiness.",
        generic_html("Reporting lane", "lane view", [
            "Each docket is tracked as an operator packet, not a spreadsheet residue.",
            "The mart keeps owner, due date, blockers, and evidence posture in one inspectable layer.",
            "This route is where reporting readiness becomes reviewable by ops, legal, and leadership.",
        ]),
        f"https://{domain}/reporting-lane/",
    ))
    write(out / "deadline-pressure" / "index.html", page(
        "Deadline Pressure",
        "Deadline pressure view for the regulatory reporting mart.",
        generic_html("Deadline pressure", "what is slipping", [
            "Late-risk and blocker counts are ranked directly from the mart output.",
            "The reporting surface highlights where filing posture is red before leadership finds out via surprise miss.",
            "This keeps the warehouse output tied to operator escalation, not passive dashboards.",
        ]),
        f"https://{domain}/deadline-pressure/",
    ))
    write(out / "evidence-posture" / "index.html", page(
        "Evidence Posture",
        "Evidence and packet posture view for the regulatory reporting mart.",
        generic_html("Evidence posture", "packet quality", [
            "Evidence packets are counted and status-ranked so reporting posture is defendable.",
            "Blocked and draft packets stay visible in the same mart that powers the summary layer.",
            "The repo demonstrates how warehouse models and approval context can ship together.",
        ]),
        f"https://{domain}/evidence-posture/",
    ))
    write(out / "verification" / "index.html", page(
        "Verification",
        "Verification notes for the regulatory reporting mart.",
        generic_html("Verification", "release gate", [
            "SQLite executes the schema, seed, and mart SQL scripts locally.",
            "Python tests verify the mart summary and output invariants.",
            "A static Pages bundle publishes the resulting operator surface with robots and sitemap.",
        ]),
        f"https://{domain}/verification/",
    ))
    write(out / "docs" / "index.html", page(
        "Docs",
        "Documentation for the regulatory reporting mart reference implementation.",
        generic_html("Docs", "reference implementation", [
            "This repo extends the language and platform atlas through warehouse-style SQL assets.",
            "The mart is local-first, auditable, and designed to explain deadline pressure to buyers and recruiters.",
            "It proves the portfolio can ship reporting surfaces as data contracts, not only front-end dashboards.",
        ]),
        f"https://{domain}/docs/",
    ))
    write(out / "api" / "dashboard.json", json.dumps(data, indent=2))
    write(out / "CNAME", domain + "\n")
    write(out / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: https://{domain}/sitemap.xml\n")
    today = date.today().isoformat()
    write(out / "sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{domain}/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/reporting-lane/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/deadline-pressure/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/evidence-posture/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/verification/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/docs/</loc><lastmod>{today}</lastmod></url>
</urlset>
""")
    write(out / "404.html", (out / "index.html").read_text(encoding="utf-8"))
    return out

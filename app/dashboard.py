from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


def _bar_svg(df: pd.DataFrame, label_col: str, value_col: str, width: int = 760, height: int = 260) -> str:
    if df.empty or label_col not in df or value_col not in df:
        return "<p>No data available.</p>"
    data = df[[label_col, value_col]].head(10).copy()
    max_value = float(data[value_col].max()) or 1.0
    bar_height = 22
    gap = 10
    left = 150
    rows = []
    for idx, row in data.reset_index(drop=True).iterrows():
        y = 20 + idx * (bar_height + gap)
        value = float(row[value_col])
        bar_width = int((width - left - 90) * value / max_value)
        label = escape(str(row[label_col]))
        rows.append(
            f'<text x="0" y="{y + 16}" class="label">{label}</text>'
            f'<rect x="{left}" y="{y}" width="{bar_width}" height="{bar_height}" rx="3"></rect>'
            f'<text x="{left + bar_width + 8}" y="{y + 16}" class="value">{value:,.0f}</text>'
        )
    svg_height = max(height, 40 + len(data) * (bar_height + gap))
    return (
        f'<svg viewBox="0 0 {width} {svg_height}" role="img">'
        "<style>.label{font:13px Arial;fill:#334155}.value{font:12px Arial;fill:#475569}"
        "rect{fill:#2563eb}</style>"
        + "".join(rows)
        + "</svg>"
    )


def _line_svg(df: pd.DataFrame, label_col: str, value_col: str, width: int = 760, height: int = 260) -> str:
    if df.empty or len(df) < 2:
        return "<p>No data available.</p>"
    data = df[[label_col, value_col]].copy()
    values = [float(v) for v in data[value_col]]
    min_v, max_v = min(values), max(values)
    spread = max(max_v - min_v, 1.0)
    points = []
    for idx, value in enumerate(values):
        x = 40 + idx * ((width - 80) / max(len(values) - 1, 1))
        y = height - 40 - ((value - min_v) / spread) * (height - 80)
        points.append((x, y))
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    circles = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3"></circle>' for x, y in points)
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img">'
        "<style>polyline{fill:none;stroke:#16a34a;stroke-width:3}circle{fill:#16a34a}"
        "text{font:12px Arial;fill:#475569}</style>"
        f'<polyline points="{polyline}"></polyline>{circles}'
        f'<text x="40" y="22">max: {max_v:,.0f}</text>'
        f'<text x="40" y="{height - 10}">min: {min_v:,.0f}</text>'
        "</svg>"
    )


def build_dashboard(results: dict, insights: list[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    kpis = results["kpis"]
    monthly = results["monthly"]
    category = results["category"]
    channel = results["channel"]
    inventory = results["inventory_risk"]

    inventory_risks = 0
    if isinstance(inventory, pd.DataFrame) and not inventory.empty and "stock_status" in inventory:
        inventory_risks = int((inventory["stock_status"] != "normal").sum())

    insight_items = "\n".join(f"<li>{escape(item)}</li>" for item in insights)
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YRH Enterprise Data Agent Dashboard</title>
  <style>
    body {{ margin:0; font-family: Arial, sans-serif; color:#111827; background:#f8fafc; }}
    header {{ padding:28px 36px; background:#111827; color:white; }}
    main {{ max-width:1100px; margin:0 auto; padding:24px; }}
    section {{ margin:22px 0; padding:20px; background:white; border:1px solid #e5e7eb; border-radius:8px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; }}
    .kpi {{ padding:14px; background:#f1f5f9; border-radius:6px; }}
    .kpi b {{ display:block; font-size:22px; margin-top:6px; }}
    h1,h2 {{ margin:0 0 14px; }}
    li {{ margin:7px 0; }}
  </style>
</head>
<body>
<header>
  <h1>YRH Enterprise Data Agent</h1>
  <p>Offline business analysis dashboard generated from CSV tables.</p>
</header>
<main>
  <section>
    <h2>Core KPIs</h2>
    <div class="kpis">
      <div class="kpi">Net Sales<b>{kpis['net_sales']:,.2f}</b></div>
      <div class="kpi">Orders<b>{kpis['orders']:,}</b></div>
      <div class="kpi">Active Users<b>{kpis['active_users']:,}</b></div>
      <div class="kpi">AOV<b>{kpis['avg_order_value']:,.2f}</b></div>
      <div class="kpi">Refund Rate<b>{kpis['refund_rate']:.2%}</b></div>
      <div class="kpi">Inventory Risks<b>{inventory_risks}</b></div>
    </div>
  </section>
  <section>
    <h2>Insights</h2>
    <ul>{insight_items}</ul>
  </section>
  <section>
    <h2>Monthly Net Sales</h2>
    {_line_svg(monthly, "month", "net_sales")}
  </section>
  <section>
    <h2>Category Net Sales</h2>
    {_bar_svg(category, "category", "net_sales")}
  </section>
  <section>
    <h2>Channel Net Sales</h2>
    {_bar_svg(channel, "channel", "net_sales")}
  </section>
</main>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")


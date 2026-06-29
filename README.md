# YRH Enterprise Data Agent

A lightweight, practical enterprise data analysis workflow for retail and e-commerce scenarios.

This project turns CSV business tables into a data quality report, processed analysis tables, a static HTML dashboard, and a Markdown business analysis report. It is designed as a resume-ready data analysis project and a foundation for a future AI data analyst agent.

## Why This Project Exists

Many beginner data analysis projects stop at charts. Real business analysis needs a fuller workflow:

```text
Business question
-> Data contract
-> Data quality check
-> KPI calculation
-> Product/user/channel/inventory analysis
-> Dashboard
-> Written business report
-> Resume/GitHub presentation
```

This repository implements that workflow in a small, inspectable codebase.

## Features

- Generate a realistic demo dataset for a small retail/e-commerce company
- Load order, product, user, inventory, marketing, and review CSV tables
- Produce a table-level and field-level data quality report
- Calculate business KPIs:
  - GMV
  - net sales
  - order count
  - active users
  - average order value
  - refund rate
  - gross margin
- Analyze:
  - monthly sales
  - category performance
  - channel performance and ROI
  - user segments
  - inventory shortage/overstock risks
  - review rating distribution
- Generate:
  - `reports/final_report.md`
  - `reports/data_quality_report.md`
  - `dashboard/index.html`
  - processed CSV outputs under `data/processed/`

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/yrh-enterprise-data-agent.git
cd yrh-enterprise-data-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the demo workflow

```bash
python run.py demo
```

After running, open:

```text
dashboard/index.html
reports/final_report.md
reports/data_quality_report.md
data/processed/
```

## Use Your Own Data

Prepare a folder containing at least:

```text
orders.csv
products.csv
```

Recommended optional tables:

```text
users.csv
inventory.csv
marketing.csv
reviews.csv
```

Run:

```bash
python run.py analyze --data-dir "path/to/your/csv_folder"
```

See the data contract:

```text
docs/data-contract.md
```

## Required Minimum Fields

`orders.csv`

```text
order_id,user_id,product_id,order_date,channel,quantity,unit_price,discount_rate,refund_flag,amount
```

`products.csv`

```text
product_id,product_name,category,brand,cost,price
```

## Project Structure

```text
yrh-enterprise-data-agent/
├── app/                         Core pipeline code
├── dashboard/                   Generated static HTML dashboard
├── data/
│   ├── raw/                     Demo or raw CSV files
│   └── processed/               Analysis outputs
├── docs/                        Architecture, data contract, project references
├── reports/                     Markdown reports
├── skills/                      Reusable data analysis agent skill drafts
├── NOTICE.md                    Reference project notice
├── requirements.txt
└── run.py                       One-command entry point
```

## Architecture

```text
CSV tables
-> loader
-> profiler
-> business analyzer
-> dashboard generator
-> report writer
-> future AI agent layer
```

Core modules:

| Module | File | Responsibility |
| --- | --- | --- |
| Mock data | `app/mock_data.py` | Generate demo business data |
| Loader | `app/loader.py` | Load and parse CSV tables |
| Profiler | `app/profiler.py` | Build data quality reports |
| Analyzer | `app/analyzer.py` | Calculate KPIs and business analysis tables |
| Dashboard | `app/dashboard.py` | Generate a dependency-light HTML dashboard |
| Report writer | `app/report_writer.py` | Generate Markdown business reports |
| CLI entry | `run.py` | Run demo or analyze user data |

## Reference Projects

This project was inspired by:

- [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills): reusable skill structure
- [PandasAI](https://github.com/Sinaptik-AI/pandas-ai): natural-language data analysis product direction
- [LIDA](https://github.com/microsoft/lida): data summary, visualization, and explanation workflow

Their source code is not copied into this project. The implementation here is a lightweight workflow built for business data analysis practice.

## Resume Description

```text
Built a lightweight enterprise data analysis workflow for retail/e-commerce scenarios. The project generates or loads order, product, user, inventory, marketing, and review data; performs data quality profiling and KPI calculation with Python/Pandas; analyzes sales, category, channel, user segment, inventory, and review performance; and automatically generates a static HTML dashboard and Markdown business analysis report.
```

## Roadmap

```text
v1: Pandas offline workflow + HTML dashboard + Markdown report
v2: Add DuckDB/SQLite SQL analysis layer
v3: Add Streamlit interactive dashboard
v4: Add LLM-powered question answering and report generation skills
v5: Integrate with BI/data-agent systems such as DataEase or DB-GPT
```

## License

MIT License.


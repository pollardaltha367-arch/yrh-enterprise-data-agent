# Architecture

## Goal

Build a practical enterprise data analysis workflow that can run before a full BI or data agent platform is deployed.

## Pipeline

```text
Data source
-> Loader
-> Profiler
-> Business analyzer
-> Dashboard generator
-> Report writer
-> Skill/Agent extension
```

## Modules

| Module | File | Responsibility |
| --- | --- | --- |
| Mock data | `app/mock_data.py` | Generate a realistic retail dataset for demos |
| Loader | `app/loader.py` | Load CSV tables and parse date fields |
| Profiler | `app/profiler.py` | Generate table and field quality reports |
| Analyzer | `app/analyzer.py` | Calculate sales, product, channel, user, inventory, and review metrics |
| Dashboard | `app/dashboard.py` | Generate a static HTML dashboard without heavy dependencies |
| Report writer | `app/report_writer.py` | Generate Markdown reports |
| Entry | `run.py` | One-command workflow |

## Design Choice

The first version avoids heavy frameworks. This is intentional:

- It can run in a weak local environment.
- It keeps the business logic visible.
- It is easier to explain in a resume or interview.
- It can later connect to DuckDB, Streamlit, DataEase, or DB-GPT.


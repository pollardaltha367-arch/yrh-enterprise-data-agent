from __future__ import annotations

import argparse
from pathlib import Path

from app.analyzer import analyze_retail_business, generate_insights
from app.dashboard import build_dashboard
from app.loader import load_tables, require_tables
from app.mock_data import generate_mock_data
from app.profiler import profile_tables, table_summary
from app.report_writer import write_profile_report, write_report


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "reports"
DEFAULT_DASHBOARD = PROJECT_ROOT / "dashboard" / "index.html"


def run_demo(args: argparse.Namespace) -> None:
    generate_mock_data(DEFAULT_DATA_DIR, seed=args.seed)
    run_analysis(args)


def run_analysis(args: argparse.Namespace) -> None:
    data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR
    processed_dir = Path(args.processed_dir) if args.processed_dir else DEFAULT_PROCESSED_DIR
    report_dir = Path(args.report_dir) if args.report_dir else DEFAULT_REPORT_DIR

    tables = load_tables(data_dir)
    if not tables:
        raise SystemExit(f"No CSV files found in {data_dir}. Run `demo` first or pass --data-dir.")
    require_tables(tables, ["orders", "products"])

    processed_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    table_report = table_summary(tables)
    field_report = profile_tables(tables)
    table_report.to_csv(processed_dir / "table_summary.csv", index=False, encoding="utf-8-sig")
    field_report.to_csv(processed_dir / "field_profile.csv", index=False, encoding="utf-8-sig")
    write_profile_report(table_report, field_report, report_dir / "data_quality_report.md")

    results = analyze_retail_business(tables)
    insights = generate_insights(results)

    for name, value in results.items():
        if hasattr(value, "to_csv"):
            value.to_csv(processed_dir / f"{name}.csv", index=False, encoding="utf-8-sig")

    write_report(results, insights, report_dir / "final_report.md")
    build_dashboard(results, insights, Path(args.dashboard) if args.dashboard else DEFAULT_DASHBOARD)

    print("Analysis completed.")
    print(f"Data quality report: {report_dir / 'data_quality_report.md'}")
    print(f"Final report: {report_dir / 'final_report.md'}")
    print(f"Dashboard: {Path(args.dashboard) if args.dashboard else DEFAULT_DASHBOARD}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YRH Enterprise Data Agent")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="Generate mock retail data and run the full pipeline.")
    demo.add_argument("--seed", type=int, default=42)
    demo.add_argument("--data-dir", default=None)
    demo.add_argument("--processed-dir", default=None)
    demo.add_argument("--report-dir", default=None)
    demo.add_argument("--dashboard", default=None)
    demo.set_defaults(func=run_demo)

    analyze = sub.add_parser("analyze", help="Run analysis on CSV tables in a folder.")
    analyze.add_argument("--data-dir", default=None)
    analyze.add_argument("--processed-dir", default=None)
    analyze.add_argument("--report-dir", default=None)
    analyze.add_argument("--dashboard", default=None)
    analyze.set_defaults(func=run_analysis)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    parsed.func(parsed)


# Reference Projects

## Scientific Agent Skills

Repository: https://github.com/K-Dense-AI/scientific-agent-skills

What to learn:

- Organize reusable skills in folders.
- Write clear task instructions for agents.
- Keep input, process, output, and quality standards explicit.

How this project uses the idea:

- `skills/` stores data-analysis-oriented Skill documents.
- Each Skill is narrow and reusable.

## PandasAI

Repository: https://github.com/Sinaptik-AI/pandas-ai

What to learn:

- Natural language can be translated into data analysis operations.
- DataFrame analysis needs guardrails and context.
- User questions should map to executable code and interpretable results.

How this project uses the idea:

- Current version keeps analysis deterministic.
- Future version can add natural-language question routing.

## LIDA

Repository: https://github.com/microsoft/lida

What to learn:

- Data analysis can be broken into summary, goal, visualization, and explanation.
- Visualization should be tied to analysis questions.

How this project uses the idea:

- `app/dashboard.py` generates charts from business metrics.
- `app/report_writer.py` turns metrics into a report.

## Why Not Directly Use DB-GPT or DataEase in v1

They are useful but heavy. For the first resume-ready version, the priority is:

```text
run successfully -> show business value -> produce report -> explain clearly
```

After the core workflow is stable, DB-GPT/DataEase can be added as advanced integrations.


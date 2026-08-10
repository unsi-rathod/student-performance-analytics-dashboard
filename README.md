# Student Performance Analytics Dashboard

An end-to-end analytics pipeline that cleans, engineers, and visualizes academic performance data for 150 students across 3 sections — built to flag at-risk students early and pinpoint exactly which question types (comprehension vs. execution gaps) need intervention.

## Overview

Raw exam data (Half-Yearly and Annual, broken down by question type: MCQ, 2-Mark, 3-Mark, Long Answer, Case Based) is cleaned and validated, then engineered into analytical features — performance bands, risk levels, growth categories, and question-level skill gaps — and surfaced in a 4-page interactive Power BI dashboard.

## Tech Stack

- **Python (pandas)** — data cleaning and feature engineering
- **SQL** — data validation and exploratory analysis queries
- **Power BI (DAX)** — interactive dashboard with custom measures for normalized scoring, section benchmarking, and gap analysis

## Pipeline

```
Raw CSV (150 students)
      │
      ▼
data_cleaning.py        → validates columns, standardizes text, recalculates totals, removes duplicates
      │
      ▼
feature_engineering.py  → adds Performance_Band, Risk_Level, Growth_Category, Strongest/Weakest_Section, Consistency_Score
      │
      ▼
SQL validation & analysis → data_validation.sql, performance_analysis.sql, growth_analysis.sql, section_analysis.sql
      │
      ▼
Power BI Dashboard (4 pages)
```

## Key Findings

- **90% overall pass rate**, with an average improvement of 13 points from Half-Yearly to Annual exams
- **15 students (10%)** flagged High Risk and require intervention
- **Section 8Q leads** with the highest average annual score (79%) and strongest improvement (+19 points), while **8N shows the least growth** (+7 points) despite a similar pass profile
- **54.67% of students** showed significant growth over the year — but some declined by as much as **44 percentage points**, now flagged for follow-up
- **3-Mark Questions show the lowest normalized performance class-wide (52–59%)**, with Section 8E scoring weakest at **50.68%** — pointing to a shared execution gap in multi-step reasoning, not just isolated student weakness

## Dashboard Pages

### 1. Executive Summary
![Executive Summary](screenshots/page1_executive_summary.png)
KPI overview — total students, pass rate, average improvement, intervention count — plus performance band, risk level, and improvement status breakdowns.

### 2. Section Comparison
![Section Comparison](screenshots/page2_section_comparison.png)
Side-by-side section performance, annual grade distribution, average improvement, and consistency scoring.

### 3. Growth & Improvement
![Growth & Improvement](screenshots/page3_growth_improvement.png)
HY-to-Annual scatter analysis, growth category breakdown, and top improving/declining student watchlists.

### 4. Question-Wise Skill Gap & Intervention
![Question-Wise Skill Gap](screenshots/page4_skill_gap.png)
Normalized (max-scorer-relative) performance heatmap by section and question type, strongest/weakest question type distribution, and a priority intervention list ranked by how far each student sits below their own section's average.

## Repository Structure

```
├── data/               # Raw, cleaned, and feature-engineered CSVs
├── scripts/            # data_cleaning.py, feature_engineering.py
├── sql/                # Validation and analysis queries
├── dashboard/           # student.pbix (open in Power BI Desktop)
├── screenshots/         # PNG exports of all 4 dashboard pages
└── README.md
```

## Running the Pipeline

```bash
pip install pandas numpy
python scripts/data_cleaning.py
python scripts/feature_engineering.py
```

Then open `dashboard/student.pbix` in Power BI Desktop to explore the full interactive report.

## Author

Unsi Rathod

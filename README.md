# 🍬 Nassau Candy Distributor — Shipping Route Efficiency Analysis

**Factory-to-customer shipping analysis for a national candy distributor — cleaning, SQL and Python analysis, and an interactive Streamlit dashboard, built around a data quality problem that shaped everything downstream.**

Prepared by **Kehkasha Ansari** · Business Analyst Intern

![Python](https://img.shields.io/badge/Python-pandas-3776AB?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-SQL_EDA-4479A1?logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white)

---

## Overview

Nassau Candy ships from five factories to customers across 49 U.S. states and Washington, D.C., but had no structured way to see which routes ran efficiently and which didn't. This project builds that visibility from the ground up: cleaning 10,194 raw order records, investigating a serious data quality issue in the shipping date fields, and turning the result into route, factory, ship mode, and geographic performance findings — delivered through SQL analysis, a Python KPI layer, and an interactive dashboard.

## ⚠️ The Data Quality Finding (read this first)

Shipping Lead Time — the metric most of this project's KPIs depend on — turned out **not to reflect real shipping chronology**. Raw values ranged from 904 to 1,642 days, and four independent checks (date range mismatch, a non-continuous three-cluster distribution, year-gap sub-groups, and a year-normalization test) confirmed the issue was structural, not a handful of outliers.

Rather than discard the metric, every KPI in this project treats Lead Time as a **relative, comparative measure only** — never a literal day count. Full evidence and reasoning is documented in `notebooks/Data_Validation_Investigation.ipynb` and Section 4.2 of the research paper.

## Key Findings

| Metric | Value |
|---|---|
| Total Orders (unique) | 8,389 |
| Total Sales | $138,830.34 |
| Total Gross Profit | $91,508.23 |
| Overall Delay Frequency | 33.26% |
| Average Route Efficiency Score | 54.7 / 100 |

- **Washington is a confirmed bottleneck** — it's the only state where both major factories (Lot's O' Nuts and Wicked Choccy's) underperform simultaneously, and it has the highest state-level delay rate in the dataset (42.82%).
- **No cost-speed trade-off exists across Ship Modes** — cost per shipment stays within a $4.42–$4.84 range regardless of mode.
- Order volume is heavily concentrated: **Lot's O' Nuts and Wicked Choccy's account for ~96.5%** of all shipments.

## Repository Structure

```
├── data/
│   └── raw/                          # Original dataset & problem statement
├── notebooks/
│   ├── Data_Validation_Investigation.ipynb   # Phase 2: cleaning + Lead Time investigation
│   └── Nassau_Candy_KPI_Metrics.ipynb        # Phase 4: KPI logic rebuilt in pandas
├── sql/
│   └── nassau_candy_EDA.sql          # Phase 3: 27-query SQL analysis (MySQL)
├── streamlit/
│   ├── Home.py                       # Dashboard entry point / Overview page
│   ├── Style.py                      # Shared theming and component styles
│   ├── pages/                        # Route Efficiency, Geographic Map,
│   │                                  # Ship Mode Comparison, Route Drill-Down
│   └── data/                         # Cleaned dataset + exported KPI CSVs
├── deliverables/
│   ├── Nassau_Candy_Research_Paper.pdf
│   └── Nassau_Candy_Executive_Summary.pdf
├── LICENSE
└── README.md
```

## Methodology at a Glance

1. **Excel exploration** — initial data familiarization and first red flags
2. **Python/pandas cleaning** — U.S.-only scope (200 Canada records dropped), Factory join correction (Fizzy Lifting Drinks Division mismatch resolved), and the Lead Time investigation
3. **SQL EDA (MySQL)** — 27 queries covering data validation, route/factory performance, delay frequency, efficiency scoring, and cost-time comparison
4. **Pandas KPI rebuild** — the same KPI logic re-implemented in pandas (required since the dashboard reads from CSV, not a live database) and cross-checked against SQL for consistency
5. **Streamlit dashboard** — 5 pages covering route efficiency, geographic performance, ship mode comparison, and state-level drill-down, with interactive filtering available on the drill-down page.

The decision to treat Lead Time as relative-only was raised for mentor guidance mid-project; the full reasoning trail is preserved in the notebooks rather than cleaned away, since it's part of the actual analytical work.

## Running This Locally

**1. Clone the repo and install dependencies**
```bash
git clone https://github.com/kehkasha786/Nassau-Candy-Shipping-Route-Efficiency.git
cd Nassau-Candy-Shipping-Route-Efficiency
pip install pandas numpy matplotlib plotly streamlit mysql-connector-python
```

**2. Explore the analysis**
- Open `notebooks/Data_Validation_Investigation.ipynb` for the cleaning process and the Lead Time investigation
- Run `sql/nassau_candy_EDA.sql` against a MySQL instance for the full query-by-query EDA
- Open `notebooks/Nassau_Candy_KPI_Metrics.ipynb` for the pandas KPI layer

**3. Run the dashboard**
```bash
cd streamlit
streamlit run Home.py
```

## Deliverables

- 📄 [Research Paper](deliverables/Nassau_Candy_Research_Paper.pdf) — full methodology, findings, limitations, and recommendations
- 📋 [Executive Summary](deliverables/Nassau_Candy_Executive_Summary.pdf) — condensed stakeholder-facing summary
- 📊 Interactive Streamlit dashboard (see above)

## Tools & Technologies

Python (pandas, matplotlib, plotly) · MySQL · Streamlit · Excel

---

*This project was completed as part of a Business Analyst internship. Questions or feedback are welcome via GitHub issues.*

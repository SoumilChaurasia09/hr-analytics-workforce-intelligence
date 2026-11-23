# HR Analytics & Workforce Intelligence: Employee Attrition & Retention

A comprehensive People Analytics project analyzing workforce attrition, turnover risk factors, and organizational retention economics using the IBM HR Analytics dataset.

---

## 📌 Project Overview

This project diagnoses the primary drivers of employee turnover across departments, job roles, and compensation bands. Rather than using external BI platforms, this project delivers an executive-ready, formula-driven **Microsoft Excel Dashboard** backed by **Python (Pandas, SciPy, Seaborn)** and an **ANSI-compliant SQL Analytical Engine (SQLite)**.

---

## 📊 Dataset Provenance & Attribution

- **Dataset Name**: IBM HR Analytics Employee Attrition & Performance
- **Original Publisher**: IBM Watson Analytics
- **Primary Source**: Available publicly on Kaggle ([IBM HR Analytics Attrition Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset))
- **Records**: 1,470 employee entries across 35 original attributes
- **Data Characteristics**: This is a **synthetic benchmark dataset** engineered by IBM data scientists to emulate realistic Fortune 500 corporate workforce distributions. It incorporates authentic human-capital dynamics (burnout, pay compression, tenure milestones) while fully respecting Personally Identifiable Information (PII) and privacy regulations.

---

## 📁 Repository Structure

```
├── HR_Analytics_and_Workforce_Intelligence.xlsx   # Master Interactive Excel Dashboard
├── requirements.txt                              # Python environment dependencies
├── .gitignore                                    # Git ignore rules for Python & Excel
├── README.md                                     # Project documentation
│
├── assets/
│   └── dashboard_preview.png                     # Dashboard snapshot
│
├── data/
│   ├── raw_hr_data.csv                           # Original raw dataset
│   ├── cleaned_hr_data.csv                       # Cleaned dataset with 50 features
│   ├── hr_workforce.db                           # SQLite relational database
│   └── data_dictionary.csv                       # Field definitions and schema metadata
│
├── notebooks/
│   └── HR_Analytics_Workforce_Intelligence.ipynb # Interactive Jupyter analysis notebook
│
├── sql/
│   └── hr_analytics_queries.sql                  # Analytical SQL queries (CTEs, Window Funcs)
│
├── scripts/
│   ├── data_cleaning.py                          # Data cleansing & feature engineering
│   ├── statistical_analysis.py                   # SciPy hypothesis testing & odds ratios
│   ├── build_sql_database.py                     # SQLite builder & query runner
│   ├── generate_visualizations.py                # 300-DPI Seaborn/Matplotlib charts
│   └── build_dashboard.py                        # Automated openpyxl Excel dashboard generator
│
├── visualizations/
│   ├── 01_executive_kpi_overview.png             # Attrition distributions by department
│   ├── 02_compensation_and_overtime_drivers.png  # Salary slabs & overtime comparisons
│   ├── 03_statistical_significance_and_correlation.png # Correlation matrix & odds ratio plot
│   └── 04_flight_risk_and_career_dynamics.png    # Tenure attrition curves & risk matrix
│
└── reports/
    ├── statistical_hypothesis_results.csv        # Detailed p-values and effect sizes
    └── odds_ratios_risk_factors.csv              # Relative risk ratios with 95% CIs
```

---

## 🔍 Key Findings & Workforce Insights

1. **Overtime Multiplier**: Employees working overtime have an attrition rate of **30.5%** compared to **10.4%** for standard hours (Odds Ratio: **3.77**, p < 0.001). Overtime is the strongest single predictor of turnover.
2. **Early-Career Flight Risk**: Turnover is heavily concentrated in the first 24 months of tenure (**29.8%** attrition for tenure $\le$ 2 years vs **12.0%** for experienced staff).
3. **Compensation Inequity**: Departing employees earn an average of **29.9% less** than retained peers ($4,787/month vs $6,833/month). Lowest quartile earners (<$2,911/month) face a **29.4%** turnover rate.
4. **Departmental Variance**: **Sales** leads organizational turnover at **20.6%**, followed by **Human Resources** at **19.0%** and **Research & Development** at **13.8%**.
5. **Annual Turnover Cost**: Estimated annual organizational turnover loss totals approximately **$6.8M** based on standard 50% replacement cost benchmarks.

---

## 🛠️ Technology Stack

- **Spreadsheets**: Microsoft Excel (Multi-tab dynamic formulas: `COUNTA`, `COUNTIF`, `COUNTIFS`, `AVERAGEIF`, `SUMIF`, native charts)
- **Database**: SQLite / ANSI SQL (CTEs, `DENSE_RANK()`, `NTILE()`, Group By aggregations)
- **Data Wrangling**: Python, Pandas, NumPy
- **Inferential Statistics**: SciPy (`scipy.stats.chi2_contingency`, Welch's Two-Sample t-test, Mann-Whitney U, Odds Ratios)
- **Data Visualization**: Matplotlib, Seaborn

---

## 🚀 Getting Started

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-username/hr-analytics-workforce-intelligence.git
cd hr-analytics-workforce-intelligence
pip install -r requirements.txt
```

### 2. Run the Full Analytical Pipeline
```bash
# Clean data and generate engineered features
python scripts/data_cleaning.py

# Run hypothesis testing with SciPy
python scripts/statistical_analysis.py

# Build SQLite database and execute queries
python scripts/build_sql_database.py

# Generate high-resolution visual plots
python scripts/generate_visualizations.py

# Build the master Excel workbook
python scripts/build_dashboard.py
```

### 3. Open the Interactive Dashboard
Open `HR_Analytics_and_Workforce_Intelligence.xlsx` in Microsoft Excel to interact with the executive KPI cards, department breakdowns, and overtime risk analysis.

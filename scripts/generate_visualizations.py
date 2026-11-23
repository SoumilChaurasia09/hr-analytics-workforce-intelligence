"""
Generate Publication-Ready Visualizations for HR Analytics & Workforce Intelligence
Tools: Matplotlib, Seaborn, Pandas, NumPy
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Style configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

DATA_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\data"
REPORTS_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\reports"
VIZ_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\visualizations"

CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_hr_data.csv")

# Corporate color palette
NAVY = "#1F4E79"
TEAL = "#2E75B6"
CORAL = "#D9534F"
LIGHT_GRAY = "#D9D9D9"
DARK_GRAY = "#333333"
GREEN = "#2CA02C"

def plot_executive_overview(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("EXECUTIVE WORKFORCE OVERVIEW & ATTRITION BENCHMARKS", fontsize=18, fontweight='bold', color=NAVY, y=0.98)

    # 1. Workforce Distribution Donut Chart
    ax1 = axes[0, 0]
    counts = df['Attrition'].value_counts()
    colors = [TEAL, CORAL]
    explode = (0, 0.08)
    wedges, texts, autotexts = ax1.pie(
        counts, 
        labels=['Retained (No)', 'Departed (Yes)'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors, 
        explode=explode,
        wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(12)
        at.set_weight('bold')
    ax1.set_title("Overall Retention vs Attrition (N=1,470)", pad=15)
    ax1.text(0, 0, f"Total\n1,470\nStaff", ha='center', va='center', fontsize=12, fontweight='bold', color=DARK_GRAY)

    # 2. Attrition Rate by Department
    ax2 = axes[0, 1]
    dept_stats = df.groupby('Department')['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    dept_stats['rate_pct'] = dept_stats['mean'] * 100
    dept_stats = dept_stats.sort_values('rate_pct', ascending=False)
    
    bars2 = ax2.bar(dept_stats['Department'], dept_stats['rate_pct'], color=[CORAL, TEAL, NAVY], width=0.55, edgecolor='black', linewidth=0.8)
    ax2.axhline(df['Attrition_Flag'].mean() * 100, color='red', linestyle='--', linewidth=1.5, label=f"Company Avg ({df['Attrition_Flag'].mean()*100:.1f}%)")
    ax2.set_title("Attrition Rate by Operational Department (%)", pad=15)
    ax2.set_ylabel("Attrition Rate (%)")
    ax2.set_ylim(0, 26)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.6, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax2.legend(loc='upper right')

    # 3. Top Attrition Roles
    ax3 = axes[1, 0]
    role_stats = df.groupby('JobRole')['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    role_stats['rate_pct'] = role_stats['mean'] * 100
    role_stats = role_stats.sort_values('rate_pct', ascending=True)
    
    colors3 = [CORAL if r >= 20 else TEAL for r in role_stats['rate_pct']]
    bars3 = ax3.barh(role_stats['JobRole'], role_stats['rate_pct'], color=colors3, edgecolor='black', linewidth=0.8)
    ax3.set_title("Turnover Propensity by Occupational Role (%)", pad=15)
    ax3.set_xlabel("Attrition Rate (%)")
    ax3.set_xlim(0, 46)
    for bar in bars3:
        xval = bar.get_width()
        ax3.text(xval + 0.8, bar.get_y() + bar.get_height()/2.0, f"{xval:.1f}%", ha='left', va='center', fontweight='bold', fontsize=9)

    # 4. Age Cohort Turnover
    ax4 = axes[1, 1]
    age_stats = df.groupby('Age_Group', observed=False)['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    age_stats['rate_pct'] = age_stats['mean'] * 100
    
    bars4 = ax4.bar(age_stats['Age_Group'].astype(str), age_stats['rate_pct'], color=TEAL, width=0.55, edgecolor='black', linewidth=0.8)
    ax4.plot(age_stats['Age_Group'].astype(str), age_stats['rate_pct'], color=CORAL, marker='o', linewidth=2.5, markersize=8)
    ax4.set_title("Attrition Rate by Demographic Age Bracket (%)", pad=15)
    ax4.set_ylabel("Attrition Rate (%)")
    ax4.set_ylim(0, 45)
    for bar in bars4:
        yval = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(VIZ_DIR, "01_executive_kpi_overview.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def plot_compensation_and_overtime(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("COMPENSATION EQUITY & OVERTIME ATTRITION DRIVERS", fontsize=18, fontweight='bold', color=NAVY, y=0.98)

    # 1. Monthly Income Violin / Box Plot
    ax1 = axes[0, 0]
    sns.boxplot(x='Attrition', y='MonthlyIncome', data=df, palette=[TEAL, CORAL], ax=ax1, width=0.4, fliersize=3)
    ax1.set_title("Monthly Income Distribution: Stayers vs Leavers", pad=15)
    ax1.set_ylabel("Monthly Income ($ USD)")
    ax1.set_xticklabels(["Retained (No)", "Departed (Yes)"])
    med_stay = df[df['Attrition']=='No']['MonthlyIncome'].median()
    med_leave = df[df['Attrition']=='Yes']['MonthlyIncome'].median()
    ax1.text(0, med_stay + 500, f"Med: ${med_stay:,.0f}", ha='center', fontweight='bold', color='white', bbox=dict(boxstyle='round', facecolor=NAVY, alpha=0.8))
    ax1.text(1, med_leave + 500, f"Med: ${med_leave:,.0f}", ha='center', fontweight='bold', color='white', bbox=dict(boxstyle='round', facecolor=CORAL, alpha=0.8))

    # 2. Overtime Impact across Departments
    ax2 = axes[0, 1]
    ot_dept = df.groupby(['Department', 'OverTime'])['Attrition_Flag'].mean().unstack() * 100
    ot_dept.plot(kind='bar', ax=ax2, color=[TEAL, CORAL], edgecolor='black', width=0.6)
    ax2.set_title("Overtime Impact on Attrition by Department (%)", pad=15)
    ax2.set_ylabel("Attrition Rate (%)")
    ax2.set_xlabel("")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    ax2.set_ylim(0, 45)
    ax2.legend(["No Overtime", "Overtime (Yes)"], title="Overtime Status")
    for p in ax2.patches:
        ax2.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 4), textcoords='offset points')

    # 3. Stock Option Level Attrition
    ax3 = axes[1, 0]
    stock_stats = df.groupby('StockOptionLevel')['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    stock_stats['rate_pct'] = stock_stats['mean'] * 100
    bars3 = ax3.bar(stock_stats['StockOptionLevel'].astype(str), stock_stats['rate_pct'], color=[CORAL, TEAL, TEAL, TEAL], edgecolor='black', width=0.55)
    ax3.set_title("Attrition by Stock Option Grant Level", pad=15)
    ax3.set_xlabel("Stock Option Level (0 = No Grant)")
    ax3.set_ylabel("Attrition Rate (%)")
    ax3.set_ylim(0, 30)
    for bar in bars3:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')

    # 4. Salary Tier Attrition Propensity
    ax4 = axes[1, 1]
    sal_stats = df.groupby('Salary_Tier', observed=False)['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    sal_stats['rate_pct'] = sal_stats['mean'] * 100
    bars4 = ax4.bar(sal_stats['Salary_Tier'].astype(str), sal_stats['rate_pct'], color=[CORAL, TEAL, TEAL, TEAL, TEAL], edgecolor='black', width=0.55)
    ax4.set_title("Attrition Propensity by Monthly Income Tier", pad=15)
    ax4.set_xlabel("Salary Tier")
    ax4.set_ylabel("Attrition Rate (%)")
    ax4.set_ylim(0, 36)
    ax4.set_xticklabels(sal_stats['Salary_Tier'].astype(str), rotation=20, ha='right')
    for bar in bars4:
        yval = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(VIZ_DIR, "02_compensation_and_overtime_drivers.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def plot_statistical_significance(df):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle("INFERENTIAL WORKFORCE ANALYTICS & STATISTICAL RISK RATIOS", fontsize=18, fontweight='bold', color=NAVY, y=0.98)

    # 1. Odds Ratio Forest Plot
    ax1 = axes[0]
    or_df = pd.read_csv(os.path.join(REPORTS_DIR, "odds_ratios_risk_factors.csv"))
    or_df = or_df.sort_values('Odds_Ratio', ascending=True)

    y_pos = np.arange(len(or_df))
    ax1.axvline(1.0, color='gray', linestyle='--', linewidth=1.5, alpha=0.8, label="Baseline Odds (OR = 1.0)")
    
    # Error bars for 95% CI
    xerr = [or_df['Odds_Ratio'] - or_df['CI_Lower'], or_df['CI_Upper'] - or_df['Odds_Ratio']]
    ax1.errorbar(or_df['Odds_Ratio'], y_pos, xerr=xerr, fmt='o', color=CORAL, ecolor=NAVY, elinewidth=2.5, capsize=6, markersize=8)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(or_df['Factor'], fontweight='bold')
    ax1.set_xlabel("Odds Ratio (OR) with 95% Confidence Interval")
    ax1.set_title("Relative Flight Risk Odds Ratio by Risk Factor", pad=15)
    ax1.set_xlim(0.5, 6.0)

    for i, row in enumerate(or_df.itertuples()):
        ax1.text(row.Odds_Ratio + 0.15, i, f"OR: {row.Odds_Ratio:.2f} ({row.CI_Lower:.2f}-{row.CI_Upper:.2f})", va='center', fontsize=9, fontweight='bold', color=NAVY)
    ax1.legend(loc='lower right')

    # 2. Correlation Matrix with Attrition_Flag
    ax2 = axes[1]
    corr_cols = [
        'Attrition_Flag', 'Age', 'Distance_km', 'JobLevel', 'MonthlyIncome', 
        'Total_Work_Experience', 'Company_Tenure', 'Role_Tenure', 
        'Years_Since_Promotion', 'Years_With_Manager', 'Composite_Satisfaction_Score'
    ]
    corr_matrix = df[corr_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='Blues', ax=ax2, cbar_kws={'label': 'Pearson Correlation'}, linewidths=0.5, square=True)
    ax2.set_title("Workforce Metrics Correlation Heatmap", pad=15)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(VIZ_DIR, "03_statistical_significance_and_correlation.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def plot_flight_risk_and_career(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("CAREER DYNAMICS, TENURE MILESTONES & FLIGHT RISK TIERS", fontsize=18, fontweight='bold', color=NAVY, y=0.98)

    # 1. Tenure Survival / Attrition Curve
    ax1 = axes[0, 0]
    tenure_stats = df.groupby('Company_Tenure')['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    tenure_stats = tenure_stats[tenure_stats['Company_Tenure'] <= 20]
    tenure_stats['rate_pct'] = tenure_stats['mean'] * 100

    ax1.plot(tenure_stats['Company_Tenure'], tenure_stats['rate_pct'], color=CORAL, marker='o', linewidth=2.5, markersize=7)
    ax1.fill_between(tenure_stats['Company_Tenure'], tenure_stats['rate_pct'], color=CORAL, alpha=0.15)
    ax1.axvline(2, color=NAVY, linestyle=':', linewidth=2, label="Early Career Cliff (<= 2 Yrs)")
    ax1.set_title("Turnover Propensity across Company Tenure (Years)", pad=15)
    ax1.set_xlabel("Years at Company")
    ax1.set_ylabel("Attrition Rate (%)")
    ax1.set_ylim(0, 45)
    ax1.legend(loc='upper right')

    # 2. Manager Tenure Effect
    ax2 = axes[0, 1]
    mgr_stats = df.groupby('Years_With_Manager')['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    mgr_stats = mgr_stats[mgr_stats['Years_With_Manager'] <= 15]
    mgr_stats['rate_pct'] = mgr_stats['mean'] * 100

    ax2.bar(mgr_stats['Years_With_Manager'], mgr_stats['rate_pct'], color=TEAL, edgecolor='black', width=0.6)
    ax2.set_title("Attrition Rate by Years with Current Manager", pad=15)
    ax2.set_xlabel("Years Under Direct Manager")
    ax2.set_ylabel("Attrition Rate (%)")
    ax2.set_ylim(0, 40)

    # 3. Flight Risk Tier Distribution
    ax3 = axes[1, 0]
    risk_stats = df.groupby('Flight_Risk_Tier', observed=False)['Attrition_Flag'].agg(['count', 'mean']).reset_index()
    risk_stats['rate_pct'] = risk_stats['mean'] * 100

    bars3 = ax3.bar(risk_stats['Flight_Risk_Tier'].astype(str), risk_stats['rate_pct'], color=[GREEN, TEAL, CORAL], edgecolor='black', width=0.55)
    ax3.set_title("Empirical Attrition Rate by Predictive Flight Risk Tier", pad=15)
    ax3.set_xlabel("Workforce Intelligence Flight Risk Classification")
    ax3.set_ylabel("Observed Attrition Rate (%)")
    ax3.set_ylim(0, 65)
    for bar in bars3:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=11)

    # 4. Work-Life Balance vs Job Satisfaction Matrix
    ax4 = axes[1, 1]
    pivot_wlb = df.pivot_table(index='Work_Life_Balance_Level', columns='Job_Satisfaction_Level', values='Attrition_Flag', aggfunc='mean') * 100
    sns.heatmap(pivot_wlb, annot=True, fmt='.1f', cmap='Reds', ax=ax4, cbar_kws={'label': 'Attrition Rate (%)'}, linewidths=0.5)
    ax4.set_title("Attrition Heatmap: Work-Life Balance vs Job Satisfaction", pad=15)
    ax4.set_xlabel("Job Satisfaction Level")
    ax4.set_ylabel("Work-Life Balance Level")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(VIZ_DIR, "04_flight_risk_and_career_dynamics.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def main():
    print("Loading cleaned dataset...")
    df = pd.read_csv(CLEANED_CSV)
    print("Generating Visualization 1: Executive KPI Overview...")
    plot_executive_overview(df)
    print("Generating Visualization 2: Compensation & Overtime Drivers...")
    plot_compensation_and_overtime(df)
    print("Generating Visualization 3: Statistical Significance & Risk Ratios...")
    plot_statistical_significance(df)
    print("Generating Visualization 4: Flight Risk & Career Dynamics...")
    plot_flight_risk_and_career(df)
    print("All visualizations successfully generated.")

if __name__ == '__main__':
    main()

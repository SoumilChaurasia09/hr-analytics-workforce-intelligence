"""
Statistical Hypothesis Testing & Inferential Workforce Analytics
Tools: SciPy, NumPy, Pandas
Tests: Chi-Square Test of Independence, Independent Two-Sample T-Test,
       Mann-Whitney U Test, Cramér's V, Cohen's d, Odds Ratios (OR).
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

DATA_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\data"
REPORTS_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\reports"
CLEANED_FILE = os.path.join(DATA_DIR, "cleaned_hr_data.csv")
OUTPUT_STATS_FILE = os.path.join(REPORTS_DIR, "statistical_hypothesis_results.csv")

def cramers_v(contingency_table):
    chi2 = stats.chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    r, k = contingency_table.shape
    phi2 = chi2 / n
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    s1, s2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    if pooled_s == 0:
        return 0.0
    return (np.mean(group1) - np.mean(group2)) / pooled_s

def run_hypothesis_tests():
    df = pd.read_csv(CLEANED_FILE)
    print(f"Loaded {len(df)} employee records for statistical testing.\n")

    results = []

    # -------------------------------------------------------------
    # 1. CATEGORICAL VARIABLES: Chi-Square Test of Independence
    # -------------------------------------------------------------
    categorical_vars = [
        'OverTime', 'JobRole', 'MaritalStatus', 'Department',
        'Travel_Frequency', 'StockOptionLevel', 'Job_Involvement_Level',
        'Environment_Satisfaction_Level', 'Job_Satisfaction_Level',
        'Work_Life_Balance_Level', 'Salary_Tier', 'Tenure_Cohort',
        'Age_Group', 'Commute_Tier', 'Flight_Risk_Tier'
    ]

    print("=" * 80)
    print("CHI-SQUARE TESTS OF INDEPENDENCE (Categorical Predictors vs Attrition)")
    print("=" * 80)

    for var in categorical_vars:
        contingency = pd.crosstab(df[var], df['Attrition'])
        chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
        effect_v = cramers_v(contingency)
        sig = "Statistically Significant (p < 0.001) ***" if p_val < 0.001 else (
              "Significant (p < 0.05) *" if p_val < 0.05 else "Not Significant (p >= 0.05)")

        results.append({
            'Category': 'Categorical',
            'Variable': var,
            'Test_Type': 'Chi-Square Test',
            'Null_Hypothesis': f'{var} is independent of Attrition',
            'Test_Statistic': round(chi2, 4),
            'p_value': p_val,
            'p_value_formatted': f"{p_val:.2e}" if p_val < 0.0001 else f"{p_val:.4f}",
            'Degrees_of_Freedom': dof,
            'Effect_Size_Metric': "Cramér's V",
            'Effect_Size': round(effect_v, 4),
            'Conclusion': sig
        })

        print(f"[{var:28}] Chi2: {chi2:9.3f} | p-val: {p_val:.3e} | Cramér's V: {effect_v:.3f} | {sig}")

    # -------------------------------------------------------------
    # 2. CONTINUOUS VARIABLES: Two-sample T-test & Mann-Whitney U
    # -------------------------------------------------------------
    continuous_vars = [
        'MonthlyIncome', 'Age', 'Total_Work_Experience', 'Company_Tenure',
        'Role_Tenure', 'Years_With_Manager', 'Years_Since_Promotion',
        'Distance_km', 'PercentSalaryHike', 'Composite_Satisfaction_Score',
        'Salary_JobLevel_Ratio'
    ]

    leavers = df[df['Attrition'] == 'Yes']
    stayers = df[df['Attrition'] == 'No']

    print("\n" + "=" * 80)
    print("TWO-SAMPLE T-TESTS & MANN-WHITNEY U (Stayers vs Leavers)")
    print("=" * 80)

    for var in continuous_vars:
        val_stayers = stayers[var].dropna()
        val_leavers = leavers[var].dropna()

        t_stat, p_val_t = stats.ttest_ind(val_stayers, val_leavers, equal_var=False)
        u_stat, p_val_u = stats.mannwhitneyu(val_stayers, val_leavers, alternative='two-sided')
        d_val = cohens_d(val_leavers, val_stayers)  # Leavers minus Stayers

        sig = "Statistically Significant (p < 0.001) ***" if p_val_t < 0.001 else (
              "Significant (p < 0.05) *" if p_val_t < 0.05 else "Not Significant (p >= 0.05)")

        results.append({
            'Category': 'Continuous',
            'Variable': var,
            'Test_Type': 'Welch Two-Sample T-Test',
            'Null_Hypothesis': f'Mean {var} is identical for Stayers and Leavers',
            'Test_Statistic': round(t_stat, 4),
            'p_value': p_val_t,
            'p_value_formatted': f"{p_val_t:.2e}" if p_val_t < 0.0001 else f"{p_val_t:.4f}",
            'Degrees_of_Freedom': round(len(val_stayers) + len(val_leavers) - 2, 0),
            'Effect_Size_Metric': "Cohen's d",
            'Effect_Size': round(d_val, 4),
            'Conclusion': sig
        })

        mean_stay = val_stayers.mean()
        mean_leave = val_leavers.mean()
        diff_pct = ((mean_leave - mean_stay) / mean_stay) * 100
        print(f"[{var:26}] Stay: {mean_stay:8.2f} | Leave: {mean_leave:8.2f} ({diff_pct:+6.1f}%) | p: {p_val_t:.3e} | d: {d_val:+.3f}")

    # -------------------------------------------------------------
    # 3. ODDS RATIO (OR) FOR PRIMARY WORKFORCE RISK FACTORS
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("ODDS RATIOS & RELATIVE RISK OF FLIGHT (2x2 Factor Analysis)")
    print("=" * 80)

    def calc_odds_ratio(name, condition_mask):
        exposed = condition_mask
        unexposed = ~condition_mask
        
        a = (exposed & (df['Attrition'] == 'Yes')).sum()
        b = (exposed & (df['Attrition'] == 'No')).sum()
        c = (unexposed & (df['Attrition'] == 'Yes')).sum()
        d = (unexposed & (df['Attrition'] == 'No')).sum()

        odds_ratio = (a * d) / (b * c) if (b * c) > 0 else np.nan
        relative_risk = (a / (a + b)) / (c / (c + d)) if (c / (c + d)) > 0 else np.nan
        se_log_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
        ci_lower = np.exp(np.log(odds_ratio) - 1.96 * se_log_or)
        ci_upper = np.exp(np.log(odds_ratio) + 1.96 * se_log_or)

        rate_exp = (a / (a + b)) * 100
        rate_unexp = (c / (c + d)) * 100

        print(f"Factor: {name:32} | OR: {odds_ratio:5.2f} (95% CI: {ci_lower:.2f}-{ci_upper:.2f}) | RR: {relative_risk:5.2f} | Attrition: {rate_exp:.1f}% vs {rate_unexp:.1f}%")
        
        return {
            'Factor': name,
            'Odds_Ratio': round(odds_ratio, 2),
            'CI_Lower': round(ci_lower, 2),
            'CI_Upper': round(ci_upper, 2),
            'Relative_Risk': round(relative_risk, 2),
            'Attrition_Rate_Exposed': round(rate_exp, 1),
            'Attrition_Rate_Unexposed': round(rate_unexp, 1)
        }

    or_list = [
        calc_odds_ratio("OverTime = Yes", df['OverTime'] == 'Yes'),
        calc_odds_ratio("StockOptionLevel = 0", df['StockOptionLevel'] == 0),
        calc_odds_ratio("MaritalStatus = Single", df['MaritalStatus'] == 'Single'),
        calc_odds_ratio("Early Tenure (<= 2 Years)", df['Company_Tenure'] <= 2),
        calc_odds_ratio("Extreme Commute (> 20 km)", df['Distance_km'] > 20),
        calc_odds_ratio("Low Satisfaction (Score < 2.5)", df['Composite_Satisfaction_Score'] < 2.5),
        calc_odds_ratio("Monthly Income < $3,000", df['MonthlyIncome'] < 3000),
        calc_odds_ratio("Frequent Business Travel", df['Travel_Frequency'] == 'Travel_Frequently')
    ]

    # Save results
    df_results = pd.DataFrame(results)
    df_results.to_csv(OUTPUT_STATS_FILE, index=False)
    print(f"\nHypothesis testing summary successfully written to: {OUTPUT_STATS_FILE}")

    df_or = pd.DataFrame(or_list)
    df_or.to_csv(os.path.join(REPORTS_DIR, "odds_ratios_risk_factors.csv"), index=False)
    print(f"Odds ratios exported to: {os.path.join(REPORTS_DIR, 'odds_ratios_risk_factors.csv')}")

if __name__ == '__main__':
    run_hypothesis_tests()

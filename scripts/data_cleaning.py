"""
Data Cleaning, Wrangling & Feature Engineering for HR Analytics & Workforce Intelligence
Dataset: IBM HR Analytics Employee Attrition & Performance
"""

import os
import pandas as pd
import numpy as np

# File Paths
DATA_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\data"
RAW_FILE = os.path.join(DATA_DIR, "raw_hr_data.csv")
CLEANED_FILE = os.path.join(DATA_DIR, "cleaned_hr_data.csv")
DICT_FILE = os.path.join(DATA_DIR, "data_dictionary.csv")

def clean_and_engineer_data():
    print(f"Loading raw data from: {RAW_FILE}")
    df = pd.read_csv(RAW_FILE)
    initial_shape = df.shape
    print(f"Initial shape: {initial_shape}")

    # 1. Drop redundant / zero-variance columns
    zero_variance_cols = ['EmployeeCount', 'StandardHours', 'Over18']
    df_cleaned = df.drop(columns=[col for col in zero_variance_cols if col in df.columns])
    print(f"Dropped zero-variance columns: {zero_variance_cols}")

    # 2. Rename columns for business standard clarity
    rename_dict = {
        'EmployeeNumber': 'EmployeeID',
        'DistanceFromHome': 'Distance_km',
        'BusinessTravel': 'Travel_Frequency',
        'NumCompaniesWorked': 'Prior_Companies_Count',
        'TotalWorkingYears': 'Total_Work_Experience',
        'YearsAtCompany': 'Company_Tenure',
        'YearsInCurrentRole': 'Role_Tenure',
        'YearsSinceLastPromotion': 'Years_Since_Promotion',
        'YearsWithCurrManager': 'Years_With_Manager'
    }
    df_cleaned.rename(columns=rename_dict, inplace=True)

    # 3. Create Binary Attrition Flag
    df_cleaned['Attrition_Flag'] = (df_cleaned['Attrition'] == 'Yes').astype(int)

    # 4. Map Likert scale columns to descriptive textual labels for HR reports
    education_map = {1: 'Below College', 2: 'College', 3: 'Bachelor', 4: 'Master', 5: 'Doctor'}
    satisfaction_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
    worklife_map = {1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'}
    performance_map = {1: 'Low', 2: 'Good', 3: 'Excellent', 4: 'Outstanding'}

    df_cleaned['Education_Level'] = df_cleaned['Education'].map(education_map)
    df_cleaned['Environment_Satisfaction_Level'] = df_cleaned['EnvironmentSatisfaction'].map(satisfaction_map)
    df_cleaned['Job_Satisfaction_Level'] = df_cleaned['JobSatisfaction'].map(satisfaction_map)
    df_cleaned['Relationship_Satisfaction_Level'] = df_cleaned['RelationshipSatisfaction'].map(satisfaction_map)
    df_cleaned['Job_Involvement_Level'] = df_cleaned['JobInvolvement'].map(satisfaction_map)
    df_cleaned['Work_Life_Balance_Level'] = df_cleaned['WorkLifeBalance'].map(worklife_map)
    df_cleaned['Performance_Rating_Level'] = df_cleaned['PerformanceRating'].map(performance_map)

    # 5. Feature Engineering: Demographics, Tenure & Compensation Bands
    # Age Groups
    bins_age = [17, 25, 35, 45, 55, 100]
    labels_age = ['Under 25', '25-34', '35-44', '45-54', '55+']
    df_cleaned['Age_Group'] = pd.cut(df_cleaned['Age'], bins=bins_age, labels=labels_age)

    # Company Tenure Cohorts
    bins_tenure = [-1, 2, 5, 10, 45]
    labels_tenure = ['0-2 Yrs (Early)', '3-5 Yrs (Mid-Level)', '6-10 Yrs (Experienced)', '10+ Yrs (Veteran)']
    df_cleaned['Tenure_Cohort'] = pd.cut(df_cleaned['Company_Tenure'], bins=bins_tenure, labels=labels_tenure)

    # Monthly Income Brackets
    bins_salary = [0, 3000, 5000, 7500, 10000, 30000]
    labels_salary = ['Tier 1 (<$3k)', 'Tier 2 ($3k-$5k)', 'Tier 3 ($5k-$7.5k)', 'Tier 4 ($7.5k-$10k)', 'Tier 5 (>$10k)']
    df_cleaned['Salary_Tier'] = pd.cut(df_cleaned['MonthlyIncome'], bins=bins_salary, labels=labels_salary)

    # Commute Distance Category
    bins_commute = [-1, 5, 10, 20, 50]
    labels_commute = ['Short (1-5 km)', 'Medium (6-10 km)', 'Long (11-20 km)', 'Extreme (>20 km)']
    df_cleaned['Commute_Tier'] = pd.cut(df_cleaned['Distance_km'], bins=bins_commute, labels=labels_commute)

    # Composite Overall Satisfaction Score (Scale 1 to 4)
    df_cleaned['Composite_Satisfaction_Score'] = np.round(
        (df_cleaned['EnvironmentSatisfaction'] +
         df_cleaned['JobSatisfaction'] +
         df_cleaned['RelationshipSatisfaction'] +
         df_cleaned['WorkLifeBalance']) / 4.0, 2
    )

    # Career Stagnation Index: Years since last promotion relative to tenure
    df_cleaned['Stagnation_Index'] = np.round(
        df_cleaned['Years_Since_Promotion'] / (df_cleaned['Company_Tenure'] + 1.0), 3
    )

    # Manager Stability Ratio: Years with current manager relative to company tenure
    df_cleaned['Manager_Stability_Ratio'] = np.round(
        df_cleaned['Years_With_Manager'] / (df_cleaned['Company_Tenure'] + 1.0), 3
    )

    # Compensation Equity Index: Monthly Income relative to mean for that Job Level
    job_level_means = df_cleaned.groupby('JobLevel')['MonthlyIncome'].transform('mean')
    df_cleaned['Salary_JobLevel_Ratio'] = np.round(df_cleaned['MonthlyIncome'] / job_level_means, 2)

    # 6. Rule-Based Flight Risk Tier (Workforce Intelligence Risk Scoring)
    # Risk factors: OverTime=Yes, MonthlyIncome below JobLevel mean, Satisfaction < 2.5, StockOptionLevel=0
    risk_score = (
        (df_cleaned['OverTime'] == 'Yes').astype(int) * 2 +
        (df_cleaned['Composite_Satisfaction_Score'] < 2.5).astype(int) * 2 +
        (df_cleaned['Salary_JobLevel_Ratio'] < 0.90).astype(int) * 1.5 +
        (df_cleaned['StockOptionLevel'] == 0).astype(int) * 1 +
        (df_cleaned['Distance_km'] > 15).astype(int) * 1 +
        (df_cleaned['Company_Tenure'] <= 2).astype(int) * 1.5
    )
    df_cleaned['Flight_Risk_Score'] = np.round(risk_score, 1)

    bins_risk = [-1, 2.5, 4.5, 10]
    labels_risk = ['Low Risk', 'Moderate Risk', 'Critical Risk']
    df_cleaned['Flight_Risk_Tier'] = pd.cut(df_cleaned['Flight_Risk_Score'], bins=bins_risk, labels=labels_risk)

    # Export cleaned dataset
    df_cleaned.to_csv(CLEANED_FILE, index=False)
    print(f"Cleaned dataset successfully exported to: {CLEANED_FILE}")
    print(f"Final cleaned shape: {df_cleaned.shape}")

    # Build Data Dictionary
    dict_records = []
    for col in df_cleaned.columns:
        dtype = str(df_cleaned[col].dtype)
        nunique = df_cleaned[col].nunique()
        sample_vals = str(df_cleaned[col].dropna().unique()[:3].tolist())
        dict_records.append({
            'Column_Name': col,
            'Data_Type': dtype,
            'Distinct_Count': nunique,
            'Sample_Values': sample_vals,
            'Description': get_column_description(col)
        })
    df_dict = pd.DataFrame(dict_records)
    df_dict.to_csv(DICT_FILE, index=False)
    print(f"Data dictionary exported to: {DICT_FILE}")

    return df_cleaned

def get_column_description(col):
    descriptions = {
        'EmployeeID': 'Unique identifier for each employee',
        'Age': 'Current age of the employee in years',
        'Attrition': 'Target variable: Whether the employee left the company (Yes/No)',
        'Attrition_Flag': 'Binary indicator: 1 if departed (Yes), 0 if retained (No)',
        'Travel_Frequency': 'Frequency of business travel (Non-Travel, Travel_Rarely, Travel_Frequently)',
        'DailyRate': 'Daily billing/pay rate',
        'Department': 'Operational department (Sales, R&D, Human Resources)',
        'Distance_km': 'Commute distance from home to workplace in kilometers/miles',
        'Education': 'Education level code (1 to 5)',
        'Education_Level': 'Descriptive educational credential',
        'EducationField': 'Degree field of study',
        'EnvironmentSatisfaction': 'Environment satisfaction rating (1-4)',
        'Gender': 'Employee biological gender',
        'HourlyRate': 'Hourly rate',
        'JobInvolvement': 'Job involvement level (1-4)',
        'JobLevel': 'Hierarchical seniority level in organization (1-5)',
        'JobRole': 'Specific occupational role title',
        'JobSatisfaction': 'Employee self-reported job satisfaction (1-4)',
        'MaritalStatus': 'Marital status (Single, Married, Divorced)',
        'MonthlyIncome': 'Gross monthly earnings in USD',
        'MonthlyRate': 'Monthly reimbursement or billing rate',
        'Prior_Companies_Count': 'Number of prior companies worked at before current employer',
        'OverTime': 'Whether employee works overtime hours (Yes/No)',
        'PercentSalaryHike': 'Percentage increase in salary received in most recent cycle',
        'PerformanceRating': 'Performance appraisal score (3=Excellent, 4=Outstanding)',
        'RelationshipSatisfaction': 'Workplace relationship satisfaction rating (1-4)',
        'StockOptionLevel': 'Stock option grant tier (0-3)',
        'Total_Work_Experience': 'Total cumulative professional working career in years',
        'TrainingTimesLastYear': 'Count of professional development training sessions attended in past year',
        'WorkLifeBalance': 'Work-life balance rating (1-4)',
        'Company_Tenure': 'Total duration with current enterprise in years',
        'Role_Tenure': 'Duration serving in current job role in years',
        'Years_Since_Promotion': 'Elapsed time since last formal promotion in years',
        'Years_With_Manager': 'Duration working under current direct supervisor in years',
        'Age_Group': 'Binned demographic age bracket',
        'Tenure_Cohort': 'Career tenure stage grouping',
        'Salary_Tier': 'Compensation tier bracket',
        'Commute_Tier': 'Binned commute distance group',
        'Composite_Satisfaction_Score': 'Average composite score across 4 satisfaction dimensions (1-4 scale)',
        'Stagnation_Index': 'Ratio of time without promotion relative to company tenure',
        'Manager_Stability_Ratio': 'Ratio of tenure with current manager relative to total company tenure',
        'Salary_JobLevel_Ratio': 'Employee monthly income relative to department/job level peer average',
        'Flight_Risk_Score': 'Multi-factor empirical risk score (higher = higher turnover probability)',
        'Flight_Risk_Tier': 'Actionable classification (Low, Moderate, Critical Risk)'
    }
    return descriptions.get(col, 'Engineered or derived workforce analytical metric')

if __name__ == '__main__':
    clean_and_engineer_data()

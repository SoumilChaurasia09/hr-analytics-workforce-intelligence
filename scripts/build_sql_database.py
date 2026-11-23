"""
Build SQLite Database and Execute Production SQL Queries
Generates: hr_workforce.db and SQL query outputs in CSV format
"""

import os
import sqlite3
import pandas as pd

DATA_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\data"
SQL_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\sql"
REPORTS_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel\reports"

CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_hr_data.csv")
DB_PATH = os.path.join(DATA_DIR, "hr_workforce.db")
SQL_FILE = os.path.join(SQL_DIR, "hr_analytics_queries.sql")

def build_and_run_sql():
    print(f"Connecting to SQLite database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load cleaned data into DataFrame
    df = pd.read_csv(CLEANED_CSV)
    
    # Save to SQLite table
    df.to_sql('employees', conn, if_exists='replace', index=False)
    print(f"Loaded {len(df)} rows into 'employees' table.")

    # Execute SQL queries and display findings
    queries = {
        "1_Executive_KPIs": """
            SELECT 
                COUNT(*) AS Total_Workforce,
                SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS Retained_Headcount,
                SUM(Attrition_Flag) AS Total_Departures,
                ROUND(AVG(Attrition_Flag) * 100, 2) AS Overall_Attrition_Rate_Pct,
                ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
                ROUND(AVG(Company_Tenure), 1) AS Avg_Company_Tenure_Yrs,
                ROUND(AVG(Composite_Satisfaction_Score), 2) AS Avg_Satisfaction_Score
            FROM employees;
        """,
        "2_Department_Turnover": """
            SELECT 
                Department,
                COUNT(*) AS Total_Employees,
                SUM(Attrition_Flag) AS Departures,
                ROUND(AVG(Attrition_Flag) * 100, 2) AS Attrition_Rate_Pct,
                ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income,
                ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome * 12 * 0.50 ELSE 0 END), 0) AS Estimated_Turnover_Cost_USD
            FROM employees
            GROUP BY Department
            ORDER BY Attrition_Rate_Pct DESC;
        """,
        "3_Job_Role_Risk_Ranking": """
            WITH RoleMetrics AS (
                SELECT 
                    JobRole,
                    Department,
                    COUNT(*) AS Role_Headcount,
                    SUM(Attrition_Flag) AS Leavers,
                    ROUND(AVG(Attrition_Flag) * 100, 2) AS Role_Attrition_Rate,
                    ROUND(AVG(MonthlyIncome), 0) AS Avg_Role_Income,
                    ROUND(AVG(Composite_Satisfaction_Score), 2) AS Avg_Role_Satisfaction
                FROM employees
                GROUP BY JobRole, Department
            )
            SELECT 
                JobRole,
                Department,
                Role_Headcount,
                Leavers,
                Role_Attrition_Rate,
                Avg_Role_Income,
                Avg_Role_Satisfaction,
                DENSE_RANK() OVER (ORDER BY Role_Attrition_Rate DESC) AS Risk_Rank
            FROM RoleMetrics
            ORDER BY Risk_Rank ASC;
        """,
        "4_Overtime_Attrition_Impact": """
            SELECT 
                OverTime,
                COUNT(*) AS Headcount,
                SUM(Attrition_Flag) AS Departures,
                ROUND(AVG(Attrition_Flag) * 100, 2) AS Attrition_Rate_Pct,
                ROUND(AVG(WorkLifeBalance), 2) AS Avg_WorkLife_Balance_1to4,
                ROUND(AVG(Composite_Satisfaction_Score), 2) AS Avg_Composite_Satisfaction,
                ROUND(AVG(MonthlyIncome), 0) AS Avg_Monthly_Income
            FROM employees
            GROUP BY OverTime;
        """,
        "5_Salary_Quartiles_Attrition": """
            WITH SalaryQuartiles AS (
                SELECT 
                    EmployeeID,
                    Department,
                    JobRole,
                    MonthlyIncome,
                    Attrition_Flag,
                    NTILE(4) OVER (ORDER BY MonthlyIncome ASC) AS Income_Quartile
                FROM employees
            )
            SELECT 
                Income_Quartile,
                MIN(MonthlyIncome) AS Min_Income,
                MAX(MonthlyIncome) AS Max_Income,
                COUNT(*) AS Employee_Count,
                SUM(Attrition_Flag) AS Departures,
                ROUND(AVG(Attrition_Flag) * 100, 2) AS Attrition_Rate_Pct
            FROM SalaryQuartiles
            GROUP BY Income_Quartile
            ORDER BY Income_Quartile ASC;
        """,
        "6_Early_Career_Retention": """
            WITH EarlyCareer AS (
                SELECT 
                    EmployeeID,
                    Department,
                    JobRole,
                    Company_Tenure,
                    OverTime,
                    MonthlyIncome,
                    Attrition_Flag
                FROM employees
                WHERE Company_Tenure <= 2
            )
            SELECT 
                Department,
                JobRole,
                COUNT(*) AS Early_Career_Headcount,
                SUM(Attrition_Flag) AS Early_Career_Leavers,
                ROUND(AVG(Attrition_Flag) * 100, 2) AS Early_Attrition_Rate_Pct,
                SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) AS Count_Working_OverTime
            FROM EarlyCareer
            GROUP BY Department, JobRole
            HAVING COUNT(*) >= 10
            ORDER BY Early_Attrition_Rate_Pct DESC;
        """,
        "7_Manager_Tenure_Stability": """
            SELECT 
                CASE 
                    WHEN Years_With_Manager = 0 THEN '0 Years (New Manager)'
                    WHEN Years_With_Manager BETWEEN 1 AND 2 THEN '1-2 Years'
                    WHEN Years_With_Manager BETWEEN 3 AND 5 THEN '3-5 Years'
                    ELSE '6+ Years (Established)'
                END AS Manager_Tenure_Bracket,
                COUNT(*) AS Headcount,
                SUM(Attrition_Flag) AS Departures,
                ROUND(AVG(Attrition_Flag) * 100, 2) AS Attrition_Rate_Pct,
                ROUND(AVG(Composite_Satisfaction_Score), 2) AS Avg_Satisfaction
            FROM employees
            GROUP BY Manager_Tenure_Bracket
            ORDER BY Attrition_Rate_Pct DESC;
        """
    }

    for name, sql in queries.items():
        print("=" * 80)
        print(f"QUERY: {name}")
        print("=" * 80)
        q_df = pd.read_sql_query(sql, conn)
        print(q_df.to_string(index=False))
        out_csv = os.path.join(REPORTS_DIR, f"sql_{name.lower()}.csv")
        q_df.to_csv(out_csv, index=False)
        print(f"Saved: {out_csv}\n")

    # Create indexes and views
    with open(SQL_FILE, 'r') as f:
        full_sql = f.read()

    # Create views from script
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_executive_kpi_summary AS
        SELECT 
            Department,
            COUNT(*) AS Headcount,
            SUM(Attrition_Flag) AS Departures,
            ROUND(AVG(Attrition_Flag) * 100, 2) AS Attrition_Rate_Pct,
            ROUND(AVG(MonthlyIncome), 0) AS Avg_Income,
            ROUND(AVG(Company_Tenure), 1) AS Avg_Tenure,
            ROUND(AVG(Composite_Satisfaction_Score), 2) AS Avg_Satisfaction
        FROM employees
        GROUP BY Department;
    """)

    cursor.execute("""
        CREATE VIEW IF NOT EXISTS v_critical_risk_employees AS
        SELECT 
            EmployeeID,
            Department,
            JobRole,
            Age,
            MonthlyIncome,
            OverTime,
            StockOptionLevel,
            Distance_km,
            Composite_Satisfaction_Score,
            Flight_Risk_Score
        FROM employees
        WHERE Flight_Risk_Tier = 'Critical Risk'
          AND Attrition = 'No';
    """)

    conn.commit()
    conn.close()
    print("Database build and SQL execution successfully completed.")

if __name__ == '__main__':
    build_and_run_sql()

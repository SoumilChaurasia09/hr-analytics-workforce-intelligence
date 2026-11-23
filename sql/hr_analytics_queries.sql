-- ==============================================================================
-- HR Analytics & Workforce Intelligence: SQL Analytical Engine
-- Database: SQLite / ANSI SQL Compatible
-- Author: Workforce Intelligence Team
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. TABLE DEFINITION & SCHEMA CREATION
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    EmployeeID INTEGER PRIMARY KEY,
    Age INTEGER NOT NULL,
    Attrition TEXT NOT NULL,
    Attrition_Flag INTEGER NOT NULL,
    Travel_Frequency TEXT,
    DailyRate INTEGER,
    Department TEXT NOT NULL,
    Distance_km INTEGER,
    Education INTEGER,
    Education_Level TEXT,
    EducationField TEXT,
    EnvironmentSatisfaction INTEGER,
    Environment_Satisfaction_Level TEXT,
    Gender TEXT,
    HourlyRate INTEGER,
    JobInvolvement INTEGER,
    Job_Involvement_Level TEXT,
    JobLevel INTEGER,
    JobRole TEXT NOT NULL,
    JobSatisfaction INTEGER,
    Job_Satisfaction_Level TEXT,
    MaritalStatus TEXT,
    MonthlyIncome INTEGER NOT NULL,
    MonthlyRate INTEGER,
    Prior_Companies_Count INTEGER,
    OverTime TEXT NOT NULL,
    PercentSalaryHike INTEGER,
    PerformanceRating INTEGER,
    Performance_Rating_Level TEXT,
    RelationshipSatisfaction INTEGER,
    Relationship_Satisfaction_Level TEXT,
    StockOptionLevel INTEGER,
    Total_Work_Experience INTEGER,
    TrainingTimesLastYear INTEGER,
    WorkLifeBalance INTEGER,
    Work_Life_Balance_Level TEXT,
    Company_Tenure INTEGER,
    Role_Tenure INTEGER,
    Years_Since_Promotion INTEGER,
    Years_With_Manager INTEGER,
    Age_Group TEXT,
    Tenure_Cohort TEXT,
    Salary_Tier TEXT,
    Commute_Tier TEXT,
    Composite_Satisfaction_Score REAL,
    Stagnation_Index REAL,
    Manager_Stability_Ratio REAL,
    Salary_JobLevel_Ratio REAL,
    Flight_Risk_Score REAL,
    Flight_Risk_Tier TEXT
);

CREATE INDEX idx_department ON employees(Department);
CREATE INDEX idx_jobrole ON employees(JobRole);
CREATE INDEX idx_attrition ON employees(Attrition);
CREATE INDEX idx_overtime ON employees(OverTime);

-- ------------------------------------------------------------------------------
-- 2. CORE BUSINESS KPI SCORECARD
-- ------------------------------------------------------------------------------
-- Query 1: Enterprise-Wide HR Key Performance Indicators
SELECT 
    COUNT(*) AS Total_Workforce,
    SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS Retained_Headcount,
    SUM(Attrition_Flag) AS Total_Departures,
    ROUND(AVG(Attrition_Flag) * 100, 2) AS Overall_Attrition_Rate_Pct,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(Company_Tenure), 1) AS Avg_Company_Tenure_Yrs,
    ROUND(AVG(Composite_Satisfaction_Score), 2) AS Avg_Satisfaction_Score
FROM employees;

-- ------------------------------------------------------------------------------
-- 3. DEPARTMENTAL BREAKDOWN & ESTIMATED TURNOVER FINANCIAL IMPACT
-- ------------------------------------------------------------------------------
-- Query 2: Department-Level Turnover & Replacement Cost (Cost = 50% Annual Salary)
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

-- ------------------------------------------------------------------------------
-- 4. JOB ROLE FLIGHT RISK RANKING (WINDOW FUNCTIONS)
-- ------------------------------------------------------------------------------
-- Query 3: Occupational Roles Ranked by Attrition Rate with DENSE_RANK()
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

-- ------------------------------------------------------------------------------
-- 5. OVERTIME CROSS-TABULATION & ATTRITION MULTIPLIER
-- ------------------------------------------------------------------------------
-- Query 4: Impact of Chronic Overtime on Retention and Satisfaction
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

-- ------------------------------------------------------------------------------
-- 6. COMPENSATION EQUITY & QUARTILE ANALYSIS (NTILE)
-- ------------------------------------------------------------------------------
-- Query 5: Salary Quartiles and Turnover Propensity
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

-- ------------------------------------------------------------------------------
-- 7. EARLY CAREER (<= 2 YEARS) FLIGHT RISK COHORT
-- ------------------------------------------------------------------------------
-- Query 6: Early Career Turnover Hotspots (CTE)
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

-- ------------------------------------------------------------------------------
-- 8. MANAGER TENURE & LEADERSHIP STABILITY
-- ------------------------------------------------------------------------------
-- Query 7: Turnover Rate by Length of Time Under Current Direct Manager
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

-- ------------------------------------------------------------------------------
-- 9. HIGH PERFORMERS AT RISK (STAR RETENTION AUDIT)
-- ------------------------------------------------------------------------------
-- Query 8: Outstanding Performers (Rating = 4) Facing High Flight Risk
SELECT 
    EmployeeID,
    Department,
    JobRole,
    Age,
    MonthlyIncome,
    OverTime,
    StockOptionLevel,
    Composite_Satisfaction_Score,
    Flight_Risk_Tier,
    Attrition
FROM employees
WHERE PerformanceRating = 4
  AND Flight_Risk_Tier IN ('Critical Risk', 'Moderate Risk')
ORDER BY MonthlyIncome ASC
LIMIT 15;

-- ------------------------------------------------------------------------------
-- 10. REUSABLE EXECUTIVE VIEWS
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS v_executive_kpi_summary;
CREATE VIEW v_executive_kpi_summary AS
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

DROP VIEW IF EXISTS v_critical_risk_employees;
CREATE VIEW v_critical_risk_employees AS
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

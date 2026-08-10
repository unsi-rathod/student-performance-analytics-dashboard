-- =====================================================
-- PURPOSE: Data quality checks before analysis
-- =====================================================


USE student_performance_analytics;


-- Total student records

SELECT
    COUNT(*) AS Total_Students
FROM student_performance_feature_engineered;



-- Duplicate student check

SELECT
    NAME,
    SECTION,
    COUNT(*) AS Duplicate_Count
FROM student_performance_feature_engineered
GROUP BY NAME, SECTION
HAVING COUNT(*) > 1;



-- Missing value check

SELECT
    SUM(NAME IS NULL OR NAME='') AS Missing_Name,
    SUM(SECTION IS NULL OR SECTION='') AS Missing_Section,
    SUM(Annual_Percentage IS NULL) AS Missing_Annual_Percentage,
    SUM(Performance_Band IS NULL) AS Missing_Performance_Band
FROM student_performance_feature_engineered;



-- Marks range validation

SELECT *
FROM student_performance_feature_engineered
WHERE
    HY_Q1 < 0 OR HY_Q1 > 100
    OR HY_Q2 < 0 OR HY_Q2 > 100
    OR HY_Q3 < 0 OR HY_Q3 > 100
    OR HY_Q4 < 0 OR HY_Q4 > 100
    OR HY_Q5 < 0 OR HY_Q5 > 100;



-- Percentage validation

SELECT *
FROM student_performance_feature_engineered
WHERE
    HY_Percentage < 0
    OR HY_Percentage > 100
    OR Annual_Percentage < 0
    OR Annual_Percentage > 100;



-- Category validation

SELECT DISTINCT PASS_FAIL_HY
FROM student_performance_feature_engineered;


SELECT DISTINCT PASS_FAIL_ANNUAL
FROM student_performance_feature_engineered;


SELECT DISTINCT Performance_Band
FROM student_performance_feature_engineered;


SELECT DISTINCT Risk_Level
FROM student_performance_feature_engineered;



-- Feature engineering validation

SELECT
    COUNT(*) AS Total_Rows,
    COUNT(HY_Percentage) AS HY_Percentage,
    COUNT(Annual_Percentage) AS Annual_Percentage,
    COUNT(Improvement_Status) AS Improvement_Status,
    COUNT(Risk_Level) AS Risk_Level
FROM student_performance_feature_engineered;



-- Sample records

SELECT *
FROM student_performance_feature_engineered
LIMIT 10;

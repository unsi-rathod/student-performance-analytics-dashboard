-- =====================================================
-- PURPOSE: Analyze overall student performance
-- =====================================================


USE student_performance_analytics;



-- Overall performance KPIs

SELECT
    COUNT(*) AS Total_Students,
    ROUND(AVG(HY_Percentage),2) AS Average_HY_Percentage,
    ROUND(AVG(Annual_Percentage),2) AS Average_Annual_Percentage,
    SUM(CASE 
        WHEN PASS_FAIL_ANNUAL='PASS' 
        THEN 1 ELSE 0 
    END) AS Total_Passed,
    SUM(CASE 
        WHEN PASS_FAIL_ANNUAL='FAIL' 
        THEN 1 ELSE 0 
    END) AS Total_Failed
FROM student_performance_feature_engineered;



-- Performance band distribution

SELECT
    Performance_Band,
    COUNT(*) AS Student_Count,
    ROUND(
        COUNT(*) * 100 /
        (SELECT COUNT(*) 
         FROM student_performance_feature_engineered),
        2
    ) AS Percentage
FROM student_performance_feature_engineered
GROUP BY Performance_Band
ORDER BY Student_Count DESC;



-- Annual grade distribution

SELECT
    Y_GRADE,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY Y_GRADE
ORDER BY Student_Count DESC;



-- Pass fail distribution

SELECT
    PASS_FAIL_ANNUAL,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY PASS_FAIL_ANNUAL;



-- Top performing students

SELECT
    NAME,
    SECTION,
    Annual_Percentage,
    Performance_Band,
    Improvement_Status
FROM student_performance_feature_engineered
ORDER BY Annual_Percentage DESC
LIMIT 10;



-- Students requiring intervention

SELECT
    NAME,
    SECTION,
    Annual_Percentage,
    Risk_Level,
    Needs_Intervention
FROM student_performance_feature_engineered
WHERE Needs_Intervention='Yes'
ORDER BY Annual_Percentage;



-- Section wise performance comparison

SELECT
    SECTION,
    COUNT(*) AS Total_Students,
    ROUND(AVG(Annual_Percentage),2) AS Average_Percentage,
    ROUND(AVG(Consistency_Score),2) AS Average_Consistency
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Average_Percentage DESC;



-- Risk level distribution

SELECT
    Risk_Level,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY Risk_Level
ORDER BY Student_Count DESC;



-- Performance band average analysis

SELECT
    Performance_Band,
    ROUND(AVG(Annual_Percentage),2) AS Average_Percentage,
    ROUND(AVG(Improvement_Percentage),2) AS Average_Improvement
FROM student_performance_feature_engineered
GROUP BY Performance_Band
ORDER BY Average_Percentage DESC;

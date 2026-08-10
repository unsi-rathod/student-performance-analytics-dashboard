-- =====================================================
-- PURPOSE: Create dashboard-ready datasets
-- =====================================================


USE student_performance_analytics;



-- =====================================================
-- KPI Summary
-- =====================================================

SELECT
    COUNT(*) AS Total_Students,

    ROUND(AVG(Annual_Percentage),2) 
    AS Average_Annual_Percentage,

    ROUND(AVG(Improvement_Percentage),2) 
    AS Average_Improvement,

    SUM(
        CASE 
            WHEN PASS_FAIL_ANNUAL='PASS' 
            THEN 1 ELSE 0 
        END
    ) AS Total_Passed,

    SUM(
        CASE 
            WHEN PASS_FAIL_ANNUAL='FAIL' 
            THEN 1 ELSE 0 
        END
    ) AS Total_Failed,

    SUM(
        CASE 
            WHEN Needs_Intervention='Yes'
            THEN 1 ELSE 0
        END
    ) AS Intervention_Required

FROM student_performance_feature_engineered;



-- =====================================================
-- Performance Band Dashboard Dataset
-- =====================================================

SELECT
    Performance_Band,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY Performance_Band
ORDER BY Student_Count DESC;



-- =====================================================
-- Growth Dashboard Dataset
-- =====================================================

SELECT
    Growth_Category,
    COUNT(*) AS Student_Count,
    ROUND(AVG(Improvement_Percentage),2) 
    AS Average_Improvement
FROM student_performance_feature_engineered
GROUP BY Growth_Category
ORDER BY Student_Count DESC;



-- =====================================================
-- Improvement Status Dashboard Dataset
-- =====================================================

SELECT
    Improvement_Status,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY Improvement_Status;



-- =====================================================
-- Section Performance Dashboard Dataset
-- =====================================================

SELECT
    SECTION,
    COUNT(*) AS Total_Students,
    ROUND(AVG(Annual_Percentage),2)
    AS Average_Percentage,
    ROUND(AVG(Improvement_Percentage),2)
    AS Average_Growth
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Average_Percentage DESC;



-- =====================================================
-- Risk Analysis Dashboard Dataset
-- =====================================================

SELECT
    Risk_Level,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY Risk_Level
ORDER BY Student_Count DESC;



-- =====================================================
-- Intervention Dashboard Dataset
-- =====================================================

SELECT
    SECTION,
    Needs_Intervention,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY SECTION, Needs_Intervention
ORDER BY SECTION;



-- =====================================================
-- Student Performance Detail Table
-- =====================================================

SELECT
    NAME,
    SECTION,
    HY_Percentage,
    Annual_Percentage,
    Improvement_Percentage,
    Performance_Band,
    Growth_Category,
    Risk_Level,
    Needs_Intervention
FROM student_performance_feature_engineered
ORDER BY Annual_Percentage DESC;
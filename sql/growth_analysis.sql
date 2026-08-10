-- =====================================================
-- PURPOSE: Analyze student growth and improvement trends
-- =====================================================


USE student_performance_analytics;



-- Overall improvement summary

SELECT
    ROUND(AVG(Improvement_Percentage),2) AS Average_Improvement,
    SUM(CASE 
        WHEN Improvement_Status='Improved' 
        THEN 1 ELSE 0 
    END) AS Students_Improved,
    SUM(CASE 
        WHEN Improvement_Status='Declined' 
        THEN 1 ELSE 0 
    END) AS Students_Declined,
    SUM(CASE 
        WHEN Improvement_Status='Stable' 
        THEN 1 ELSE 0 
    END) AS Students_Stable
FROM student_performance_feature_engineered;



-- Improvement status distribution

SELECT
    Improvement_Status,
    COUNT(*) AS Student_Count,
    ROUND(
        COUNT(*) * 100 /
        (SELECT COUNT(*) 
         FROM student_performance_feature_engineered),
        2
    ) AS Percentage
FROM student_performance_feature_engineered
GROUP BY Improvement_Status
ORDER BY Student_Count DESC;



-- Growth category distribution

SELECT
    Growth_Category,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY Growth_Category
ORDER BY Student_Count DESC;



-- Top improving students

SELECT
    NAME,
    SECTION,
    HY_Percentage,
    Annual_Percentage,
    Improvement_Percentage,
    Growth_Category
FROM student_performance_feature_engineered
ORDER BY Improvement_Percentage DESC
LIMIT 10;



-- Students with performance decline

SELECT
    NAME,
    SECTION,
    HY_Percentage,
    Annual_Percentage,
    Improvement_Percentage,
    Improvement_Status
FROM student_performance_feature_engineered
WHERE Improvement_Status='Declined'
ORDER BY Improvement_Percentage;



-- Students with highest growth category

SELECT
    NAME,
    SECTION,
    Growth_Category,
    Improvement_Percentage
FROM student_performance_feature_engineered
WHERE Growth_Category IS NOT NULL
ORDER BY Improvement_Percentage DESC;



-- Growth comparison by section

SELECT
    SECTION,
    COUNT(*) AS Total_Students,
    ROUND(AVG(Improvement_Percentage),2) AS Average_Growth
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Average_Growth DESC;



-- Performance improvement by initial performance

SELECT
    Performance_Band,
    ROUND(AVG(Improvement_Percentage),2) AS Average_Improvement
FROM student_performance_feature_engineered
GROUP BY Performance_Band
ORDER BY Average_Improvement DESC;



-- Students who improved but still need support

SELECT
    NAME,
    SECTION,
    Annual_Percentage,
    Improvement_Percentage,
    Risk_Level
FROM student_performance_feature_engineered
WHERE 
    Improvement_Status='Improved'
    AND Needs_Intervention='Yes'
ORDER BY Annual_Percentage;

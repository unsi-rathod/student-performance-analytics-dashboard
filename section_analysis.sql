-- =====================================================
-- PURPOSE: Analyze section-wise performance
-- =====================================================


USE student_performance_analytics;



-- Section wise student count

SELECT
    SECTION,
    COUNT(*) AS Total_Students
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Total_Students DESC;



-- Section wise average performance

SELECT
    SECTION,
    ROUND(AVG(HY_Percentage),2) AS Average_HY_Percentage,
    ROUND(AVG(Annual_Percentage),2) AS Average_Annual_Percentage
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Average_Annual_Percentage DESC;



-- Section wise improvement analysis

SELECT
    SECTION,
    ROUND(AVG(Improvement_Percentage),2) AS Average_Improvement
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Average_Improvement DESC;



-- Section wise consistency analysis
-- Consistency_Score is stored as text (High/Moderate/Low), so it is
-- mapped to a numeric scale before averaging: High=3, Moderate=2, Low=1
-- (higher score = more consistent performance).

SELECT
    SECTION,
    ROUND(
        AVG(
            CASE Consistency_Score
                WHEN 'High' THEN 3
                WHEN 'Moderate' THEN 2
                WHEN 'Low' THEN 1
            END
        ),
        2
    ) AS Average_Consistency_Score,
    SUM(CASE WHEN Consistency_Score='High' THEN 1 ELSE 0 END) AS High_Consistency_Count,
    SUM(CASE WHEN Consistency_Score='Moderate' THEN 1 ELSE 0 END) AS Moderate_Consistency_Count,
    SUM(CASE WHEN Consistency_Score='Low' THEN 1 ELSE 0 END) AS Low_Consistency_Count
FROM student_performance_feature_engineered
GROUP BY SECTION
ORDER BY Average_Consistency_Score DESC;



-- Performance band distribution by section

SELECT
    SECTION,
    Performance_Band,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY SECTION, Performance_Band
ORDER BY SECTION, Student_Count DESC;



-- Risk level distribution by section

SELECT
    SECTION,
    Risk_Level,
    COUNT(*) AS Student_Count
FROM student_performance_feature_engineered
GROUP BY SECTION, Risk_Level
ORDER BY SECTION;



-- Students requiring intervention by section

SELECT
    SECTION,
    COUNT(*) AS Intervention_Required
FROM student_performance_feature_engineered
WHERE Needs_Intervention='Yes'
GROUP BY SECTION
ORDER BY Intervention_Required DESC;



-- Top performing student in each section

SELECT
    SECTION,
    NAME,
    Annual_Percentage
FROM student_performance_feature_engineered s
WHERE Annual_Percentage =
(
    SELECT MAX(Annual_Percentage)
    FROM student_performance_feature_engineered
    WHERE SECTION=s.SECTION
)
ORDER BY SECTION;



-- Section performance ranking

SELECT
    SECTION,
    ROUND(AVG(Annual_Percentage),2) AS Average_Percentage,
    RANK() OVER(
        ORDER BY AVG(Annual_Percentage) DESC
    ) AS Section_Rank
FROM student_performance_feature_engineered
GROUP BY SECTION;
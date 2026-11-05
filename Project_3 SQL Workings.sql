show databases;
create database myproject3db;
use myproject3db;
show tables;

select * from job_acceptance;
select * from results;

# EDA
# Academic scores vs placement outcome
select status as Placement_outcome, round(avg(Qualification_percentage),2) as Avg_Academic_score from job_acceptance
group by status order by Avg_Academic_score desc;

# Skills match vs interview performance
select Skills_match_level as Skills_Match, format(avg(Interview_Score),2) as Interview_Perf from job_acceptance
group by Skills_match_level order by Interview_Perf desc;

# Certification impact on job acceptance
select status as Job_Acceptance, format(count(certifications_count),0) as Count_Certificates from job_acceptance
group by status order by Count_Certificates;

# Acceptance rate by company tier
SELECT company_tier,
    SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) AS Placed_Count,
    SUM(CASE WHEN status = 'Not Placed' THEN 1 ELSE 0 END) AS Not_Placed_Count,
    ROUND(SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) * 100.0 /COUNT(*), 2) AS Acceptance_Rate_Percent
FROM job_acceptance
GROUP BY company_tier;

# Experience vs placement success
select status as Placement, avg(years_of_experience) as Avg_Experience from job_acceptance
group by status order by Avg_Experience desc;

# Interview score vs placement probability


#change column names in both the tables
ALTER TABLE job_acceptance 
    CHANGE COLUMN `Experience category_Junior` Experience_category_Junior VARCHAR(255),
    CHANGE COLUMN `Experience category_Senior` Experience_category_Senior VARCHAR(255),
    CHANGE COLUMN `Academic_performance_bands_Good` Academic_performance_bands_Good VARCHAR(255),
    CHANGE COLUMN `Skills_match_level_Low` Skills_match_level_Low VARCHAR(255),
    CHANGE COLUMN `Skills_match_level_Medium` Skills_match_level_Medium VARCHAR(255),
    CHANGE COLUMN `Interview_performance_category_Excellent` Interview_performance_category_Excellent VARCHAR(255),
    CHANGE COLUMN `Interview_performance_category_Good` Interview_performance_category_Good VARCHAR(255);

ALTER TABLE results 
    CHANGE COLUMN `Experience category_Junior` Experience_category_Junior VARCHAR(255),
    CHANGE COLUMN `Experience category_Senior` Experience_category_Senior VARCHAR(255),
    CHANGE COLUMN `Academic_performance_bands_Good` Academic_performance_bands_Good VARCHAR(255),
    CHANGE COLUMN `Skills_match_level_Low` Skills_match_level_Low VARCHAR(255),
    CHANGE COLUMN `Skills_match_level_Medium` Skills_match_level_Medium VARCHAR(255),
    CHANGE COLUMN `Interview_performance_category_Excellent` Interview_performance_category_Excellent VARCHAR(255),
    CHANGE COLUMN `Interview_performance_category_Good` Interview_performance_category_Good VARCHAR(255);
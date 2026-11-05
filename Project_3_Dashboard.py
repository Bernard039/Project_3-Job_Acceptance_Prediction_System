## Streamlit

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pymysql
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine

Connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='Tommy039',
    database='myproject3db'
    )
host='localhost'
port=3306
user='root'
password='Tommy039'
database='myproject3db'

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")


all_queries ={
'Academic scores vs placement outcome':
"""select status as Placement_outcome, round(avg(Qualification_percentage),2) as Avg_Academic_score from job_acceptance
group by status order by Avg_Academic_score desc;""",

'Skills match vs interview performance':
"""select Skills_match_level as Skills_Match, format(avg(Interview_Score),2) as Interview_Perf from job_acceptance
group by Skills_match_level order by Interview_Perf desc;""",

'Certification impact on job acceptance':
"""select status as Job_Acceptance, format(count(certifications_count),0) as Count_Certificates from job_acceptance
group by status order by Count_Certificates;""",

'Acceptance rate by company tier':
"""SELECT company_tier,
    SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) AS Placed_Count,
    SUM(CASE WHEN status = 'Not Placed' THEN 1 ELSE 0 END) AS Not_Placed_Count,
    ROUND(SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) * 100.0 /COUNT(*), 2) AS Acceptance_Rate_Percent
FROM job_acceptance
GROUP BY company_tier order by Acceptance_Rate_Percent desc;""",

'Experience vs placement success':
"""select status as Placement, avg(years_of_experience) as Avg_Experience from job_acceptance
group by status order by Avg_Experience desc;""",

'Interview score vs placement probability':"""  """
}

# Declare df2 globally

df2 = None

# Streamlit UI
# --------------------------------------
# Navigator
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to",['Introduction','Dashboard','SQL Queries','Creator Info'])


# Introduction Page
if page == "Introduction":
    st.title("Job Acceptance Prediction System",width="content",text_alignment="center")
    st.image(image="Job accept.jpg",)
    st.subheader("Introduction:")
    st.write("""
This project focuses on predicting whether candidates will be successfully placed based on the provided dataset. 
Machine Learning models are applied to estimate the probability of candidates joining the company, 
while key KPIs are highlighted to present a clear numerical representation of the data through an interactive dashboard.

Features:

- Filter and view placement data by Gender and placement status .
- The dataset is represented using key KPIs, providing rate‑based and numerical indicators that highlight important outcomes. 
- Execute predefined SQL queries to explore deeper analytical insights.
    """)

# SQL Query Page

elif page == "SQL Queries":
    st.title("📋Exploratory Data Analysis using SQL")

# Dropdown
    task = st.selectbox("Please select from below", list(all_queries.keys()))

# Run button
    if st.button("Run Query"):
        query = all_queries[task]
        df2 = pd.read_sql(query, engine)
    
        st.subheader(f"Results for: {task}")
        st.dataframe(df2, use_container_width=True)


# Dashboard page

elif page == "Dashboard":
        st.title("📊 Job Acceptance Prediction Dashboard")

        query1 = "SELECT * FROM job_acceptance"
        df2 = pd.read_sql(query1, engine) 

        filtered_df = df2.copy()

        st.subheader("Filters:")

        # Filters
        col1,col2 = st.columns(2)
        with col1:
            gender_filter = st.selectbox("Gender", ["Please select","Male", "Female"])
        with col2:
            status_filter = st.selectbox("Status", ["Please select","Placed", "Not Placed"])
        
        # Apply filters
        if gender_filter != "Please select":
            filtered_df = df2[df2["gender"] == gender_filter]
        if status_filter != "Please select":
            filtered_df = df2[df2["status"] == status_filter]

        # --- KPI: Total Candidates ---
        st.subheader("Key KPIs:")

        Total_candidates = len(filtered_df)
        Placement_Rate = (filtered_df["status"].eq("Placed").mean()) * 100
        Job_Acceptance_Rate = (filtered_df['status'].eq("Placed").mean()) *100
        Average_Interview_Score = (filtered_df['Interview_Score'].median())
        Average_Skills_Match = (filtered_df['skills_match_percentage'].median())
        Offer_Dropout_Rate = (filtered_df["status"].eq("Not Placed").mean()) * 100

        # Display KPI
        coll1, coll2, coll3 = st.columns(3)
        
        with coll1:
            st.metric("Total Candidates", Total_candidates)
        with coll2:
            st.metric("Placement Rate", f"{Placement_Rate:.2f}%")
        with coll3:
            st.metric("Job Acceptance Rate", f"{Job_Acceptance_Rate:.2f}%")

        coll4, coll5, coll6 = st.columns(3)
        with coll4:
            st.metric("Average Interview Score", f"{Average_Interview_Score:.2f}")
        with coll5:
            st.metric("Average Skills Match", f"{Average_Skills_Match:.2f}")
        with coll6:
            st.metric("Offer Dropout Rate", f"{Offer_Dropout_Rate:.2f}%")



# Creator Info page
elif page == "Creator Info":
        st.title("🎓 Project Creator Information",text_alignment="center")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("**Name:** Bernard Arokiaraj. A")
        st.markdown(" ")
        st.markdown("**Course:** Data Science")
        st.markdown(" ")
        st.markdown("**Batch:** B4")    
        



# streamlit run Project_3_Dashboard.py
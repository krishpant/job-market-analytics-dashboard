
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

st.title("Job Market Analytics Dashboard")

df = pd.read_csv("jobs_in_data.csv")

st.sidebar.header("Job Filters")

# Job Title Filter
job_options = ["All"] + sorted(df["job_title"].dropna().unique().tolist())
selected_job = st.sidebar.selectbox("Select Job Title", job_options)

# Experience Filter
experience_options = ["All"] + sorted(df["experience_level"].dropna().unique().tolist())
selected_experience = st.sidebar.selectbox("Experience Level", experience_options)

# Work Setting Filter
work_options = ["All"] + sorted(df["work_setting"].dropna().unique().tolist())
selected_work = st.sidebar.selectbox("Work Setting", work_options)

# Salary Filter
min_salary = int(df["salary_in_usd"].min())
max_salary = int(df["salary_in_usd"].max())

salary_range = st.sidebar.slider(
    "Select Salary Range (USD)",
    min_salary,
    max_salary,
    (min_salary, max_salary)
)

# Apply Filters
filtered_df = df.copy()

if selected_job != "All":
    filtered_df = filtered_df[filtered_df["job_title"] == selected_job]

if selected_experience != "All":
    filtered_df = filtered_df[filtered_df["experience_level"] == selected_experience]

if selected_work != "All":
    filtered_df = filtered_df[filtered_df["work_setting"] == selected_work]

filtered_df = filtered_df[
    (filtered_df["salary_in_usd"] >= salary_range[0]) &
    (filtered_df["salary_in_usd"] <= salary_range[1])
]

# Dashboard Metrics
st.subheader("Job Market Overview")

col1, col2, col3 = st.columns(3)

if len(filtered_df) > 0:

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_jobs.csv",
        mime="text/csv"
    )

    col1.metric("Total Jobs", len(filtered_df))
    col2.metric("Average Salary (USD)", round(filtered_df["salary_in_usd"].mean()))
    col3.metric("Highest Salary (USD)", filtered_df["salary_in_usd"].max())

    st.subheader("Top 10 Job Titles")
    top_jobs = filtered_df["job_title"].value_counts().head(10)
    st.bar_chart(top_jobs)

    st.subheader("Average Salary by Experience")
    experience_salary = filtered_df.groupby("experience_level")["salary_in_usd"].mean()
    st.bar_chart(experience_salary)

    st.subheader("Average Salary by Work Setting")
    work_salary = filtered_df.groupby("work_setting")["salary_in_usd"].mean()
    st.bar_chart(work_salary)

else:
    st.warning("No jobs found. Please change your filters.")

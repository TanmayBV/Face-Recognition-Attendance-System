import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up the dashboard page layout
st.set_page_config(layout="wide", page_title="Admin Dashboard")

# Sidebar menu
st.sidebar.title("Dashboard")
st.sidebar.button("Task")
st.sidebar.button("User")
st.sidebar.button("Messages")
st.sidebar.button("Activities")
st.sidebar.button("Calendar")
st.sidebar.button("Post")
st.sidebar.button("Tickets")
st.sidebar.button("Reports")
st.sidebar.button("Jobs")
st.sidebar.button("Documents")
st.sidebar.button("Payroll")

# Header
st.header("Admin Dashboard")

# Top metrics section
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", "1259")
col2.metric("Job Openings", "23")
col3.metric("New Applicants", "123")
col4.info("Upcoming Company Event\n\nWatch a thriller")

# Visitor statistics section (example line chart)
st.subheader("Visitor Statistics")
months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
visitors_last6 = [475, 273, 300, 320, 450, 600, 525, 575]
visitors_previous = [782, 396, 430, 390, 460, 580, 500, 550]

plt.figure(figsize=(10, 4))
plt.plot(months, visitors_last6, label="Last 6 Months", color="blue")
plt.plot(months, visitors_previous, label="Previous", color="green")
plt.xlabel("Months")
plt.ylabel("Visitors")
plt.legend()
st.pyplot(plt)

# Tasks section (gauge chart representation using a radial progress indicator)
st.subheader("Tasks")
task_col1, task_col2 = st.columns(2)
task_col1.metric("Tasks Completion", "60%")
fig, ax = plt.subplots()
ax.pie([60, 40], labels=["Completed", "Remaining"], colors=["#66bb6a", "#ffcccb"], startangle=90, counterclock=False, wedgeprops=dict(width=0.3))
st.pyplot(fig)

# Invite section
st.subheader("Upcoming Event")
st.write("Invite to office meet-up")
st.write("Due date: December 23, 2018")
st.write("Rebecca Moore")
st.button("Call")

# Add further interactive elements and data connections as needed

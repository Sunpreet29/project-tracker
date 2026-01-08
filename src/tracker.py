import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import pandas as pd
import streamlit as st
from utils.db_ops import init_data, load_course_config, edit_progress, save_course_config

date_today = str(datetime.date.today())

# -------------------------------
# Streamlit setup
# -------------------------------
st.set_page_config(page_title="Progress Tracker", layout="wide")
st.title("📚 Progress Tracking Dashboard 📚")

# Load or create data
df_data = init_data()
course_config = load_course_config()

# Sidebar for role selection
role = st.sidebar.radio("Select Role", ["User", "Admin"])

# -------------------------------
# Admin Panel
# -------------------------------
if role == "Admin":
    st.subheader("🧑‍💼 Admin Panel")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":  # simple protection
        tab1, tab2 = st.tabs(["📈 Update Progress", "⚙️ Manage Courses"])

        # --- Progress Update Tab ---
        with tab1:
            if len(course_config) == 0:
                st.warning("No courses found. Please add one in the 'Manage Courses' tab.")
            else:
                date = st.date_input("Select Date", datetime.date.today())
                course = st.selectbox("Select Course", list(course_config.keys()))
                units_completed = st.number_input("Units Completed", min_value=0, step=1)

                if st.button("💾 Add Progress"):
                    edit_progress(str(date), course, units_completed)
                    st.success(f"Progress updated successfully for {course}!")

        # --- Course Management Tab ---
        with tab2:
            st.markdown("### Add or Edit Course Configurations")
            all_configs = dict(course_config)  # copy current configs

            selected_course = st.selectbox(
                "Select Course to Edit",
                ["➕ Add New"] + list(all_configs.keys())
            )

            if selected_course == "➕ Add New":
                course_name = st.text_input("New Course Name")
                existing = False
            else:
                course_name = selected_course
                existing = True

            if course_name:
                start_date = st.date_input(
                    "Start Date",
                    datetime.date.fromisoformat(
                        all_configs.get(course_name, {}).get("start_date", str(datetime.date.today()))
                    )
                )
                target_days = st.number_input(
                    "Target Days",
                    min_value=1,
                    value=int(all_configs.get(course_name, {}).get("target_days", 30))
                )
                target_units = st.number_input(
                    "Target Total Videos/Chapters/Units",
                    min_value=1,
                    value=int(all_configs.get(course_name, {}).get("target_units", 50))
                )

                if st.button("💾 Save Course Configuration"):
                    all_configs[course_name] = {
                        "start_date": str(start_date),
                        "target_days": int(target_days),
                        "target_units": int(target_units)
                    }
                    save_course_config(all_configs)
                    st.success(f"Configuration saved for {course_name}!")
                    st.experimental_rerun()

            st.markdown("### Existing Courses")
            if all_configs:
                st.dataframe(pd.DataFrame(all_configs).T)
            else:
                st.info("No courses configured yet.")

    else:
        st.warning("Enter valid password to edit data.", icon="🚨")


# -------------------------------
# Dashboard (Visible to Everyone)
# -------------------------------
st.subheader("📊 Progress Overview")

all_courses = sorted(df_data["course"].unique())

visible_courses = st.multiselect(
    "Select projects to display",
    all_courses,
    default=all_courses[0]  # or any subset
)

if not visible_courses:
    st.info("Select at least one project to display.")
    st.stop()

for course, cfg in course_config.items():
    if course not in visible_courses:
        continue

    st.markdown(f"## {course} Progress")

    # --- Planned progress ---
    start_date = pd.to_datetime(cfg["start_date"])
    target_days = cfg["target_days"]
    target_units = cfg["target_units"]
    planned_per_day = target_units / target_days

    dates = [start_date + datetime.timedelta(days=j) for j in range(target_days)]
    df_planned = pd.DataFrame({
        "dates": dates,
        "planned_progress": np.arange(
            planned_per_day,
            target_units + planned_per_day,
            planned_per_day
        )
    })
    df_planned_till_date = df_planned[df_planned["dates"] <= date_today]

    # --- Actual progress ---
    df_course = df_data[df_data["course"] == course].sort_values("date")
    if not df_course.empty:
        df_course["cumulative_progress"] = df_course["units_completed"].cumsum()

    # --- Plotting ---
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_planned["dates"],
        y=df_planned["planned_progress"],
        mode="lines+markers",
        name=f"{course} Planned",
        line=dict(color="lightgreen")
    ))

    fig.add_trace(go.Scatter(
        x=df_planned_till_date["dates"],
        y=df_planned_till_date["planned_progress"],
        mode="lines+markers",
        name=f"{course} Planned till today",
        line=dict(color="green", width=3)
    ))

    if not df_course.empty:
        fig.add_trace(go.Scatter(
            x=df_course["date"],
            y=df_course["cumulative_progress"],
            mode="lines+markers",
            name=f"{course} Actual",
            line=dict(color="blue", width=3)
        ))

    fig.update_layout(
        height=500,
        width=1000,
        showlegend=True,
        title=f"{course} Tutorials Progress",
        xaxis_title="Date",
        yaxis_title="Videos/Chapters/Units Completed",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")  # visual separator between courses

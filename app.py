import streamlit as st
import streamlit.components.v1 as components
from data_manager import create_sub_table, add_priority, sort_by_priority
from plannerlogic import allocate_time

#CALENDER
def render_full_calendar():
    calendar_html = """
    <html>
      <head>
        <link href='https://cdn.jsdelivr.net/npm/fullcalendar@5.11.3/main.min.css' rel='stylesheet' />
        <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.11.3/main.min.js'></script>
      </head>
      <body>
        <div id='calendar'></div>
        <script>
          document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
              initialView: 'dayGridMonth',
              height: 450
            });
            calendar.render();
          });
        </script>
      </body>
    </html>
    """
    components.html(calendar_html, height=500)

#PAGE CONFIG
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📘",
    layout="wide"
)

#HEADER 
st.title("📘My Magic Planner")
st.caption("Plan smarter, not harder.")
st.divider()

#SESSION STATE
if "subjects" not in st.session_state:
    st.session_state.subjects = []

#LAYOUT
left_col, middle_col, right_col = st.columns([1.2, 1.6, 1.2])



#LEFT: ADD SUBJECT
with left_col:
    st.subheader("➕ Add Subject")

    with st.form("subject_form", clear_on_submit=True):
        subject = st.text_input("📚 Subject Name",key="subject_name")

        difficulty = st.slider("🔥 Difficulty",1, 5,key="difficulty")
        
        chapters = st.number_input("📖 Chapters",min_value=1,step=1,key="chapters")
        
        days_left = st.number_input("⏳ Days Left",min_value=1,step=1,key="days_left")

        submitted = st.form_submit_button("Add Subject")


        if submitted:
            if subject.strip() == "":
                st.warning("Subject name cannot be empty")
            else:
                st.session_state.subjects.append({
                "Subject": subject,
                "Difficulty": difficulty,
                "chapters": chapters,
                "days_left": days_left
            })

            st.success(f"✅ {subject} added!")

#MIDDLE: SUBJECT LIST
with middle_col:
    st.subheader("📋 Your Subjects")

    if len(st.session_state.subjects) == 0:
        st.info("No subjects added yet.")
    else:
        df = create_sub_table(st.session_state.subjects)
        st.dataframe(df, use_container_width=True)

#RIGHT: SETTINGS
with right_col:
    st.subheader("⚙️ Settings")

    study_hours = st.number_input(
        "🕒 Daily Study Hours",
        min_value=2,
        max_value=12,
        value=4
    )

    generate = st.button("🧠 Generate Study Plan")

#STUDY PLAN OUTPUT
st.divider()

if generate:
    if len(st.session_state.subjects) == 0:
        st.warning("⚠️ Please add at least one subject first.")
    else:
        # Create DataFrame from session data
        df = create_sub_table(st.session_state.subjects)

        # Apply planner logic
        df = add_priority(df)
        df = sort_by_priority(df)
        df = allocate_time(df, study_hours)

        st.subheader("🗓️ Today's Study Plan")

        # Show plan as messages
        for _, row in df.iterrows():
            st.success(
                f"📘 {row['Subject']} → {row['Allocated_Hours']:.2f} hrs"
            )

        # Visual chart
        st.subheader("📊 Time Distribution & Calendar")

        chart_col, cal_col = st.columns([1.5, 1])

        with chart_col:
            st.write("### 📊 Time Distribution")
            st.bar_chart(df.set_index("Subject")["Allocated_Hours"])

        with cal_col:
            st.write("### 📅 Calendar")
            render_full_calendar()

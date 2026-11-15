
import streamlit as st
import pandas as pd


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

    /* Main Background */

    .stApp {
        background-color: #F4F7FB;
    }

    /* Main Container */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */

    .main-header {
        background: linear-gradient(120deg, #142D4E, #245B78);
        padding: 35px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
    }

    .main-header h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 8px;
    }

    .main-header p {
        color: #D8E8F3;
        font-size: 16px;
    }

    /* Section Headers */

    .section-title {
        color: #183B56;
        font-size: 23px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Metric Cards */

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2EAF2;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #183B56;
        font-weight: 700;
    }

    /* Form Container */

    div[data-testid="stForm"] {
        background-color: white;
        padding: 25px;
        border: 1px solid #E2EAF2;
        border-radius: 14px;
    }

    /* Buttons */

    .stButton button,
    .stFormSubmitButton button {
        background-color: #147D78;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 10px 22px;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover {
        background-color: #10645F;
        color: white;
    }

    /* Table */

    div[data-testid="stDataFrame"] {
        border: 1px solid #E2EAF2;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Footer */

    .footer {
        text-align: center;
        color: #8291A5;
        padding: 30px;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "students" not in st.session_state:
    st.session_state.students = []


# ==========================================
# FUNCTION 1: CALCULATE GRADE
# SAME LOGIC AS DAY 2
# ==========================================

def get_grade(mark):

    if mark >= 90:
        return "A"

    elif mark >= 80:
        return "B"

    elif mark >= 70:
        return "C"

    elif mark >= 60:
        return "D"

    else:
        return "E"


# ==========================================
# FUNCTION 2: ADD STUDENT
# ==========================================

def add_student(name, mark):

    student = {
        "Name": name,
        "Mark": mark,
        "Grade": get_grade(mark)
    }

    st.session_state.students.append(student)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="main-header">
    <h1>🎓 Student Grade Manager</h1>
    <p>
        Manage student performance, track academic results
        and monitor classroom statistics.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# STUDENT REGISTRATION FORM
# ==========================================

st.markdown(
    '<div class="section-title">📝 Add New Student</div>',
    unsafe_allow_html=True
)

with st.form("student_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Student Name",
            placeholder="Enter student name",
            max_chars=30
        )

    with col2:

        mark = st.number_input(
            "Student Mark",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

    submit = st.form_submit_button(
        "➕ Add Student",
        use_container_width=True
    )


# ==========================================
# FORM VALIDATION
# ==========================================

if submit:

    name = name.strip()

    if not name:

        st.error("Please enter a student name.")

    elif len(name) > 30:

        st.error("Student name cannot exceed 30 characters.")

    elif any(
        s["Name"].casefold() == name.casefold()
        for s in st.session_state.students
    ):

        st.error("This student is already registered.")

    else:

        add_student(name, int(mark))

        st.success(
            f"Student {name} added successfully!"
        )

        st.rerun()


# ==========================================
# CLASS PERFORMANCE DASHBOARD
# ==========================================

st.markdown(
    '<div class="section-title">📊 Class Performance Overview</div>',
    unsafe_allow_html=True
)


if st.session_state.students:

    marks = [
        student["Mark"]
        for student in st.session_state.students
    ]

    average = sum(marks) / len(marks)

    highest = max(marks)

    lowest = min(marks)

    total_students = len(st.session_state.students)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Students",
            total_students
        )

    with col2:

        st.metric(
            "Class Average",
            f"{average:.1f}"
        )

    with col3:

        st.metric(
            "Highest Mark",
            highest
        )

    with col4:

        st.metric(
            "Lowest Mark",
            lowest
        )

else:

    st.info(
        "No student records available. "
        "Add your first student to view class statistics."
    )


# ==========================================
# STUDENT RESULTS TABLE
# ==========================================

st.markdown(
    '<div class="section-title">📋 Student Results</div>',
    unsafe_allow_html=True
)


if st.session_state.students:

    df = pd.DataFrame(st.session_state.students)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={

            "Name": st.column_config.TextColumn(
                "Student Name"
            ),

            "Mark": st.column_config.NumberColumn(
                "Marks",
                format="%d / 100"
            ),

            "Grade": st.column_config.TextColumn(
                "Grade"
            )

        }
    )

    # Download student records

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Student Results",
        data=csv,
        file_name="student_results.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "Student results will appear here after adding records."
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    Student Grade Manager | Built with Python & Streamlit
    <br>
    Academic Performance Management Dashboard
</div>
""", unsafe_allow_html=True)

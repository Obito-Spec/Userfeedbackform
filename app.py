# app.py

import streamlit as st
from datetime import date
from db_utils import insert_feedback, fetch_all_feedback

st.set_page_config("Visitor Feedback", layout="centered")
st.title("📋 Visitor Feedback Form")

with st.form("feedback_form"):
    st.subheader("Entry Details")
    name = st.text_input("Name")
    contact = st.text_input("Contact Number")
    purpose = st.text_area("Purpose of Visit")

    st.subheader("Exit Feedback")
    mobile = st.text_input("Registered Mobile Number")
    feedback = st.text_area("Feedback")

    st.subheader("Report Filter")
    report_date = st.date_input("Report Date", value=date.today())

    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        insert_feedback({
            "name": name,
            "contact_number": contact,
            "purpose": purpose,
            "mobile_number": mobile,
            "feedback": feedback,
            "report_date": report_date
        })
        st.success("✅ Feedback submitted to database!")
    except Exception as e:
        st.error(f"❌ Submission failed: {e}")

if st.button("📊 Show All Submissions"):
    try:
        df = fetch_all_feedback()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Failed to fetch data: {e}")

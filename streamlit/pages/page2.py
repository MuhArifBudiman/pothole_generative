import streamlit as st
import requests
import time
from services.api import get_status

job_id = st.session_state.get("job_id")
st.title(f"⏳ Processing data id: {job_id}")

if not job_id:
    st.warning("No job found")
    st.stop()

status_box = st.empty()
progress_bar = st.progress(0)

while True:
    res = get_status(job_id=job_id)
    data = res.json()

    progress = data.get("progress", 0)
    stage = data.get("stage")   # 0–100

    progress_bar.progress(progress)
    status_box.info(f"Current stage: **{stage}**")

    if data["status"] == "done":
        st.success("Processing completed")
        st.switch_page("pages/page3.py")
        break

    if data["status"] == "failed":
        st.error("Job failed")
        break

    time.sleep(2)

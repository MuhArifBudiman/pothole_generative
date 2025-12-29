import streamlit as st
import requests
from services.api import create_job

BASE_URL = 'http://127.0.0.1:8000/request'

st.set_page_config(
    page_title="Upload Data",
    page_icon="⏳",
    layout="wide"
)

st.title("📤 Video + GPX Processing")

video_file = st.file_uploader("Upload Video (.mp4)", type=["mp4"])
gpx_file = st.file_uploader("Upload GPS Track (.gpx)", type=["gpx"])

if st.button("🚀 Start Processing", disabled=not (video_file and gpx_file)):
    with st.spinner("Submitting job..."):
        files = {
            "video": video_file,
            "gpx": gpx_file
        }

        res = create_job(
            video=video_file,
            gpx=gpx_file
        )

        if res.status_code == 200:
            job_id = res.json()["job_id"]
            st.session_state["job_id"] = job_id
            st.success(f"Job created: {job_id}")
            st.switch_page("pages/page2.py")
        else:
            st.error("Failed to start job")

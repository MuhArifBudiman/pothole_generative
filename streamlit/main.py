import streamlit as st

st.set_page_config(page_title="Video + GPX AI", layout="centered")

st.title("🎥📍 Video + GPS AI Analysis")
st.markdown("""
This tool processes:
- Video (.mp4)
- GPS track (.gpx)

Using job-based background inference.
""")

st.page_link("pages/page1.py", label="Start Processing →")

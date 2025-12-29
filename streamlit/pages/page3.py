import streamlit as st
from services.api import get_result
from utils.json_parser import flatten_result
from components.filters import confidence_filter
from components.map_view import render_map
from components.frame_viewer import render_frame_viewer

st.set_page_config(page_title="Results", layout="wide")
st.title("🗺️ Result Overview")

job_id = st.session_state.get("job_id")
if not job_id:
    st.warning("No job found")
    st.stop()

res = get_result(job_id)
data = res.json()["data"]

df = flatten_result(data)
df = confidence_filter(df)

st.subheader("Map Overview")
render_map(df)

st.subheader("Frame Viewer")
render_frame_viewer(df)

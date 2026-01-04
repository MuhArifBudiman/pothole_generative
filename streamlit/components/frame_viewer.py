import streamlit as st
from PIL import Image
import os


def render_frame_viewer(df):
    job_id = st.session_state.get("job_id")
    if not job_id:
        st.error("Job ID not found in session")
        return

    frames = sorted(df["frame"].unique())
    selected = st.selectbox("Select Frame", frames)

    frame_row = df[df["frame"] == selected].iloc[0]

    # JSON gives: frames/frame_00001.jpg
    relative_frame_path = frame_row["frame_result_file"]

    # Construct full path: jobs/{job_id}/frames/xxx.jpg
    full_frame_path = os.path.join(
        "jobs",
        job_id,
        relative_frame_path
    )

    if not os.path.exists(full_frame_path):
        st.error(f"Frame not found: {full_frame_path}")
        return

    image = Image.open(full_frame_path)
    if image:
        print("Success open image")
    else:
        print("No Image")

    st.image(image, caption=f"Frame {selected}")
    st.json(frame_row.to_dict())

import streamlit as st
from PIL import Image
import os
import requests
from io import BytesIO

BASE_URL = "https://metalliferous-diploic-phoebe.ngrok-free.dev"


def render_frame_viewer(df):
    job_id = st.session_state.get("job_id")
    if not job_id:
        st.error("Job ID not found in session")
        return

    frames = sorted(df["frame"].unique())
    selected = st.selectbox("Select Frame", frames)

    frame_row = df[df["frame"] == selected].iloc[0]

    # JSON file name: frame_00001.jpg
    frame_name = os.path.basename(frame_row["frame_result_file"])
    frame_name = frame_name.replace("frame_results\\", "")
    # st.title(frame_name)
    image_url = f"{BASE_URL}/job/{job_id}/{frame_name}"

    image_resp = requests.get(image_url)

    if image_resp.status_code != 200:
        st.error(f"Failed to fetch image: {image_url}")
        return

    image = Image.open(BytesIO(image_resp.content))
    if image:
        print("Success open image")
    else:
        print("No Image")

    st.image(image, caption=f"Frame {selected}")
    # st.json(frame_row.to_dict())

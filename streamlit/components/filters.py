import streamlit as st

def confidence_filter(df):
    st.sidebar.header("Filter")
    conf = st.sidebar.slider(
        "Confidence Threshold",
        0.0, 1.0, 0.5
    )
    return df[df["confidence"] >= conf]

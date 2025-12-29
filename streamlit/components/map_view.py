import streamlit as st
import pydeck as pdk

def render_map(df):
    if df.empty:
        st.warning("No data to display")
        return

    map_df = (
        df.groupby(["lat", "lon"])
        .size()
        .reset_index(name="total_detect")
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        map_df,
        get_position='[lon, lat]',
        get_radius="total_detect * 3",
        pickable=True
    )

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=map_df["lat"].mean(),
            longitude=map_df["lon"].mean(),
            zoom=14
        ),
        layers=[layer]
    ))

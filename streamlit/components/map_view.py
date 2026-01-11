import streamlit as st
import pydeck as pdk


def render_map(df):
    if df.empty:
        st.warning("No data to display")
        return

    map_df = (
        df.groupby(["longitude", "latitude"]).size()
        .reset_index(name="total_detect")
    )
    map_df["radius"] = map_df["total_detect"].apply(
        lambda x: x * 20.5 if x < 10 else x * 10.5
    )

    layer = pdk.Layer("ScatterplotLayer",
                      map_df, get_position='[longitude, latitude]',
                      get_radius="radius",
                      pickable=True,
                      get_fill_color=[10, 201, 90, 180]
                      )

    deck = pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=map_df["latitude"].mean(),
            longitude=map_df["longitude"].mean(),
            zoom=17),
        layers=[layer],
        tooltip={
            "html": """
    <b>Total Detect:</b> {total_detect}<br/>
    <b>Latitude:</b> {latitude}<br/>
    <b>Longitude:</b> {longitude}
    """,
        })
    st.pydeck_chart(deck)

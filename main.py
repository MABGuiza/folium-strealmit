import requests
import folium
import streamlit as st
import pandas as pd
import geopandas as geopandas
from streamlit_folium import st_folium

API = 'https://elyssa.tsaas.tn/api'

REQUEST = {"req": {
    "type": "map_decoupage",
    "pays": "Tunisie",
    "version": "10",
    "decoupages": ["gouvernorat"]},
}

st.session_state.setdefault('center', [33.9989, 10.1658])
st.session_state.setdefault('zoom', 6)


@st.cache_data
def get_df() -> pd.DataFrame:
    response = requests.post(url=API, json=REQUEST)
    data = response.json()['map']['gouvernorat']

    gouvernorat = geopandas.GeoDataFrame.from_features(data, crs="EPSG:4326")

    return gouvernorat


df = get_df()

m = folium.Map(location=[33.9989, 10.1658], zoom_start=6)
folium.GeoJson(df).add_to(m)
# folium.GeoJson(load_geojson('gouvernorat')).add_to(m)

st_data = st_folium(m, center=st.session_state["center"],
                    zoom=st.session_state["zoom"], width=725)

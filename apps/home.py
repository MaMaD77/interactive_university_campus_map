import streamlit as st
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import base64
import os
from streamlit_image_select import image_select


def app():
    m = leafmap.Map(center=(36.17217, 43.96712), zoom=17.4)

    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(
        "assets/maps/home.geojson"))
    m.add_layer(fg)

    dataset = pd.read_json(
        "assets/data/home.json")

    for data in dataset.datas:
        popup_content = f'<img src="{data["image"]}" style="width:190px;height:150px;border-radius: 5px;"><br><b>{data["building_name"]}</b>'
        popup = folium.Popup(popup_content, max_width=200)
        folium.Marker(location=[data['latitude'], data['longitude']], popup=popup, icon=folium.Icon(
            color='blue', icon='graduation-cap', prefix='fa')).add_to(m)

    out = st_folium(
        fig=m,
        width=1200,
        height=600,
    )

    if (out['last_object_clicked']):

        index = out['last_object_clicked']
        selectedData = get_value_by_lat_lng(
            dataset.datas, index['lat'], index['lng'])

        img = image_select(
            label="Select a image",
            images=selectedData['images'],
        )

        if img:
            st.image(img)

        for department in selectedData['departments']:
            st.header(department['name'], divider='rainbow')
            st.markdown(department['description'])


def get_value_by_lat_lng(objects, lat, lng):
    for obj in objects:
        if ('latitude' in obj and obj['latitude'] == lat) and ('longitude' in obj and obj['longitude'] == lng):
            return obj
    return None

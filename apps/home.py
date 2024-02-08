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
    with open('assets/css/all.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    m = folium.Map(location=[36.17217,
                   43.96712], zoom_start=17.4)

    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(
        "assets/maps/home.geojson"))

    dataset = pd.read_json(
        "assets/data/home.json")
    html = '<h5>Building 9</h5><img src="data:image/png;base64,{}">'.format

    with open("assets/building9.jpg", "rb") as imagefile:
        convert = base64.b64encode(imagefile.read())
    pic1 = convert.decode('utf-8')
    iframe1 = folium.IFrame(html(pic1), width=130+10, height=150+10)
    popup1 = folium.Popup(iframe1, max_width=150)
    icon1 = folium.CustomIcon(
        "assets/dep-icon.png", icon_size=(40, 40))
    print('------------')
    for data in dataset.datas:
        print(data['latitude'])
        print(data['building_name'])
        print(popup1)
        print(icon1)
        fg.add_child(
            folium.Marker(
                location=[data['latitude'], data['longitude']],
                popup=str(popup1),
                tooltip=f"{data['building_name']}",
                # icon=icon1
            )
        )

    out = st_folium(
        m,
        feature_group_to_add=fg,
        center='center',
        width=1200,
        height=600,
    )

    def get_value_by_lat_lng(objects, lat, lng):
        for obj in objects:
            if ('latitude' in obj and obj['latitude'] == lat) and ('longitude' in obj and obj['longitude'] == lng):
                return obj
        return None

    if (out['last_object_clicked']):

        index = out['last_object_clicked']
        selectedData = get_value_by_lat_lng(
            dataset.datas, index['lat'], index['lng'])
        # imageindex = selectedData[0]
        # img_1 = dataset.datas.loc[imageindex]['image']

        img = image_select(
            label="Select a image",
            images=selectedData['images'],
        )

        if img:
            st.image(img)

        for department in selectedData['departments']:
            st.header(department['name'], divider='rainbow')
            st.markdown(department['description'])

import streamlit as st
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
import pandas as pd
from streamlit_image_select import image_select
import base64


def app():
    m = leafmap.Map(center=(36.17217, 43.96712), zoom=17.4)

    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(
        "assets/maps/home.geojson"))
    m.add_layer(fg)

    dataset = pd.read_json("assets/data/home.json")

    for data in dataset.datas:
        with open(data['image'], "rb") as f:
            image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        popup_content = f'<img src="data:image/png;base64,{encoded_image}" style="width:190px;height:150px;border-radius: 5px;"><br><b>{data["building_name"]}</b>'
        popup = folium.Popup(popup_content, max_width=200)
        folium.Marker(location=[data['latitude'], data['longitude']], popup=popup, tooltip=data['building_name'], icon=folium.Icon(
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

import streamlit as st
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
import pandas as pd
from streamlit_image_select import image_select
import base64


@st.cache_data
def load_data():
    return pd.read_json("assets/data/administration.json")


def render_marker(selectedData):
    url = selectedData['link']
    url_text = selectedData['building_name']
    contact = selectedData['contact']

    st.markdown(
        f'<a href="{url}" target="_blank" style="text-decoration:none;color:white;font-size:35px;font-weight:600">{url_text}</a>', unsafe_allow_html=True)
    st.markdown(
        f'<a href="tel:{contact}" target="_blank" style="text-decoration:none;color:white;font-size:25px;font-weight:600">Contact: {contact}</a>', unsafe_allow_html=True)

    st.markdown(selectedData['description'])

    img = image_select(
        label="Select an image",
        images=selectedData['images'],
    ) if len(selectedData['images']) > 1 else None

    st.image(img if img else selectedData['image'])

    divider_rainbow = """
        <style>
            p {
                margin-bottom: 0;
                line-height: 1.1;
            }
            
            .rainbow-border {
                position: relative;
                padding-bottom: 12px;
                display: block;
                margin-bottom: 7px;
            }

            .rainbow-border::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 2px;
                background-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
                background-size: 200% 200%;
                animation: rainbow 2s linear infinite;
            }

            @keyframes rainbow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
        </style>
        <hr class="rainbow">
        """
    st.markdown(divider_rainbow, unsafe_allow_html=True)

    for department in selectedData['departments']:
        d_url = department['link']
        name = department['name']
        d_contact = department['contact']

        st.markdown(
            f'<a href="{d_url}" target="_blank" style="text-decoration:none;color:white;font-size:35px;font-weight:600">{name}</a>', unsafe_allow_html=True)
        st.markdown(
            f'<a href="tel:{d_contact}" target="_blank" class="rainbow-border" style="text-decoration:none;color:white;font-size:25px;font-weight:600">Contact: {d_contact}</a>', unsafe_allow_html=True)


def app():
    m = leafmap.Map(center=(36.17217, 43.96712), zoom=17.4)

    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(
        "assets/maps/administration.geojson"))
    m.add_layer(fg)

    dataset = load_data()

    for data in dataset.datas:
        with open(data['image'], "rb") as f:
            image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        popup_content = f'<img src="data:image/png;base64,{encoded_image}" style="width:190px;height:150px;border-radius: 5px;"><br><b>{data["building_name"]}</b>'
        popup = folium.Popup(popup_content, max_width=200)
        folium.Marker(location=[data['latitude'], data['longitude']], popup=popup, tooltip=data['building_name'], icon=folium.Icon(
            color=data['icon_bg_color'], icon=data['icon'], prefix='fa')).add_to(m)

    out = st_folium(
        fig=m,
        width=1200,
        height=600,
    )

    if out['last_object_clicked']:
        index = out['last_object_clicked']
        selectedData = get_value_by_lat_lng(
            dataset.datas, index['lat'], index['lng'])
        render_marker(selectedData)


def get_value_by_lat_lng(objects, lat, lng):
    for obj in objects:
        if ('latitude' in obj and obj['latitude'] == lat) and ('longitude' in obj and obj['longitude'] == lng):
            return obj
    return None

import streamlit as st
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import base64
import os


def app():
    with open('assets/css/all.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    m = folium.Map(location=[36.17217,
                   43.96712], zoom_start=17.4)

    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(
        "assets/maps/home.geojson"))

    datas = pd.read_csv(
        "assets/data/home.csv")
    html = '<h5>Building 9</h5><img src="data:image/png;base64,{}">'.format
    pic1 = base64.b64encode(open("assets/building9.jpg").read()).decode()
    iframe1 = folium.IFrame(html(pic1),width=130+10, height=150+10)
    popup1 = folium.Popup(iframe1,max_width=150)
    icon1 = folium.features.CustomIcon("assets/dep-icon.png",icon_size=(40,40))
    for data in datas.itertuples():
        fg.add_child(
            folium.Marker(
                location=[data.latitude, data.longitude],
                popup=popup1,
                tooltip=f"{data.building_name}",
                icon=icon1

            )
        )

    out = st_folium(
        m,
        feature_group_to_add=fg,
        center='center',
        width=1200,
        height=600,
    )

    if (out['last_object_clicked']):

        index = out['last_object_clicked']
        selectedData = datas.index[(datas['latitude']==index['lat'])&(datas['longitude']==index['lng'])].tolist()
        imageindex=selectedData[0]
        img_1 = datas.loc[imageindex]['image_1']

        html_string = '''
        <div>
            <div class="carousel">
                <ul class="slides">
                <input type="radio" name="radio-buttons" id="img-1" checked />
                <li class="slide-container">
                    <div class="slide-image">
                    <img src="'''+img_1+'''">
                    </div>
                    <div class="carousel-controls">
                    <label for="img-3" class="prev-slide">
                        <span>&lsaquo;</span>
                    </label>
                    <label for="img-2" class="next-slide">
                        <span>&rsaquo;</span>
                    </label>
                    </div>
                </li>
                <input type="radio" name="radio-buttons" id="img-2" />
                <li class="slide-container">
                    <div class="slide-image">
                    <img src="'''+img_1+'''">
                    </div>
                    <div class="carousel-controls">
                    <label for="img-1" class="prev-slide">
                        <span>&lsaquo;</span>
                    </label>
                    <label for="img-3" class="next-slide">
                        <span>&rsaquo;</span>
                    </label>
                    </div>
                </li>
                <input type="radio" name="radio-buttons" id="img-3" />
                <li class="slide-container">
                    <div class="slide-image">
                    <img src="'''+img_1+'''">
                    </div>
                    <div class="carousel-controls">
                    <label for="img-2" class="prev-slide">
                        <span>&lsaquo;</span>
                    </label>
                    <label for="img-1" class="next-slide">
                        <span>&rsaquo;</span>
                    </label>
                    </div>
                </li>
                <div class="carousel-dots">
                    <label for="img-1" class="carousel-dot" id="img-dot-1"></label>
                    <label for="img-2" class="carousel-dot" id="img-dot-2"></label>
                    <label for="img-3" class="carousel-dot" id="img-dot-3"></label>
                </div>
                </ul>
            </div>
        </div>
        '''
        st.markdown(
            html_string,
            unsafe_allow_html=True,
        )
        
        st.title(datas.loc[imageindex]['header'])

        for i in range(9,18):
            dept_name = datas.iloc[imageindex,i+9]
            emptycell = datas.isnull().iloc[imageindex,i+9]
            if not emptycell:
                st.write(f"[{dept_name}]({datas.iloc[imageindex,i]}) - Phone: {datas.iloc[imageindex,i+18]} - Email: {datas.iloc[imageindex,i+27]}")


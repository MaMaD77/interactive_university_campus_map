import streamlit as st
import leafmap.foliumap as leafmap
import folium
from streamlit_folium import st_folium
import pandas as pd


def app():
    with open('assets/css/all.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    m = folium.Map(location=[36.17163205508429,
                   43.966015123674374], zoom_start=17)

    fg = folium.FeatureGroup(name="State bounds")
    fg.add_child(folium.features.GeoJson(
        "assets/maps/home.geojson"))

    datas = pd.read_csv(
        "assets/data/home.csv")

    for data in datas.itertuples():
        fg.add_child(
            folium.Marker(
                location=[data.latitude, data.longitude],
                popup=f"{data.index}",
                tooltip=f"{data.name}",
                icon=folium.Icon(color="green")

            )
        )

    out = st_folium(
        m,
        feature_group_to_add=fg,
        center='center',
        width=1200,
        height=500,
    )

    if (out['last_object_clicked_popup']):
        index = out['last_object_clicked_popup']
        selectedData = datas.loc[int(index)]
        img_1 = selectedData['image_1']

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

        st.title(selectedData['name'])
        st.write(selectedData['description'])

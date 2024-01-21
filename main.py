import streamlit as st
from streamlit_option_menu import option_menu
# import your app modules here
from apps import department, home, centers, sport, administration


st.set_page_config(page_title="Cihan University Campus",
                   page_icon="favicon.ico", layout="wide")

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": department.app, "title": "Departments", "icon": "buildings"},
    {"func": centers.app, "title": "Centers", "icon": "tree"},
    {"func": sport.app, "title": "Sport", "icon": "dribbble"},
    {"func": administration.app, "title": "Administration",
        "icon": "journal-bookmark-fill"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Cihan University",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break

import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import pages as pg
from pages.admin_dashboard import show_admin_dashboard

parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "logo.svg")

# Set up the Streamlit page configuration
st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Island Breeze", page_icon="🌴")

# Define the pages for the navbar, including emojis
pages = ["Home", "Tours", "Excursions", "Events", "Book", "Contact Us", "👤"]

# Define the styles for the navbar
styles = {
    "nav": {"background-color": "rgba(255, 191, 0, 1)"},
    "div": {"max-width": "65rem", "max-height": "50rem"},
    "span": {"border-radius": "0.5rem", "color": "rgb(49, 51, 63)", "margin": "0 0.125rem", "padding": "0.4375rem 0.625rem"},
    "active": {"background-color": "rgba(32, 204, 185, 0.49)"},
    "hover": {"background-color": "rgba(32, 204, 185, 1)"},
}

# Options for the navbar
options = {"show_menu": False, "show_sidebar": False}

# Create the navbar
page = st_navbar(pages, logo_path=logo_path, styles=styles, options=options)

# Initialize session state for page navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Define the page functions
functions = {
    "Home": pg.show_home,
    "Tours": pg.show_tours,
    "Excursions": pg.show_excursions,
    "Events": pg.show_events,
    "Book": pg.show_booking,
    "Contact Us": pg.show_contact,
    "Admin Dashboard": pg.show_admin_dashboard,
    "👤": pg.show_login  # Use emoji directly
}

# Redirect to the selected page
if st.session_state.logged_in:
    if st.session_state.page == "Admin Dashboard":
        show_admin_dashboard()
    else:
        st.write("You are already logged in.")
else:
    go_to = functions.get(page)
    if go_to:
        go_to()

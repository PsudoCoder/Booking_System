import streamlit as st
from pages.login import show_login
import base64
import streamlit.components.v1 as components

def show_home():

    st.markdown("""
        <style>
            .content-section {
                padding: 2rem;
                text-align: center;
            }
            .content-section h2 {
                font-size: 2.5rem;
                color: #33475b;
            }
            .content-section p {
                font-size: 1.2rem;
                color: #5f6368;
            }
        </style>
    """, unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/home1.jpg")

    with col2:
        st.image("images/home2.jpg")

    with col3:
        st.image("images/home3.jpg")


    st.write("  ")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.write(" ")

    with col5:
        st.image("logo.svg")

    with col6:
        st.write(" ")

    st.write("  ")

    col7, col8, col9 = st.columns(3)

    with col7:
        st.image("images/home4.jpg")

    with col8:
        st.image("images/home5.jpg")

    with col9:
        st.image("images/home6.jpg")


    st.markdown("""
        <div class="content-section" id="content-section">
            <h2>What We Offer</h2>
            <p></p>
            <p>Cultural Journeys: Dive into Cyprus's rich history with guided tours of historical sites, museums, and ancient temples.</p>
<p>Adventure Escapes: For the thrill-seekers, embark on exciting hikes, water sports, and off-road adventures.</p>
<p>Relaxing Retreats: Unwind with our leisurely tours of beautiful beaches, serene nature spots, and calming wellness activities.</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("<hr style='margin: 3rem 0;'>", unsafe_allow_html=True)

    st.markdown("""
        <div class="content-section">
            <h2>Why Choose Us</h2>
            <p></p>
            <p>Personalized Service: We tailor each experience to match your preferences and interests.</p>
            <p>Local Expertise: Our team of experts is passionate about Cyprus and eager to share its treasures with you.</p>
            <p>Sustainable Tourism: We are committed to responsible travel practices that respect and preserve the beauty of Cyprus.</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("<hr style='margin: 3rem 0;'>", unsafe_allow_html=True)
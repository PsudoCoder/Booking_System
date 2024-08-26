import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Excursion

# Setup the database engine and session
engine = create_engine('sqlite:///island_breeze.db', pool_size=5, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

def show_excursions():
    st.title("Explore Our Exciting Excursions")
    st.write("")
    st.write("")

    # Query the database for excursions
    excursions = session.query(Excursion).all()

    # Define the product to image name mapping
    image_map = {
        "Jeep Safari in the Akamas Peninsula": "jeep_safari_akamas.jpg",
        "Troodos Mountains & Kykkos Monastery": "troodos_kykkos_monastery.jpg",
        "Scuba Diving in Zenobia Wreck (Larnaca)": "scuba_diving_zenobia.jpg",
        "Omodos Winery Excursion": "omodos_winery_tour.jpg",
        "Cape Greco & Sea Caves Adventure Boat Trip": "cape_greco_sea_caves.jpg",
        "Sea Caves & Blue Lagoon Boat Trip": "sea_caves_blue_lagoon.jpg"
    }

    # Iterate over each excursion and display details
    for excursion in excursions:
        col1, col2 = st.columns([1, 2])
        with col1:
            # Use the product name to find the corresponding image file
            image_name = image_map.get(excursion.product, "default_excursion.jpg")
            image_path = f"images/{image_name}"
            st.image(image_path, use_column_width=True)
        with col2:
            st.subheader(excursion.product)
            st.write(excursion.description)
            st.write(f"**Price per Person:** €{excursion.price_per_person}")
            st.write(f"**Available Times:** {excursion.available_times}")
            st.write(f"**Available Days:** {excursion.available_days}")
            st.write(f"**Included Food:** {'Yes' if excursion.included_food == 'Yes' else 'No'}")
        st.markdown("---")

# Call the function to display the excursions
show_excursions()

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Tour

# Setup the database engine and session
engine = create_engine('sqlite:///island_breeze.db', pool_size=5, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


def show_tours():
    st.title("Explore Our Exciting Tours")
    st.write("")
    st.write("")

    # Query the database for tours
    tours = session.query(Tour).all()

    # Define the product to image name mapping
    image_map = {
        "Ancient Kingdoms Tour (Paphos, Kourion, Amathus)": "ancient_kingdoms_tour.jpg",
        "Village & Vineyard Tour (Lefkara, Omodos, Platres)": "village_vineyard_tour.jpg",
        "Venetian Bridges Safari": "venetian_bridges_safari.jpg",
        "Nicosia City Tour": "nicosia_city_tour.jpg",
        "Aphrodite’s Route (Paphos)": "aphrodite_route.jpg",
        "Waterfalls of Troodos Tour": "waterfalls_troodos_tour.jpg"
    }

    # Iterate over each tour and display details
    for tour in tours:
        col1, col2 = st.columns([1, 2])
        with col1:
            # Use the product name to find the corresponding image file
            image_name = image_map.get(tour.product, "default_tour.jpg")
            image_path = f"images/{image_name}"
            st.image(image_path, use_column_width=True)
        with col2:
            st.subheader(tour.product)
            st.write(tour.description)
            st.write(f"**Price per Person:** €{tour.price_per_person}")
            st.write(f"**Available Times:** {tour.available_times}")
            st.write(f"**Available Days:** {tour.available_days}")
            st.write(f"**Included Food:** {'Yes' if tour.included_food == 'Yes' else 'No'}")
        st.markdown("---")

# Call the function to display the tours
show_tours()

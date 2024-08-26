import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Event

# Setup the database engine and session
engine = create_engine('sqlite:///island_breeze.db', pool_size=5, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


def show_events():
    st.title("Explore Our Exciting Events")
    st.write("")
    st.write("")

    # Query the database for events
    events = session.query(Event).all()

    # Define the product to image name mapping
    image_map = {
        "Limassol Wine Festival": "limassol_wine_festival.jpg",
        "Ayia Napa International Music Festival": "ayia_napa_music_festival.jpg",
        "Paphos Aphrodite Festival": "paphos_aphrodite_festival.jpg",
        "Troodos Mountain Bike Challenge": "troodos_mountain_bike_challenge.jpeg",
        "Lefkara Street Food Festival": "lefkara_street_food_festival.jpg",
        "Paphos Beer Festival": "paphos_beer_festival.jpg"
    }

    # Iterate over each event and display details
    for event in events:
        col1, col2 = st.columns([1, 2])
        with col1:
            # Use the product name to find the corresponding image file
            image_name = image_map.get(event.product, "default_event.jpg")
            image_path = f"images/{image_name}"
            st.image(image_path, use_column_width=True)
        with col2:
            st.subheader(event.product)
            st.write(event.description)
            st.write(f"**Price per Person:** €{event.price_per_person}")
            st.write(f"**Available Times:** {event.available_times}")
            st.write(f"**Available Dates:** {event.available_dates}")
            st.write(f"**Included Food:** {'Yes' if event.included_food == 'Yes' else 'No'}")
        st.markdown("---")

# Call the function to display the events
show_events()
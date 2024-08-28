import streamlit as st
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Booking, Event, Tour, Excursion
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns

# Create a database session
engine = create_engine('sqlite:///island_breeze.db', pool_size=5, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


@st.dialog("Confirmation")
def delete_booking():
    booking_id = st.number_input("Enter Booking ID to Cancel", min_value=1, step=1)
    booking = session.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        if st.button("Confirm"):
            session.delete(booking)
            session.commit()
            st.success(f"Booking ID {booking_id} for {booking.product} has been cancelled.")
    else:
       st.warning("Please enter a valid Booking ID.")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

@st.dialog("Edit Product")
def edit_product():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("You need to be logged in to access this page.")
        return

    # Dashboard Title
    st.title("Edit Product")

    # Fetch all products
    events = session.query(Event).all()
    tours = session.query(Tour).all()
    excursions = session.query(Excursion).all()

    # Create a list of all products for dropdown
    products = [(event.product, 'Event', event) for event in events] + \
               [(tour.product, 'Tour', tour) for tour in tours] + \
               [(excursion.product, 'Excursion', excursion) for excursion in excursions]

    # Dropdown to select a product
    product_options = [product[0] for product in products]
    selected_product_name = st.selectbox("Select a Product to Edit", product_options)

    # Find the selected product
    selected_product = next((prod for prod in products if prod[0] == selected_product_name), None)

    if selected_product:
        product_name, product_type, product_instance = selected_product

        # Display current details in editable fields
        with st.form(key='edit_product_form'):
            st.subheader(f"Editing {product_name}")

            description = st.text_input("Description", value=product_instance.description)
            price_per_person = st.number_input("Price Per Person", value=product_instance.price_per_person,
                                               format="%0.2f")
            available_times = st.text_input("Available Times", value=product_instance.available_times)
            available_days = st.text_input("Available Days", value=product_instance.available_days)
            spots_per_time_slot = st.number_input("Spots Per Time Slot", value=product_instance.spots_per_time_slot)
            included_food = st.selectbox("Included Food", ['Yes', 'No'],
                                         index=['Yes', 'No'].index(product_instance.included_food))
            available_dates = st.text_input("Available Dates", value=product_instance.available_dates)

            # Save changes
            save_button = st.form_submit_button("Save Changes")

            if save_button:
                # Update the product in the database
                if product_type == 'Event':
                    product_instance.description = description
                    product_instance.price_per_person = price_per_person
                    product_instance.available_times = available_times
                    product_instance.available_days = available_days
                    product_instance.spots_per_time_slot = spots_per_time_slot
                    product_instance.included_food = included_food
                    product_instance.available_dates = available_dates
                elif product_type == 'Tour':
                    product_instance.description = description
                    product_instance.price_per_person = price_per_person
                    product_instance.available_times = available_times
                    product_instance.available_days = available_days
                    product_instance.spots_per_time_slot = spots_per_time_slot
                    product_instance.included_food = included_food
                    product_instance.available_dates = available_dates
                elif product_type == 'Excursion':
                    product_instance.description = description
                    product_instance.price_per_person = price_per_person
                    product_instance.available_times = available_times
                    product_instance.available_days = available_days
                    product_instance.spots_per_time_slot = spots_per_time_slot
                    product_instance.included_food = included_food
                    product_instance.available_dates = available_dates

                session.commit()
                st.success(f"Product '{product_name}' has been updated successfully.")

@st.dialog("Create Product")
def create_product():
    # Choose product type
    product_type = st.selectbox("Select Product Type", ['Event', 'Tour', 'Excursion'])

    with st.form(key='create_product_form'):
        st.subheader(f"Create {product_type}")

        product_name = st.text_input("Product Name")
        description = st.text_area("Description")
        price_per_person = st.number_input("Price Per Person", format="%0.2f")
        available_times = st.text_input("Available Times")
        if product_type != "Event":
            available_days = st.text_input("Available Days")
        spots_per_time_slot = st.number_input("Spots Per Time Slot")
        included_food = st.selectbox("Included Food", ['Yes', 'No'])
        if product_type == "Event":
            available_dates = st.text_input("Available Dates")

        # Save new product
        save_button = st.form_submit_button("Create Product")

        if save_button:
            # Create and add product to the database
            if product_type == 'Event':
                new_product = Event(
                    product=product_name,
                    description=description,
                    price_per_person=price_per_person,
                    available_times=available_times,
                    spots_per_time_slot=spots_per_time_slot,
                    included_food=included_food,
                    available_dates=available_dates
                )
            elif product_type == 'Tour':
                new_product = Tour(
                    product=product_name,
                    description=description,
                    price_per_person=price_per_person,
                    available_times=available_times,
                    available_days=available_days,
                    spots_per_time_slot=spots_per_time_slot,
                    included_food=included_food,
                )
            elif product_type == 'Excursion':
                new_product = Excursion(
                    product=product_name,
                    description=description,
                    price_per_person=price_per_person,
                    available_times=available_times,
                    available_days=available_days,
                    spots_per_time_slot=spots_per_time_slot,
                    included_food=included_food,
                )

            session.add(new_product)
            session.commit()
            st.success(f"{product_type} '{product_name}' has been created successfully.")

@st.dialog("Delete a product")
def delete_product():
    # Fetch all products from each table
    events = session.query(Event).all()
    tours = session.query(Tour).all()
    excursions = session.query(Excursion).all()

    # Create a list of all products for dropdown
    products = [(event.product, 'Event', event) for event in events] + \
               [(tour.product, 'Tour', tour) for tour in tours] + \
               [(excursion.product, 'Excursion', excursion) for excursion in excursions]

    # Dropdown to select a product
    product_options = [product[0] for product in products]
    selected_product_name = st.selectbox("Select a Product to Delete", product_options)

    if selected_product_name:
        # Find the selected product instance
        selected_product = next((prod for prod in products if prod[0] == selected_product_name), None)
        if selected_product:
            product_name, product_type, product_instance = selected_product

            # Confirm deletion
            if st.button(f"Delete {product_type} '{product_name}'"):
                session.delete(product_instance)
                session.commit()
                st.success(f"{product_type} '{product_name}' has been deleted successfully.")

@st.dialog("Edit Booking")
def edit_booking():
    booking_id_input = st.number_input("Enter Booking ID to Edit", min_value=1, step=1)

    if booking_id_input:
        # Fetch the booking from the database
        selected_booking = session.query(Booking).filter(Booking.id == booking_id_input).first()

        if selected_booking:
            # Display current details
            st.write("Current Details")
            st.write(f"Product: {selected_booking.product}")
            st.write(f"Date: {selected_booking.date}")
            st.write(f"Time: {selected_booking.time}")
            st.write(f"Total Slots: {selected_booking.total_slots}")
            st.write(f"Taken Slots: {selected_booking.taken_slots}")
            st.write(f"Date Booked: {selected_booking.date_booked}")
            st.write(f"Amount Paid: {selected_booking.amount_paid}")

            # Edit booking details
            new_product = st.text_input("Product", value=selected_booking.product)
            new_date = st.date_input("Date", value=selected_booking.date)
            new_time = st.time_input("Time", value=selected_booking.time)
            new_total_slots = st.number_input("Total Slots", value=selected_booking.total_slots)
            new_taken_slots = st.number_input("Taken Slots", value=selected_booking.taken_slots)
            new_date_booked = st.date_input("Date Booked", value=selected_booking.date_booked)
            new_amount_paid = st.number_input("Amount Paid", value=selected_booking.amount_paid)

            # Save changes
            if st.button("Save Changes"):
                if new_product and new_date and new_time and new_total_slots >= 0 and new_taken_slots >= 0:
                    selected_booking.product = new_product
                    selected_booking.date = new_date
                    selected_booking.time = new_time
                    selected_booking.total_slots = new_total_slots
                    selected_booking.taken_slots = new_taken_slots
                    selected_booking.date_booked = new_date_booked
                    selected_booking.amount_paid = new_amount_paid

                    session.commit()
                    st.success("Booking details updated successfully.")
                else:
                    st.error("Please ensure all fields are filled out correctly.")
        else:
            st.error("No booking found with the provided ID.")


def show_admin_dashboard():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("You need to be logged in to access this page.")
        return

    # Dashboard Title and Logout Button
    st.title("Admin Dashboard")

    # Define date range for the last week and last month
    today = dt.datetime.today().date()
    last_week = today - dt.timedelta(days=7)
    last_month = today - dt.timedelta(days=30)

    bookings_query = session.query(Booking).all()
    full_bookings_df = pd.DataFrame([{
        'id': booking.id,
        'product': booking.product,
        'date': booking.date,
        'time': booking.time,
        'total_slots': booking.total_slots,
        'taken_slots': booking.taken_slots,
        'date_booked': booking.date_booked,
        'amount_paid': booking.amount_paid
    } for booking in bookings_query])

    events_query = session.query(Event).all()
    tours_query = session.query(Tour).all()
    excursions_query = session.query(Excursion).all()

    # Convert to DataFrame
    events_df = pd.DataFrame([{
        'Type': 'Event',
        'Product': event.product,
        'Description': event.description,
        'Price_Per_Person': event.price_per_person,
        'Available_Times': event.available_times,
        'Available_Days': event.available_days,
        'Spots_Per_Time_Slot': event.spots_per_time_slot,
        'Included_Food': event.included_food,
        'Available_Dates': event.available_dates
    } for event in events_query])

    tours_df = pd.DataFrame([{
        'Type': 'Tour',
        'Product': tour.product,
        'Description': tour.description,
        'Price_Per_Person': tour.price_per_person,
        'Available_Times': tour.available_times,
        'Available_Days': tour.available_days,
        'Spots_Per_Time_Slot': tour.spots_per_time_slot,
        'Included_Food': tour.included_food,
        'Available_Dates': tour.available_dates
    } for tour in tours_query])

    excursions_df = pd.DataFrame([{
        'Type': 'Excursion',
        'Product': excursion.product,
        'Description': excursion.description,
        'Price_Per_Person': excursion.price_per_person,
        'Available_Times': excursion.available_times,
        'Available_Days': excursion.available_days,
        'Spots_Per_Time_Slot': excursion.spots_per_time_slot,
        'Included_Food': excursion.included_food,
        'Available_Dates': excursion.available_dates
    } for excursion in excursions_query])

    # Combine DataFrames
    all_products_df = pd.concat([events_df, tours_df, excursions_df], ignore_index=True)

    # Fetch data from the database for the last week by booking date
    bookings_last_week = session.query(
        Booking.date_booked,
        func.count(Booking.id).label('count'),
        func.sum(Booking.amount_paid).label('total_revenue')
    ).filter(Booking.date_booked >= last_week).group_by(Booking.date_booked).all()

    # Combine bookings data into a single DataFrame
    bookings_data = {
        'Date_Booked': [],
        'Bookings': [],
        'Total_Revenue': []
    }

    # Populate bookings_data with data
    for booking in bookings_last_week:
        bookings_data['Date_Booked'].append(booking.date_booked)
        bookings_data['Bookings'].append(booking.count)
        bookings_data['Total_Revenue'].append(booking.total_revenue)

    bookings_df = pd.DataFrame(bookings_data)
    bookings_per_day = bookings_df.groupby('Date_Booked').agg({'Bookings': 'sum'}).reset_index()
    revenue_per_day = bookings_df.groupby('Date_Booked').agg({'Total_Revenue': 'sum'}).reset_index()

    # Fetch most popular products in the last month
    most_popular_products = session.query(
        Booking.product.label('product'),
        func.count(Booking.id).label('count')
    ).filter(Booking.date_booked >= last_month).group_by(Booking.product).all()

    # Convert to DataFrame and sort by popularity
    popular_products_df = pd.DataFrame(most_popular_products, columns=['Product', 'Count']).sort_values(by='Count')

    cols = st.columns(8)
    with cols[0]:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    with cols[1]:
        if st.button("Cancel Booking"):
            delete_booking()

    with cols[2]:
        if st.button("Edit Booking"):
            edit_booking()

    with cols[3]:
        csv = convert_df(bookings_df)
        st.download_button(
            label="Summary ⬇️",
            data=csv,
            file_name="bookings_summary.csv",
            mime="text/csv",
        )

    with cols[4]:
        csv2 = convert_df(full_bookings_df)
        st.download_button(
            label="Bookings ⬇️",
            data=csv2,
            file_name="bookings.csv",
            mime="text/csv",
        )

    with cols[5]:
        if st.button("Create a Product"):
            create_product()

    with cols[6]:
        if st.button("Edit a Product"):
            edit_product()

    with cols[7]:
        if st.button("Delete a Product"):
            delete_product()

    # Plotting
    col1, col2 = st.columns(2)

    # Bookings in Last Week Per Day based on date booked
    with col1:
        st.subheader("Bookings in Last Week Per Day")
        st.line_chart(bookings_per_day.set_index('Date_Booked'))

    # Total Revenue Per Day in Last Week based on date booked
    with col2:
        st.subheader("Total Revenue Per Day in Last Week")
        st.bar_chart(revenue_per_day.set_index('Date_Booked'))

    # Second row for charts and booking cancellation
    col3, col4 = st.columns(2)

    # Most Popular Products in Last Month
    with col3:
        st.subheader("Top 5 Most Popular Products in Last Month")
        top_5_products = popular_products_df.tail(5)
        fig2, ax2 = plt.subplots(facecolor='white')  # Set the figure background to black
        ax2.set_facecolor('white')  # Set the axes background to black
        ax2.barh(top_5_products['Product'], top_5_products['Count'], color='skyblue')
        ax2.set_xlabel('Number of Bookings', color='black')
        ax2.set_title('Top 5 Most Popular Products', color='black')
        ax2.tick_params(axis='x', colors='black')  # Change x-axis tick color to white
        ax2.tick_params(axis='y', colors='black')  # Change y-axis tick color to white
        st.pyplot(fig2)

    with col4:

        st.subheader("Bookings for each Product")
        bookings_per_product = full_bookings_df.groupby('product').size().reset_index(name='number_of_bookings')
        bookings_per_product = bookings_per_product.sort_values(by='number_of_bookings', ascending=False)

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(bookings_per_product['product'], bookings_per_product['number_of_bookings'], color='skyblue')

        # Customize the plot
        ax.set_xlabel('Number of Bookings')
        ax.set_ylabel('Product')
        ax.set_title('Number of Bookings Per Product')

        # Set background color
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.title.set_color('black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')

        st.pyplot(fig)


    st.subheader("Available Products")
    st.dataframe(all_products_df)

    session.close()



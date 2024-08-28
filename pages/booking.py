
from sqlite3 import OperationalError
from courier.client import Courier
import streamlit as st
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Tour, Excursion, Event, Booking
import pandas as pd
import boto3
import re

# Create an engine and session
engine = create_engine('sqlite:///island_breeze.db', pool_size=5, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


def load_data():
    """Load data from the database."""
    tours = session.query(Tour).all()
    excursions = session.query(Excursion).all()
    events = session.query(Event).all()
    bookings = session.query(Booking).all()  # Load from the unified Booking table
    return tours, excursions, events, bookings


def next_available_date(day_name):
    """Get the next available date for a given day."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = dt.datetime.today()
    today_day_name = today.strftime("%A")
    days_ahead = (days.index(day_name) - days.index(today_day_name)) % 7
    return today + dt.timedelta(days=days_ahead)


def convert_to_time(time_str):
    """Convert a time string to a datetime object and extract time part."""
    # Check if time string has a single-digit hour with format H:MM
    if len(time_str) == 4 and time_str[1] == ':':
        time_str = '0' + time_str  # Prepend '0' to make it HH:MM

    return dt.datetime.strptime(time_str, '%H:%M').time()


def check_availability(product, date, time, total_slots):
    """Check availability for the selected date and time by aggregating existing bookings."""

    # Convert date to datetime.date object if it's a string
    if isinstance(date, str):
        try:
            date = dt.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Date string must be in 'YYYY-MM-DD' format.")
    elif not isinstance(date, dt.date):
        raise ValueError("Date must be a datetime.date object or a string in 'YYYY-MM-DD' format.")

    # Convert time to datetime.time object if it's a string
    if isinstance(time, str):
        try:
            time = time.strip()
            # Convert time string with format 'H:MM' or 'HH:MM' to 'HH:MM:SS'
            if len(time.split(':')) == 2:
                time = dt.datetime.strptime(time, '%H:%M').time()
            elif len(time.split(':')) == 3:
                time = dt.datetime.strptime(time, '%H:%M:%S').time()
            else:
                raise ValueError("Time string must be in 'H:MM', 'HH:MM', or 'HH:MM:SS' format.")
        except ValueError:
            raise ValueError("Time string must be in 'H:MM', 'HH:MM', or 'HH:MM:SS' format.")
    elif not isinstance(time, dt.time):
        raise ValueError("Time must be a datetime.time object or a string in 'H:MM', 'HH:MM', or 'HH:MM:SS' format.")

    # Perform the query to find all bookings with the specific product
    bookings_query = session.query(Booking).filter_by(product=product).all()

    # Convert the query result to a DataFrame
    bookings_df = pd.DataFrame([{
        'id': booking.id,
        'product': booking.product,
        'date': booking.date,
        'time': booking.time,
        'total_slots': booking.total_slots,
        'taken_slots': booking.taken_slots,
        'date_booked': booking.date_booked,
        'amount_paid': booking.amount_paid
    } for booking in bookings_query])

    # Filter bookings DataFrame by the specified date and time
    filtered_bookings = bookings_df[
        (bookings_df['date'] == date) &
        (bookings_df['time'] == time)
    ]

    # Calculate total booked slots
    taken_slots = filtered_bookings['taken_slots'].sum()

    # Calculate available slots
    available_slots = total_slots - taken_slots

    # Close the session
    session.close()

    # Return available slots, ensuring it is not negative
    return max(available_slots, 0)


def display_bookings(bookings, booking_type):
    """Display bookings for a given type."""
    st.write(f"**{booking_type} Bookings**")
    if bookings:
        bookings_data = [
            {
                "product": booking.product,
                "date": booking.date,
                "time": booking.time,
                "total_slots": booking.total_slots,
                "taken_slots": booking.taken_slots
            }
            for booking in bookings
        ]
        bookings_df = pd.DataFrame(bookings_data)
        st.write(bookings_df.head(3))
    else:
        st.write(f"No {booking_type.lower()} bookings available.")


def handle_booking(user_name, user_email, activity_selected, date_selected_str, time_selected,
                   num_people, total_price, total_slots):
    try:
        date_selected_obj = dt.datetime.strptime(date_selected_str, '%Y-%m-%d').date()
        time_selected_obj = convert_to_time(time_selected)
        current_date = dt.datetime.now().date()

        # Create a new booking record
        new_booking = Booking(
            product=activity_selected,
            date=date_selected_obj,
            time=time_selected_obj,
            total_slots=total_slots,
            taken_slots=num_people,
            date_booked=current_date,
            amount_paid=total_price
        )

        session.add(new_booking)
        session.commit()
        booking_num = new_booking.id

        ssm = boto3.client('ssm',
                           region_name="us-east-1",
                           aws_access_key_id=st.secrets["aws_key"],
                           aws_secret_access_key=st.secrets["aws_secret"]
                           )
        auth_token = ssm.get_parameter(Name='/prod/courier_token', WithDecryption=True)
        template_id = ssm.get_parameter(Name='/prod/courier_booking_template', WithDecryption=True)

        client = Courier(authorization_token=auth_token['Parameter']['Value'])

        client.send(
            message={
                "to": {
                    "email": user_email,
                },
                "template": template_id['Parameter']['Value'],
                "data": {
                    "booking_num": booking_num,
                    "user_name": user_name,
                    "activity": activity_selected,
                    "date": date_selected_str,
                    "time": time_selected,
                    "num_people": num_people,
                    "total": total_price
                }
            }
        )

    except OperationalError as e:
        session.rollback()
        st.error(f"Database error: {e}")
    except Exception as e:
        session.rollback()
        st.error(f"Failed to handle booking: {e}")
    finally:
        session.close()



@st.dialog("Payment")
def payment(user_name, user_email, activity_selected, date_selected_str, time_selected, num_people, total_price, total_slots):
    st.write("  ")
    st.header("You will now be redirected to JCC to complete your payment")
    st.write("  ")

    if st.button("Agree"):
        handle_booking(user_name, user_email, activity_selected, date_selected_str, time_selected, num_people, total_price, total_slots)
        st.success("Payment Successful! Your will get a confirmation via email shortly!")


def show_booking():
    """Display the booking form."""
    st.header("Book Now")

    user_name = st.text_input("Enter your name")
    user_email = st.text_input("Enter your email")

    # Load data
    tours, excursions, events, bookings = load_data()

    # Combine tours, excursions, and events into one list for simplicity
    combined_list = []
    combined_list.extend([(tour.product, 'Tour') for tour in tours])
    combined_list.extend([(excursion.product, 'Excursion') for excursion in excursions])
    combined_list.extend([(event.product, 'Event') for event in events])

    # Convert list to DataFrame
    combined_df = pd.DataFrame(combined_list, columns=['product', 'type'])

    # Dropdown to select the activity type (Tour, Excursion, or Event)
    activity_type = st.selectbox("Choose an activity type", combined_df['type'].unique())

    # Filter the combined DataFrame based on the selected activity type
    activity_df = combined_df[combined_df['type'] == activity_type]

    # Dropdown to select the activity
    activity_selected = st.selectbox("Choose an activity", activity_df['product'].unique())

    # Get the details for the selected activity
    if activity_type == 'Tour':
        activity_details = next((tour for tour in tours if tour.product == activity_selected), None)
    elif activity_type == 'Excursion':
        activity_details = next((excursion for excursion in excursions if excursion.product == activity_selected), None)
    else:
        activity_details = next((event for event in events if event.product == activity_selected), None)

    if activity_details is None:
        st.error("No activity found for the selected product. Please select a different activity.")
    else:
        if activity_type == 'Event':
            # Event specific handling
            available_dates = activity_details.available_dates.split(',') if activity_details.available_dates else []
            available_times = activity_details.available_times.split(',') if activity_details.available_times else []
            total_slots = float('inf')
            available_dates = [dt.datetime.strptime(date.strip(), "%d/%m/%Y").date() for date in available_dates]
            available_dates_str = [date.strftime("%d/%m/%Y") for date in available_dates]
        else:
            # Tours and excursions specific handling
            available_days = activity_details.available_days.split(',') if activity_details.available_days else []
            available_times = activity_details.available_times.split(',') if activity_details.available_times else []
            total_slots = activity_details.spots_per_time_slot if activity_details.spots_per_time_slot else float('inf')
            available_days = [day.strip() for day in available_days]

        price_per_person = activity_details.price_per_person

        if activity_type == 'Event':
            # Handle event-specific date selection
            date_selected = st.date_input("Select a date", min_value=min(available_dates),
                                          max_value=max(available_dates))
        else:
            # Show the calendar widget with only the available days
            available_dates = [next_available_date(day) for day in available_days]
            date_selected = st.date_input("Select a date", min_value=min(available_dates),
                                          max_value=max(available_dates))

        date_selected_str = date_selected.strftime('%Y-%m-%d')

        if activity_type == 'Event':
            if date_selected.strftime("%d/%m/%Y") not in available_dates_str:
                st.error(
                    f"Please select a valid date. Only {', '.join(available_dates_str)} are available for this activity.")
            else:
                available_times_filtered = [time for time in available_times if
                                            check_availability(activity_selected, date_selected_str,
                                                               time, total_slots) > 0]
                time_selected = st.selectbox("Choose a time", available_times_filtered)

                num_people = st.number_input("Number of people", min_value=1, max_value=50, value=1)
                total_price = num_people * price_per_person
                st.write(f"**Total Price:** €{total_price}")

                if st.button("Confirm Booking"):
                    payment(user_name, user_email, activity_selected, date_selected_str, time_selected,
                            num_people, total_price, total_slots)
        else:
            if date_selected.strftime("%A") not in available_days:
                st.error(
                    f"Please select a valid date. Only {', '.join(available_days)} are available for this activity.")
            else:
                available_times_filtered = [time for time in available_times if
                                            check_availability(activity_selected, date_selected_str,
                                                               time, total_slots) > 0]
                time_selected = st.selectbox("Choose a time", available_times_filtered)

                # Calculate available slots
                available_slots = check_availability(activity_selected, date_selected_str, time_selected,
                                                     total_slots)
                num_people = st.number_input(f"Number of people ( {available_slots} spots available )", min_value=1, max_value=available_slots, value=1)
                total_price = num_people * price_per_person
                st.write(f"**Total Price:** €{total_price}")

                if not user_name or not user_email or not activity_selected or not num_people or not time_selected or not date_selected:
                    st.error("Please fill out all fields.")
                else:
                    if st.button("Confirm Booking"):
                        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_regex, user_email):
                            st.error("Invalid email address. Please enter a valid email.")
                        else:
                            payment(user_name, user_email, activity_selected, date_selected_str,
                                    time_selected,
                                    num_people, total_price, total_slots)


if __name__ == "__main__":
    show_booking()

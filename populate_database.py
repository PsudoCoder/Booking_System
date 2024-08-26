import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Event, Tour, Excursion, Booking

# Create an engine and session
engine = create_engine('sqlite:///island_breeze.db')
Session = sessionmaker(bind=engine)
session = Session()

def clear_tables():
    session.query(Event).delete()
    session.query(Tour).delete()
    session.query(Excursion).delete()
    session.query(Booking).delete()
    session.commit()

# Function to remove BOM and process CSV
def clean_header(header):
    return header.lstrip('\ufeff')

# Function to populate tours with BOM handling
def populate_tours(csv_file):
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        headers = [clean_header(header) for header in csv_reader.fieldnames]  # Clean BOM from headers
        for row in csv_reader:
            print("CSV Row:", row)  # Debugging: Print each row
            if not row:  # Skip empty rows
                continue
            try:
                tour = Tour(
                    product=row[headers[0]].strip(),  # Access using cleaned header
                    description=row[headers[1]].strip(),
                    price_per_person=float(row[headers[2]]),
                    available_times=row[headers[3]].strip(),
                    available_days=row[headers[4]].strip(),
                    spots_per_time_slot=int(row[headers[5]]),
                    included_food=row[headers[6]].strip(),
                    available_dates=row[headers[7]].strip()
                )
                session.add(tour)
            except KeyError as e:
                print(f"KeyError: {e} in row {row}")  # Debugging: Print error and problematic row
            except Exception as e:
                print(f"Error: {e} in row {row}")  # Debugging: Catch other exceptions
    session.commit()

def populate_events(csv_file):
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        headers = [clean_header(header) for header in csv_reader.fieldnames]  # Clean BOM from headers
        for row in csv_reader:
            if not row:  # Skip empty rows
                continue
            event = Event(
                product=row[headers[0]].strip(),
                description=row[headers[1]].strip(),
                price_per_person=float(row[headers[2]]),
                available_times=row[headers[3]].strip(),
                available_days=row[headers[4]].strip(),
                spots_per_time_slot=int(row[headers[5]]),
                included_food=row[headers[6]].strip(),
                available_dates=row[headers[7]].strip()
            )
            session.add(event)
    session.commit()

def populate_excursions(csv_file):
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        headers = [clean_header(header) for header in csv_reader.fieldnames]  # Clean BOM from headers
        for row in csv_reader:
            if not row:  # Skip empty rows
                continue
            excursion = Excursion(
                product=row[headers[0]].strip(),
                description=row[headers[1]].strip(),
                price_per_person=float(row[headers[2]]),
                available_times=row[headers[3]].strip(),
                available_days=row[headers[4]].strip(),
                spots_per_time_slot=int(row[headers[5]]),
                included_food=row[headers[6]].strip(),
                available_dates=row[headers[7]].strip()
            )
            session.add(excursion)
    session.commit()


def convert_to_time(time_str):
    """Convert a time string in HH:MM format to a time object."""
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return None

def populate_bookings(csv_file):
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            headers = [clean_header(header) for header in csv_reader.fieldnames]
            for row in csv_reader:
                if not row:
                    continue

                # Convert date strings to date objects
                date_str = row[headers[1]].strip()
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

                date_booked_str = row[headers[5]].strip()
                date_booked_obj = datetime.strptime(date_booked_str, '%Y-%m-%d').date() if date_booked_str else None

                # Convert time strings to time objects
                time_str = row[headers[2]].strip()
                time_obj = convert_to_time(time_str) if time_str else None

                booking = Booking(
                    product=row[headers[0]].strip(),
                    date=date_obj,
                    time=time_obj,
                    total_slots=int(row[headers[3]]),
                    taken_slots=int(row[headers[4]]),
                    date_booked=date_booked_obj,
                    amount_paid=int(row[headers[6]]),
                )
                session.add(booking)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback in case of error


clear_tables()
populate_tours('data/tours.csv')
populate_events('data/events.csv')
populate_excursions('data/excursions.csv')
populate_bookings('data/bookings.csv')

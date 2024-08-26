import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to the SQLite database
db_path = 'island_breeze.db'

# Remove the existing database file if it exists
# if os.path.exists(db_path):
#     os.remove(db_path)

# Create an engine to the SQLite database
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Base class for declarative class definitions
Base = declarative_base()

# Define the Tours model
class Tour(Base):
    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True)
    product = Column(String, unique=True)
    description = Column(String)
    price_per_person = Column(Float)
    available_times = Column(String)
    available_days = Column(String)
    spots_per_time_slot = Column(Integer)
    included_food = Column(String)
    available_dates = Column(String)

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    product = Column(String, unique=True)
    description = Column(String)
    price_per_person = Column(Float)
    available_times = Column(String)
    available_days = Column(String)
    spots_per_time_slot = Column(Integer)
    included_food = Column(String)
    available_dates = Column(String)

class Excursion(Base):
    __tablename__ = 'excursions'

    id = Column(Integer, primary_key=True)
    product = Column(String, unique=True)
    description = Column(String)
    price_per_person = Column(Float)
    available_times = Column(String)
    available_days = Column(String)
    spots_per_time_slot = Column(Integer)
    included_food = Column(String)
    available_dates = Column(String)

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    product = Column(String)
    date = Column(Date)
    time = Column(Time)
    total_slots = Column(Integer)
    taken_slots = Column(Integer)
    date_booked = Column(Date)
    amount_paid = Column(Float)

# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

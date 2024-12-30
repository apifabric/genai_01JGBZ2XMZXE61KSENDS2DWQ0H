# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Airport(Base):
    """description: This table contains information about airports including IATA and ICAO codes, geographic data, and time zones."""
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    iata = Column(String(3), nullable=True)
    icao = Column(String(4), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Integer, nullable=True)
    timezone = Column(String, nullable=True)
    dst = Column(String, nullable=True)
    tz_database_timezone = Column(String, nullable=True)

class Flight(Base):
    """description: This table registers flight information including airlines, origin, destination, and schedule."""
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String, nullable=True)
    airline_id = Column(Integer, ForeignKey('airline.id'))
    origin_airport_id = Column(Integer, ForeignKey('airport.id'))
    destination_airport_id = Column(Integer, ForeignKey('airport.id'))
    departure_time = Column(DateTime, nullable=True)
    arrival_time = Column(DateTime, nullable=True)

class Airline(Base):
    """description: This table stores different airlines with their respective IATA and ICAO codes, and country."""
    __tablename__ = 'airline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    iata = Column(String(2), nullable=True)
    icao = Column(String(3), nullable=True)
    country = Column(String, nullable=True)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    airport1 = Airport(name="Los Angeles International", city="Los Angeles", country="USA", iata="LAX", icao="KLAX", latitude=33.942791, longitude=-118.410042, altitude=125, timezone="-8:00", dst="U", tz_database_timezone="America/Los_Angeles")
    airport2 = Airport(name="Heathrow", city="London", country="UK", iata="LHR", icao="EGLL", latitude=51.4706, longitude=-0.461941, altitude=83, timezone="0:00", dst="E", tz_database_timezone="Europe/London")
    airport3 = Airport(name="Tokyo International", city="Tokyo", country="Japan", iata="HND", icao="RJTT", latitude=35.549393, longitude=139.779839, altitude=13, timezone="9:00", dst="N", tz_database_timezone="Asia/Tokyo")
    airport4 = Airport(name="Charles de Gaulle", city="Paris", country="France", iata="CDG", icao="LFPG", latitude=49.0097, longitude=2.5479, altitude=392, timezone="1:00", dst="E", tz_database_timezone="Europe/Paris")
    airline1 = Airline(name="American Airlines", iata="AA", icao="AAL", country="USA")
    airline2 = Airline(name="British Airways", iata="BA", icao="BAW", country="UK")
    airline3 = Airline(name="Japan Airlines", iata="JL", icao="JAL", country="Japan")
    airline4 = Airline(name="Air France", iata="AF", icao="AFR", country="France")
    flight1 = Flight(flight_number="AA100", airline_id=1, origin_airport_id=1, destination_airport_id=2, departure_time=datetime(2023, 10, 5, 12, 0), arrival_time=datetime(2023, 10, 5, 22, 0))
    flight2 = Flight(flight_number="BA200", airline_id=2, origin_airport_id=2, destination_airport_id=3, departure_time=datetime(2023, 10, 6, 14, 0), arrival_time=datetime(2023, 10, 6, 20, 0))
    flight3 = Flight(flight_number="JL300", airline_id=3, origin_airport_id=3, destination_airport_id=4, departure_time=datetime(2023, 10, 7, 10, 0), arrival_time=datetime(2023, 10, 7, 18, 0))
    flight4 = Flight(flight_number="AF400", airline_id=4, origin_airport_id=4, destination_airport_id=1, departure_time=datetime(2023, 10, 8, 16, 0), arrival_time=datetime(2023, 10, 8, 8, 0))
    
    
    
    session.add_all([airport1, airport2, airport3, airport4, airline1, airline2, airline3, airline4, flight1, flight2, flight3, flight4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')

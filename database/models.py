# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 30, 2024 14:22:25
# Database: sqlite:////tmp/tmp.I8zvu247kh-01JGBZ2XMZXE61KSENDS2DWQ0H/AirportDatabase/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Airline(Base):  # type: ignore
    """
    description: This table stores different airlines with their respective IATA and ICAO codes, and country.
    """
    __tablename__ = 'airline'
    _s_collection_name = 'Airline'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    iata = Column(String(2))
    icao = Column(String(3))
    country = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    FlightList : Mapped[List["Flight"]] = relationship(back_populates="airline")



class Airport(Base):  # type: ignore
    """
    description: This table contains information about airports including IATA and ICAO codes, geographic data, and time zones.
    """
    __tablename__ = 'airport'
    _s_collection_name = 'Airport'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    iata = Column(String(3))
    icao = Column(String(4))
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Integer)
    timezone = Column(String)
    dst = Column(String)
    tz_database_timezone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    FlightList : Mapped[List["Flight"]] = relationship(foreign_keys='[Flight.destination_airport_id]', back_populates="destination_airport")
    originFlightList : Mapped[List["Flight"]] = relationship(foreign_keys='[Flight.origin_airport_id]', back_populates="origin_airport")



class Flight(Base):  # type: ignore
    """
    description: This table registers flight information including airlines, origin, destination, and schedule.
    """
    __tablename__ = 'flight'
    _s_collection_name = 'Flight'  # type: ignore

    id = Column(Integer, primary_key=True)
    flight_number = Column(String)
    airline_id = Column(ForeignKey('airline.id'))
    origin_airport_id = Column(ForeignKey('airport.id'))
    destination_airport_id = Column(ForeignKey('airport.id'))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)

    # parent relationships (access parent)
    airline : Mapped["Airline"] = relationship(back_populates=("FlightList"))
    destination_airport : Mapped["Airport"] = relationship(foreign_keys='[Flight.destination_airport_id]', back_populates=("FlightList"))
    origin_airport : Mapped["Airport"] = relationship(foreign_keys='[Flight.origin_airport_id]', back_populates=("originFlightList"))

    # child relationships (access children)

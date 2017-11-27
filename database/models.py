import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Sensor(Base):
    __tablename__ = 'sensors'
    # Here we define columns for the table captors.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(250))
    mac = Column(String(250), nullable=False)
    type = Column(String(250))
    model = Column(String(250))
    state = Column(Integer, nullable=False)
    # init method which will be useful later
    def __init__(self, name, mac, type, model, state):
        self.name = name
        self.mac = mac
        self.type = type
        self.model = model
        self.state = state
    
 
class Position(Base):
    __tablename__ = 'positions'
    # Here we define columns for the table positions.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    room = Column(String(250), nullable=False)
    bus = Column(String(250), nullable=False)
    index = Column(String(250), nullable=False)
    # init method which will be useful later
    def __init__(self, room, bus, index):
        self.room = room
        self.bus = bus
        self.index = index
    

class Assignment(Base):
    __tablename__ = 'assignments'
    # Here we define columns for the table affectations.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_position = Column(String(250), ForeignKey('positions.id', ondelete="CASCADE"), nullable=False, unique=True)
    id_sensor = Column(String(250), ForeignKey('sensors.id', ondelete="CASCADE"), nullable=False, unique=True)
    # init method which will be useful later
    def __init__(self, id_sensor, id_position):
        self.id_sensor = id_sensor
        self.id_position = id_position
        
 
class History(Base):
    __tablename__ = 'history'
    # Here we define columns for the table history.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_position = Column(String(250), ForeignKey('positions.id', ondelete="SET NULL"), nullable=False)
    id_sensor = Column(String(250), ForeignKey('sensors.id', ondelete="SET NULL"), nullable=False)
    start_of_service = Column(TIMESTAMP, nullable=False)
    end_of_service = Column(TIMESTAMP, nullable=True)
    # init method which will be useful later
    def __init__(self, id_sensor, id_position, start_of_service, end_of_service):
        self.id_sensor = id_sensor
        self.id_position = id_position
        self.start_of_service = start_of_service
        self.end_of_service = end_of_service
    
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///database.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

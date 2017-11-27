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
    
 
class Position(Base):
    __tablename__ = 'positions'
    # Here we define columns for the table positions.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    room = Column(String(250), nullable=False)
    bus = Column(String(250), nullable=False)
    index = Column(String(250), nullable=False)
    

class Assignment(Base):
    __tablename__ = 'assignments'
    # Here we define columns for the table affectations.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_position = Column(String(250), ForeignKey('positions.id', ondelete="CASCADE"), nullable=False, unique=True)
    id_captor = Column(String(250), ForeignKey('sensors.id', ondelete="CASCADE"), nullable=False, unique=True)
 
 
class History(Base):
    __tablename__ = 'history'
    # Here we define columns for the table history.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_position = Column(String(250), ForeignKey('positions.id', ondelete="SET NULL"), nullable=False)
    id_captor = Column(String(250), ForeignKey('sensors.id', ondelete="SET NULL"), nullable=False)
    start_of_service = Column(TIMESTAMP, nullable=False)
    end_of_service = Column(TIMESTAMP, nullable=True)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
#engine = create_engine('sqlite:///database.db')
engine = create_engine('sqlite:///db.sqlite')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

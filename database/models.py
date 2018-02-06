from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import db


class Sensor(db.Model):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(250))
    mac = Column(String(250), nullable=False)
    type = Column(String(250))
    model = Column(String(250))
    state = Column(Integer, nullable=False)

    def __init__(self, name, mac, type, model, state):
        self.name = name
        self.mac = mac
        self.type = type
        self.model = model
        self.state = state

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class Position(db.Model):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    room = Column(String(250), nullable=False)
    bus = Column(Integer, nullable=False)
    index = Column(Integer, nullable=False)

    def __init__(self, room, bus, index):
        self.room = room
        self.bus = bus
        self.index = index

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class Assignment(db.Model):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_position = Column(Integer, ForeignKey('positions.id', ondelete="CASCADE"), nullable=False, unique=True)
    id_sensor = Column(Integer, ForeignKey('sensors.id', ondelete="CASCADE"), nullable=False, unique=True)

    def __init__(self, id_sensor, id_position):
        self.id_sensor = id_sensor
        self.id_position = id_position

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class History(db.Model):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id_position = Column(Integer, ForeignKey('positions.id', ondelete="SET NULL"), nullable=False)
    id_sensor = Column(Integer, ForeignKey('sensors.id', ondelete="SET NULL"), nullable=False)
    start_of_service = Column(TIMESTAMP, nullable=False)
    end_of_service = Column(TIMESTAMP, nullable=True)

    def __init__(self, id_sensor, id_position):
        self.id_sensor = id_sensor
        self.id_position = id_position
        self.start_of_service = func.now()

    def close_history(self):
        self.end_of_service = func.now()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class Event(db.Model):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(250), nullable=False)
    importance = Column(Integer, nullable=False)
    start = Column(TIMESTAMP, nullable=False)
    end = Column(TIMESTAMP, nullable=True)
    sensor = Column(Integer, nullable=False)
    ended = Column(Integer, nullable=False, default = False)

    def __init__(self, title, importance, sensor, ended = False):
        self.title = title
        self.importance = importance
        self.start = func.now()
        self.sensor = sensor
        if ended != None:
            self.ended = ended

    def close_history(self):
        self.end = func.now()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

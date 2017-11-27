from seduce_api.api.database import db
from seduce_api.api.database.models import Sensor, Position, Assignement, History
from sqlalchemy import update, insert, delete

def get_capteur(id):
	return None

def get_capteur_by_name(name):
	return None

def get_position_sensor(id):
	return None

def get_history_sensor(id):
	return None

def create_sensor(data):
	return None

def remove_position(room, bus, index):
	idn = data.get('id')
	room = data.get('room')
	bus = data.get('bus')
	undex = data.get('index') 
	pos = Position(idn, room, bus, index)
	db.session.delete(pos)
	db.session.commit()

def add_position(data):
	idn = data.get('id')
	room = data.get('room')
	bus = data.get('bus')
	undex = data.get('index')
	pos = Position(idn, room, bus, index)
	db.session.add(pos)
	db.session.commit()

def update_sensor(id, data):
	return None

def filter_position(room, bus, index):
	return Position.query.filter(Sensor.room == room and Sensor.bus == bus and Sensor.index == index).one()




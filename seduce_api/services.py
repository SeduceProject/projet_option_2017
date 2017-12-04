from database import db
from database.models import Sensor, Position, Assignment, History

def get_sensor(id):
	return Sensor.query.get(id)

def get_sensor_by_name(name):
	print Sensor.query.filter_by(name = name).one()
	return Sensor.query.filter_by(name = name).one()

def get_sensor_position(id):
	return Position.query.get(id)

def get_sensor_history(id):
	return History.query.get(id)

def create_sensor(data):
	name = data.get('name')
	mac = data.get('mac')
	type = data.get('type')
	model = data.get('model')
	state = data.get('state')
	sensor = Sensor(name, mac, type, model, state)
	db.session.add(sensor)
	db.session.commit()
	return sensor

def delete_sensor(id):
	sensor = get_sensor(id)
	db.session.delete(sensor)
	db.session.commit()

def update_sensor(id, data):
	sensor = get_sensor(id)
	sensor.name = data.get('name')
	sensor.mac = data.get('mac')
	sensor.type = data.get('type')
	sensor.model = data.get('model')
	sensor.state = data.get('state')
	db.session.add(sensor)
	db.session.commit()

def remove_position(room, bus, index):
	idn = data.get('id')
	room = data.get('room')
	bus = data.get('bus')
	index = data.get('index') 
	pos = Position(idn, room, bus, index)
	db.session.delete(pos)
	db.session.commit()

def add_position(data):
	idn = data.get('id')
	room = data.get('room')
	bus = data.get('bus')
	index = data.get('index')
	pos = Position(idn, room, bus, index)
	db.session.add(pos)
	db.session.commit()

def filter_position(room, bus, index):
	return Position.query.filter(Sensor.room == room and Sensor.bus == bus and Sensor.index == index).one()

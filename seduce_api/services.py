from database import db
from database.models import Sensor, Position, Assignment, History, Event

# Sensors

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

def get_sensor(id):
	return Sensor.query.get(id)

def get_sensor_by_name(name):
	return Sensor.query.filter_by(name = name).one()

def get_sensor_position(id):
	return Position.query.get(id)

def get_sensor_history(id):
	return History.query.get(id)

def update_sensor(id, data):
	sensor = get_sensor(id)
	sensor.name = data.get('name')
	sensor.mac = data.get('mac')
	sensor.type = data.get('type')
	sensor.model = data.get('model')
	sensor.state = data.get('state')
	db.session.add(sensor)
	db.session.commit()
	return sensor

def delete_sensor(id):
	sensor = get_sensor(id)
	db.session.delete(sensor)
	db.session.commit()

# Positions

def add_bus(room, data):
	bus_index = data.get('index')
	size = data.get('size')
	for i in xrange(size):
		db.session.add(Position(room, bus_index, i))
	db.session.commit()
	return submit_bus

def remove_bus(room, bus):
	positions = Position.query.filter(Position.room == room and Position.bus == bus)
	for p in positions:
		db.session.delete(p)
	db.session.commit()

def filter_position(room, bus, index):
	return Position.query.filter(Sensor.room == room and Sensor.bus == bus and Sensor.index == index).one()

#Event

def create_event(data):
	title = data.get('title')
	importance = data.get('importance')
	sensor = data.get('sensor')
	ended = data.get('ended')
	event = Event(title, importance, sensor, ended)
	db.session.add(event)
	db.session.commit()
	return event

def get_event(id):
	return Event.query.get(id)

def get_event_by_importance(name):
	return Event.query.filter_by(importance = name).one()

def get_event_by_sensor_id(sensor):
	return Event.query.filter_by(sensor = sensor).one()

def end_event(id):
	event = get_event(id)
	event.close_history()
	event.ended = True
	db.session.add(event)
	db.session.commit()
	return event

# Assignments

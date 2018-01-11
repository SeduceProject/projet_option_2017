from database import db
from database.models import Sensor, Position, Assignment, History

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

def remove_bus(room, bus):
	positions = Position.query.filter(Position.room == room and Position.bus == bus)
	for p in positions:
		db.session.delete(p)
	db.session.commit()

def filter_position(room, bus, index):
	return Position.query.filter(Sensor.room == room and Sensor.bus == bus and Sensor.index == index).one()

# Assignments

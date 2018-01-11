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
	return Sensor.query.filter(Sensor.name == name).one()

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
	if Position.query.filter(Position.room == room).filter(Position.bus == bus_index).count() > 0:
		raise Exception('A bus with this id already exists in this room.')
	size = data.get('size')
	if size < 1:
		raise Exception('A bus must have at least one position.')
	for i in xrange(size):
		db.session.add(Position(room, bus_index, i))
	db.session.commit()

def remove_bus(room, bus):
	positions = Position.query.filter(Position.room == room).filter(Position.bus == bus)
	for p in positions:
		db.session.delete(p)
	db.session.commit()

def remove_room(room):
	positions = Position.query.filter(Position.room == room)
	for p in positions:
		db.session.delete(p)
	db.session.commit()

def get_position_by_values(room, bus, index):
	return Position.query.filter(Position.room == room).filter(Position.bus == bus).filter(Position.index == index).one()

# Assignments

def add_assignment(room, bus, index, data):
	position_id = get_position_by_values(room, bus, index).id
	if get_assignments(room, bus, index).count() > 0:
		raise Exception('There is already a sensor at this position.')

	sensor_id = data.get('sensor')
	sensor = get_sensor(sensor_id)
	optional_previous_assignment = Assignment.query.filter(Assignment.id_sensor == sensor_id)
	if optional_previous_assignment.count() > 0:
		db.session.delete(optional_previous_assignment.one())
		db.session.commit()

	db.session.add(Assignment(sensor_id, position_id))
	db.session.commit()
	return sensor

def get_assignments(room, bus, index):
	return Assignment.query.filter(Assignment.id_position == get_position_by_values(room, bus, index).id)

def get_assigned_sensor(room, bus, index):
	assignments = get_assignments(room, bus, index)
	if assignments.count() > 0:
		return get_sensor(assignments.one().id_sensor)
	else:
		# TODO handle this properly
		return Sensor("EMPTY", "", "", "", -1)

def remove_assignment(room, bus, index):
	assignment = get_assignments(room, bus, index).one()
	db.session.delete(assignment)
	db.session.commit()

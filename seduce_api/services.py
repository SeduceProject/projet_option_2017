from database import db
from database.models import Sensor, Position, Assignment, History


# Sensors

def create_sensor(data):
	if Sensor.query.filter(Sensor.mac == data.get('mac')).count() > 0:
		raise Exception('A sensor with this mac already exists.')
	if Sensor.query.filter(Sensor.name == data.get('name')).count() > 0:
		raise Exception('A sensor with this name already exists.')

	sensor = Sensor(data.get('name'), data.get('mac'), data.get('type'), data.get('model'), data.get('state'))
	db.session.add(sensor)
	db.session.commit()
	return sensor

def get_sensor(id):
	return Sensor.query.filter(Sensor.id == id).one()

def get_sensor_by_name(name):
	return Sensor.query.filter(Sensor.name == name).one()

def get_sensor_position(id, data):
	optional_assignment = get_assignments(data.get('room'), data.get('bus'), data.get('index'))
	if optional_assignment.count() == 0:
		raise Exception('This sensor is not assigned currently.')
	return Position.query.filter(Position.id == optional_assignment.one().id_position)

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
	db.session.delete(get_sensor(id))
	db.session.commit()


# Positions

def add_bus(room, data):
	bus_index = data.get('index')
	if Position.query.filter(and_(Position.room == room, Position.bus == bus_index)).count() > 0:
		raise Exception('A bus with this id already exists in this room.')

	size = data.get('size')
	if size < 1:
		raise Exception('A bus must have at least one position.')

	for i in xrange(size):
		db.session.add(Position(room, bus_index, i))
	db.session.commit()

def remove_bus(room, bus):
	positions = Position.query.filter(and_(Position.room == room, Position.bus == bus))
	for p in positions:
		db.session.delete(p)
	db.session.commit()

def remove_room(room):
	positions = Position.query.filter(Position.room == room)
	for p in positions:
		db.session.delete(p)
	db.session.commit()

def get_position_by_values(room, bus, index):
	return Position.query.filter(and_(Position.room == room, Position.bus == bus, Position.index == index)).one()


# Assignments

def add_assignment(room, bus, index, data):
	position_id = get_position_by_values(room, bus, index).id
	if get_assignments(room, bus, index).count() > 0:
		raise Exception('There is already a sensor at this position.')

	sensor_id = data.get('sensor')
	sensor = get_sensor(sensor_id)
	optional_previous_assignment = Assignment.query.filter(Assignment.id_sensor == sensor_id)
	if optional_previous_assignment.count() > 0:
		delete_assignment(optional_previous_assignment.one())

	db.session.add(Assignment(sensor_id, position_id))
	db.session.add(History(sensor_id, position_id))
	db.session.commit()
	return sensor

def get_assignments(room, bus, index):
	return Assignment.query.filter(Assignment.id_position == get_position_by_values(room, bus, index).id)

def get_assigned_sensor(room, bus, index):
	assignments = get_assignments(room, bus, index)
	if assignments.count() > 0:
		return get_sensor(assignments.one().id_sensor)
	else:
		raise Exception('There is no sensor at this position.')

def remove_assignment(room, bus, index):
	delete_assignment(get_assignments(room, bus, index).one())

def delete_assignment(assignment):
	close_sensor_history_element(assignment.id_sensor)
	db.session.delete(assignment)
	db.session.commit()


# History

def close_sensor_history_element(sensor_id):
	history = History.query.filter(and_(History.end_of_service.is_(None), History.id_sensor == sensor_id)).one()
	history.close_history()
	db.session.add(history)
	db.commit()

def get_sensor_history(sensor_id):
	return History.query.filter(History.id_sensor == sensor_id)
	# TODO what if there is no history ? Is that possible ?

def get_position_history(room, bus, index):
	return History.query.filter(History.id_position == get_position_by_values(room, bus, index).id)
	# TODO what if there is no history ? Is that possible ?

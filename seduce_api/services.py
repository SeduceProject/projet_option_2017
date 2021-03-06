from database import db
from database.models import Sensor, Position, Assignment, History, Event
from seduce_api.serializers import position as ser_position
from seduce_api.serializers import sensor as ser_sensor
from seduce_api.restplus import api, SensorNotFoundException, SensorNotValidException, PositionNotFoundException, PositionNotValidException, AssignmentNotFoundException, AssignmentNotValidException, EventNotFoundException
from sqlalchemy.sql import and_


# Sensors

def create_sensor(data):
	if len(data.get('mac')) == 0:
		raise SensorNotValidException('A mac cannot be empty.')
	if Sensor.query.filter(Sensor.mac == data.get('mac')).count() > 0:
		raise SensorNotValidException('A sensor with mac ' + data.get('mac') + ' already exists.')
	if Sensor.query.filter(Sensor.name == data.get('name')).count() > 0:
		raise SensorNotValidException('A sensor with name ' + data.get('name') + ' already exists.')

	sensor = Sensor(data.get('name'), data.get('mac'), data.get('type'), data.get('model'), data.get('state'))
	db.session.add(sensor)
	db.session.commit()
	return sensor

def get_sensor(id):
	query = Sensor.query.filter(Sensor.id == id)
	if query.count() == 1:
		return query.one()
	else:
		raise SensorNotFoundException('There is no sensor with id ' + str(id) + '.')

def get_sensor_by_name(name):
	query = Sensor.query.filter(Sensor.name == name)
	if query.count() == 1:
		return query.one()
	else:
		raise SensorNotFoundException('There is no sensor with name ' + name + '.')

def get_sensor_position(id):
	assignments = Assignment.query.filter(Assignment.id_sensor == id)
	if assignments.count() > 0:
		return Position.query.filter(Position.id == assignments.one().id_position).one()
	else:
		raise AssignmentNotFoundException('The sensor ' + str(id) + ' is not assigned currently.')

def update_sensor(id, data):
	sensor = get_sensor(id)

	if len(data.get('mac')) == 0:
		raise SensorNotValidException('A mac cannot be empty.')
	mac_query = Sensor.query.filter(Sensor.mac == data.get('mac'))
	if mac_query.count() == 1 and mac_query.one().id != id:
		raise SensorNotValidException('A sensor with mac ' + data.get('mac') + ' already exists.')

	name_query = Sensor.query.filter(Sensor.name == data.get('name'))
	if name_query.count() == 1 and name_query.one().id != id:
		raise SensorNotValidException('A sensor with name ' + data.get('name') + ' already exists.')

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

def get_sensors():
	return Sensor.query.all()


# Positions

def add_bus(room, data):
	bus_index = data.get('index')
	if bus_index < 0:
		raise PositionNotValidException(str(bus_index) + ' is not a valid bus id.')
	if Position.query.filter(and_(Position.room == room, Position.bus == bus_index)).count() > 0:
		raise PositionNotValidException('A bus with id ' + str(bus_index) + ' already exists in room ' + room + '.')

	size = data.get('size')
	if size < 1:
		raise PositionNotValidException(str(size) + ' is not a valid bus size.')

	result = []
	for i in xrange(size):
		p = Position(room, bus_index, i)
		db.session.add(p)
		result.append(p)
	db.session.commit()
	return result

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

	# Auxiliary method
def get_position_by_values(room, bus, index):
	query = Position.query.filter(and_(Position.room == room, Position.bus == bus, Position.index == index))
	if query.count() > 0:
		return query.one()
	else:
		raise PositionNotFoundException('Position [' + room + ', ' + str(bus) + ', ' + str(index) + '] does not exist.')


# Events

def create_event(data):
	title = data.get('title')
	importance = data.get('importance')
	sensor = data.get('sensor')
	try:
		get_sensor(sensor)
	except:
		raise SensorNotFoundException('No event can be associated with a sensor with id ' + str(id) + ' because it does not exist.')
	ended = data.get('ended')
	if Sensor.query.filter(Sensor.id == sensor).count() == 1:
		event = Event(title, importance, sensor, ended)
		db.session.add(event)
		db.session.commit()
		return event
	else:
		raise SensorNotFoundException('There is no sensor with id ' + str(id) + '.')

def get_event(id):
	query = Event.query.filter(Event.id == id)
	if query.count() > 0:
		return query.one()
	else:
		raise EventNotFoundException('There is no event with id ' + str(id) + '.')

def get_event_by_importance(importance):
	query = Event.query.filter(Event.importance == importance)
	if query.count() > 0:
		return query.all()
	else:
		raise EventNotFoundException('There is no event with importance ' + str(importance) + '.')

def get_event_by_sensor_id(sensor):
	query = Event.query.filter(Event.sensor == sensor)
	if query.count() > 0:
		return query.all()
	else:
		raise EventNotFoundException('There is no event for sensor ' + str(sensor) + '.')

def end_event(id):
	event = get_event(id)
	event.close_history()
	db.session.add(event)
	db.session.commit()
	return event

def get_events():
	return Event.query.all()

def get_events_after_id(id):
	return Event.query.filter(Event.id >= id).all()


# Assignments

def add_assignment(room, bus, index, data):
	position_id = get_position_by_values(room, bus, index).id
	if get_assignments_aux(room, bus, index).count() > 0:
		raise AssignmentNotValidException('There is already a sensor at position [' + room + ', ' + str(bus) + ', ' + str(index) + '].')

	sensor_id = data.get('sensor')
	sensor = get_sensor(sensor_id)
	optional_previous_assignment = Assignment.query.filter(Assignment.id_sensor == sensor_id)
	if optional_previous_assignment.count() > 0:
		delete_assignment(optional_previous_assignment.one())

	db.session.add(Assignment(sensor_id, position_id))
	db.session.add(History(sensor_id, position_id))
	db.session.commit()
	return sensor

	# Auxiliary method
def get_assignments_aux(room, bus, index):
	return Assignment.query.filter(Assignment.id_position == get_position_by_values(room, bus, index).id)

def get_assigned_sensor(room, bus, index):
	assignments = get_assignments_aux(room, bus, index)
	if assignments.count() > 0:
		return get_sensor(assignments.one().id_sensor)
	else:
		raise AssignmentNotFoundException('There is no sensor at position [' + room + ', ' + str(bus) + ', ' + str(index) + '].')

def remove_assignment(room, bus, index):
	assignments = get_assignments_aux(room, bus, index)
	if assignments.count() > 0:
		delete_assignment(assignments.one())
	# No need for an error if there wasn't a sensor assigned to this position

	# Auxiliary method
def delete_assignment(assignment):
	close_sensor_history_element(assignment.id_sensor)
	db.session.delete(assignment)
	db.session.commit()


# History

	# Auxiliary method
def close_sensor_history_element(sensor_id):
	history = History.query.filter(and_(History.end_of_service.is_(None), History.id_sensor == sensor_id)).one()
	history.close_history()
	db.session.add(history)

def get_sensor_history(sensor_id):
	return marshalling_aux_sensor(History.query.filter(History.id_sensor == sensor_id))

def get_position_history(room, bus, index):
	return marshalling_aux_position(History.query.filter(History.id_position == get_position_by_values(room, bus, index).id))

	# Auxiliary method
def marshalling_aux_sensor(full_history):
	result = []
	for history in full_history:
		position = Position.query.filter(Position.id == history.id_position).one()
		result.append({"start_of_service": history.start_of_service, "end_of_service": history.end_of_service, "position": api.marshal(position, ser_position)})
	return {"positions": result}

	# Auxiliary method
def marshalling_aux_position(full_history):
	result = []
	for history in full_history:
		sensor = Sensor.query.filter(Sensor.id == history.id_sensor).one()
		result.append({"start_of_service": history.start_of_service, "end_of_service": history.end_of_service, "sensor": api.marshal(sensor, ser_sensor)})
	return {"sensors": result}

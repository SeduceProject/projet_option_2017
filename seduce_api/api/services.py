from seduce_api.database import db
from seduce_api.database.models import Sensor, Position, Assignment, History

def get_sensor(id):
	return Sensor.query.filter(Sensor.id == id).one()

def get_sensor_by_name(name):
	return Sensor.query.filter(Sensor.name == name).one()

def get_position_sensor(id):
	return Position.query.join(Assignment.id_position).filter(Assignment.id_sensor == id).one()

def get_history_sensor(id):
	return History.query.filter(History.id_sensor == id).one()

def create_sensor(data):
	name = data.get('name')
	mac = data.get('mac')
	type = data.get('type')
	model = data.get('model')
	state = data.get('state')
	sensor = Sensor(name, mac, type, model, state)
    db.session.add(sensor)
    db.session.commit()

def update_sensor(id, data):
	sensor = Sensor.query.filter(Sensor.id == id).one()
	sensor.name = data.get('name')
	sensor.mac = data.get('mac')
	sensor.type = data.get('type')
	sensor.model = data.get('model')
	sensor.state = data.get('state')
	db.session.add(sensor)
    db.session.commit()

def remove_position(room, bus, index):
	return None

def add_position(data):
	return None

def filter_position(room, bus, index):
	return None



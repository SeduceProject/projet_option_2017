from flask_restplus import fields
from seduce_api.restplus import api

sensor = api.model("Sensors information", {
	'name': fields.String(required=False, description='Sensor name'),
	'mac': fields.String(required=True, description='Sensor mac'),
	'type': fields.String(required=False, description='Sensor type'),
	'model': fields.String(required=False, description='Sensor model'),
	'state': fields.Integer(required=True, description='Sensor state')
})

position = api.model("Full description of a position", {
	'room': fields.String(required=True, description='Room number'),
	'bus': fields.Integer(required=True, description='Bus number'),
	'index': fields.Integer(required=True, description='Bus index')
})

history_element = api.model("Dated position of a sensor", {
	'start_of_service': fields.DateTime(required=True, description="Start date of a given position by a sensor"),
	'end_of_service': fields.DateTime(required=False, description="End date of a given position by a sensor"),
	'position': fields.Nested(position)
})

history = api.inherit("History of a sensor positions", {
    'positions': fields.List(fields.Nested(history_element))
})

submit_sensor = api.model('Information for a sensor creation', {
	'name': fields.String(required=False, description='Sensor name'),
	'mac': fields.String(required=True, description='Sensor mac'),
	'type': fields.String(required=False, description='Sensor type'),
	'model': fields.String(required=False, description='Sensor model'),
	'state': fields.Integer(required=True, description='Sensor state')
})

submit_position = api.model('Information for a position creation', {
	'room': fields.String(required=True, description='Room number'),
	'bus': fields.Integer(required=True, description='Bus number'),
	'index': fields.Integer(required=True, description='Bus index')
})

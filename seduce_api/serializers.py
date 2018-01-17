from flask_restplus import fields
from seduce_api.restplus import api


# Sensors

sensor = api.model("Sensors information", {
	'id': fields.Integer(required=True, description='Sensor id'),
	'name': fields.String(required=False, description='Sensor name'),
	'mac': fields.String(required=True, description='Sensor mac'),
	'type': fields.String(required=False, description='Sensor type'),
	'model': fields.String(required=False, description='Sensor model'),
	'state': fields.Integer(required=True, description='Sensor state')
})

submit_sensor = api.model('Information for a sensor creation', {
	'name': fields.String(required=False, description='Sensor name'),
	'mac': fields.String(required=True, description='Sensor mac'),
	'type': fields.String(required=False, description='Sensor type'),
	'model': fields.String(required=False, description='Sensor model'),
	'state': fields.Integer(required=True, description='Sensor state')
})


# Positions

submit_sensor_position = api.model('Information to move a sensor to a position', {
	'sensor': fields.Integer(required=True, description='Sensor id')
})

submit_bus = api.model('Information to create a bus', {
	'index': fields.Integer(required=True, description='Bus id'),
	'size': fields.Integer(required=True, description='Bus size')
})

position = api.model("Full description of a position", {
	'room': fields.String(required=True, description='Room number'),
	'bus': fields.Integer(required=True, description='Bus number'),
	'index': fields.Integer(required=True, description='Bus index')
})


# Event

event = api.model("Full description of an event", {
	'id': fields.Integer(required=True, description='Event id'),
	'title': fields.String(required=True, description='Title'),
	'importance': fields.Integer(required=True, description='Importance from 0 to 10'),
	'start': fields.DateTime(required=True, description='Start date'),
	'end': fields.DateTime(required=False, description='End Date'),
	'sensor': fields.Integer(required=True, description='Sensor id'),
	'ended' : fields.Boolean(required=True, description='End of the event')
})

submit_event = api.model('Information for an event creation', {
	'id': fields.Integer(required=True, description='Event id'),
	'title': fields.String(required=True, description='Title'),
	'importance': fields.Integer(required=True, description='Importance from 0 to 10'),
	'start': fields.DateTime(required=True, description='Start date'),
	#'end': fields.DateTime(required=False, description='End Date'),
	'sensor': fields.Integer(required=True, description='Sensor id'),
	'ended' : fields.Boolean(required=False, description='End of the event', default = False)
})


# History

history_of_sensor_element = api.model("Dated positions of a sensor", {
	'start_of_service': fields.DateTime(required=True, description="Start date of a given position by a sensor"),
	'end_of_service': fields.DateTime(required=False, description="End date of a given position by a sensor"),
	'position': fields.Nested(position)
})

history_of_sensor = api.model("History of a sensor's positions", {
    'positions': fields.List(fields.Nested(history_of_sensor_element))
})

history_of_position_element = api.model("Dated sensors of a position", {
	'start_of_service': fields.DateTime(required=True, description="Start date of a given position by a sensor"),
	'end_of_service': fields.DateTime(required=False, description="End date of a given position by a sensor"),
	'sensor': fields.Nested(sensor)
})

history_of_position = api.model("History of a position's sensors", {
    'sensors': fields.List(fields.Nested(history_of_position_element))
})

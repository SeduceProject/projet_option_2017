from flask_restplus import fields
from seduce_api.api.restplus import api

capteur = api.model("Sensors information", {
	'nom': fields.String(required=False, description='Sensor name'),
	'type': fields.String(required=True, description='Sensor type')
})

position = api.model("Full description of a position", {
	'salle': fields.String(required=True, description='Room number'),
	'bus': fields.Integer(required=True, description='Bus number'),
	'index': fields.Integer(required=True, description='Bus index')
})

element_historique = api.model("Dated position of a sensor", {
	'debut': fields.DateTime(required=True, description="Start date of a given position by a sensor"),
	'fin': fields.DateTime(required=False, description="End date of a given position by a sensor"),
	'position': fields.Nested(position)
})

historique = api.inherit("History of a sensor positions", {
    'positions': fields.List(fields.Nested(element_historique))
})

submit_capteur = api.model('Information for a sensor creation', {
	'nom': fields.String(required=False, description='Sensor name'),
	'type': fields.String(required=True, description='Sensor type')
})

submit_position = api.model('Information for a position creation', {
	'salle': fields.String(required=True, description='Room number'),
	'bus': fields.Integer(required=True, description='Bus number'),
	'index': fields.Integer(required=True, description='Bus index')
})

import logging

from flask import request
from flask_restplus import Resource
from seduce_api.api.restplus import api
from seduce_api.api.serializers import capteur, position, historique, submit_capteur
from seduce_api.api.services import get_capteur, get_capteur_par_nom, get_position_capteur, get_historique_capteur, create_capteur

log = logging.getLogger(__name__)

ns = api.namespace('capteurs', description='Sensors operations')


@ns.route('/byName/<string:nom>')
class SensorByName(Resource):

	@api.marshal_with(sensor)
	def get(self, name):
		"""
		Retrieve the sensor with the given name.
		"""
		return get_capteur_by_name(name)


@ns.route('/<int:id>')
class SensorIdentity(Resource):

	@api.marshal_with(sensor)
	def get(self, id):
		"""
		Retrieve the sensor with the given id.
		"""
		return get_sensor(id)

	@api.response(200, 'Sensor successfully updated.')
	@api.expect(submit_sensor)
	def put(self, id):
		"""
		Sensor creation.
		"""
		data = request.json
		update_sensor(id, data)
		return None, 200


@ns.route('/<int:id>/position')
class PositionSensorById(Resource):

	@api.marshal_with(position)
	def get_position_sensor(self, id):
		"""
		Retrieve the position of a sensor with the given id.
		"""
		return get_position_sensor(id)


@ns.route('/<int:id>/history')
class HistorySensorById(Resource):

	@api.marshal_with(history)
	def get(self, id):
		"""
		Retrieve the position history of a sensor with the given id.
		"""
		return get_history_sensor(id)


@ns.route('/')
class CreateSensor(Resource):

	@api.response(201, 'Sensor successfully created.')
	@api.expect(submit_sensor)
	def put(self):
		"""
		Sensor creation.
		"""
		data = request.json
		create_sensor(data)
		return None, 201

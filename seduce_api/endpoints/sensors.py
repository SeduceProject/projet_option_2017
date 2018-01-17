import logging
import json

from flask import request
from flask_restplus import Resource
from seduce_api.serializers import sensor, position, submit_sensor, history_of_sensor
from seduce_api.services import create_sensor, get_sensor_by_name, get_sensor, delete_sensor, update_sensor, get_sensor_position, get_sensor_history
from seduce_api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('sensors', description='Sensors operations')


@ns.route('/')
class CreateSensor(Resource):

	@api.expect(submit_sensor)
	@api.marshal_with(sensor)
	def post(self):
		"""
		Creates a sensor.
		"""
		return create_sensor(request.json), 201


@ns.route('/byName/<string:name>')
class SensorByName(Resource):

	@api.marshal_with(sensor)
	def get(self, name):
		"""
		Retrieves the sensor with the given name.
		"""
		return get_sensor_by_name(name), 200


@ns.route('/<int:id>')
class SensorIdentity(Resource):

	@api.marshal_with(sensor)
	def get(self, id):
		"""
		Retrieves the sensor with the given id.
		"""
		return get_sensor(id), 200

	@api.marshal_with(sensor)
	def delete(self, id):
		"""
		Deletes the sensor with the given id.
		"""
		delete_sensor(id), 204

	@api.expect(submit_sensor)
	@api.marshal_with(sensor)
	def put(self, id):
		"""
		Updates the sensor.
		"""
		return update_sensor(id, request.json), 200


@ns.route('/<int:id>/position')
class PositionSensorById(Resource):

	@api.marshal_with(position)
	def get_position_sensor(self, id):
		"""
		Retrieves the position of a sensor with the given id.
		"""
		return get_sensor_position(id), 200


@ns.route('/<int:id>/history')
class HistorySensorById(Resource):

	@api.marshal_with(history_of_sensor)
	def get(self, id):
		"""
		Retrieves the position history of a sensor with the given id.
		"""
		return get_sensor_history(id), 200

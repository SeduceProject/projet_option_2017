import logging
import json

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api, SensorNotFoundException
from seduce_api.serializers import sensor, position, history, submit_sensor, event
from seduce_api.services import get_sensor, get_sensor_by_name, get_sensor_position, get_sensor_history, create_sensor, update_sensor, delete_sensor

log = logging.getLogger(__name__)

ns = api.namespace('sensors', description='Sensors operations')


@ns.route('/byName/<string:name>')
class SensorByName(Resource):

	@api.errorhandler
	@api.marshal_with(sensor)
	def get(self, name):
		"""
		Retrieves the sensor with the given name.
		"""
		try:
			return get_sensor_by_name(name)
		except Exception as e:
			raise SensorNotFoundException()


@ns.route('/<int:id>')
class SensorIdentity(Resource):

	@api.errorhandler
	@api.marshal_with(sensor)
	def get(self, id):
		"""
		Retrieves the sensor with the given id.
		"""
		try:
			return get_sensor(id)
		except Exception as e:
			raise SensorNotFoundException()

	@api.errorhandler
	@api.marshal_with(sensor)
	def delete(self, id):
		"""
		Deletes the sensor with the given id.
		"""
		try:
			delete_sensor(id)
			return 200
		except Exception as e:
			raise SensorNotFoundException()


	@api.marshal_with(sensor)
	@api.errorhandler
	@api.response(200, 'Sensor successfully updated.')
	@api.expect(submit_sensor)
	def put(self, id):
		"""
		Updates the sensor.
		"""
		try:
			data = request.json
			return update_sensor(id, data), 200
		except Exception as e:
			raise SensorNotFoundException()


@ns.route('/<int:id>/position')
class PositionSensorById(Resource):

	@api.errorhandler
	@api.marshal_with(position)
	def get_position_sensor(self, id):
		"""
		Retrieves the position of a sensor with the given id.
		"""
		try:
			return get_sensor_position(id)
		except Exception as e:
			raise SensorNotFoundException()


#@ns.route('/<int:id>/history')
#class HistorySensorById(Resource):
#
#	@api.marshal_with(history)
#	def get(self, id):
#		"""
#		Retrieves the position history of a sensor with the given id.
#		"""
#		return get_sensor_history(id)


@ns.route('/')
class CreateSensor(Resource):

	@api.marshal_with(sensor)
	@api.response(201, 'Sensor successfully created.')
	@api.expect(submit_sensor)
	def put(self):
		"""
		Creates the sensor.
		"""
		data = request.json
		return create_sensor(data), 201

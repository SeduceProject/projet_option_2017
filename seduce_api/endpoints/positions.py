import logging

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api
from seduce_api.serializers import sensor, position, history, submit_sensor, submit_position
from seduce_api.services import remove_position, add_position, update_sensor, filter_position

log = logging.getLogger(__name__)

ns = api.namespace('position', description='Position operations')


@ns.route('/<string:room>/<int:bus>/<int:index>')
class OperationsCapteur(Resource):

	@api.response(201, 'Sensor Successfully created.')
	@api.expect(submit_position)
	def post(self, id, room, bus, index):
		"""
		Add a sensor to a given position or remove it if the id is null.
		"""
		data = request.json
		if id == 0:
			remove_position(room, bus, index)
		else:
			add_position(data)
		return data, 201

	@api.expect(submit_position)
	def put(self, id):
		"""
		Change / Replace a sensor.
		"""
		data = request.json
		update_capteur(id, data)
		return data, 201

	@api.marshal_with(sensor)
	def get(self, room, bus, index):
		"""
		Retrieve the sensor information with a given position.
		"""
		return filter_position(room, bus, index), 200


@ns.route('/<string:room>/<int:bus>/<int:index>/history')
class HistoryPositionById(Resource):

	@api.marshal_with(history)
	def get(self, room, bus, index):
		"""
		History of a position.
		"""
		position = filter_position(room, bus, index)
		return position.history(), 200




import logging

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api
from seduce_api.serializers import sensor, position, history, submit_sensor, submit_sensor_position, submit_bus
from seduce_api.services import add_bus, remove_bus, filter_position

log = logging.getLogger(__name__)

ns = api.namespace('position', description='Position operations')


@ns.route('/<string:room>')
class RoomManagement(Resource):

	@api.expect(submit_bus)
	def post(self, room):
		"""
		Adds a bus to the room with the given id and size.
		"""
		data = request.json
		add_bus(room, data)
		return 201

	# TODO delete whole room

@ns.route('/<string:room>/<int:bus>')
class BusDeletion(Resource):

	def delete(self, room, bus):
		"""
		Deletes a bus from the room with the given id.
		"""
		remove_bus(room, bus)
		return 200


@ns.route('/<string:room>/<int:bus>/<int:index>')
class AssignSensorToPosition(Resource):

	@api.expect(submit_sensor_position)
	def put(self, room, bus, index):
		"""
		Adds a sensor to a given position or remove it if the id is null.
		"""
		data = request.json
		# TODO set sensor to position
		return 200

	@api.marshal_with(sensor)
	def get(self, room, bus, index):
		"""
		Retrieves the sensor information for a given position.
		"""
		return filter_position(room, bus, index), 200


#@ns.route('/<string:room>/<int:bus>/<int:index>/history')
#class HistoryPositionById(Resource):
#
#	@api.marshal_with(history)
#	def get(self, room, bus, index):
#		"""
#		History of a position.
#		"""
#		position = filter_position(room, bus, index)
#		return 200 #TODO position.history() ?

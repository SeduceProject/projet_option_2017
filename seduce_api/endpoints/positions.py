import logging

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api
from seduce_api.serializers import sensor, position, history, submit_sensor, submit_sensor_position, submit_bus
from seduce_api.services import add_bus, remove_bus, remove_room, get_position_by_values, add_assignment, remove_assignment

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
		return add_bus(room, data), 201

	def delete(self, room):
		"""
		Deletes the room.
		"""
		remove_room(room)
		return None, 204

@ns.route('/<string:room>/<int:bus>')
class BusDeletion(Resource):

	def delete(self, room, bus):
		"""
		Deletes a bus from the room with the given id.
		"""
		remove_bus(room, bus)
		return None, 204


@ns.route('/<string:room>/<int:bus>/<int:index>')
class AssignSensorToPosition(Resource):

	@api.expect(submit_sensor_position)
	def put(self, room, bus, index):
		"""
		Adds a sensor assignment to the given position.
		"""
		data = request.json
		return add_assignment(room, bus, index, data), 200

	def delete(self, room, bus, index):
		"""
		Removes the assignment from the given position if it exists.
		"""
		data = request.json
		remove_assignment(room, bus, index)
		return None, 204

#	@api.marshal_with(sensor)
#	def get(self, room, bus, index):
#		"""
#		Retrieves the sensor information for a given position.
#		"""
#		return 200 #TODO


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

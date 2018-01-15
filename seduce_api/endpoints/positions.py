import logging

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api
from seduce_api.serializers import sensor, position, submit_sensor, submit_sensor_position, submit_bus
from seduce_api.services import add_bus, remove_bus, remove_room, get_position_by_values, add_assignment, get_assigned_sensor, remove_assignment

log = logging.getLogger(__name__)

ns = api.namespace('position', description='Position operations')


@ns.route('/<string:room>')
class RoomManagement(Resource):

	@api.expect(submit_bus)
	def post(self, room):
		"""
		Adds a bus to the room with the given id and size.
		"""
		return add_bus(room, request.json), 201

	def delete(self, room):
		"""
		Deletes the room.
		"""
		return remove_room(room), 204

@ns.route('/<string:room>/<int:bus>')
class BusDeletion(Resource):

	def delete(self, room, bus):
		"""
		Deletes a bus from the room with the given id.
		"""
		return remove_bus(room, bus), 204


@ns.route('/<string:room>/<int:bus>/<int:index>')
class AssignSensorToPosition(Resource):

	@api.marshal_with(sensor)
	@api.expect(submit_sensor_position)
	def put(self, room, bus, index):
		"""
		Sets a sensor assignment to the given position.
		"""
		return add_assignment(room, bus, index, request.json), 200

	def delete(self, room, bus, index):
		"""
		Removes the assignment from the given position if it exists.
		"""
		return remove_assignment(room, bus, index), 204

	@api.marshal_with(sensor)
	def get(self, room, bus, index):
		"""
		Retrieves the sensor information for a given position.
		"""
		return get_assigned_sensor(room, bus, index), 200


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

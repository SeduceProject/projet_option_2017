import logging

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api
from seduce_api.serializers import sensor, position, submit_sensor, submit_sensor_position, submit_bus, history_of_position
from seduce_api.services import add_bus, remove_room, remove_bus, add_assignment, remove_assignment, get_assigned_sensor, get_position_history

log = logging.getLogger(__name__)

ns = api.namespace('position', description='Position operations')


@ns.route('/<string:room>')
class RoomManagement(Resource):

	@api.expect(submit_bus)
	def post(self, room):
		"""
		Adds a bus to the room with the given id and size.
		"""
		add_bus(room, request.json)
		return None, 201

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
		Adds a sensor to a given position.
		"""
		return add_assignment(room, bus, index, request.json), 201

	def delete(self, room, bus, index):
		"""
		Removes the sensor from a given position if there is one.
		"""
		return remove_assignment(room, bus, index), 204

	@api.marshal_with(sensor)
	def get(self, room, bus, index):
		"""
		Retrieves the sensor information for a given position.
		"""
		return get_assigned_sensor(room, bus, index), 200


@ns.route('/<string:room>/<int:bus>/<int:index>/history')
class HistoryPositionById(Resource):

	@api.marshal_with(history_of_position)
	def get(self, room, bus, index):
		"""
		Retrieves the sensor history of a position with the given coordinates.
		"""
		return get_position_history(room, bus, index), 200

import logging
import json

from flask import request
from flask_restplus import Resource
from seduce_api.restplus import api, SensorNotFoundException, EventNotFoundException
from seduce_api.serializers import sensor, position, history, submit_sensor, event, submit_event
from seduce_api.services import get_sensor, get_sensor_by_name, get_sensor_position, get_sensor_history, create_sensor, update_sensor, delete_sensor, create_event, get_event, get_event_by_importance, get_event_by_sensor_id, end_event

log = logging.getLogger(__name__)

ns = api.namespace('event', description='Event operations')


@ns.route('/byImportance/<int:name>')
class EventByImportance(Resource):

	@api.errorhandler
	@api.marshal_with(event)
	def get(self, name):
		"""
		Retrieves the event with the given importance.
		"""
		try:
			return get_event_by_importance(name)
		except Exception as e:
			raise EventNotFoundException()

@ns.route('/bySensor/<int:sensor>')
class EventBySensor(Resource):

	@api.errorhandler
	@api.marshal_with(event)
	def get(self, sensor):
		"""
		Retrieves the event with the given sensor.
		"""
		try:
			return get_event_by_sensor_id(sensor)
		except Exception as e:
			raise EventNotFoundException()


@ns.route('/<int:id>')
class EventIdentity(Resource):

	@api.errorhandler
	@api.marshal_with(event)
	def get(self, id):
		"""
		Retrieves the event with the given id.
		"""
		try:
			return get_event(id)
		except Exception as e:
			raise EventNotFoundException()

	@api.marshal_with(event)
	@api.response(201, 'Event successfully ended.')
	@api.errorhandler
	#@api.expect(submit_event)
	def put(self, id):
		"""
		Ends the event.
		"""
		#try:
		return end_event(id), 200
		#except Exception as e:
			#raise EventNotFoundException()


@ns.route('/')
class CreateEvent(Resource):

	@api.marshal_with(event)
	@api.response(201, 'Event successfully created.')
	@api.expect(submit_event)
	def post(self):
		"""
		Creates the event.
		"""
		data = request.json
		return create_event(data), 201





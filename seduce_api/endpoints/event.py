import logging

from flask import request
from flask_restplus import Resource
from seduce_api.serializers import event, submit_event
from seduce_api.services import create_event, get_event, get_event_by_importance, get_events, get_events_after_id, \
    get_event_by_sensor_id, end_event
from seduce_api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('event', description='Event operations')


@ns.route('/')
class CreateEvent(Resource):
    @api.marshal_with(event)
    @api.expect(submit_event)
    def post(self):
        """
        Creates the event.
        """
        return create_event(request.json), 201


@ns.route('/byImportance/<int:importance>')
class EventByImportance(Resource):
    @api.marshal_with(event)
    def get(self, importance):
        """
        Retrieves the event with the given importance.
        """
        return get_event_by_importance(importance), 200


@ns.route('/bySensor/<int:sensor>')
class EventBySensor(Resource):
    @api.marshal_with(event)
    def get(self, sensor):
        """
        Retrieves the event with the given sensor.
        """
        return get_event_by_sensor_id(sensor), 200


@ns.route('/all')
class Events(Resource):
    @api.marshal_with(event)
    def get(self):
        """
        Retrieves all the events.
        """
        return get_events(), 200


@ns.route('/after/<int:id>')
class EventsAfter(Resource):
    @api.marshal_with(event)
    def get(self, id):
        """
        Retrieves all the events after the given id.
        """
        return get_events_after_id(id), 200


@ns.route('/<int:id>')
class EventIdentity(Resource):
    @api.marshal_with(event)
    def get(self, id):
        """
        Retrieves the event with the given id.
        """
        return get_event(id), 200

    @api.marshal_with(event)
    def put(self, id):
        """
        Ends the event.
        """
        return end_event(id), 200

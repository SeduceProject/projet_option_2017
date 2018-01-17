import logging
import traceback

from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Seduce API',
		description='Seduce Project - Thermal sensors monitoring')

class SensorNotFoundException(Exception):
	
	def __init__(self):
		super(SensorNotFoundException, self).__init__("mon message")
		

@api.errorhandler
def default_error_handler(e):
	message = 'Unhandled exception caught.'
	log.exception(message)

	if not settings.FLASK_DEBUG:
		return {'message': message}, 500

@api.errorhandler(SensorNotFoundException)
def handle_sensor_not_found_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'No sensor found'}, 404


class EventNotFoundException(Exception):
	
	def __init__(self):
		super(EventNotFoundException, self).__init__("mon message")

@api.errorhandler(EventNotFoundException)
def handle_event_not_found_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'No event found'}, 404

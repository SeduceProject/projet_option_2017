import logging
import traceback

from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Seduce API',
		description='Seduce Project - Thermal sensors monitoring')


# Exceptions

class SensorNotFoundException(Exception):
	def __init__(self, message="Sensor not found"):
		super(SensorNotFoundException, self).__init__(message)

class SensorNotValidException(Exception):
	def __init__(self, message="Sensor not valid"):
		super(SensorNotValidException, self).__init__(message)

class PositionNotFoundException(Exception):
	def __init__(self, message="Position not found"):
		super(PositionNotFoundException, self).__init__(message)

class PositionNotValidException(Exception):
	def __init__(self, message="Position not valid"):
		super(PositionNotValidException, self).__init__(message)

class AssignmentNotFoundException(Exception):
	def __init__(self, message="Assignment not found"):
		super(AssignmentNotFoundException, self).__init__(message)

class AssignmentNotValidException(Exception):
	def __init__(self, message="Assignment not valid"):
		super(AssignmentNotValidException, self).__init__(message)

class EventNotFoundException(Exception):
	def __init__(self, message="Event not found"):
		super(EventNotFoundException, self).__init__(message)


# Error Handlers

@api.errorhandler
def default_error_handler(e):
	message = 'Unhandled exception caught.'
	log.exception(message)

	if not settings.FLASK_DEBUG:
		return {'message': message}, 500

@api.errorhandler(SensorNotFoundException)
def handle_sensor_not_found_exception(error):
    '''In case of a sensor being not found.'''
    return {'message': error.message}, 404

@api.errorhandler(SensorNotValidException)
def handle_sensor_not_valid_exception(error):
    '''In case of a sensor being not valid.'''
    return {'message': error.message}, 412

@api.errorhandler(PositionNotFoundException)
def handle_position_not_found_exception(error):
    '''In case of a position being not found.'''
    return {'message': error.message}, 404

@api.errorhandler(PositionNotValidException)
def handle_position_not_valid_exception(error):
    '''In case of a position being not valid.'''
    return {'message': error.message}, 412

@api.errorhandler(AssignmentNotFoundException)
def handle_assignment_not_found_exception(error):
    '''In case of an assignment being not found.'''
    return {'message': error.message}, 404

@api.errorhandler(AssignmentNotValidException)
def handle_assignment_not_valid_exception(error):
    '''In case of an assignment being not valid.'''
    return {'message': error.message}, 412

@api.errorhandler(EventNotFoundException)
def handle_event_not_found_exception(error):
    '''In case of an event being not found.'''
    return {'message': error.message}, 404

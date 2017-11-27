import logging
import traceback

from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Seduce API',
		description='Seduce Project - Thermal sensors monitoring')

@api.errorhandler
def default_error_handler(e):
	message = 'Unhandled exception caught.'
	log.exception(message)

	if not settings.FLASK_DEBUG:
		return {'message': message}, 500

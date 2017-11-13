import logging
import traceback

from flask_restplus import Api
from seduce_api import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Seduce API',
		description='Projet Seduce - Surveillance de capteurs thermiques')

@api.errorhandler
def default_error_handler(e):
	message = 'Une erreur non prise en charge a eu lieu.'
	log.exception(message)

	if not settings.FLASK_DEBUG:
		return {'message': message}, 500

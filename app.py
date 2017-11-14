import logging.config

from flask import Flask, Blueprint, g
from seduce_api import settings
from seduce_api.api.endpoints.capteurs import ns as capteurs_namespace
from seduce_api.api.restplus import api

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

base_url = 'seduce'

def configure_app(flask_app):
	flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
	flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
	flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
	flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
	flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
	flask_app.config['DATABASE'] = os.path.join(app.root_path, 'database', settings.DATABASE)

@app.cli.command('initdb')	
def connect_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = sqlite3.connect(flask_app.config['DATABASE'])
		g.sqlite_db.execute('pragma_foreign_keys=ON')
	return g.sqlite_db

def initialize_app(flask_app):
	configure_app(flask_app)

	blueprint = Blueprint('Seduce', __name__, url_prefix='/'+base_url)
	api.init_app(blueprint)
	api.add_namespace(capteurs_namespace)
	flask_app.register_blueprint(blueprint)

	db.init_app(flask_app)

def main():
	initialize_app(app)
	log.info('>>>>> Starting development server at http://{}/'+base_url+'/ <<<<<'.format(app.config['SERVER_NAME']))
	app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
	main()

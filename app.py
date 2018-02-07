import logging.config

from flask import Flask, Blueprint
import settings
from seduce_api.endpoints.sensors import ns as sensors_namespace
from seduce_api.endpoints.positions import ns as positions_namespace
from seduce_api.endpoints.event import ns as event_namespace
from seduce_api.restplus import api
from database import db
from flask_bootstrap import Bootstrap
from flask import render_template, Flask 
from seduce_api import services

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

base_url = 'seduce'


def configure_app(flask_app):
	flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
	flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
	flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
	flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
	flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
	flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
	flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
	blueprint = Blueprint('Seduce', __name__, url_prefix='/'+base_url)
	api.init_app(blueprint)
	api.add_namespace(sensors_namespace)
	api.add_namespace(positions_namespace)
	api.add_namespace(event_namespace)
	flask_app.register_blueprint(blueprint)

def init_db(flask_app):
	db.init_app(flask_app)
	db.create_all()

@app.route('/seduce/event/all')
def table(): 
	events = services.get_events()
	return render_template('table.html', events=events)

def main():
	with app.app_context():
		configure_app(app)
		initialize_app(app)
		init_db(app)
	log.info('>>>>> Starting development server at http://{}/'+base_url+'/ <<<<<'.format(app.config['SERVER_NAME']))
	Bootstrap(app)
	app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
	main()

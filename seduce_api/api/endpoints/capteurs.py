import logging

from flask import request
from flask_restplus import Resource
from seduce_api.api.restplus import api
from seduce_api.api.serializers import capteur, position, historique, submit_capteur
from seduce_api.api.services import get_capteur, get_capteur_par_nom, get_position_capteur, get_historique_capteur, create_capteur

log = logging.getLogger(__name__)

ns = api.namespace('capteurs', description='Operations liees aux capteurs')


@ns.route('/parNom/<string:nom>')
class CapteurParNom(Resource):

	@api.marshal_with(capteur)
	def get(self, nom):
		"""
		Renvoie le capteur correspondant au nom fourni.
		"""
		return get_capteur_par_nom(nom)


@ns.route('/<int:id>')
class IdentiteCapteur(Resource):

	@api.marshal_with(capteur)
	def get(self, id):
		"""
		Renvoie le capteur correspondant a l'identifiant fourni.
		"""
		return get_capteur(id)


@ns.route('/<int:id>/position')
class PositionCapteurParId(Resource):

	@api.marshal_with(position)
	def get(self, id):
		"""
		Renvoie la position du capteur correspondant a l'identifiant fourni.
		"""
		return get_position_capteur(id)


@ns.route('/<int:id>/historique')
class HistoriqueCapteurParId(Resource):

	@api.marshal_with(historique)
	def get(self, id):
		"""
		Renvoie l'historique des positions du capteur correspondant a l'identifiant fourni.
		"""
		return get_historique_capteur(id)


@ns.route('/')
class CreationCapteur(Resource):

	@api.response(201, 'Capteur cree avec succes.')
	@api.expect(submit_capteur)
	def post(self):
		"""
		Cree un capteur.
		"""
		data = request.json
		create_capteur(data)
		return None, 201

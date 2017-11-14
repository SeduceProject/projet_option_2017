import logging

from flask import request
from flask_restplus import Resource
from seduce_api.api.restplus import api
from seduce_api.api.serializers import submit_capteur
from seduce_api.api.services import create_capteur

log = logging.getLogger(__name__)

ns = api.namespace('position', description='Operations liees aux positions')


@ns.route('/<string:salle>/<int:bus>/<int:index>')
class OperationsCapteur(Resource):

	def put(self, id):
		"""
		Changer / remplacer un capteur
		"""
		data = request.json
		update_position(data)
		return data, 201


	def post(self, id=0):
		"""
		Retirer un capteur
		"""
		data = request.json
		retirer_capteur(data)
		return data, 201

	def get(self, salle, bus, index):
		"""
		Informations sur un capteur avec une position donnee
		"""
		return Capteur.query.filter(Position.salle == salle and Position.bus == bus and Position.index == index), 200


@ns.route('/<string:salle>/<int:bus>/<int:index>/historique')
class HistoriquePositionParId(Resource):

	def get(self, salle, bus, index):
		"""
		Historique d’une position
		"""
		position = filter_position(salle, bus, index)
		return position.historique(), 200




import logging

from flask import request
from flask_restplus import Resource
from seduce_api.api.restplus import api
from seduce_api.api.serializers import capteur, position, historique, submit_capteur, submit_position
from seduce_api.api.services import retirer_position, ajouter_position, update_capteur, filter_position

log = logging.getLogger(__name__)

ns = api.namespace('position', description='Operations liees aux positions')


@ns.route('/<string:salle>/<int:bus>/<int:index>')
class OperationsCapteur(Resource):

	@api.response(201, 'Capteur cree avec succes.')
	@api.expect(submit_position)
	def post(self, id, salle, bus, index):
		"""
		Ajouter un capteur à une position donnée ou le retirer si l'identifiant fourni est nul.
		"""
		data = request.json
		if id == 0:
			retirer_position(salle, bus, index)
		else:
			ajouter_position(data)
		return data, 201

	@api.expect(submit_position)
	def put(self, id):
		"""
		Changer / Remplacer un capteur.
		"""
		data = request.json
		update_capteur(id, data)
		return data, 201

	@api.marshal_with(capteur)
	def get(self, salle, bus, index):
		"""
		Renvoie les informations sur un capteur avec une position donnée.
		"""
		return filter_position(salle, bus, index), 200


@ns.route('/<string:salle>/<int:bus>/<int:index>/historique')
class HistoriquePositionParId(Resource):

	@api.marshal_with(historique)
	def get(self, salle, bus, index):
		"""
		Historique d’une position.
		"""
		position = filter_position(salle, bus, index)
		return position.historique(), 200




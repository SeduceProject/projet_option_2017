from flask_restplus import fields
from seduce_api.api.restplus import api

capteur = api.model("Informations d'un capteur", {
	'nom': fields.String(required=False, description='Nom du capteur'),
	'type': fields.String(required=True, description='Type du capteur')
})

position = api.model("Description complete d'une position", {
	'salle': fields.String(required=True, description='Numero de salle'),
	'bus': fields.Integer(required=True, description='Numero de bus'),
	'index': fields.Integer(required=True, description='Index sur le bus')
})

element_historique = api.model("Position datee d'un capteur", {
	'debut': fields.DateTime(required=True, description="Debut de l'occupation de la position par le capteur"),
	'fin': fields.DateTime(required=False, description="Fin de l'occupation de la position par le capteur"),
	'position': fields.Nested(position)
})

historique = api.inherit("Historique des positions d'un capteur", {
    'positions': fields.List(fields.Nested(element_historique))
})

submit_capteur = api.model('Informations pour creer un capteur', {
	'nom': fields.String(required=False, description='Nom du capteur'),
	'type': fields.String(required=True, description='Type du capteur')
})

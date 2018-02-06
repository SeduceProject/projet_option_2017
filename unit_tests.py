from flask import Flask
import unittest
from app import db
from seduce_api.restplus import SensorNotFoundException, SensorNotValidException, PositionNotFoundException, PositionNotValidException, AssignmentNotFoundException, AssignmentNotValidException, EventNotFoundException
import seduce_api.services as ser
from database.models import Sensor, Position, Assignment, History, Event

class TestSeduceApi(unittest.TestCase):
	"""Unit tests for Seduce API."""

	def setUp(self):
		self.app = Flask(__name__)
		self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db-test.sqlite'
		self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		db.init_app(self.app)
		with self.app.app_context():
			db.create_all()

	def tearDown(self):
		with self.app.app_context():
			db.drop_all()

	def test_get_sensor_ok(self):
		"""
		Test case for get_sensor_identity

		Retrieves the sensor with the given id
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			found_sensor = ser.get_sensor(sensor.id)
			self.assertEqual(sensor, found_sensor)
			db.session.delete(sensor)
			db.session.commit()

	def test_get_sensor_not_found(self):
		"""
		Test case for get_sensor_identity

		Fails because of a wrong id
		"""
		with self.app.app_context():
			with self.assertRaises(SensorNotFoundException):
				ser.get_sensor(0)

	def test_get_sensor_by_name(self):
		"""
		Test case for get_sensor_by_name

		Retrieves the sensor with the given name
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			found_sensor = ser.get_sensor_by_name(sensor.name)
			self.assertEqual(sensor, found_sensor)
			db.session.delete(sensor)
			db.session.commit()


if __name__ == '__main__':
	unittest.main()

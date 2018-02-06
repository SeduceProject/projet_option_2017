from flask import Flask
import unittest
from app import db
from seduce_api.restplus import SensorNotFoundException, SensorNotValidException, PositionNotFoundException, PositionNotValidException, AssignmentNotFoundException, AssignmentNotValidException, EventNotFoundException
import seduce_api.services as ser
from database.models import Sensor, Position, Assignment, History, Event
import json

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


	# Sensors

	def test_create_sensor(self):
		"""
		Test case for create_sensor
		"""
		with self.app.app_context():
			old_sensor = Sensor("old name", "old mac", "type", "model", 0)
			db.session.add(old_sensor)
			db.session.commit()
			# Invalid mac
			with self.assertRaises(SensorNotValidException):
				ser.create_sensor(dict(name="name", mac="", type="type", model="model", state=0))
			# Duplicate mac
			with self.assertRaises(SensorNotValidException):
				ser.create_sensor(dict(name="name", mac="old mac", type="type", model="model", state=0))
			# Duplicate name
			with self.assertRaises(SensorNotValidException):
				ser.create_sensor(dict(name="old name", mac="mac", type="type", model="model", state=0))
			# OK
			sensor = ser.create_sensor(dict(name="name", mac="mac", type="type", model="model", state=0))
			db.session.delete(sensor)
			db.session.delete(old_sensor)
			db.session.commit()

	def test_get_sensor(self):
		"""
		Test case for get_sensor
		"""
		with self.app.app_context():
			# Wrong id
			with self.assertRaises(SensorNotFoundException):
				ser.get_sensor(0)
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			# OK
			found_sensor = ser.get_sensor(sensor.id)
			self.assertEqual(sensor, found_sensor)
			db.session.delete(sensor)
			db.session.commit()

	def test_get_sensor_by_name(self):
		"""
		Test case for get_sensor_by_name
		"""
		with self.app.app_context():
			# Wrong name
			with self.assertRaises(SensorNotFoundException):
				ser.get_sensor_by_name("not a name")
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			# OK
			found_sensor = ser.get_sensor_by_name(sensor.name)
			self.assertEqual(sensor, found_sensor)
			db.session.delete(sensor)
			db.session.commit()

	def test_get_sensor_position(self):
		"""
		Test case for get_sensor_position
		"""
		with self.app.app_context():
			pass # TODO

	def test_update_sensor(self):
		"""
		Test case for update_sensor
		"""
		with self.app.app_context():
			old_sensor = Sensor("old name", "old mac", "type", "model", 0)
			other_sensor = Sensor("other name", "other mac", "type", "model", 0)
			db.session.add(old_sensor)
			db.session.add(other_sensor)
			db.session.commit()
			# Invalid mac
			with self.assertRaises(SensorNotValidException):
				ser.update_sensor(old_sensor.id, dict(name="new name", mac="", type="type", model="model", state=0))
			# Duplicate mac
			with self.assertRaises(SensorNotValidException):
				ser.update_sensor(old_sensor.id, dict(name="new name", mac="other mac", type="type", model="model", state=0))
			# Duplicate name
			with self.assertRaises(SensorNotValidException):
				ser.update_sensor(old_sensor.id, dict(name="other name", mac="new mac", type="type", model="model", state=0))
			# OK
			sensor = ser.update_sensor(old_sensor.id, dict(name="new name", mac="new mac", type="type", model="model", state=0))
			# OK
			sensor = ser.update_sensor(old_sensor.id, dict(name="another new name", mac="new mac", type="type", model="model", state=0))
			db.session.delete(sensor)
			db.session.delete(old_sensor)
			db.session.delete(other_sensor)
			db.session.commit()

	def test_delete_sensor(self):
		"""
		Test case for delete_sensor
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			# OK
			ser.delete_sensor(sensor.id)
			with self.assertRaises(SensorNotFoundException):
				ser.get_sensor(sensor.id)


	# Positions

	def test_add_bus(self):
		"""
		Test case for add_bus
		"""
		with self.app.app_context():
			old_position = Position("room", 1, 0)
			db.session.add(old_position)
			db.session.commit()
			# Invalid bus id
			with self.assertRaises(PositionNotValidException):
				ser.add_bus("room", dict(index=-1, size=2))
			# Duplicate (room, bus)
			with self.assertRaises(PositionNotValidException):
				ser.add_bus("room", dict(index=1, size=2))
			# Invalid bus size
			with self.assertRaises(PositionNotValidException):
				ser.add_bus("room", dict(index=0, size=0))
			# OK
			positions_list = ser.add_bus("room", dict(index=0, size=2))
			self.assertEqual(2, len(positions_list))
			for p in positions_list:
				db.session.delete(p)
			db.session.delete(old_position)
			db.session.commit()

	def test_remove_bus(self):
		"""
		Test case for remove_bus
		"""
		with self.app.app_context():
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			# OK
			ser.remove_bus("room", 1)
			with self.assertRaises(PositionNotFoundException):
				ser.get_position_by_values("room", 1, 0)

	def test_remove_room(self):
		"""
		Test case for remove_room
		"""
		with self.app.app_context():
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			# OK
			ser.remove_room("room")
			with self.assertRaises(PositionNotFoundException):
				ser.get_position_by_values("room", 1, 0)

	def test_get_position_by_values(self):
		"""
		Test case for get_position_by_values
		"""
		with self.app.app_context():
			# Wrong position
			with self.assertRaises(PositionNotFoundException):
				ser.get_position_by_values("room", 1, 0)
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			# OK
			found_position = ser.get_position_by_values("room", 1, 0)
			self.assertEqual(position, found_position)
			db.session.delete(position)
			db.session.commit()


if __name__ == '__main__':
	unittest.main()

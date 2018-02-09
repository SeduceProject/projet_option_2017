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
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()

			# Sensor not assigned
			with self.assertRaises(AssignmentNotFoundException):
				ser.get_sensor_position(sensor.id)

			ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))

			# OK
			found_position = ser.get_sensor_position(sensor.id)
			self.assertEqual(position, found_position)

			db.session.delete(sensor)
			db.session.delete(position)
			db.session.commit()

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


	# Events

	def test_create_event(self):
		"""
		Test case for create_event
		"""
		with self.app.app_context():
			# Invalid sensor
			with self.assertRaises(SensorNotFoundException):
				ser.create_event(dict(title="title", importance=5, sensor=0, ended=False))

			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()

			# OK
			event = ser.create_event(dict(title="title", importance=5, sensor=sensor.id, ended=False))

			db.session.delete(event)
			db.session.delete(sensor)
			db.session.commit()

	def test_get_event(self):
		"""
		Test case for get_event
		"""
		with self.app.app_context():
			# Invalid id
			with self.assertRaises(EventNotFoundException):
				ser.get_event(0)

			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			event = Event("title", 5, sensor.id)
			db.session.add(event)
			db.session.commit()

			# OK
			found_event = ser.get_event(event.id)
			self.assertEqual(event, found_event)

			db.session.delete(event)
			db.session.delete(sensor)
			db.session.commit()

	def test_get_event_by_importance(self):
		"""
		Test case for get_event_by_importance
		"""
		with self.app.app_context():
			# No event with given importance
			with self.assertRaises(EventNotFoundException):
				ser.get_event_by_importance(5)

			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			event = Event("title", 5, sensor.id)
			db.session.add(event)
			db.session.commit()

			# OK
			events = ser.get_event_by_importance(5)
			self.assertEqual(1, len(events))
			self.assertEqual(event, events[0])

			db.session.delete(event)
			db.session.delete(sensor)
			db.session.commit()

	def test_get_event_by_sensor_id(self):
		"""
		Test case for get_event_by_sensor_id
		"""
		with self.app.app_context():
			# No event for given sensor
			with self.assertRaises(EventNotFoundException):
				ser.get_event_by_sensor_id(0)

			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			event = Event("title", 5, sensor.id)
			db.session.add(event)
			db.session.commit()

			# OK
			events = ser.get_event_by_sensor_id(sensor.id)
			self.assertEqual(1, len(events))
			self.assertEqual(event, events[0])

			db.session.delete(event)
			db.session.delete(sensor)
			db.session.commit()

	def test_end_event(self):
		"""
		Test case for end_event
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			event = Event("title", 5, sensor.id)
			db.session.add(event)
			db.session.commit()

			# OK
			found_event = ser.end_event(event.id)
			self.assertEqual(event.id, found_event.id)
			self.assertIsNotNone(found_event.end)
			self.assertTrue(found_event.ended)

			db.session.delete(event)
			db.session.delete(sensor)
			db.session.commit()


	# Assignments

	def test_add_assignment(self):
		"""
		Test case for add_assignment
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			other_sensor = Sensor("other name", "other mac", "type", "model", 0)
			db.session.add(other_sensor)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()

			# OK
			same_sensor = ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))
			self.assertEqual(sensor, same_sensor)
			found_position = ser.get_sensor_position(sensor.id)
			self.assertEqual(position, found_position)
			found_sensor = ser.get_assigned_sensor(position.room, position.bus, position.index)
			self.assertEqual(sensor, found_sensor)

			# Trying to assign a sensor but there is already one
			with self.assertRaises(AssignmentNotValidException):
				ser.add_assignment("room", 1, 0, dict(sensor=other_sensor.id))

			db.session.delete(sensor)
			db.session.delete(other_sensor)
			db.session.delete(position)
			db.session.commit()

	def test_get_assigned_sensor(self):
		"""
		Test case for get_assigned_sensor
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()

			# No sensor assigned to position
			with self.assertRaises(AssignmentNotFoundException):
				ser.get_assigned_sensor(position.room, position.bus, position.index)

			ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))

			# OK
			found_sensor = ser.get_assigned_sensor(position.room, position.bus, position.index)
			self.assertEqual(sensor, found_sensor)

			db.session.delete(sensor)
			db.session.delete(position)
			db.session.commit()

	def test_remove_assignment(self):
		"""
		Test case for remove_assignment
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))

			# OK
			ser.remove_assignment(position.room, position.bus, position.index)
			with self.assertRaises(AssignmentNotFoundException):
				ser.get_assigned_sensor(position.room, position.bus, position.index)
			with self.assertRaises(AssignmentNotFoundException):
				ser.get_sensor_position(sensor.id)

			db.session.delete(sensor)
			db.session.delete(position)
			db.session.commit()


	# History

	def test_close_sensor_history_element(self):
		"""
		Test case for close_sensor_history_element
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))
			ser.remove_assignment("room", 1, 0)

			# OK
			history = ser.get_sensor_history(sensor.id)["positions"][0]
			self.assertEqual({"room": position.room, "bus": position.bus, "index": position.index}, history["position"])
			self.assertIsNotNone(history["end_of_service"])

			db.session.delete(sensor)
			db.session.delete(position)
			db.session.commit()

	def test_get_sensor_history(self):
		"""
		Test case for get_sensor_history
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			position2 = Position("room", 1, 1)
			db.session.add(position2)
			db.session.commit()
			ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))
			ser.add_assignment("room", 1, 1, dict(sensor=sensor.id))

			# OK
			history = sorted(ser.get_sensor_history(sensor.id)["positions"], key=lambda element: element["start_of_service"])
			self.assertEqual(2, len(history))
			self.assertEqual({"room": position.room, "bus": position.bus, "index": position.index}, history[0]["position"])
			self.assertIsNotNone(history[0]["end_of_service"])
			self.assertEqual({"room": position2.room, "bus": position2.bus, "index": position2.index}, history[1]["position"])
			self.assertIsNone(history[1]["end_of_service"])

			db.session.delete(sensor)
			db.session.delete(position)
			db.session.delete(position2)
			db.session.commit()

	def test_get_position_history(self):
		"""
		Test case for get_position_history
		"""
		with self.app.app_context():
			sensor = Sensor("name", "mac", "type", "model", 0)
			db.session.add(sensor)
			db.session.commit()
			sensor2 = Sensor("name2", "mac2", "type", "model", 0)
			db.session.add(sensor2)
			db.session.commit()
			position = Position("room", 1, 0)
			db.session.add(position)
			db.session.commit()
			ser.add_assignment("room", 1, 0, dict(sensor=sensor.id))
			ser.remove_assignment("room", 1, 0)
			ser.add_assignment("room", 1, 0, dict(sensor=sensor2.id))

			# OK
			history = sorted(ser.get_position_history("room", 1, 0)["sensors"], key=lambda element: element["start_of_service"])
			self.assertEqual(2, len(history))
			self.assertEqual(sensor.id, history[0]["sensor"]["id"])
			self.assertIsNotNone(history[0]["end_of_service"])
			self.assertEqual(sensor2.id, history[1]["sensor"]["id"])
			self.assertIsNone(history[1]["end_of_service"])

			db.session.delete(sensor)
			db.session.delete(sensor2)
			db.session.delete(position)
			db.session.commit()


if __name__ == '__main__':
	unittest.main()

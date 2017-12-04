import os
import app
import unittest
import tempfile
import json
from service.api import services

# See : http://flask.pocoo.org/docs/0.12/testing/

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		app.testing = True

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(app.config['DATABASE'])

	def test_sensor_creation(self):
		data = json.dumps({"mac": "mac", "model": "model", "name": "cute sensor", "state": 0, "type": "temp"})
		sensor = create_sensor(data)
		assert sensor.id != None and sensor.mac == "mac" and sensor.name == "cute sensor" and sensor.state == 0 and sensor.type == "temp"
		delete_sensor(sensor.id)

	def test_data_sensor(self):
		data = json.dumps({"mac": "mac", "model": "model", "name": "cute sensor", "state": 0, "type": "temp"})
		sensor = create_sensor(data)
		sensor1 = get_sensor(sensor.id)
		sensor2 = get_sensor_by_name(sensor.name)
		assert sensor.id == sensor1.id and sensor.mac == sensor1.mac and sensor.name == sensor1.name and sensor.state == sensor1.state and sensor.type == sensor1.type
		assert sensor.id == sensor2.id and sensor.mac == sensor2.mac and sensor.name == sensor2.name and sensor.state == sensor2.state and sensor.type == sensor2.type
		delete_sensor(sensor.id)

	


if __name__ == '__main__':
	unittest.main()

import os
import app
import unittest
import tempfile

# See : http://flask.pocoo.org/docs/0.12/testing/

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		app.testing = True

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(app.config['DATABASE'])

if __name__ == '__main__':
	unittest.main()

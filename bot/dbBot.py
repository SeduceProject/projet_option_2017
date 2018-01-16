import sqlite3

class DBBot:
	def __init__(self, dbname="../database/db_test_bot.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	def get_sensor(self, name):
		req = "SELECT id FROM sensors WHERE name=(?)"
		args = (name, )
		return [x[0] for x in self.conn.execute(req, args)]
		
#test = DBBot()
#print(test.get_sensor("Claude"))

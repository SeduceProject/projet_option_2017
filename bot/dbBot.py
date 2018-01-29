import sqlite3
import json
import requests

URL_API = "http://localhost:8888/seduce"

def get_json_from_url(url):
		print url
		a = requests.get(url)
		print a 
		b = a.content
		print b
		c = b.decode("utf8")
		print c
		return json.loads(c)

class DBBot:
	def __init__(self, dbname="../database/db_test_bot.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	def get_sensor(self, name):
		"""req = "SELECT id FROM sensors WHERE name=(?)"
		args = (name, )
		return [x[0] for x in self.conn.execute(req, args)][0]"""
		#//////////////via api et json//////////////
		print "get_sensor de dbbot"
		print name
		url = URL_API + "/sensors/byName/" + name
		js = get_json_from_url(url)
		print js
		return js["id"]
		
		
#test = DBBot()
#print(test.get_sensor("Claude"))

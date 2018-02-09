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
    def __init__(self, dbname="event_bot_db.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def get_sensor_by_name(self, name):
        url = URL_API + "/sensors/byName/" + name
        js = get_json_from_url(url)
        return js

    def get_sensor_by_id(self, id):
        url = URL_API + "/sensors/" + id
        js = get_json_from_url(url)
        return js

    def get_sensor_history(self, id):
        url = URL_API + "/sensors/" + id + "/history"
        js = get_json_from_url(url)
        return js

    def get_sensor_position(self, id):
        url = URL_API + "/sensors/" + id + "/position"
        js = get_json_from_url(url)
        return js

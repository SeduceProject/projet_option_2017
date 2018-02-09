import json 
import requests
import time
import urllib
import dbBot

TOKEN_BOT = "472925886:AAHoewEo-y9D9wIaljXJllows3UNIPHOIao"
URL_BOT = "https://api.telegram.org/bot{}/".format(TOKEN_BOT)
DB = dbBot.DBBot()
CHAT = ""

def get_url(url):
	response = requests.get(url)
	content = response.content.decode("utf8")
	return content

def get_json_from_url(url):
	content = get_url(url)
	js = json.loads(content)
	return js

def set_chat(chat):
	global CHAT
	CHAT = chat

def get_updates(offset=None):
	url = URL_BOT + "getUpdates?timeout=100"
	if offset:
		url += "&offset={}".format(offset)
	js = get_json_from_url(url)
	return js
	
def get_events(offset):
	url = dbBot.URL_API + "/event/after/" + str(offset)
	js = get_json_from_url(url)
	return js
	
def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

def get_last_event_id(events):
	event_ids = []
	for event in events:
		event_ids.append(int(event["id"]))
	return max(event_ids)
	
def answer_all_updates(updates):
	for update in updates["result"]:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			set_chat(chat)
			send_message(text)
		except Exception as e:
			print(e)
			
def send_all_events(events):
	print "dans le send all events"
	for event in events:
		print event["ended"], type(event["ended"])
		if (event["ended"] == False):
			try:
				start = event["start"]
				importance = event["importance"]
				title = event["title"]
				id_sensor = event["sensor"]
				text = "At the moment " + str(start) + ", the sensor with the id " + str(id_sensor) + "reported an event of importance " + str(importance) + " and of title '" + title + "'."
				print "event du sensor " + str(id_sensor)
				send_alert(text)
			except Exception as e:
				print(e)

def send_message(text):
	if (text[:16]=="/sensors/byName/"):
		name_s = text[16:]
		res = str(DB.get_sensor_by_name(name_s))
		params = {"text": res, "chat_id": CHAT}
	elif (text[:14]=="/sensors/byId/"):
		id_s = text[14:]
		res = str(DB.get_sensor_by_id(id_s))
		params = {"text": res, "chat_id": CHAT}
	elif (text[:17]=="/sensors/history/"):
		id_s = text[17:]
		res = str(DB.get_sensor_history(id_s))
		params = {"text": res, "chat_id": CHAT}
	elif (text[:18]=="/sensors/position/"):
		id_s = text[18:]
		res = str(DB.get_sensor_position(id_s))
		params = {"text": res, "chat_id": CHAT}
	else:
		params = {"text": text, "chat_id": CHAT}
	url = URL_BOT + "sendMessage?" + urllib.urlencode(params)
	get_url(url)	
	
def send_alert(text):
	print "dans le send alert"
	params = {"text": text, "chat_id": CHAT}
	url = URL_BOT + "sendMessage?" + urllib.urlencode(params)
	get_url(url)

def main():
	last_update_id = None
	last_event_id = 0
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			answer_all_updates(updates)
		events = get_events(last_event_id)
		if len(events) > 0:
			print "dans le if events"
			last_event_id = get_last_event_id(events) + 1
			send_all_events(events)
		time.sleep(0.5)


if __name__ == '__main__':
	main()

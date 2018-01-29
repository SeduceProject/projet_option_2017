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
	
def get_events(offset=None):
	"""if offset:
		#ici on met l'url de la fonction de l'api qui renvoie tous les evenements a partir de offset 
		#url = dbBot.URL_API + "/events/get_all/" + str(offset)
	else:
		#ici on met l'url de la fonction de l'api qui renvoie tous les evenements
		#url = dbBot.URL_API + "/events/get_all" """
	js = get_json_from_url(url)
	return js
	
def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

def get_last_event_id(events):
	event_ids = []
	for event in events["quelqueChoseVoirDansLeFormatDuJson"]:
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
	for event in events["quelqueChoseVoirDansLeFormatDuJson"]:
		if (event["ended"] == false):
			try:
				start = event["start"]
				importance = event["importance"]
				title = event["title"]
				id_sensor = event["id_sensor"]
				text = "At the moment " + str(start) + ", the sensor with the id " + str(id_sensor) + "reported an event of importance " + str(importance) + " and of title '" + title + "'."
				send_alert(text)
			except Exception as e:
				print(e)

def send_message(text):
	if (text[:19]=="/sensors/id/byName/"):
		name_s = text[19:]
		res = str(DB.get_sensor(name_s))
		params = {"text": res, "chat_id": CHAT}
	else:
		params = {"text": text, "chat_id": CHAT}
	url = URL_BOT + "sendMessage?" + urllib.urlencode(params)
	get_url(url)	
	
def send_alert(text):
	params = {"text": text, "chat_id": CHAT}
	url = URL_BOT + "sendMessage?" + urllib.urlencode(params)
	get_url(url)

def main():
	last_update_id = None
	#last_event_id = None
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			answer_all_updates(updates)
		"""events = get_events(last_event_id)
		if len(events["quelqueChoseVoirDansLeFormatDuJson"]) > 0:
			last_event_id = get_last_event_id(events) + 1
			answer_all_events(events)"""
		time.sleep(0.5)


if __name__ == '__main__':
	main()

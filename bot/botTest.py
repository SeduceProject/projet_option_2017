import json 
import requests
import time
import urllib
import dbBot

TOKEN = "472925886:AAHoewEo-y9D9wIaljXJllows3UNIPHOIao"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = dbBot.DBBot()

def get_url(url):
	response = requests.get(url)
	content = response.content.decode("utf8")
	return content

def get_json_from_url(url):
	content = get_url(url)
	js = json.loads(content)
	return js

def get_updates(offset=None):
	url = URL + "getUpdates?timeout=100"
	if offset:
		url += "&offset={}".format(offset)
	js = get_json_from_url(url)
	return js

def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

def get_last_chat_id_and_text(updates):
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	text = updates["result"][last_update]["message"]["text"]
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	return (text, chat_id)

def answer_all(updates):
	for update in updates["result"]:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			send_message(text, chat)
		except Exception as e:
			print(e)

def send_message(text, chat_id):
	if (text[:19]=="get_id_sensor/name/"):
		name_s = text[19:]
		print name_s
		res = str(db.get_sensor(name_s)[0])
		params = {"text": res, "chat_id": chat_id}
	else:
		params = {"text": text, "chat_id": chat_id}
	url = URL + "sendMessage?" + urllib.urlencode(params)
	get_url(url)	

def main():
	last_update_id = None
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			answer_all(updates)
		time.sleep(0.5)


if __name__ == '__main__':
	main()

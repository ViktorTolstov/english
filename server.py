from flask import Flask
from flask import request
from flask import jsonify
#from flask_cors import CORS
import requests
import os
import json
import re
#from flask_sslify import SSLify
import vk
# import random
import database
import time
import math
# from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime

# now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")

app = Flask(__name__)
#sslify = SSLify(app)
#CORS(app)

session = vk.Session(access_token='99a11e00502987b24bcb91adc963708fd2c264f5143d4f8bbd1a25549b1fb34f003371ca7a3c36dd76ad0')
vk_api = vk.API(session)

#{'type': 'wall_reply_new', 
#'object': {'id': 3, 'from_id': 195194669, 'date': 1575076854, 'text': 'asd', 
#'post_owner_id': -188996934, 'post_id': 1}, 'group_id': 188996934, 
#'event_id': '33f4566143ab8c5975b7b41e76bb26f4fbd84ecc'}

# print(vk_api.messages.getConversations(v=5.103))

# @app.route('/', methods=['POST', 'GET'])
def init():
	body = request.get_json()
	if body == { "type": "confirmation", "group_id": 188996934 }:
		return "8806c6d6"

@app.route('/', methods=['POST', 'GET'])
def bot():
    body = request.get_json()
    user_id = body["object"]["message"]["from_id"]
    if "payload" in body["object"]["message"]:
        if body["object"]["message"]["payload"] == '{"command":"start"}':
            text = "Напиши мне новый пост, который ты хочешь добавить в очередь публикаций"
            random_id = int(str(round(time.time()))+str(user_id))
            vk_api.messages.send(user_id=user_id, random_id=random_id,v=5.103)
            return "ok"
        elif body["object"]["message"]["payload"] == '{"command":"group2"}':
            update_group("group2",body)
        elif body["object"]["message"]["payload"] == '{"command":"group3"}':
            update_group("group3",body)
        elif body["object"]["message"]["payload"] == '{"command":"group4"}':
            update_group("group4",body)
        elif body["object"]["message"]["payload"] == '{"command":"group5"}':
            update_group("group5",body)
        elif body["object"]["message"]["payload"] == '{"command":"morning"}':
            update_time("morning",body)
        elif body["object"]["message"]["payload"] == '{"command":"afternoon"}':
            update_time("afternoon",body)
        elif body["object"]["message"]["payload"] == '{"command":"evening"}':
            update_time("evening",body)
    elif body["object"]["message"]["text"].rfind("дата-")!=-1:
        day = body["object"]["message"]["text"][5:7:1]
        mounth = body["object"]["message"]["text"][8:10:1]
        year = body["object"]["message"]["text"][11:15:1]
        update_date(day,mounth,year,body)
    else:
        new_post(body)

def update_time(post_time,body):
    database.update_time(post_time)
    user_id = body["object"]["message"]["from_id"]
    random_id = int(str(round(time.time()))+str(user_id))
    text = """
    Время успешно выбрано

    Напиши мне новый пост, который ты хочешь добавить в очередь публикаций
    """
    vk_api.messages.send(user_id=user_id, message=text, random_id=random_id,v=5.103)
    return "ok"

def update_group(group,body):
    database.update_group(group)
    user_id = body["object"]["message"]["from_id"]
    random_id = int(str(round(time.time()))+str(user_id))
    text = """
    Группа успешно установлена на """+group+"""
    Напиши дату публикации в формате сообщения:
    дата-dd.mm.yyyy
    """
    vk_api.messages.send(user_id=user_id, message=text, random_id=random_id,v=5.103)
    return "ok"

def update_date(day,mounth,year,body):
    database.update_date(day,mounth,year)
    user_id = body["object"]["message"]["from_id"]
    random_id = int(str(round(time.time()))+str(user_id))
    text = """
    Дата успешно установлена для последнего поста
    Выбери время публикации из предложеного списка
    """
    keyboard = {
		"one_time": True,
		"buttons": [
			[{
				"action": {
					"type": "text",
					"payload": '{"command":"morning"}',
					"label": "Утро (10.00)"
				},
				"color": "primary"
			}],
            [{
				"action": {
					"type": "text",
					"payload": '{"command":"afternoon"}',
					"label": "День (14.00)"
				},
				"color": "primary"
			}],
            [{
				"action": {
					"type": "text",
					"payload": '{"command":"evening"}',
					"label": "Вечер (19.00)"
				},
				"color": "primary"
			}]
		]
	}
    vk_api.messages.send(user_id=user_id, message=text,keyboard=json.dumps(keyboard), random_id=random_id,v=5.103)
    return "ok"



def new_post(body):
    text = body["object"]["message"]["text"]
    attachments = body["object"]["message"]["attachments"]
    attachment = []
    for index in attachments:
        if index["type"] == "photo":
            attachment.append("photo"+str(index["photo"]["owner_id"])+"_"+str(index["photo"]["id"]))
        if index["type"] == "doc":
            attachment.append("doc"+str(index["doc"]["owner_id"])+"_"+str(index["doc"]["id"]))
        if index["type"] == "video":
            attachment.append("video"+str(index["video"]["owner_id"])+"_"+str(index["video"]["id"]))
    database.add_post(text,attachment)
    user_id = body["object"]["message"]["from_id"]
    random_id = int(str(round(time.time()))+str(user_id))
    text = """
    Запись успешно добавлена, выберете группу для которой эта запись предназначена.
    Если вы не выберете группу, запись не будет опубликована
    """
    keyboard = {
		"one_time": True,
		"buttons": [
			[{
				"action": {
					"type": "text",
					"payload": '{"command":"group2"}',
					"label": "Группа 1"
				},
				"color": "primary"
			}],
            [{
				"action": {
					"type": "text",
					"payload": '{"command":"group3"}',
					"label": "Группа 2"
				},
				"color": "primary"
			}],
            [{
				"action": {
					"type": "text",
					"payload": '{"command":"group4"}',
					"label": "Группа 3"
				},
				"color": "primary"
			}],
            [{
				"action": {
					"type": "text",
					"payload": '{"command":"group5"}',
					"label": "Группа 4"
				},
				"color": "primary"
			}]
		]
	}
    vk_api.messages.send(user_id=user_id, message=text,keyboard=json.dumps(keyboard), random_id=random_id,v=5.103)
    return "ok"

@app.route('/get_db', methods=['GET'])
def get_db():
    post = database.get_post()
    return post


if __name__ == '__main__': 
	#port = int(os.environ.get("PORT", 5000))
	# app.run(host='0.0.0.0', port=port)
    app.run()
    # sched.start()
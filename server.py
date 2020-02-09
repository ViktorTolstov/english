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

@app.route('/', methods=['POST', 'GET'])
def bot():
    body = request.get_json()
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
    database.add_post(text,attachment,"dialog","time")
    user_id = body["object"]["message"]["from_id"]
    random_id = int(str(round(time.time()))+str(user_id))
    text = """
    Запись успешно добавлена, выберете группу для которой эта запись предназначена.
    Если вы не выберете группу, запись не будет опубликована
    """
    vk_api.messages.send(user_id=user_id, message=text, random_id=random_id,v=5.103)
    return "ok"

@app.route('/get_db', methods=['GET'])
def get_db():
    post = database.get_post()
    return post


# sched = BlockingScheduler()
# @sched.scheduled_job('cron', hour=2, minute=47)  # запускать c понедельника по пятницу в 10.00
# def scheduled_job():
#     post = database.get_post()
#     attachment = ""
#     for index in post["attachments"]:
#         attachment += index + ","
#     vk_api.messages.send(chat_id=1, message=post["text"],attachment=attachment, random_id=random_id,v=5.103)
#     print('This job is run every weekday at 10am.')

# @app.route('/', methods=['POST', 'GET'])
def init():
	body = request.get_json()
	if body == { "type": "confirmation", "group_id": 188996934 }:
		return "8806c6d6"

if __name__ == '__main__': 
	#port = int(os.environ.get("PORT", 5000))
	# app.run(host='0.0.0.0', port=port)
    app.run()
    # sched.start()
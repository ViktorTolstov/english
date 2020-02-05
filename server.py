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

app = Flask(__name__)
#sslify = SSLify(app)
#CORS(app)

session = vk.Session(access_token='99a11e00502987b24bcb91adc963708fd2c264f5143d4f8bbd1a25549b1fb34f003371ca7a3c36dd76ad0')
vk_api = vk.API(session)

#{'type': 'wall_reply_new', 
#'object': {'id': 3, 'from_id': 195194669, 'date': 1575076854, 'text': 'asd', 
#'post_owner_id': -188996934, 'post_id': 1}, 'group_id': 188996934, 
#'event_id': '33f4566143ab8c5975b7b41e76bb26f4fbd84ecc'}

@app.route('/', methods=['POST', 'GET'])
def bot():
    r = request.get_json()
    # print(r["object"]["message"]["attachments"])
    text = r["object"]["message"]
    attachments = r["object"]["message"]["attachments"]
    images = []
    videos = []
    docs = []
    for attachment in attachments:
        if attachment
    return "ok"
    # message = [
    #     'Пусть в Новом году сбывается всё хорошее! 🎅',
    #     'В наступающем году всё обязательно сбудется! 🎄',
    #     'В Новом году всё получится! 🎁'
    # ]
    # if r["type"] == 'wall_reply_new' and r["object"]["attachments"][0]["type"] == 'sticker' and r["object"]["post_id"]==93:
    #     post_id = r["object"]["post_id"]
    #     reply_to_comment = r["object"]["id"]
    #     #message = "pam"
    #     guid = int(str(r["object"]["date"])+str(abs(r["object"]["from_id"])))
    #     owner_id = r["object"]["post_owner_id"]
    #     num = 700
    #     while num == 700 or num == 670 or num == 671 or num == 672:
    #         num = random.randint(640,701)
    #     attachments = "photo-146739653_457239"+str(num)
    #     vk_api.wall.createComment(
    #         message = message[random.randint(0,2)],
    #         post_id=post_id,
    #         attachments = attachments,
    #         owner_id = owner_id,
    #         reply_to_comment=reply_to_comment,
    #         guid = guid,
    #         v = 5.103
    #     )
    # return 'ok'

# @app.route('/', methods=['POST', 'GET'])
def init():
	body = request.get_json()
	if body == { "type": "confirmation", "group_id": 188996934 }:
		return "8806c6d6"

if __name__ == '__main__': 
	#port = int(os.environ.get("PORT", 5000))
	# app.run(host='0.0.0.0', port=port)
    app.run()
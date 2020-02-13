from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import vk
import time
import math
import database
import requests

now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
print(now)

session = vk.Session(access_token='99a11e00502987b24bcb91adc963708fd2c264f5143d4f8bbd1a25549b1fb34f003371ca7a3c36dd76ad0')
vk_api = vk.API(session)

sched = BlockingScheduler()

# @sched.scheduled_job('cron', hour=18, minute=56)  # запускать c понедельника по пятницу в 10.00
def scheduled_job_morning():
    server_posts = requests.get('http://localhost:5000/get_db').json()
    random_id = int(round(time.time()))
    posts = server_posts["posts"]
    today = datetime.date(datetime.today())
    for post in posts:
        print(post)
        if post["date"] == str(today):
            if post["time"] == "morning":
                attachment = ""
                for index in post["attachments"]:
                    attachment += index + ""
                vk_api.messages.send(chat_id=1, message=post["text"],attachment=attachment, random_id=random_id,v=5.103)

@sched.scheduled_job('cron', hour=12, minute=00)  # запускать c понедельника по пятницу в 10.00
def scheduled_job_afternon():
    server_posts = requests.get('http://localhost:5000/get_db').json()
    random_id = int(round(time.time()))
    posts = server_posts["posts"]
    today = datetime.date(datetime.today())
    for post in posts:
        print(post)
        if post["date"] == str(today):
            if post["time"] == "morning":
                attachment = ""
                for index in post["attachments"]:
                    attachment += index + ","
                vk_api.messages.send(chat_id=1, message=post["text"],attachment=attachment, random_id=random_id,v=5.103)

@sched.scheduled_job('cron', hour=18, minute=00)  # запускать c понедельника по пятницу в 10.00
def scheduled_job_evening():
    server_posts = requests.get('http://localhost:5000/get_db').json()
    random_id = int(round(time.time()))
    posts = server_posts["posts"]
    today = datetime.date(datetime.today())
    for post in posts:
        print(post)
        if post["date"] == str(today):
            if post["time"] == "morning":
                attachment = ""
                for index in post["attachments"]:
                    attachment += index + ","
                vk_api.messages.send(chat_id=1, message=post["text"],attachment=attachment, random_id=random_id,v=5.103)


scheduled_job_morning()
# sched.start()
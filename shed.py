from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
print(now)

sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds=10)    # запускать задание каждые 10 сек
def timed_job():
    print('This job is run every 10 seconds.')

@sched.scheduled_job('cron', hour=15, minute=52)  # запускать c понедельника по пятницу в 10.00
def scheduled_job():
    print('This job is run every weekday at 10am.')

sched.start()
print(123)
sched.stop()
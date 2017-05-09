import os
import schedule
import time

def job():
   os.system(">nohup.out")

schedule.every(12).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)

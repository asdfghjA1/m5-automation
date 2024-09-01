import schedule
import time
import subprocess
import os
import shutil
import threading

file_path = './videos'

def site_cleaner():
    if os.path.isfile(file_path):
        os.remove(file_path)
        print("State has been cleared")
    else:
        print("State Clearance Failed")

def job1(script_path):
    subprocess.run(['node', script_path])

def job2(script_path):
    subprocess.run(['python3', script_path])

def schedule_task(task, *args):
    threading.Thread(target=task, args=args).start()

# Schedule tasks

# 12:30 INDIA TIME PULL
# 07:00 INDIA TIME PULL
# 01:00 INDIA TIME PULL
# 07:00 INDIA TIME PULL


schedule.every().day.at("11:30").do(schedule_task, job1, './index.js')
schedule.every().day.at("00:01").do(schedule_task, job2, './getter.py')
schedule.every().day.at("01:00").do(schedule_task, job2, './deleter.py')

schedule.every().day.at("06:00").do(schedule_task, job1, './index1.js')
schedule.every().day.at("06:30").do(schedule_task, job2, './getter.py')
schedule.every().day.at("07:30").do(schedule_task, job2, './deleter.py')

schedule.every().day.at("12:00").do(schedule_task, job1, './index2.js')
schedule.every().day.at("12:30").do(schedule_task, job2, './getter.py')
schedule.every().day.at("13:30").do(schedule_task, job2, './deleter.py')

schedule.every().day.at("18:00").do(schedule_task, job1, './index3.js')
schedule.every().day.at("18:30").do(schedule_task, job2, './getter.py')
schedule.every().day.at("19:30").do(schedule_task, job2, './deleter.py')


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)


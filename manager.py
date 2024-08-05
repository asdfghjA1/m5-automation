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
schedule.every().day.at("00:25").do(schedule_task, job1, './index.js')
schedule.every().day.at("00:29").do(schedule_task, job2, './getter.py')
# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)


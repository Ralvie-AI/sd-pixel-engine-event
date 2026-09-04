import os 
from datetime import timedelta

EVENT_SCREENSHOT_FOLDER_USER = os.path.join(
                    os.path.expanduser("~"),
                    "Library", "Application Support", "Sundial", "EventScreenshots", '{user_id}')
EVENT_SCREENSHOT_FOLDER = os.path.join(
                    os.path.expanduser("~"),
                    "Library", "Application Support", "Sundial", "EventScreenshots")

INTERVAL = 30  # seconds

#detect_sleep.py
SLEEP_THRESHOLD = timedelta(minutes=45) # for system sleep
LOCKSCREEN_THRESHOLD = timedelta(hours=1) # for lockscreen
CHECK_INTERVAL = 5  # seconds
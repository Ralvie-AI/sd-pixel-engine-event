import os 
import argparse
import shutil
import logging 
import threading
from datetime import time

from sd_pixel_engine_event.log import setup_logging
from sd_pixel_engine_event.event_screenshot import EventScreenShot
from sd_pixel_engine_event.const import EVENT_SCREENSHOT_FOLDER_USER
from sd_pixel_engine_event.utils import str2bool
from sd_pixel_engine_event.detect_sleep import sleep_wake_monitor_loop

logger = logging.getLogger(__name__)

def main():

    parser = argparse.ArgumentParser(description="Event Screenshot")
    parser.add_argument("--server_url", required=True, help="URL to upload screenshots")
    parser.add_argument("--user_id", required=True, help="User ID for identification")    
    parser.add_argument("--is_ocr_text_enabled", type=str2bool, nargs="?", const=True, 
                        default=False, help="Extract ocr text from screenshots (true/false, default=True)")

    args = parser.parse_args()

    # Set up logging
    setup_logging("sd-pixel-engine-event", log_file=True)

    # Detect long sleep
    detect_sleep_thread = threading.Thread(target=sleep_wake_monitor_loop,daemon=True)
    detect_sleep_thread.start()

    screenshot_folder = EVENT_SCREENSHOT_FOLDER_USER.format(user_id=args.user_id)   
    if os.path.exists(screenshot_folder):
        logger.debug(f"deleteing screenshot_folder => {screenshot_folder}")
        shutil.rmtree(screenshot_folder)    

    screenshot = EventScreenShot(
        server_url=args.server_url,
        user_id=args.user_id,  
        is_ocr_text_enabled=args.is_ocr_text_enabled,
    )

    screenshot.run()

if __name__ == '__main__':
    main()
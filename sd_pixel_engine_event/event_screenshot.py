import logging
import os
import time

from datetime import datetime, timezone

from sd_pixel_engine_event.const import EVENT_SCREENSHOT_FOLDER_USER
from sd_pixel_engine_event.capture_window import capture_screenshots

logger = logging.getLogger(__name__)

SCREENSHOT_INTERVAL = 30

class EventScreenShot:
    def __init__(self, user_id, is_ocr_text_enabled=True):
        self.user_id = user_id
        self.is_ocr_text_enabled = is_ocr_text_enabled

    def run(self):
        next_capture = time.monotonic()

        while True:
            self._take_screenshot_30_seconds()

            next_capture += SCREENSHOT_INTERVAL

            sleep_time = next_capture - time.monotonic()

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Screenshot processing took longer than the interval.
                next_capture = time.monotonic()

    # 2026-01-13 06:58:16.823000+00:00 UTC Time 
    # # 2026-01-13T06-58-16.823000Z.png
    def _take_screenshot_30_seconds(self, screenshot_folder=None):
        if screenshot_folder is None:
            screenshot_folder = EVENT_SCREENSHOT_FOLDER_USER.format(
                user_id=self.user_id
            )

        os.makedirs(screenshot_folder, exist_ok=True)

        try:
            utc_now = datetime.now(timezone.utc)
            timestamp = utc_now.strftime("%Y-%m-%dT%H-%M-%S.%fZ")

            output_file = os.path.join(
                screenshot_folder,
                f"{self.user_id}_{timestamp}.png"
            )

            output_file_ocr = os.path.join(
                screenshot_folder,
                f"{self.user_id}_{timestamp}_ocr.png"
            )

            capture_screenshots(output_file, output_file_ocr)

        except Exception:
            logger.exception("MSS screenshot capture failed") 
        
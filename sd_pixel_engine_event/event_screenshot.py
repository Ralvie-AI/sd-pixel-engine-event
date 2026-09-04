import logging
import os
import time

from datetime import datetime, timezone

from sd_pixel_engine_event.const import EVENT_SCREENSHOT_FOLDER_USER, INTERVAL
from sd_pixel_engine_event.utils import get_image_name_to_utc, capture_active_window_screenshot, capture_fullscreen
import requests

logger = logging.getLogger(__name__)


class EventScreenShot:
    def __init__(self, server_url, user_id, is_ocr_text_enabled=True):
        self.server_url = server_url if server_url else "http://localhost:7600/screenshot/"
        self.user_id = user_id
        self.is_ocr_text_enabled = is_ocr_text_enabled

    def run(self):
        next_capture = time.monotonic()

        while True:

            self._take_screenshot_30_seconds()

            next_capture += INTERVAL

            sleep_time = next_capture - time.monotonic()

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Screenshot processing took longer than the interval.
                next_capture = time.monotonic()

    def _take_screenshot_30_seconds(self, screenshot_folder=None):
        if screenshot_folder is None:
            screenshot_folder = EVENT_SCREENSHOT_FOLDER_USER.format(user_id=self.user_id)
        os.makedirs(screenshot_folder, exist_ok=True)

        utc_now = datetime.now(timezone.utc)
        timestamp = utc_now.strftime("%Y-%m-%dT%H-%M-%S.%fZ")

        full_path = f"{screenshot_folder}/{self.user_id}_{timestamp}.png"
        active_path = f"{screenshot_folder}/{self.user_id}_{timestamp}_active.png"

        # 1. ลองแคปหน้าจอหลัก (Fullscreen)
        try:
            capture_fullscreen(full_path)
        except Exception as e:
            logger.warning(
                f"Mac Screen Locked / Sleep - Fullscreen capture skipped: {e}"
            )
            # เคลียร์ไฟล์ขยะขนาด 0 byte (ถ้ามี)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except OSError:
                    pass
            full_path = None

        # 2. ลองแคปหน้าต่างที่ใช้งานอยู่ (Active Window)
        try:
            capture_active_window_screenshot(active_path)
        except Exception as e:
            logger.warning(
                f"Mac Screen Locked / Sleep - Active window capture skipped: {e}"
            )
            # เคลียร์ไฟล์ขยะขนาด 0 byte (ถ้ามี)
            if os.path.exists(active_path):
                try:
                    os.remove(active_path)
                except OSError:
                    pass
            active_path = None

        return full_path, active_path

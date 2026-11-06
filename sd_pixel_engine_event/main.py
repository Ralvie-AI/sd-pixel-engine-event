import argparse
import logging 
import threading

import win32event
import winerror
import win32api

from sd_pixel_engine_event.log import setup_logging
from sd_pixel_engine_event.event_screenshot import EventScreenShot
from sd_pixel_engine_event.utils import str2bool
from sd_pixel_engine_event.detect_sleep import create_hidden_power_listener

logger = logging.getLogger(__name__)


_instance_mutex = None  # keep a module-level reference so the handle stays alive

def acquire_single_instance() -> bool:
    """Return True if we are the only instance, False if another is running."""
    global _instance_mutex
    _instance_mutex = win32event.CreateMutex(None, False, r"Local\SDPixelEngineEvent_SingleInstance")
    return win32api.GetLastError() != winerror.ERROR_ALREADY_EXISTS

def setup_argument_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(description="Event Screenshot")
    parser.add_argument("--user_id", required=True, help="User ID for identification")
    parser.add_argument("--company_id", required=True, help="User's Company ID")
    parser.add_argument("--is_ocr_text_enabled", type=str2bool, nargs="?", const=True, 
                        default=False, help="Extract ocr text from screenshots (true/false, default=True)")
    return parser


def start_sleep_detection():
    """Start the sleep detection daemon thread."""
    detect_sleep_thread = threading.Thread(
        target=create_hidden_power_listener, 
        daemon=True
    )
    detect_sleep_thread.start()

def main():

    if not acquire_single_instance():
        logging.warning("Another instance is already running. Exiting.")
        raise SystemExit(0)
    
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Set up logging
    setup_logging("sd-pixel-engine-event", log_file=True)

    screenshot = EventScreenShot(
        user_id=args.user_id,
        company_id=args.company_id,
        is_ocr_text_enabled=args.is_ocr_text_enabled,
    )

    screenshot.run()

if __name__ == '__main__':
    start_sleep_detection()
    main()

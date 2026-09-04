import time
import logging
import subprocess
import os
import sys
import Quartz
from datetime import datetime
from sd_pixel_engine_event.const import SLEEP_THRESHOLD, LOCKSCREEN_THRESHOLD, CHECK_INTERVAL
import signal

logger = logging.getLogger(__name__)

# SLEEP_THRESHOLD = timedelta(minutes=45) # for system sleep
# LOCKSCREEN_THRESHOLD = timedelta(hours=1) # for lockscreen
# CHECK_INTERVAL = 5  # seconds

last_tick_time = None
already_killed = False
lock_start_time = None

def is_screen_locked() -> bool:
    """check is macOS screen Locking """
    try:
        session_info = Quartz.CGSessionCopyCurrentDictionary()
        if session_info:
            # if CGSSessionScreenIsLocked is True = lockscreen
            return session_info.get("CGSSessionScreenIsLocked", False)
    except Exception as e:
        logger.debug(f"Failed to check screen lock status: {e}")
    return False


def on_long_sleep_detected(reason: str):
    global already_killed
    
    if already_killed:
        return
        
    already_killed = True
    logger.warning(f"Kill trigger activated reason: [{reason}]. Terminating process...")

    try:
        from sd_main.sd_desktop.monitor import stop_process, get_running_process_id
        
        pid = get_running_process_id("sd-pixel-engine")
        if pid:
            stop_process(pid)
        else:
            logger.warning("PID not found via monitor, killing self process...")
            os.kill(os.getpid(), signal.SIGTERM)
            
    except Exception:
        logger.exception("Failed to stop process safely, forcing exit...")
        os._exit(1)


def sleep_wake_monitor_loop():
    global last_tick_time, lock_start_time

    logger.info("Starting macOS sleep & lock-screen detector loop")
    last_tick_time = datetime.now()

    while True:
        time.sleep(CHECK_INTERVAL)

        now = datetime.now()
        gap = now - last_tick_time

        # Case 1 : System Sleep more than 45 minutes
        if gap >= SLEEP_THRESHOLD:
            on_long_sleep_detected(f"System sleep gap detected ({gap.total_seconds():.1f}s)")
            break

        # Case 2 : Lock Screen
        if is_screen_locked():
            if lock_start_time is None:
                lock_start_time = now  
                logger.debug("Screen locked detected. Start counting lock duration...")
            else:
                locked_duration = now - lock_start_time
                # if lockscreen more than 1 hour
                if locked_duration >= LOCKSCREEN_THRESHOLD:
                    on_long_sleep_detected(f"Lock screen duration exceeded ({locked_duration.total_seconds():.1f}s)")
                    break
        else:
            if lock_start_time is not None:
                logger.info("Screen unlocked. Resetting lock timer.")
                lock_start_time = None

        last_tick_time = now
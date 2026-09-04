import subprocess
import os 
import sys
import time
import logging 


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
EXE_PATH = os.path.join(
                    os.path.expanduser("~"),
                    "Desktop", "activitywatch", "sd-pixel-engine-event", "dist", 'sd-pixel-engine-event', 'sd-pixel-engine-event')

def start_sd_pixel_engine_event_mac(command_list):
    try:
        logger.info("Starting sd-pixel-engine-event...")
        logger.debug("Command: %s", " ".join(command_list))

        proc = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        logger.debug(f"Started pid={proc.pid}")

        time.sleep(2)

        if proc.poll() is not None:
            stdout, stderr = proc.communicate()

            logger.error(
                f"sd-pixel-engine-event exited immediately. "
                f"returncode={proc.returncode}"
            )

            if stdout:
                logger.error(stdout.decode(errors="ignore"))

            if stderr:
                logger.error(stderr.decode(errors="ignore"))
        else:
            logger.debug("sd-pixel-engine-event is still running")

    except Exception:
        logger.exception("Failed to start sd-pixel-engine-event")


if __name__ == "__main__":

    screenshot_exe_file = EXE_PATH
    logger.info(f"screenshot is file => {os.path.isfile(screenshot_exe_file)}")


    user_id = ""
    times_per_hour = None


    command_list = [
        screenshot_exe_file,
        "--server_url", "",
        "--user_id", str(user_id),
        "--is_ocr_text_enabled", str("true"),
    ]


    logger.info(f"command_list => {str(command_list)}")
    start_sd_pixel_engine_event_mac(command_list)
import subprocess
import os 
import sys

import logging 


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
exe_path = r"add your exe path"


def start_exe(exec_cmd, process_name=None):
    if not isinstance(exec_cmd, list):
        print("no list")
        exec_cmd = [exec_cmd]        
    else:
        print("list")
                  
    logger.info(f"Starting module {exec_cmd}")
     
    logger.debug("Running: {}".format(exec_cmd))

    # Don't display a console window on Windows
    # See: https://github.com/ActivityWatch/activitywatch/issues/212
    startupinfo = None
    if sys.platform == "win32" or sys.platform == "cygwin":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
   

    # There is a very good reason stdout and stderr is not PIPE here
    # See: https://github.com/ActivityWatch/aw-server/issues/27
    _process = subprocess.Popen(
        exec_cmd, universal_newlines=True, startupinfo=startupinfo
    )




screenshot_exe_file = exe_path
logger.info(f"screenshot is file => {os.path.isfile(screenshot_exe_file)}")


user_id = "0a07029c9a901fe0819abf69dca12c0d"
times_per_hour = None


command_list = [
    screenshot_exe_file,
    "--user_id", str(user_id),
    "--is_ocr_text_enabled", str("true"),
]


logger.info(f"command_list => {str(command_list)}")
start_exe(command_list)
from tendo import singleton

# script lock
me = singleton.SingleInstance()

import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import List

import serial
from adafruit_board_toolkit import circuitpython_serial

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("serial")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("serial.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# File needs to be in the same dir as this script
powershell_script_name = "getActiveWindowProcessName.ps1"


def current_active_window_process_name():
    pwd = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(pwd, powershell_script_name)
    p = subprocess.Popen(
        f'powershell.exe  -ExecutionPolicy Bypass -file "{script_path}"',
        stdout=subprocess.PIPE,
    )
    output = p.stdout.read()
    return output.decode("utf-8").strip()


def send_data_to_serial_port(data, ports: List[str]):
    data_to_send = (json.dumps(data) + "\n\r").encode("ascii")
    for port in ports:
        logger.debug(f"{port} :: {data}")
        try:
            ser = serial.Serial(port, 115200)
            ser.write(data_to_send)
            ser.close()
        except Exception as e:
            logger.error(f"{e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        current_active_window = sys.argv[1].split(".")[0]
    else:
        current_active_window = current_active_window_process_name()

    data_to_send = {
        "computername": os.environ["COMPUTERNAME"],
        "timestamp": int(datetime.now().timestamp()),
        "process": current_active_window,
    }

    try:
        ports = [comport.device for comport in circuitpython_serial.data_comports()]
        send_data_to_serial_port(data_to_send, ports)
    except Exception as e:
        logger.debug(e)

    print("done...")

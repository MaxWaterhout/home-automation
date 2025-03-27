import os
from datetime import datetime
from home_automation.app.settings import settings_init
from PyTado.interface.interface import Tado

def count_lines(file_path: str) -> int:
    """
    Count the number of lines in a given log file.

    Args:
        file_path (str): Path to the file.

    Returns:
        int: Number of lines in the file.
    """
    with open(file_path) as f:
        return sum(1 for _ in f)
    
def rotate_log(log_file: str):
    """
    Rotate the log file by renaming it with a timestamp and starting a new empty log.

    Args:
        log_file (str): Path to the log file to rotate.
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_log_file = log_file.replace(".log", f"_{timestamp}.log")
    os.rename(log_file, new_log_file)
    open(log_file, "w").close()

def print_log(message: str, last_message_container: dict):
    """
    Print a timestamped log message and write it to the log file if enabled.

    Args:
        message (str): The message to log.
        last_message_container (dict): Dictionary holding the last logged message to avoid duplicates.
    """
    if message != last_message_container.get("last"):
        timestamped_message = f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} # {message}"
        print(timestamped_message)
        if settings_init.save_log:
            try:
                with open(settings_init.log_file, "a") as log:
                    log.write(timestamped_message + "\n")
                if count_lines(settings_init.log_file) >= settings_init.max_log_lines:
                    rotate_log(settings_init.log_file)
            except Exception as e:
                print(f"Log error: {e}")
        last_message_container["last"] = message



def login() -> Tado:
    """Retrieve all zones, once successfully logged in"""
    tado = Tado(token_file_path="/var/tado/refresh_token")

    print("Device activation status: ", tado.device_activation_status())
    print("Device verification URL: ", tado.device_verification_url())

    print("Starting device activation")
    tado.device_activation()
    print("Device activation status: ", tado.device_activation_status())


    return tado
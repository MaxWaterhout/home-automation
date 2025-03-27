from PyTado.interface import Tado
from home_automation.app import utils, settings 
import time 

def handle_presence(tado_instance: Tado, devices_home: list, last_message_container: dict, home_state: str= "HOME"):
    """
    Handle presence logic: switch between HOME and AWAY modes based on detected devices.

    Args:
        tado_instance (Tado): The Tado instance.
        devices_home (list): List of devices currently at home.
        home_state (str): The current home state ("HOME" or "AWAY").
        last_message_container (dict): Dictionary holding the last logged message.
    """
    
    devices_detected = bool(devices_home)
    is_home = home_state == "HOME"
    is_away = home_state == "AWAY"

    if not devices_detected and is_home:
        utils.print_log("No devices at home but state is HOME — switching to AWAY mode.", last_message_container)
        tado_instance.set_away()
    elif devices_detected and is_away:
        utils.print_log(f"Devices {devices_home} detected at home — switching to HOME mode.", last_message_container)
        tado_instance.set_home()


    utils.print_log("Monitoring started. Waiting for location or open window changes.", last_message_container)

def monitor_home(tado_instance: Tado, last_message_container: dict):
    """
    Monitor home presence and react to device location changes.

    Args:
        tado_instance (Tado): The Tado instance.
        last_message_container (dict): Dictionary holding the last logged message.
    """
    try:
        home_state = tado_instance.get_home_state()["presence"]
        devices_home = [
            device["name"]
            for device in tado_instance.get_mobile_devices()
            if device["settings"]["geoTrackingEnabled"]
            and device["location"] is not None
            and device["location"]["atHome"]
        ]

        handle_presence(tado_instance=tado_instance, devices_home=devices_home, last_message_container=last_message_container, home_state=home_state)

    except Exception as e:
        utils.print_log(
            f"Error checking home status: {e}. Retrying in {settings.settings_init.error_retry_interval} seconds.",
            last_message_container,
        )
        time.sleep(settings.settings_init.error_retry_interval)
        monitor_home(tado_instance, last_message_container)
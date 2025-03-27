from home_automation.app.controller import handle_presence

from unittest.mock import Mock, patch
import pytest

def test_switch_to_away():
    tado_mock = Mock()
    last_message = {"last": "message"}

    devices_home = []
    home_state = "HOME"

    handle_presence(tado_instance= tado_mock, devices_home = devices_home , last_message_container = last_message, home_state= home_state)
    
    tado_mock.set_away.assert_called_once()
    tado_mock.set_home.assert_not_called()

def test_switch_to_home():
    tado_mock = Mock()
    last_message = {"last": "message"}

    devices_home = ["device1", "device2"]
    home_state = "AWAY"

    handle_presence(tado_instance= tado_mock, devices_home = devices_home , last_message_container = last_message , home_state= home_state)
    
    tado_mock.set_home.assert_called_once()
    tado_mock.set_away.assert_not_called()
   
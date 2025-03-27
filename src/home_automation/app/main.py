from home_automation.app import settings, utils, controller
import time
import sys


def main():
    """
    Main function to start Tado monitoring.
    - Logs into the Tado system.
    - Starts continuous home monitoring loop.
    """
    utils.print_log("Starting Tado Auto-Assist...", {"last": None})
    last_message_container = {"last": None}

    try:
        utils.print_log("Logging in to Tado...", last_message_container)
        tado_instance = utils.login()
        utils.print_log(
            "Successfully logged in to Tado. Starting home monitoring loop...",
            last_message_container,
        )

        while True:
            controller.monitor_home(tado_instance, last_message_container)
            time.sleep(settings.settings_init.checking_interval)

    except KeyboardInterrupt:
        utils.print_log(
            "Process interrupted by user. Exiting gracefully with home status.",
            last_message_container,
        )
        if tado_instance:
            try:
                tado_instance.set_home()
                utils.print_log(
                    "Successfully set HOME mode before exiting.", last_message_container
                )
            except Exception as e:
                utils.print_log(f"Failed to set HOME mode: {e}", last_message_container)
        sys.exit(0)
    except Exception as e:
        utils.print_log(f"An unexpected error occurred: {e}", last_message_container)
        sys.exit(1)


if __name__ == "__main__":
    main()

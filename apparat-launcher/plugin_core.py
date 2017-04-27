#!/usr/bin/python
"""apparat - plugin: core"""

## general


## apparat
import ini
import tools



# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!help', '!preferences', '!prefs')


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting', 1)

    # Reset status notification back to OK
    main_window.status_notification_reset()

    if current_search_string == '!help': # opens online documentation of apparat
        tools.debug_output('prepare_general', 'Case: Help', 1)
        main_window.open_app_url()
        # hide UI
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == 'True':
            tools.debug_output('prepare_general', 'Hide Main UI after executing a command', 1)
            main_window.tbicon.execute_tray_icon_left_click()
        main_window.reset_ui()

    elif current_search_string == '!preferences' or current_search_string == '!prefs': # opens apparat preferences
        tools.debug_output('prepare_general', 'Case: Preferences', 1)
        main_window.open_preference_window()
        main_window.reset_ui()

    else:
        tools.debug_output('prepare_general', 'Error: Unexpected core plugin command', 3)
        main_window.status_notification_display_error('Unexpected core plugin command')

    tools.debug_output('prepare_general', 'finished', 1)

#!/usr/bin/python
"""apparat_launcher - plugin: core"""

## general
import wx

## apparat
import ini
import tools



# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!help', '!preferences', '!prefs',)

PLUGINS = ('plugin_misc', 'plugin_nautilus', 'plugin_passwordgen', 'plugin_screenshot', 'plugin_search_internet', 'plugin_search_local', 'plugin_session', 'plugin_shell')

# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output(__name__, 'prepare_general', 'starting', 1)

    icon_size = ini.read_single_ini_value('General', 'icon_size') # get preference value

    # Reset status notification back to OK
    main_window.status_notification_reset()

    if current_search_string == '!help': # opens online documentation of apparat
        tools.debug_output(__name__, 'prepare_general', 'Case: Help', 1)

        # show icon for really fast users
        main_window.ui__bt_command_img = wx.Image('gfx/plugins/core/'+icon_size+'/help.png', wx.BITMAP_TYPE_PNG)
        main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
        main_window.ui__bt_command.SetToolTipString('Open help')

        main_window.open_app_url()

        # hide UI
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == 'True':
            tools.debug_output(__name__, 'prepare_general', 'Hide Main UI after executing a command', 1)
            main_window.tbicon.execute_tray_icon_left_click()
        main_window.reset_ui()

    elif current_search_string == '!preferences' or current_search_string == '!prefs': # opens apparat_launcher preferences
        tools.debug_output(__name__, 'prepare_general', 'Case: Preferences', 1)

        # show icon for really fast users
        main_window.ui__bt_command_img = wx.Image('gfx/plugins/core/'+icon_size+'/preferences.png', wx.BITMAP_TYPE_PNG)
        main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
        main_window.ui__bt_command.SetToolTipString('Open preferences')

        main_window.open_preference_window()
        main_window.reset_ui()

    else:
        tools.debug_output(__name__, 'prepare_general', 'Error: Unexpected core plugin command', 3)
        main_window.status_notification_display_error('Unexpected core plugin command')

    tools.debug_output(__name__, 'prepare_general', 'Finished handling core command', 1)

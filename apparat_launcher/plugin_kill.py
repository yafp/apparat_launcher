#!/usr/bin/python
"""apparat_launcher - plugin: kill"""

## general
import wx

## apparat
import ini
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------

TRIGGER = ('!kill', '!xkill',)


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_plugin_kill(main_window):
    """Plugin kill"""
    tools.debug_output(__name__, 'prepare_plugin_kill', 'starting', 1)

    main_window.status_notification_reset() # Reset status notification back to OK
    main_window.plugin__update_general_ui_information('Kill') # update plugin info

    icon_size = ini.read_single_ini_value('General', 'icon_size') # get preference value

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/kill/'+icon_size+'/kill.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Kill application by selecting a window with your cursor')
    main_window.ui__txt_command.SetValue('xkill')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Start rampage')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('')


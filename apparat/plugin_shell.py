#!/usr/bin/python
"""apparat - plugin: search-internet"""

## general

import wx

## apparat
import config
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------

TRIGGER = ('!sh')


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting')

    if  current_search_string.startswith("!sh"):
        tools.debug_output('prepare_general', 'Case: Shell')
        prepare_plugin_shell(main_window)
        return

    else:
        tools.debug_output('prepare_general', 'Error: unexpected shell plugin command')
        return

    tools.debug_output('prepare_general', 'finished')


def prepare_plugin_shell(main_window):
    """Plugin Shell"""
    tools.debug_output('prepare_plugin_shell', 'starting')
    main_window.plugin__update_general_ui_information('Shell') ## update plugin info

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/shell/'+str(config.TARGET_ICON_SIZE)+'/shell.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Lock Session')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Open')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    ## http://askubuntu.com/questions/484993/run-command-on-anothernew-terminal-window
    main_window.ui__txt_selected_app.SetValue('xterm')
    main_window.ui__txt_selected_parameter.SetValue(main_window.ui__cb_search.GetValue()[4:])





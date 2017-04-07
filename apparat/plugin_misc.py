#!/usr/bin/python
"""apparat - plugin: search-internet"""

## general

import wx

## apparat
import apparat
import config
import tools



# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------

TRIGGER = ('!open', '!help', '!preferences', '!prefs')


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting')

    if  current_search_string.startswith('!open'):
        tools.debug_output('prepare_general', 'Case: Open')
        prepare_plugin_misc_open(main_window)
        return

    if  current_search_string == '!help':
        tools.debug_output('prepare_general', 'Case: Help')
        main_window.open_app_url()
        main_window.reset_ui()
        return

    if  current_search_string == '!preferences' or current_search_string == '!prefs':
        tools.debug_output('prepare_general', 'Case: Preferences')
        main_window.open_preference_window()
        main_window.reset_ui()
        return

    else:
        tools.debug_output('prepare_general', 'Error: unexpected misc plugin command')
        return

    tools.debug_output('prepare_general', 'finished')


def prepare_plugin_misc_open(main_window):
    """Plugin Misc - Open"""
    tools.debug_output('prepare_plugin_misc_open', 'starting')
    main_window.plugin__update_general_ui_information('Misc (Open)') ## update plugin info

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/misc/'+str(config.TARGET_ICON_SIZE)+'/open.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Open')

    if(main_window.ui__cb_search.GetValue()[6:] != ''):
        ## parameter buttons
        main_window.ui__bt_selected_parameter.SetToolTipString('Open')
        main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
        main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set parameter
        main_window.ui__txt_selected_parameter.SetValue(main_window.ui__cb_search.GetValue()[6:])

        ## set command
        main_window.ui__txt_selected_app.SetValue('xdg-open')

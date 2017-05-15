#!/usr/bin/python
"""apparat_launcher - plugin: screenshot"""

# general
import os
import sys
import wx

# apparat
import ini
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!ss', '!fs',)


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------

def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting', 1, __name__)

    # Reset status notification back to OK
    main_window.status_notification_reset()

    icon_size = ini.read_single_ini_value('General', 'icon_size') # get preference value

    if current_search_string == "!ss":
        tools.debug_output('prepare_general', 'Case: Selective Screenshot', 1, __name__)
        prepare_selective_screenshot(main_window, icon_size)

    elif current_search_string == "!fs":
        tools.debug_output('prepare_general', 'Case: Full Screenshot', 1, __name__)
        prepare_full_screenshot(main_window, icon_size)

    else:
        tools.debug_output('prepare_general', 'Error: Unexpected screenshot plugin command', 3, __name__)
        main_window.status_notification_display_error('Unexpected screenshot plugin command')

    tools.debug_output('prepare_general', 'finished', 1)



def prepare_selective_screenshot(main_window, icon_size):
    """Prepare selective screenshot"""
    tools.debug_output('prepare_selective_screenshot', 'starting', 1, __name__)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Screenshot (Selective)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/screenshot/'+icon_size+'/screenshot_selective.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Selective Screenshot')
    main_window.ui__txt_command.SetValue('import')

    ## parameter button
    main_window.ui__bt_parameter.SetToolTipString('Do')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    ## parameter txt
    current_timestamp = tools.generate_timestamp()
    parameter = os.environ['HOME']+'/'+current_timestamp+'_selection.png'
    main_window.ui__txt_parameter.SetValue(parameter)


def prepare_full_screenshot(main_window, icon_size):
    """Prepare full screenshot"""
    tools.debug_output('prepare_full_screenshot', 'starting', 1, __name__)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Screenshot (Full)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/screenshot/'+icon_size+'/screenshot_full.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Full Screenshot')
    main_window.ui__txt_command.SetValue('import')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Do')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    ## parameter txt
    current_timestamp = tools.generate_timestamp()
    parameter = '-window root '+os.environ['HOME']+'/'+current_timestamp+'_full.png'
    main_window.ui__txt_parameter.SetValue(parameter)

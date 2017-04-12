#!/usr/bin/python
"""apparat - plugin: screenshot"""

# general
import os
import wx

# apparat
import config
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!ss', '!fs')


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------

def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting', 1)

    if  current_search_string == "!ss":
        tools.debug_output('prepare_general', 'Case: Selective Screenshot', 1)
        prepare_selective_screenshot(main_window)
        return

    if  current_search_string == "!fs":
        tools.debug_output('prepare_general', 'Case: Full Screenshot', 1)
        prepare_full_screenshot(main_window)
        return

    else:
        tools.debug_output('prepare_general', 'Error: Unexpected screenshot plugin command', 3)
        main_window.display_error_notification('Unexpected screenshot plugin command')
        return

    tools.debug_output('prepare_general', 'finished', 1)



def prepare_selective_screenshot(main_window):
    """Prepare selective screenshot"""
    tools.debug_output('prepare_selective_screenshot', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Screenshot (Selective)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/screenshot/'+str(config.TARGET_ICON_SIZE)+'/screenshot_selective.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Selective Screenshot')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Do')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command
    main_window.ui__txt_selected_app.SetValue('import')

    ## set parameter
    current_timestamp = tools.generate_timestamp()
    parameter = os.environ['HOME']+'/'+current_timestamp+'_selection.png'
    main_window.ui__txt_selected_parameter.SetValue(parameter)


def prepare_full_screenshot(main_window):
    """Prepare full screenshot"""
    tools.debug_output('prepare_full_screenshot', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Screenshot (Full)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/screenshot/'+str(config.TARGET_ICON_SIZE)+'/screenshot_full.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Full Screenshot')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Do')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command
    main_window.ui__txt_selected_app.SetValue('import')

    ## set parameter
    current_timestamp = tools.generate_timestamp()
    parameter = '-window root '+os.environ['HOME']+'/'+current_timestamp+'_full.png'
    main_window.ui__txt_selected_parameter.SetValue(parameter)

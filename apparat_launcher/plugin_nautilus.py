#!/usr/bin/python
"""apparat_launcher - plugin: nautilus"""

# general
import os
import wx

# apparat
import ini
import tools

# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!goto', '!recent', '!trash', '!network', '!net',)


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------

def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output(__name__, 'prepare_general', 'starting', 1)

    # Reset status notification back to OK
    main_window.status_notification_reset()

    icon_size = ini.read_single_ini_value('General', 'icon_size') # get preference value

    if current_search_string.startswith('!goto'):
        tools.debug_output(__name__, 'prepare_general', 'Case: Goto', 1)
        prepare_plugin_nautilus_goto(main_window, icon_size)

    elif current_search_string == ('!recent'):
        tools.debug_output(__name__, 'prepare_general', 'Case: Recent', 1)
        prepare_plugin_nautilus_show_recent(main_window, icon_size)

    elif current_search_string == ('!trash'):
        tools.debug_output(__name__, 'prepare_general', 'Case: Trash', 1)
        prepare_plugin_nautilus_open_trash(main_window, icon_size)

    elif current_search_string == ('!network') or current_search_string == ('!net'):
        tools.debug_output(__name__, 'prepare_general', 'Case: Network', 1)
        prepare_plugin_nautilus_show_network_devices(main_window, icon_size)

    else:
        tools.debug_output(__name__, 'prepare_general', 'Error: Unexpected nautilus plugin command', 3)
        main_window.status_notification_display_error('Unexpected nautilus plugin command')

    tools.debug_output(__name__, 'prepare_general', 'finished', 1)


def prepare_plugin_nautilus_goto(main_window, icon_size):
    """Plugin Nautilus - GoTo"""
    tools.debug_output(__name__, 'prepare_plugin_nautilus_goto', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (GoTo)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/nautilus/'+icon_size+'/goto.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Go to folder')
    main_window.ui__txt_command.SetValue('nautilus')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Open')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    ## set parameter txt
    if (main_window.ui__cb_search.GetValue()[6:7] == '~'):
        tools.debug_output(__name__, 'prepare_plugin_nautilus_goto', 'Replacing ~', 1)
        home = os.environ['HOME']
        main_window.ui__txt_parameter.SetValue(home+main_window.ui__cb_search.GetValue()[7:]) # possible parameter
    else:
        main_window.ui__txt_parameter.SetValue(main_window.ui__cb_search.GetValue()[6:]) # possible parameter


def prepare_plugin_nautilus_show_network_devices(main_window, icon_size):
    """Plugin Nautilus - Network"""
    tools.debug_output(__name__, 'prepare_plugin_nautilus_show_network_devices', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (Network)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/nautilus/'+icon_size+'/network.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Show network devices')
    main_window.ui__txt_command.SetValue('nautilus')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Open')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('network://')


def prepare_plugin_nautilus_show_recent(main_window, icon_size):
    """Plugin Nautilus - Recent"""
    tools.debug_output(__name__, 'prepare_plugin_nautilus_show_recent', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (Recent)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/nautilus/'+icon_size+'/recent.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Show recent files')
    main_window.ui__txt_command.SetValue('nautilus')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Open')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('recent://')


def prepare_plugin_nautilus_open_trash(main_window, icon_size):
    """Plugin Nautilus - Trash"""
    tools.debug_output(__name__, 'prepare_plugin_nautilus_open_trash', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (Trash)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/nautilus/'+icon_size+'/trash.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Open Trash')
    main_window.ui__txt_command.SetValue('nautilus')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Open')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('trash://')

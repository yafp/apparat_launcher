#!/usr/bin/python
"""apparat - plugin: nautilus"""

import tools
import wx


def prepare_plugin_nautilus_goto(main_window):
    """Plugin Nautilus - GoTo"""
    tools.debug_output('prepare_plugin_nautilus_goto', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (GoTo)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_goto_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Go to folder')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Open')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command
    main_window.ui__txt_selected_app.SetValue('nautilus')

    # set parameter
    main_window.ui__txt_selected_parameter.SetValue(main_window.ui__cb_search.GetValue()[6:])


def prepare_plugin_nautilus_show_network_devices(main_window):
    """Plugin Nautilus - Network"""
    tools.debug_output('prepare_plugin_nautilus_show_network_devices', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (Network)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_network_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Show network devices')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Open')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('nautilus')
    main_window.ui__txt_selected_parameter.SetValue('network://')


def prepare_plugin_nautilus_show_recent(main_window):
    """Plugin Nautilus - Recent"""
    tools.debug_output('prepare_plugin_nautilus_show_recent', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (Recent)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_recent_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Show recent files')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Open')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('nautilus')
    main_window.ui__txt_selected_parameter.SetValue('recent://')


def prepare_plugin_nautilus_open_trash(main_window):
    """Plugin Nautilus - Trash"""
    tools.debug_output('prepare_plugin_nautilus_open_trash', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Nautilus (Trash)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_trash_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Open Trash')

    ## parameter buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Open')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('nautilus')
    main_window.ui__txt_selected_parameter.SetValue('trash://')

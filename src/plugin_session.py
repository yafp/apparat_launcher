#!/usr/bin/python
"""apparat - plugin: session"""


import tools
import wx


def prepare_plugin_session_hibernate(main_window):
    """Plugin Session - Hibernate"""
    tools.debug_output('prepare_plugin_session_hibernate', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Hibernate')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_hibernate_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Hibernate machine')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('systemctl')
    main_window.ui__txt_selected_parameter.SetValue('suspend')


def prepare_plugin_session_lock(main_window):
    """Plugin Session - Lock"""
    tools.debug_output('prepare_plugin_session_lock', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Lock')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_lock_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Lock Session')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-screensaver-command')
    main_window.ui__txt_selected_parameter.SetValue('--lock')


def prepare_plugin_session_logout(main_window):
    """Plugin Session - Logout"""
    tools.debug_output('prepare_plugin_session_logout', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Logout')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_logout_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Logout Session')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-session-quit')
    main_window.ui__txt_selected_parameter.SetValue('--logout')


def prepare_plugin_session_shutdown(main_window):
    """Plugin Session - Shutdown"""
    tools.debug_output('prepare_plugin_session_shutdown', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Shutdown')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_shutdown_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Shutdown machine')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-session-quit')
    main_window.ui__txt_selected_parameter.SetValue('--power-off')




def prepare_plugin_session_reboot(main_window):
    """Plugin Session - Reboot"""
    tools.debug_output('prepare_plugin_session_reboot', 'starting')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Reboot')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_reboot_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Reboot machine')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-session-quit')
    main_window.ui__txt_selected_parameter.SetValue('--reboot')

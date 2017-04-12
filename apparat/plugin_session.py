#!/usr/bin/python
"""apparat - plugin: session"""

# general
import wx

# apparat
import config
import tools



# Plugin: Session
TRIGGER = ('!hibernate', '!sleep', '!lock', '!logout', '!reboot', '!restart', '!shutdown', '!halt', 'screensaver', '!saver')


def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting', 1)

    ## Hibernate
    if current_search_string == '!hibernate' or current_search_string == '!sleep':
        prepare_plugin_session_hibernate(main_window)

    ## Lock
    elif current_search_string == '!lock':
        prepare_plugin_session_lock(main_window)

    ## Logout
    elif current_search_string == '!logout':
        prepare_plugin_session_logout(main_window)

    ## Reboot
    elif current_search_string == '!reboot' or current_search_string == '!restart':
        prepare_plugin_session_reboot(main_window)

    ## Shutdown
    elif current_search_string == '!shutdown' or current_search_string == '!halt':
        prepare_plugin_session_shutdown(main_window)

    ## Screensaver
    elif current_search_string == '!screensaver' or current_search_string == '!saver':
        prepare_plugin_session_screensaver(main_window)

    else:
        tools.debug_output('parse_user_search_input', 'Error: Unexpected session command', 3)
        main_window.display_error_notification('Unexpected session plugin command')
        return

    tools.debug_output('prepare_general', 'finished', 1)


def prepare_plugin_session_hibernate(main_window):
    """Plugin Session - Hibernate"""
    tools.debug_output('prepare_plugin_session_hibernate', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Hibernate)', 1)

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/hibernate.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Hibernate machine')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('systemctl')
    main_window.ui__txt_selected_parameter.SetValue('suspend')


def prepare_plugin_session_lock(main_window):
    """Plugin Session - Lock"""
    tools.debug_output('prepare_plugin_session_lock', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Lock)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/lock.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Lock Session')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-screensaver-command')
    main_window.ui__txt_selected_parameter.SetValue('--lock')


def prepare_plugin_session_logout(main_window):
    """Plugin Session - Logout"""
    tools.debug_output('prepare_plugin_session_logout', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Logout)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/logout.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Logout Session')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-session-quit')
    main_window.ui__txt_selected_parameter.SetValue('--logout')


def prepare_plugin_session_shutdown(main_window):
    """Plugin Session - Shutdown"""
    tools.debug_output('prepare_plugin_session_shutdown', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Shutdown)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/shutdown.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Shutdown machine')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-session-quit')
    main_window.ui__txt_selected_parameter.SetValue('--power-off')


def prepare_plugin_session_reboot(main_window):
    """Plugin Session - Reboot"""
    tools.debug_output('prepare_plugin_session_reboot', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Reboot)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/reboot.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Reboot machine')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('gnome-session-quit')
    main_window.ui__txt_selected_parameter.SetValue('--reboot')


def prepare_plugin_session_screensaver(main_window):
    """Plugin Session - Screensaver"""
    tools.debug_output('prepare_plugin_session_screensaver', 'starting', 1)

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Screensaver)')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/screensaver.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Start screensaver')

    ## option buttons
    main_window.ui__bt_selected_parameter.SetToolTipString('Launch')
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

    ## set command and parameter
    main_window.ui__txt_selected_app.SetValue('xdg-screensaver')
    main_window.ui__txt_selected_parameter.SetValue('activate')

#!/usr/bin/python
"""apparat_launcher - plugin: session"""

# general
import wx

# apparat
import config
import ini
import tools



# Plugin: Session
TRIGGER = ('!hibernate', '!sleep', '!lock', '!logout', '!reboot', '!restart', '!shutdown', '!halt', '!screensaver', '!saver')


def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting with searchstring: '+current_search_string, 1)

    # Reset status notification back to OK
    main_window.status_notification_reset()

    icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    ## Hibernate
    if current_search_string == '!hibernate' or current_search_string == '!sleep':
        prepare_plugin_session_hibernate(main_window, icon_size)

    ## Lock
    elif current_search_string == '!lock':
        prepare_plugin_session_lock(main_window, icon_size)

    ## Logout
    elif current_search_string == '!logout':
        prepare_plugin_session_logout(main_window, icon_size)

    ## Reboot
    elif current_search_string == '!reboot' or current_search_string == '!restart':
        prepare_plugin_session_reboot(main_window, icon_size)

    ## Shutdown
    elif current_search_string == '!shutdown' or current_search_string == '!halt':
        prepare_plugin_session_shutdown(main_window, icon_size)

    ## Screensaver
    elif current_search_string == '!screensaver' or current_search_string == '!saver':
        prepare_plugin_session_screensaver(main_window, icon_size)

    else:
        tools.debug_output('parse_user_search_input', 'Error: Unexpected session command', 3)
        main_window.status_notification_display_error('Unexpected session plugin command')
        return

    tools.debug_output('prepare_general', 'finished', 1)


def prepare_plugin_session_hibernate(main_window, icon_size):
    """Plugin Session - Hibernate"""
    tools.debug_output('prepare_plugin_session_hibernate', 'starting', 1)
    #icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Hibernate)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/session/'+icon_size+'/hibernate.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Hibernate machine')
    main_window.ui__txt_command.SetValue('systemctl')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Launch')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('suspend')


def prepare_plugin_session_lock(main_window, icon_size):
    """Plugin Session - Lock"""
    tools.debug_output('prepare_plugin_session_lock', 'starting', 1)
    #icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Lock)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/session/'+icon_size+'/lock.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Lock Session')
    main_window.ui__txt_command.SetValue('gnome-screensaver-command')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Launch')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('--lock')


def prepare_plugin_session_logout(main_window, icon_size):
    """Plugin Session - Logout"""
    tools.debug_output('prepare_plugin_session_logout', 'starting', 1)
    #icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Logout)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/session/'+icon_size+'/logout.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Logout Session')
    main_window.ui__txt_command.SetValue('gnome-session-quit')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Launch')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('--logout')


def prepare_plugin_session_shutdown(main_window, icon_size):
    """Plugin Session - Shutdown"""
    tools.debug_output('prepare_plugin_session_shutdown', 'starting', 1)
    #icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Shutdown)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/session/'+str(config.TARGET_ICON_SIZE)+'/shutdown.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Shutdown machine')
    main_window.ui__txt_command.SetValue('gnome-session-quit')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Launch')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('--power-off')


def prepare_plugin_session_reboot(main_window, icon_size):
    """Plugin Session - Reboot"""
    tools.debug_output('prepare_plugin_session_reboot', 'starting', 1)
    #icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Reboot)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/session/'+icon_size+'/reboot.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Reboot machine')
    main_window.ui__txt_command.SetValue('gnome-session-quit')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Launch')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('--reboot')


def prepare_plugin_session_screensaver(main_window, icon_size):
    """Plugin Session - Screensaver"""
    tools.debug_output('prepare_plugin_session_screensaver', 'starting', 1)
    main_window.ui__txt_command.SetValue('gnome-session-quit')

    ## update plugin info
    main_window.plugin__update_general_ui_information('Session (Screensaver)')

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/session/'+icon_size+'/screensaver.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Start screensaver')
    main_window.ui__txt_command.SetValue('xdg-screensaver')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Launch')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('activate')

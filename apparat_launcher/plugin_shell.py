#!/usr/bin/python
"""apparat_launcher - plugin: shell"""

## general
import wx

## apparat
import config
import ini
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
    tools.debug_output('prepare_general', 'starting', 1)
    main_window.status_notification_reset() # Reset status notification back to OK
    icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    if current_search_string.startswith("!sh"):
        tools.debug_output('prepare_general', 'Case: Shell', 1)
        prepare_plugin_shell(main_window, icon_size)

        if (len(current_search_string) > 3):
            if current_search_string.startswith("!sh "):
                prepare_plugin_shell(main_window)
            else:
                main_window.plugin__update_general_ui_information('')
                tools.debug_output('prepare_general', 'Aborting shell', 2)
        return

    else:
        tools.debug_output('prepare_general', 'Error: Unexpected shell plugin command', 3)
        main_window.status_notification_display_error('Unexpected shell plugin command')
        return

    tools.debug_output('prepare_general', 'finished', 1)


def prepare_plugin_shell(main_window, icon_size):
    """Plugin Shell"""
    tools.debug_output('prepare_plugin_shell', 'starting', 1)
    main_window.plugin__update_general_ui_information('Shell') # update plugin info

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/shell/'+icon_size+'/shell.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Execute terminal command')
    main_window.ui__txt_command.SetValue('x-terminal-emulator')

    ## parameter button & txt
    main_window.ui__bt_parameter.SetToolTipString('Run')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__txt_parameter.SetValue('-e '+main_window.ui__cb_search.GetValue()[4:])

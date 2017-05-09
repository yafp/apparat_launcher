#!/usr/bin/python
"""apparat_launcher - plugin: passwordgen"""

## general
import os
import wx
# 
import random
import string

## apparat
import constants
import ini
import tools



# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!pw')


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output('prepare_general', 'starting', 1)

    # Reset status notification back to OK
    main_window.status_notification_reset()

    icon_size = ini.read_single_value('General', 'icon_size') # get preference value

    if current_search_string == ('!pw'):
        tools.debug_output('prepare_general', 'Case: Password Generator', 1)
        prepare_plugin_passwordgen(main_window, icon_size)

    else:
        tools.debug_output('prepare_general', 'Error: Unexpected passwordgen plugin command', 3)
        main_window.status_notification_display_error('Unexpected passwordgen plugin command')

    tools.debug_output('prepare_general', 'finished', 1)


def prepare_plugin_passwordgen(main_window, icon_size):
    """Plugin PasswordGen"""
    tools.debug_output('prepare_plugin_passwordgen', 'starting', 1)
    main_window.plugin__update_general_ui_information('Password Generator') ## update plugin info

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/passwordgen/'+icon_size+'/password.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Password Generator')

    ## parameter button
    main_window.ui__bt_parameter.SetToolTipString('Generate')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())

    tools.debug_output('prepare_plugin_passwordgen', 'finished', 1)


def execute_password_generation(main_window):
    """Generate a password"""
    tools.debug_output('execute_password_generation', 'started', 0)
    dlg = wx.TextEntryDialog(None,'Please insert desired password length','Password Generator', '8')
    ret = dlg.ShowModal()
    if ret == wx.ID_OK:
        tools.debug_output('execute_password_generation', 'Password length set to: '+dlg.GetValue(), 1)
        try:
            length = int(dlg.GetValue())
            if length > 7:
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                generated_password = ''.join(random.choice(chars) for i in range(length))

                # output the password
                wx.MessageBox('Your generated password is:\n\n'+generated_password, 'Password Generator', wx.OK | wx.ICON_INFORMATION)

                ## human readable
                #
                #blub = make_pseudo_word(syllables=1)
                #print blub
                #
                #blub2 = make_pseudo_word(syllables=1,add_number=True)
                #print blub2
                
                ## update usage-statistics
                tools.debug_output('execute_password_generation', 'Updating statistics (plugin_executed)', 1)
                current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed') # get current value from ini
                ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

                # reset the UI
                main_window.reset_ui()

                ## if enabled in ini - hide the UI after executing the command
                cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
                if cur_ini_value_for_hide_ui_after_command_execution == 'True':
                    main_window.tbicon.execute_tray_icon_left_click()

            else:
                wx.MessageBox('Min. password length is 8', 'Password Generator', wx.OK | wx.ICON_WARNING)

        except ValueError:
            tools.debug_output('execute', 'Password length entered by user was not a number', 3)

    else:
        tools.debug_output('execute', 'Password length definition canceld by user', 2)


# read other comments: http://stackoverflow.com/questions/7479442/high-quality-simple-random-password-generator
#
# NOT YET IN USE
def make_pseudo_word(syllables=5, add_number=False):
    """Alternate random consonants & vowels creating decent memorable passwords
    """
    rnd = random.SystemRandom()
    s = string.ascii_lowercase
    vowels = 'aeiou'
    consonants = ''.join([x for x in s if x not in vowels])
    pwd = ''.join([rnd.choice(consonants)+rnd.choice(vowels)
               for x in 'x'*syllables]).title()
    if add_number:
        pwd += str(rnd.choice(range(10)))
    return pwd


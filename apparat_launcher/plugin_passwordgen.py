#!/usr/bin/python
"""apparat_launcher - plugin: passwordgen"""

## general
import os
import random
import string
import wx


## apparat
import ini
import tools



# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------
TRIGGER = ('!pw', '!password',)


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def prepare_general(current_search_string, main_window):
    """Prepare General"""
    tools.debug_output(__name__, 'prepare_general', 'starting', 1)

    ## Reset status notification back to OK
    main_window.status_notification_reset()

    icon_size = ini.read_single_ini_value('General', 'icon_size') # get preference value

    if current_search_string == ('!pw') or current_search_string == ('!password'):
        tools.debug_output(__name__, 'prepare_general', 'Case: Password Generator', 1)
        prepare_plugin_passwordgen(main_window, icon_size)

    else:
        tools.debug_output(__name__, 'prepare_general', 'Error: Unexpected passwordgen plugin command', 3)
        main_window.status_notification_display_error('Unexpected passwordgen plugin command')

    tools.debug_output(__name__, 'prepare_general', 'finished', 1)


def prepare_plugin_passwordgen(main_window, icon_size):
    """Prepares UI for plugin PasswordGen"""
    tools.debug_output(__name__, 'prepare_plugin_passwordgen', 'starting', 1)
    main_window.plugin__update_general_ui_information('Password Generator') ## update plugin info

    ## command button & txt
    main_window.ui__bt_command_img = wx.Image('gfx/plugins/passwordgen/'+icon_size+'/password.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())
    main_window.ui__bt_command.SetToolTipString('Password Generator')

    ## parameter button
    main_window.ui__bt_parameter.SetToolTipString('Generate')
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/execute.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())

    tools.debug_output(__name__, 'prepare_plugin_passwordgen', 'Finished preparing password UI', 1)


def execute_password_generation(main_window):
    """Handles the actual password generation process"""
    tools.debug_output(__name__, 'execute_password_generation', 'started', 1)
    dlg = wx.TextEntryDialog(None, 'Please insert desired password length', 'Password Generator', '8')
    ret = dlg.ShowModal()
    if ret == wx.ID_OK:
        tools.debug_output(__name__, 'execute_password_generation', 'Password length set to: '+dlg.GetValue(), 1)
        try:
            password_length = int(dlg.GetValue())
            if password_length < 8:
                password_length = 8
                wx.MessageBox('Forced minimal password length 8', 'Password Generator', wx.OK | wx.ICON_WARNING)

            dial = wx.MessageDialog(None, 'Should the password be memorable?', 'Password Generator', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            pw_type = dial.ShowModal()

            single_generated_password = ''
            generated_passwords = ''

            if pw_type == wx.ID_YES:
                tools.debug_output(__name__, 'execute_password_generation', 'User selected memorable password type', 1)

                for x in range(0, 5): # generate 5 memorizable passwords
                    tools.debug_output(__name__, 'execute_password_generation', 'Generating memorable password '+str(x), 1)
                    single_generated_password = make_pseudo_word(syllables=password_length, add_number=False)
                    single_generated_password = single_generated_password[0:password_length] # substring to correct length
                    generated_passwords = generated_passwords+single_generated_password+'\n'

                ## add xkcd style pw_type
                xkcd = generate_xkcd_password()
                generated_passwords = generated_passwords+'\n\nXKCD (936) like:\n'+xkcd

            else:
                tools.debug_output(__name__, 'execute_password_generation', 'User selected default password type', 1)

                for x in range(0, 5): # generate 5 default passwords
                    tools.debug_output(__name__, 'execute_password_generation', 'Generating general password '+str(x), 1)

                    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                    random.seed = (os.urandom(1024))

                    single_generated_password = ''.join(random.choice(chars) for i in range(password_length))
                    generated_passwords = generated_passwords+single_generated_password+'\n'

            ## output the passwords
            wx.MessageBox('Choose from the following:\n\n'+generated_passwords, 'Password Generator', wx.OK | wx.ICON_INFORMATION)

            ## update usage-statistics
            tools.debug_output(__name__, 'execute_password_generation', 'Updating statistics (plugin_executed)', 1)
            current_plugin_executed_count = ini.read_single_ini_value('Statistics', 'plugin_executed') # get current value from ini
            ini.write_single_ini_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

        except ValueError:
            tools.debug_output(__name__, 'execute', 'Password length entered by user was not a number', 3)
            wx.MessageBox('Length was not a number', 'Password Generator', wx.OK | wx.ICON_WARNING)

    else:
        tools.debug_output(__name__, 'execute', 'Password length definition canceld by user', 2)

    ## reset the UI
    main_window.reset_ui()

    ## if enabled in ini - hide the UI after executing the command
    cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
    if cur_ini_value_for_hide_ui_after_command_execution == 'True':
        main_window.tbicon.execute_tray_icon_left_click()


# via comments in: http://stackoverflow.com/questions/7479442/high-quality-simple-random-password-generator
def make_pseudo_word(syllables=5, add_number=False):
    """Alternate random consonants & vowels creating decent memorable passwords"""
    rnd = random.SystemRandom()
    s = string.ascii_lowercase
    vowels = 'aeiou'
    consonants = ''.join([x for x in s if x not in vowels])
    pwd = ''.join([rnd.choice(consonants)+rnd.choice(vowels)
    for x in 'x'*syllables]).title()
    if add_number:
        pwd += str(rnd.choice(range(10)))
    return pwd


def get_random_word():
    """Picks a random file from the file words"""
    wordlist = open('words', 'r')
    line = next(wordlist)
    for num, wordlist in enumerate(wordlist):
        if random.randrange(num + 2):
            continue
        line = wordlist
    return line


def generate_xkcd_password():
    """Generated an xkcd like password - see: https://xkcd.com/936/"""
    single = ''
    full = ''
    for x in range(0, 5):
        single = get_random_word()
        single = single.rstrip()
        full = full+' '+single
    tools.debug_output(__name__, 'generate_xkcd_password', 'Finished generating an xkcd-like password', 1)
    return full

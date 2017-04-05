#!/usr/bin/python
"""apparat - an application launcher for linux"""


# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

# general
import os
import ConfigParser                 # to handle .ini/configuration files

## apparat
import constants
import tools



# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def read_single_value(section_name, key_name):
    """Method to read a single value from the configuration file apparat.ini"""
    check_if_ini_exists()
    tools.debug_output('read_single_value', 'starting')
    config = ConfigParser.ConfigParser()
    config.read(constants.APP_INI_PATH)
    #print config.sections()
    try:
        value = config.get(section_name, key_name)
        tools.debug_output('read_single_value', 'Section: '+section_name)
        tools.debug_output('read_single_value', 'Key: '+key_name)
        tools.debug_output('read_single_value', 'Value: '+value)
    except ConfigParser.ParsingError:
        # Issue: #13 - Create key if it doesnt exist already
        print('read_single_ini_value', 'key '+key_name+' does not exist. Should create the key with a default value in this case - see #13')
        tools.debug_output('read_single_value', 'key '+key_name+' does not exist. Should create the key with a default value in this case - see #13')
        if(key_name == 'apparat_started') or (key_name == 'command_executed') or (key_name == 'plugin_executed'):
            value = '0'
        elif (key_name == 'hide_ui_after_command_execution'):
            value = 'True'
        elif (key_name == 'lang'):
            value = 'EN'
        write_single_value(section_name, key_name, value)
        return
    return value


def write_single_value(section_name, key_name, value):
    """Method to write a single value to the configuration file apparat.ini"""
    check_if_ini_exists()
    tools.debug_output('write_single_value', 'starting')
    config = ConfigParser.ConfigParser()
    config.read(constants.APP_INI_PATH)
    config.set(section_name, key_name, value)
    tools.debug_output('write_single_value', 'Section: '+section_name)
    tools.debug_output('write_single_value', 'Key: '+key_name)
    tools.debug_output('write_single_value', 'Value: '+str(value))
    with open(constants.APP_INI_PATH, 'wb') as configfile:
        config.write(configfile)


def check_if_ini_exists():
    """Method to check if an ini file exists - and generate it if it doesnt"""
    tools.debug_output('check_if_ini_exists', 'starting')

    ## check if config folder exists - if not create it
    if not os.path.exists(constants.APP_INI_FOLDER):
        tools.debug_output('check_if_ini_exists', 'Creating config folder')
        os.makedirs(constants.APP_INI_FOLDER)

    ## check if config file exists
    if os.path.isfile(constants.APP_INI_PATH):
        tools.debug_output('check_if_ini_exists', 'Found ini file')
    else:
        tools.debug_output('check_if_ini_exists', 'No ini file found')
        tools.debug_output('check_if_ini_exists', 'Creating default ini file')
        mode = 'a' if os.path.exists(constants.APP_INI_PATH) else 'w'
        with open(constants.APP_INI_PATH, mode) as f:
            f.write('[Language]\n')
            f.write('lang = EN\n\n')
            f.write('[General]\n')
            f.write('hide_ui_after_command_execution = True\n')
            f.write('[Statistics]\n')
            f.write('apparat_started = 0\n')
            f.write('command_executed = 0\n')
            f.write('plugin_executed = 0\n')
        tools.debug_output('check_if_ini_exists', 'Finished ini file creation')
    tools.debug_output('check_if_ini_exists', 'finished')


def validate():
    """Validate the entire ini"""
    tools.debug_output('validate', 'Dummy: Validate ini')

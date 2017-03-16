#!/usr/bin/python
"""apparat - an application launcher for linux"""

import os
import ConfigParser                 # to handle .ini/configuration files
import constants



def read_single_ini_value(section_name, key_name):
    """Method to read a single value from the configuration file apparat.ini"""
    check_if_ini_file_exists()
    #print_debug_to_terminal('read_single_ini_value', 'starting')
    config = ConfigParser.ConfigParser()
    config.read(constants.APP_INI_PATH)
    #print config.sections()
    try:
        value = config.get(section_name, key_name)
        #print_debug_to_terminal('read_single_ini_value', 'Section: '+section_name)
        #print_debug_to_terminal('read_single_ini_value', 'Key: '+key_name)
        #print_debug_to_terminal('read_single_ini_value', 'Value: '+value)
    except ConfigParser.ParsingError:
        # Issue: #13 - Create key if it doesnt exist already
        print('read_single_ini_value', 'key '+key_name+' does not exist. Should create the key with a default value in this case - see #13')
        #print_debug_to_terminal('read_single_ini_value', 'key '+key_name+' does not exist. Should create the key with a default value in this case - see #13')
    return value


def write_single_ini_value(section_name, key_name, value):
    """Method to write a single value to the configuration file apparat.ini"""
    check_if_ini_file_exists()
    #print_debug_to_terminal('write_single_ini_value', 'starting')
    config = ConfigParser.ConfigParser()
    config.read(constants.APP_INI_PATH)
    config.set(section_name, key_name, value)
    #print_debug_to_terminal('write_single_ini_value', 'Section: '+section_name)
    #print_debug_to_terminal('write_single_ini_value', 'Key: '+key_name)
    #print_debug_to_terminal('write_single_ini_value', 'Value: '+str(value))
    with open(constants.APP_INI_PATH, 'wb') as configfile:
        config.write(configfile)



def check_if_ini_file_exists():
    """Method to check if an ini file exists - and generate it if it doesnt"""
    #print_debug_to_terminal('check_if_ini_file_exists', 'starting')

    ## check if config folder exists - if not create it
    if not os.path.exists(constants.APP_INI_FOLDER):
        #print_debug_to_terminal('check_if_ini_file_exists', 'Creating config folder')
        os.makedirs(constants.APP_INI_FOLDER)

    ## check if config file exists
    if os.path.isfile(constants.APP_INI_PATH):
        print('found ini')
        #print_debug_to_terminal('check_if_ini_file_exists', 'Found ini file')
    else:
        #print_debug_to_terminal('check_if_ini_file_exists', 'No ini file found')
        #print_debug_to_terminal('check_if_ini_file_exists', 'Creating default ini file')
        mode = 'a' if os.path.exists(constants.APP_INI_PATH) else 'w'
        with open(constants.APP_INI_PATH, mode) as f:
            f.write('[Language]\n')
            f.write('lang = EN\n\n')
            f.write('[General]\n')
            f.write('hide_ui_after_command_execution = True\n')
            f.write('enable_debug_output = True\n\n')
            f.write('[Statistics]\n')
            f.write('apparat_started = 0\n')
            f.write('command_executed = 0\n')
            f.write('plugin_executed = 0\n')
        #print_debug_to_terminal('check_if_ini_file_exists', 'Finished ini file creation')

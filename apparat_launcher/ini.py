#!/usr/bin/python
"""apparat_launcher - an application launcher for linux"""


# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

# general
import os
import sys
import ConfigParser # to handle .ini/configuration files

## apparat
import constants
import tools



# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def read_single_ini_value(section_name, key_name):
    """Method to read a single value from the configuration file apparat.ini"""

    config = ConfigParser.ConfigParser()
    config.read(constants.APP_INI_PATH)
    try:
        value = config.get(section_name, key_name)
        tools.debug_output('read_single_ini_value', 'Section: '+section_name+' - Key: '+key_name+' - Value: '+value, 1, __name__)
    except ConfigParser.NoOptionError:
        tools.debug_output('read_single_ini_value', 'key '+key_name+' does not exist. Should create the key with a default value in this case - see #13', 2, __name__)
        if \
        (key_name == 'apparat_started') or \
        (key_name == 'command_executed') or \
        (key_name == 'plugin_executed'):
            value = '0'
        elif (key_name == 'hide_ui_after_command_execution'):
            value = 'True'
        elif (key_name == 'icon_size'):
            value = '128'
        elif (key_name == 'transparency'):
            value = '255'
        elif (key_name == 'lang'):
            value = 'EN'
        elif key_name.startswith('plugin'): # any plugin
            value = 'False'
        write_single_ini_value(section_name, key_name, value) # write default value for missing key/value pair
        tools.debug_output('read_single_ini_value', 'key '+key_name+' written with value: '+value, 1, __name__)
        return value
    return value


def write_single_ini_value(section_name, key_name, value):
    """Method to write a single value to the configuration file apparat.ini"""
    try:
        config = ConfigParser.ConfigParser()
        config.read(constants.APP_INI_PATH)
        config.set(section_name, key_name, value)
        tools.debug_output('write_single_ini_value', 'Section: '+section_name+' - Key: '+key_name+' - Value: '+str(value), 1, __name__)
        with open(constants.APP_INI_PATH, 'wb') as configfile:
            config.write(configfile)
    except ConfigParser.NoSectionError:
        tools.debug_output('write_single_ini_value', 'Section '+section_name+' does not exist.', 3, __name__)
        return


def check_if_ini_exists():
    """Method to check if an ini file exists - and generate it if it doesnt"""
    tools.debug_output('check_if_ini_exists', 'Start checking for ini file', 0, __name__)

    ## check if config folder exists - if not create it
    if not os.path.exists(constants.APP_INI_FOLDER):
        tools.debug_output('check_if_ini_exists', 'Creating config folder', 2, __name__)
        os.makedirs(constants.APP_INI_FOLDER)

    ## check if config file exists
    if os.path.isfile(constants.APP_INI_PATH):
        tools.debug_output('check_if_ini_exists', 'Found ini file ('+constants.APP_INI_PATH+')', 1, __name__)
    else:
        tools.debug_output('check_if_ini_exists', 'No ini file found', 2)
        tools.debug_output('check_if_ini_exists', 'Creating default ini file', 2, __name__)
        mode = 'a' if os.path.exists(constants.APP_INI_PATH) else 'w'
        with open(constants.APP_INI_PATH, mode) as f:
            f.write('[Language]\n')
            f.write('lang = EN\n\n')
            f.write('[General]\n')
            f.write('hide_ui_after_command_execution = True\n')
            f.write('icon_size = 128\n')
            f.write('transparency = 255\n')
            f.write('[Statistics]\n')
            f.write('apparat_started = 0\n')
            f.write('command_executed = 0\n')
            f.write('plugin_executed = 0\n')
            f.write('[Plugins]\n')
            f.write('plugin_misc = False\n')
            f.write('plugin_nautilus = False\n')
            f.write('plugin_passwordgen = False\n')
            f.write('plugin_screenshot = False\n')
            f.write('plugin_search_internet = False\n')
            f.write('plugin_search_local = False\n')
            f.write('plugin_session = False\n')
            f.write('plugin_shell = False\n')
        tools.debug_output('check_if_ini_exists', 'Finished ini file creation', 1, __name__)


def validate():
    """Validate the entire ini"""
    check_if_ini_exists()
    # https://pymotw.com/3/configparser/
    tools.debug_output('validate', 'Validating ini ('+constants.APP_INI_PATH+') for existing sections and options', 0, __name__)

    ## Section: Language
    SECTIONS = ['Language']
    OPTIONS = ['lang']
    validate_single_section(SECTIONS, OPTIONS)

    ## Section: General
    SECTIONS = ['General']
    OPTIONS = ['hide_ui_after_command_execution', 'icon_size', 'transparency']
    validate_single_section(SECTIONS, OPTIONS)

    ## Section: Statistics
    SECTIONS = ['Statistics']
    OPTIONS = ['apparat_started', 'command_executed', 'plugin_executed']
    validate_single_section(SECTIONS, OPTIONS)

    ## Section: Plugins
    SECTIONS = ['Plugins']
    OPTIONS = ['plugin_misc', 'plugin_nautilus', 'plugin_passwordgen', 'plugin_screenshot', 'plugin_search_internet', 'plugin_search_local', 'plugin_session', 'plugin_shell']
    validate_single_section(SECTIONS, OPTIONS)

    tools.debug_output('validate', 'Finished validating complete ini ('+constants.APP_INI_PATH+')', 0, __name__)


def validate_single_section(sections, options):
    """Validates a given ini section for a defined amount of options"""
    tools.debug_output('validate_single_section', 'Validating ini ('+constants.APP_INI_PATH+') for section'+str(sections), 0, __name__)
    config = ConfigParser.ConfigParser()
    config.read(constants.APP_INI_PATH)

    for section in sections:
        ## sections
        has_section = config.has_section(section)
        if has_section is True:
            tools.debug_output('validate_single_section', '{} section exists: {}'.format(section, has_section), 1, __name__)
        else:
            tools.debug_output('validate_single_section', '{} section is missing: {}'.format(section, has_section), 3, __name__)
            # create the missing section
            config.add_section(section)
            tools.debug_output('validate_single_section', 'Created new section '+section, 1, __name__)
            with open(constants.APP_INI_PATH, 'wb') as configfile:
                config.write(configfile)
        ## options
        for candidate in options:
            has_option = config.has_option(section, candidate)
            if has_option is True:
                tools.debug_output('validate_single_section', '{}.{:<12}  : {}'.format(section, candidate, has_option), 1, __name__)
            else:
                tools.debug_output('validate_single_section', '{}.{:<12}  : {}'.format(section, candidate, has_option), 3, __name__)

    tools.debug_output('validate_single_section', 'Validating ini ('+constants.APP_INI_PATH+') for section'+str(sections)+' finished', 0, __name__)

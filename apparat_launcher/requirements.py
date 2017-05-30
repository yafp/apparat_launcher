#!/usr/bin/python
"""Handles plugin requirement checks while enabling a plugin"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules


## apparat
import tools

PLUGIN_KILL_REQUIREMENTS = ('xkill',)
PLUGIN_MISC_REQUIREMENTS = ('xdg-open',)
PLUGIN_SEARCH_LOCAL_REQUIREMENTS = ('xdg-open',)
PLUGIN_SESSION_REQUIREMENTS = ('gnome-screensaver-command', 'gnome-session-quit', 'systemctl')


def check_plugin_requirements(plugin_name):
    """Check the plugin-requirements before enabling a plugin"""
    tools.debug_output(__name__, 'check_requirements', 'Starting for plugin: '+plugin_name, 1)

    ## plugin_kill
    #
    if(plugin_name == 'kill'):
        for i, (a) in enumerate(PLUGIN_KILL_REQUIREMENTS):
            tools.debug_output(__name__, 'check_plugin_requirements', 'Checking '+a, 1)
            if tools.which(PLUGIN_KILL_REQUIREMENTS[i]) is None:
                tools.debug_output(__name__, 'check_plugin_requirements', 'Error: '+PLUGIN_KILL_REQUIREMENTS[i]+' is missing. Plugin plugin_'+plugin_name+' can not be enabled', 3)
                return False

    ## plugin_misc
    #
    if(plugin_name == 'misc'):
        for i, (a) in enumerate(PLUGIN_MISC_REQUIREMENTS):
            tools.debug_output(__name__, 'check_plugin_requirements', 'Checking '+a, 1)
            if tools.which(PLUGIN_MISC_REQUIREMENTS[i]) is None:
                tools.debug_output(__name__, 'check_plugin_requirements', 'Error: '+PLUGIN_MISC_REQUIREMENTS[i]+' is missing. Plugin plugin_'+plugin_name+' can not be enabled', 3)
                return False

    ## plugin_search_local
    #
    if(plugin_name == 'search_local'):
        for i, (a) in enumerate(PLUGIN_SEARCH_LOCAL_REQUIREMENTS):
            tools.debug_output(__name__, 'check_plugin_requirements', 'Checking '+a, 1)
            if tools.which(PLUGIN_SEARCH_LOCAL_REQUIREMENTS[i]) is None:
                tools.debug_output(__name__, 'check_plugin_requirements', 'Error: '+PLUGIN_SEARCH_LOCAL_REQUIREMENTS[i]+' is missing. Plugin plugin_'+plugin_name+' can not be enabled', 3)
                return False

    ## plugin_session
    #
    if(plugin_name == 'session'):
        for i, (a) in enumerate(PLUGIN_SESSION_REQUIREMENTS):
            tools.debug_output(__name__, 'check_plugin_requirements', 'Checking '+a, 1)
            if tools.which(PLUGIN_SESSION_REQUIREMENTS[i]) is None:
                tools.debug_output(__name__, 'check_plugin_requirements', 'Error: '+PLUGIN_SESSION_REQUIREMENTS[i]+' is missing. Plugin plugin_'+plugin_name+' can not be enabled', 3)
                return False


    ## if a plugin has no requirements - everything is fine
    return True

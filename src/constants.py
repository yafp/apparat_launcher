#!/usr/bin/python
"""apparat - an application launcher for linux"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os                           # for searching applications and file/folder/path handling



# -----------------------------------------------------------------------------------------------
# CONSTANTS (DEVELOPER)
# -----------------------------------------------------------------------------------------------
APP_NAME = 'Apparat'
APP_URL = 'https://github.com/yafp/apparat'
APP_LICENSE = 'GPL3'
APP_TRAY_TOOLTIP = 'apparat'
APP_TRAY_ICON = 'gfx/core/bt_appIcon_16.png'
APP_INI_FOLDER = os.environ['HOME']+'/.config/apparat/'
APP_INI_PATH = APP_INI_FOLDER+'apparat.ini'

# Plugin-Commands
APP_PLUGINS_INTERNET_SEARCH_TRIGGER = ('!a', '!b', '!e', '!g', '!l', '!o', '!r', '!s', '!t', '!v', '!w', '!y') # must be tuple
APP_PLUGINS_SESSION_TRIGGER = ('!hibernate', '!sleep', '!lock', '!logout', '!reboot', '!restart', '!shutdown')
APP_PLUGINS_TRASH_TRIGGER = ('!trash')

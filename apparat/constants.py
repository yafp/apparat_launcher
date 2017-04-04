#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------
# built-in modules
import os                           # for searching applications and file/folder/path handling



# -----------------------------------------------------------------------------------------------
# GENERAL STRINGS
# -----------------------------------------------------------------------------------------------
APP_NAME = 'Apparat'
APP_DESCRIPTION = 'An application launcher for linux'
APP_URL = 'https://github.com/yafp/apparat'
APP_LICENSE = 'GPL3'
APP_TRAY_TOOLTIP = 'apparat'
APP_TRAY_ICON = 'gfx/core/bt_appIcon_16.png'
APP_INI_FOLDER = os.environ['HOME']+'/.config/apparat/'
APP_INI_PATH = APP_INI_FOLDER+'apparat.ini'




# -----------------------------------------------------------------------------------------------
# PLUGINS
# -----------------------------------------------------------------------------------------------

# Plugin: Internet-Search
APP_PLUGINS_INTERNET_SEARCH_TRIGGER = ('!a', '!b', '!e', '!g', '!l', '!m', '!o', '!r', '!s', '!t', '!v', '!w', '!y')
PLUGIN_INTERNET_SEARCH_URL_A = 'https://www.amazon.de/s/field-keywords='
PLUGIN_INTERNET_SEARCH_URL_B = 'https://bandcamp.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_E = 'https://stackexchange.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_G = 'https://www.google.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_L = 'https://www.last.fm/search?q='
PLUGIN_INTERNET_SEARCH_URL_M = 'http://www.maps.google.de/maps/place/'
PLUGIN_INTERNET_SEARCH_URL_O = 'https://stackoverflow.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_R = 'https://www.reddit.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_S = 'https://soundcloud.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_T = 'https://twitter.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_V = 'https://vimeo.com/search?q='
PLUGIN_INTERNET_SEARCH_URL_W = 'https://en.wikipedia.org/w/index.php?search='
PLUGIN_INTERNET_SEARCH_URL_Y = 'https://www.youtube.com/results?search_query='

# Plugin: Local search
APP_PLUGINS_SEARCH_LOCAL_TRIGGER = ('?')

# Plugin: Misc
APP_PLUGINS_MISC_TRIGGER = ('!open')

# Plugin: Screenshot
APP_PLUGINS_SCREENSHOT_TRIGGER = ('!ss', '!fs')

# Plugin: Nautilus
APP_PLUGINS_NAUTILUS_TRIGGER = ('!goto', '!recent', '!trash', '!network', '!net')

# Plugin: Session
APP_PLUGINS_SESSION_TRIGGER = ('!hibernate', '!sleep', '!lock', '!logout', '!reboot', '!restart', '!shutdown', '!halt')

# Plugin: Shell
APP_PLUGINS_SHELL_TRIGGER = ('!sh')

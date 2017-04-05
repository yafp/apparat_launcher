#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------
# general
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
APP_PLUGINS_INTERNET_SEARCH_URLS = (
    'https://www.amazon.de/s/field-keywords=',
    'https://bandcamp.com/search?q=',
    'https://stackexchange.com/search?q=',
    'https://www.google.com/search?q=',
    'https://www.last.fm/search?q=',
    'http://www.maps.google.de/maps/place/',
    'https://stackoverflow.com/search?q=',
    'https://www.reddit.com/search?q=',
    'https://soundcloud.com/search?q=',
    'https://twitter.com/search?q=',
    'https://vimeo.com/search?q=',
    'https://en.wikipedia.org/w/index.php?search=',
    'https://www.youtube.com/results?search_query='
)

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

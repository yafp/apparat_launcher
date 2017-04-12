#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------
# general
import os # for searching applications and file/folder/path handling



# -----------------------------------------------------------------------------------------------
# GENERAL CONSTANTS
# -----------------------------------------------------------------------------------------------
APP_NAME = 'Apparat'
APP_DESCRIPTION = 'An application launcher for linux'
APP_URL = 'https://github.com/yafp/apparat'
APP_LICENSE = 'GPL3'
APP_TRAY_TOOLTIP = 'apparat'
APP_TRAY_ICON = 'gfx/core/16/appIcon.png'
APP_INI_FOLDER = os.environ['HOME']+'/.config/apparat/'
APP_INI_PATH = APP_INI_FOLDER+'apparat.ini'



# -----------------------------------------------------------------------------------------------
# COLORS - http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
# -----------------------------------------------------------------------------------------------
C_DEFAULT = '\x1b[0m'       # Default

# colored text on dark background
C_BLACK = '\x1b[0;30;40m'       # UNUSED
C_RED = '\x1b[0;31;40m'         # Error (3)
C_GREEN = '\x1b[0;32;40m'       # Info (1)
C_YELLOW = '\x1b[0;33;40m'      # Warning (2)
C_BLUE = '\x1b[0;34;40m'        # UNUSED
C_PINK = '\x1b[0;35;40m'        # UNUSED
C_BLUE_LIGHT = '\x1b[0;36;40m'  # Other (else)
C_WHITE = '\x1b[0;37;40m'       # UNUSED

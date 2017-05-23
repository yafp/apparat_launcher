#!/usr/bin/python
"""Defines some constants like appname, UI size and color-codes"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------
# general
import os # for home folder


# -----------------------------------------------------------------------------------------------
# GENERAL CONSTANTS
# -----------------------------------------------------------------------------------------------
APP_NAME = 'apparat_launcher'
APP_DESCRIPTION = 'An application launcher for linux'
APP_URL = 'https://github.com/yafp/apparat_launcher'
APP_LICENSE = 'GPL3'
APP_TRAY_TOOLTIP = 'apparat_launcher'
APP_TRAY_ICON = 'gfx/core/16/appIcon.png'
APP_INI_FOLDER = os.environ['HOME']+'/.config/apparat_launcher/'
APP_INI_PATH = APP_INI_FOLDER+'apparat_launcher.ini'

WINDOW_WIDTH = 650 # Default: 650
WINDOW_HEIGHT = 460 # Default: 460


# -----------------------------------------------------------------------------------------------
# COLORS - http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
# -----------------------------------------------------------------------------------------------
C_DEFAULT = '\x1b[0m'       # Default

# colored text on dark background
C_BLACK = '\x1b[0;30;40m'       # UNUSED
C_RED = '\x1b[0;31;40m'         # Error (2)
C_GREEN = '\x1b[0;32;40m'       # Info (1)
C_YELLOW = '\x1b[0;33;40m'      # Warning (3)
C_BLUE = '\x1b[0;34;40m'        # UNUSED
C_PINK = '\x1b[0;35;40m'        # UNUSED
C_BLUE_LIGHT = '\x1b[0;36;40m'  # UNUSED
C_WHITE = '\x1b[0;37;40m'       # UNUSED

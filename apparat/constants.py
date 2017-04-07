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

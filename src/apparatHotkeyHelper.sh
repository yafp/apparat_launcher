#!/bin/bash

# Function:
#   checks if apparat.py is already running
#   if it is running: the apparat window gets focus if it isnt active already. If it is active it gets minimized
#   if it is not runnung: apparat.py gets started
#
# Usage:
#   should be configured to be launched via a global hotkey using system-settings
#
# Requirements:
# - xdotool
# - wmctrl


# CONFIG
#
APPARAT_FOLDER=$HOME'/Dropbox/Temp/apparat/src/'
APPARAT_EXECUTABLE='apparat.py'


# MAIN
#
wmctrl -lx | awk '{print $3}' | grep -i "$APPARAT_EXECUTABLE" # check if apparat.py is running right now

if [ $? -eq 0 ]; then # it is running

    ACTIVE_APP_WINDOW_TITLE=$(xdotool getwindowfocus getwindowname) # check active app
    if [ $ACTIVE_APP_WINDOW_TITLE == 'Apparat' ]; then 
        xdotool windowminimize $(xdotool getactivewindow) # apparat is active already - minimize it
        
    else # focus it
        #sleep 1
        wmctrl -xa $APPARAT_EXECUTABLE
        exit 1
    fi

else # apparat is not running -> start it
    #notify-send "Starting: "$APPARAT_EXECUTABLE -t 3000
    cd "$APPARAT_FOLDER" && python "./apparat.py"
    exit 0
fi

#!/bin/bash

# Function:
#   checks if apparat.py is already running
#   if it is running: the apparat_launcher window gets focus if it isnt active already. If it is active it gets minimized
#   if it is not runnung: apparat.py gets started
#
# Usage:
#   should be configured to be launched via a global hotkey using system-settings
#
# Requirements:
# - xdotool
# - wmctrl


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
APPARAT_FOLDER=$HOME'/Dropbox/Temp/apparat_launcher/apparat_launcher'
APPARAT_EXECUTABLE='apparat_launcher.py'



# ---------------------------------------------------------
# CHECK REQUIREMENTS
# ---------------------------------------------------------
#echo "Checking requirements"

# xdotool
if hash xdotool 2>/dev/null; then
    :
    #echo "Found required package xdotool"
else
    #echo "xdotool missing"
    exit
fi

# wmctrl
if hash wmctrl 2>/dev/null; then
    :
    #echo "Found required package wmctrl"
else
    #echo "wmctrl missing"
    exit
fi


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
wmctrl -lx | awk '{print $3}' | grep -i "$APPARAT_EXECUTABLE" # check if apparat.py is running right now

if [ $? -eq 0 ]; then # it is running
    #echo "Is running already"
    ACTIVE_APP_WINDOW_TITLE=$(xdotool getwindowfocus getwindowname) # check name of current foreground app
    if [ "$ACTIVE_APP_WINDOW_TITLE" == 'Apparat_launcher' ]; then  #if it is apparat
        #echo "Try minimizing it"
        xdotool windowminimize $(xdotool getactivewindow) # apparat_launcher is active already - minimize it
    else # focus it
        #echo "Try focusing the running session"
        wmctrl -xa "$APPARAT_EXECUTABLE"
    fi
    exit 0

else # apparat_launcher is not running -> start it
    #echo "Not yet running, launching it now"
    #notify-send 'Apparat_Launcher' 'Started via Hotkey'
    cd "$APPARAT_FOLDER" && python2 "./"$APPARAT_EXECUTABLE
    exit 0
fi

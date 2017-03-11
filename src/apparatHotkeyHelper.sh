#!/bin/bash

# Function:
#   checks if apparat.py is already running
#   if it is - the apparat window gets focus
#   if not - apparat.py gets started
#
# Usage:
#   should be configured to be launched via a global hotkey using system-settings
#

# CONFIG
#
APPARAT_FOLDER=$HOME'/Dropbox/Temp/apparat/src/'
APPARAT_EXECUTABLE='apparat.py'

# MAIN
#
wmctrl -lx | awk '{print $3}' | grep -i "$APPARAT_EXECUTABLE" # check if apparat.py is running right now

if [ $? -eq 0 ]; then # it is - so focus it
    #notify-send "Focusing apparat" -t 3000
    #sleep 1
    wmctrl -xa $APPARAT_EXECUTABLE
    exit 1

else # it isnt - so start it
    #notify-send "Starting: "$APPARAT_EXECUTABLE -t 3000
    #sleep 1
    cd "$APPARAT_FOLDER" && python "./apparat.py"
    exit 0
fi

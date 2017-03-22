#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

# General
import datetime                     # for timestamp in debug output
import os
import subprocess                   # for checking if cmd_exists
import sys

# Apparat
import config


DEBUG = False

# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def cmd_exists(cmd):
    """Method to check if a command exists."""
    print_debug_to_terminal('cmd_exists', 'starting')
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def check_arguments():
    """Checks if apparat was started with arguments or not"""
    # TODO: check getopt
    global DEBUG
    if len(sys.argv) > 2: # too much arguments
        print('Error: unsupported amount of parameters')
        
    elif len(sys.argv) < 2: # no user argument available
        DEBUG = False

    elif (sys.argv[1] in ("-d", "--debug")):
        DEBUG = True

    elif (sys.argv[1] in ("-h", "--help")):
        show_help()
        sys.exit()

    elif (sys.argv[1] in ("-v", "--version")):
        show_version()
        sys.exit()

    else:
        print('Error: unknown argument. Loading help')
        show_help()
        sys.exit()



def print_debug_to_terminal(source, message):
    """Method to print debug messages (if debug = True)."""
    if DEBUG is True:
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        print("debug # "+timestamp+" # "+source+" # "+message)



def check_linux_requirements():
    """Method to check the used linux packages on app start"""
    ## needed for session commands:
    # - gnome-screensaver-command
    # - gnome-session-quit
    # - systemctl
    # - xdg-open
    if which('gnome-screensaver-command') is None:
        print('Error: gnome-screensaver-command is missing')
        sys.exit()

    if which('gnome-session-quit') is None:
        print('Error: gnome-session-quit is missing')
        sys.exit()

    if which('systemctl') is None:
        print('Error: systemctl is missing')
        sys.exit()

    if which('xdg-open') is None:
        print('Error: xdg-open is missing')
        sys.exit()



def which(program):
    """Method to check if executable exists"""
    print_debug_to_terminal('which', program)
    def is_exe(fpath):
        """foo"""
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    print_debug_to_terminal('which', fpath)
    print_debug_to_terminal('which', fname)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None



def show_version():
    """Show version"""
    print(config.APP_VERSION)



def show_help():
    """Show help"""
    print("\nParameter:")
    print("\t-d / --debug\tShow debug output")
    print("\t-h / --help\tShow help")
    print("\t-v / --version\tShow version")



def check_platform():
    """Method to check the platform (supported or not)"""
    print_debug_to_terminal('check_platform', 'starting')

    ## Linux
    if sys.platform == "linux" or sys.platform == "linux2":
        print_debug_to_terminal('check_platform', 'Detected linux')

    ## Mac OS
    elif sys.platform == "darwin":
        print_debug_to_terminal('check_platform', 'Detected unsupported platform (darwin)')
        print("Error: Unsupported platform detected")
        sys.exit()

    ## Windows
    elif sys.platform == "win32":
        print_debug_to_terminal('check_platform', 'Detected unsupported platform (windows)')
        print("Error: Unsupported platform detected")
        sys.exit()

    print_debug_to_terminal('check_platform', 'finished')

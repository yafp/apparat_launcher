#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules
import datetime                     # for timestamp in debug output
import os
import subprocess                   # for checking if cmd_exists
import sys

## projects internal modules
import constants
import config


DEBUG = False

# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
def cmd_exists(cmd):
    """Method to check if a command exists."""
    debug_output('cmd_exists', 'starting')
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def check_arguments():
    """Checks if apparat was started with arguments or not"""
    debug_output('check_arguments', 'starting')
    global DEBUG
    if len(sys.argv) > 2: # too much arguments
        print('Error: Unsupported amount of parameters')
        show_help()
        sys.exit()

    elif len(sys.argv) == 1: # no user argument available
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
        print('Error: Unknown argument. Loading help')
        show_help()
        sys.exit()

    debug_output('check_arguments', 'finished')



def debug_output(source, message):
    """Method to print debug messages (if debug = True)."""
    if DEBUG is True:
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        print(constants.APP_NAME+" debug output # "+timestamp+" # "+source+" # "+message)



def generate_timestamp():
    """Generates and returns a timestamp in the format: YYYYMMDD__HHMMSS"""
    timestamp = '{:%Y%m%d__%H%M%S}'.format(datetime.datetime.now())
    return timestamp


def check_linux_requirements():
    """Method to check the used linux packages on app start"""
    debug_output('check_linux_requirements', 'starting')
    ## needed for session commands:
    # - gnome-screensaver-command
    # - gnome-session-quit
    # - systemctl
    # - xdg-open
    # - xdotool
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

    if which('xdotool') is None:
        print('Error: xdotool is missing')
        sys.exit()

    debug_output('check_linux_requirements', 'finished')


def which(program):
    """Method to check if executable exists"""
    debug_output('which', 'starting')
    def is_exe(fpath):
        """foo"""
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    debug_output('which', 'fpath: '+fpath)
    debug_output('which', 'fname: '+fname)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    debug_output('which', 'finished')
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
    debug_output('check_platform', 'starting')

    ## Linux
    if sys.platform == "linux" or sys.platform == "linux2":
        debug_output('check_platform', 'Detected linux')

    ## Mac OS
    elif sys.platform == "darwin":
        debug_output('check_platform', 'Detected unsupported platform (darwin)')
        print("Error: Unsupported platform detected")
        sys.exit()

    ## Windows
    elif sys.platform == "win32":
        debug_output('check_platform', 'Detected unsupported platform (windows)')
        print("Error: Unsupported platform detected")
        sys.exit()

    debug_output('check_platform', 'finished')


def trunc_at(s, d, n=3):
    """Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."""
    debug_output('trunc_at', 'starting')
    return d.join(s.split(d)[:n])
    debug_output('trunc_at', 'finished')

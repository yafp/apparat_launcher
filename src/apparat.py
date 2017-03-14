#!/usr/bin/python
"""apparat - an application launcher for linux"""

# NAME:         apparat
# DESCRIPTION:  Python based application launcher
# AUTHOR:       yafp
# URL:          https://github.com/yafp/apparat


# -----------------------------------------------------------------------------------------------
# RESOURCES
# -----------------------------------------------------------------------------------------------
# TrayIcon:                             http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
# Icons Font Awesome - Color: #7f8c8d


# -----------------------------------------------------------------------------------------------
# REMINDER/OPEN
# -----------------------------------------------------------------------------------------------
# global hotkey to bring running app in foreground:
#   https://wxpython.org/docs/api/wx.Window-class.html#RegisterHotKey
#   https://github.com/schurpf/pyhk



# -----------------------------------------------------------------------------------------------
# IMPORTING
# -----------------------------------------------------------------------------------------------
import sys                          # to show python version used

if sys.version_info >= (3, 0):
    sys.stdout.write('Python version used: '+sys.version) ## show python version
    sys.stdout.write("Sorry, requires Python 2.x, not Python 3.x\n")
    sys.exit(1)
else:
    import ConfigParser                 # to handle .ini/configuration files
    import difflib                      # for intelligent list sort
    import fnmatch                      # for searching applications
    import os                           # for searching applications
    import subprocess                   # for checking if cmd_exists
    import platform                     # to detect the platform the script is executed on
    import webbrowser                   # for opening urls (example: github project page)
    import gtk                          # for app-icon handling - crashes - reason: wx?
    gtk.remove_log_handlers()           # GTK/WX Issue - fix for Ubuntu
    import wx                           # for all the WX GUI items


# -----------------------------------------------------------------------------------------------
# CONSTANTS (DEVELOPER)
# -----------------------------------------------------------------------------------------------
APP_NAME = 'Apparat'
APP_URL = 'https://github.com/yafp/apparat'
APP_LICENSE = 'GPL3'
APP_TRAY_TOOLTIP = 'apparat'
APP_TRAY_ICON = 'gfx/core/bt_appIcon_16.png'
APP_INI_FOLDER = os.environ['HOME']+'/.config/apparat/'
APP_INI_PATH = APP_INI_FOLDER+'apparat.ini'
APP_PLUGINS_INTERNET_SEARCH_TRIGGER = ['!a', '!b', '!g', '!r', '!s', '!t', '!v', '!w', '!y']


# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
APP_VERSION = '20170314.01'
DEBUG = True                    # True or False - overwritten by Preference Window
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 280
TARGET_ICON_SIZE = 128

is_combobox_open = 0
is_resetted = True


# -----------------------------------------------------------------------------------------------
# CONFIG (USER)
# -----------------------------------------------------------------------------------------------
TRANSPARENCY_VALUE = 255                # app TRANSPARENCY_VALUE - Values: 0-255


# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HELPER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cmd_exists(cmd):
    """Method to check if a command exists."""
    print_debug_to_terminal('cmd_exists')
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def print_debug_to_terminal(string):
    """Method to print debug messages (if debug = True)."""
    if DEBUG is True or DEBUG == "True":
        print("debug >> "+string)


def check_platform():
    """Method to check the platform (supported or not)"""
    print_debug_to_terminal('check_platform')

    ## Linux
    if platform == "linux" or platform == "linux2":
        print_debug_to_terminal('\tDetected linux')

    ## Mac OS
    elif platform == "darwin":
        print_debug_to_terminal('\tDetected unsupported platform (darwin)')
        wx.MessageBox('Unsupported platform detected, aborting '+APP_NAME+' startup now.', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()

    ## Windows
    elif platform == "win32":
        print_debug_to_terminal('\tDetected unsupported platform (windows)')
        wx.MessageBox('Unsupported platform detected, aborting '+APP_NAME+' startup now.', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()


def check_linux_requirements():
    """Method to check the used linux packages on app start"""
    # gnome-screensaver-command
    # gnome-session-quit
    # systemctl
    if which('gnome-screensaver-command') is None:
        wx.MessageBox('gnome-screensaver-command is missing', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()

    if which('gnome-session-quit') is None:
        wx.MessageBox('gnome-session-quit is missing', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()

    if which('systemctl') is None:
        wx.MessageBox('gnome-session-quit is missing', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()


def which(program):
    """Method to check if executable exists"""
    print_debug_to_terminal('which: '+program)
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
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

def read_single_ini_value(section_name, key_name):
    """Method to read a single value from the configuration file apparat.ini"""
    check_if_ini_file_exists()
    print_debug_to_terminal('read_single_ini_value')
    config = ConfigParser.ConfigParser()
    config.read(APP_INI_PATH)
    #print config.sections()
    try:
        value = config.get(section_name, key_name)
        print_debug_to_terminal('\tSection:\t'+section_name)
        print_debug_to_terminal('\tKey:\t\t'+key_name)
        print_debug_to_terminal('\tValue:\t\t'+value)
    except ConfigParser.ParsingError:
        print_debug_to_terminal('key does not exist')
        # Issue: #13 - Create key if it doesnt exist already
    return value


def write_single_ini_value(section_name, key_name, value):
    """Method to write a single value to the configuration file apparat.ini"""
    check_if_ini_file_exists()
    print_debug_to_terminal('write_single_ini_value')
    config = ConfigParser.ConfigParser()
    config.read(APP_INI_PATH)
    config.set(section_name, key_name, value)
    print_debug_to_terminal('\tSection:\t'+section_name)
    print_debug_to_terminal('\tKey:\t\t'+key_name)
    print_debug_to_terminal('\tValue:\t\t'+str(value))
    with open(APP_INI_PATH, 'wb') as configfile:
        config.write(configfile)


def check_if_ini_file_exists():
    """Method to check if an ini file exists - and generate it if it doesnt"""
    print_debug_to_terminal('check_if_ini_file_exists')

    ## check if config folder exists - if not create it
    if not os.path.exists(APP_INI_FOLDER):
        print_debug_to_terminal("\tCreating config folder")
        os.makedirs(APP_INI_FOLDER)

    ## check if config file exists
    if os.path.isfile(APP_INI_PATH):
        print_debug_to_terminal("\tFound ini file")
    else:
        print_debug_to_terminal("\tNo ini file found")
        print_debug_to_terminal("\tCreating default ini file")
        mode = 'a' if os.path.exists(APP_INI_PATH) else 'w'
        with open(APP_INI_PATH, mode) as f:
            f.write('[Language]\n')
            f.write('lang = EN\n\n')
            f.write('[General]\n')
            f.write('hide_ui_after_command_execution = True\n')
            f.write('enable_debug_output = True\n\n')
            f.write('[Statistics]\n')
            f.write('apparat_started = 0\n')
            f.write('command_executed = 0\n')
            f.write('plugin_executed = 0\n')
        print_debug_to_terminal("\tFinished ini file creation")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN-WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MyFrame(wx.Frame):

    """Class for MainWindow"""

    def __init__(self, parent, title):
        """Initialize the MainWindow"""

        ## Update Statistics (ini) - Apparat launched
        print_debug_to_terminal('\tUpdating statistics (apparat_started)')
        cur_app_start_count = read_single_ini_value('Statistics', 'apparat_started')          # get current value from ini
        write_single_ini_value('Statistics', 'apparat_started', int(cur_app_start_count)+1)    # update ini +1

        ## check debug setting
        print_debug_to_terminal('\tReading Debug settings from .ini (enable_debug_output)')
        global DEBUG
        DEBUG = read_single_ini_value('General', 'enable_debug_output')          # get current value from ini

        ## define fonts
        global FONT_BIG
        FONT_BIG = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD) # family, style, weight
        global FONT_NORMAL_MONO
        FONT_NORMAL_MONO = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')

        ## Define the style of the frame
        style = (wx.MINIMIZE_BOX | wx.CLIP_CHILDREN | wx.NO_BORDER | wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR)

        self.mainUI = wx.Frame.__init__(self, parent, title=title, size=(WINDOW_WIDTH, WINDOW_HEIGHT), style=style)              # Custom Frame
        self.SetSizeHintsSz(wx.Size(WINDOW_WIDTH, WINDOW_HEIGHT), wx.Size(WINDOW_WIDTH, WINDOW_HEIGHT))         # forcing min and max size to same values - prevents resizing option
        self.tbicon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close_application)

        ## define and set an application icon
        app_icon = wx.Icon('gfx/core/bt_appIcon_16.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(app_icon)

        # ------------------------------------------------
        # Define UI Elements
        # ------------------------------------------------

        ## Preference button
        self.ui__img_prefs = wx.Bitmap('gfx/core/bt_prefs_16.png', wx.BITMAP_TYPE_BMP)
        self.ui__bt_prefs = wx.BitmapButton(self, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=self.ui__img_prefs, size=(self.ui__img_prefs.GetWidth()+10, self.ui__img_prefs.GetHeight()+10))
        self.ui__bt_prefs.SetLabel('Preferences')
        self.ui__bt_prefs.SetToolTipString(u'Open Preferences')

        ## result counter
        self.ui__txt_result_counter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE)
        self.ui__txt_result_counter.SetFont(wx.Font(10, 74, 90, 92, False, 'Sans'))
        self.ui__txt_result_counter.SetToolTipString(u'Results')
        self.ui__txt_result_counter.SetMinSize(wx.Size(35, 30))
        self.ui__txt_result_counter.SetMaxSize(wx.Size(35, 30))
        self.ui__txt_result_counter.SetEditable(False)
        self.ui__txt_result_counter.Enable(False)

        ## Search & Search Results as comboBox
        search_results = []
        combo_box_style = wx.TE_PROCESS_ENTER
        self.search_and_result_combobox = wx.ComboBox(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(265, 30), search_results, style=combo_box_style)

        ## selected result button
        self.ui__img_selected_result = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(150, 150), wx.BU_AUTODRAW)
        self.ui__bt_selected_result.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_selected_result.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
        self.ui__bt_selected_result.SetLabel('Applications')
        self.ui__bt_selected_result.Enable(False)

        ## launch options button
        self.ui__img_launch_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(150, 150), wx.BU_AUTODRAW)
        self.ui__bt_launch_options.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_launch_options.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.SetLabel('Options')
        self.ui__bt_launch_options.Enable(False)

        ## command (hidden)
        self.ui__txt_selected_result = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE)
        self.ui__txt_selected_result.SetFont(wx.Font(10, 74, 90, 92, False, 'Sans'))
        #self.ui__txt_selected_result.SetToolTipString(u'Command')
        self.ui__txt_selected_result.SetMinSize(wx.Size(150, 30))
        self.ui__txt_selected_result.SetMaxSize(wx.Size(150, 30))
        self.ui__txt_selected_result.SetEditable(False)
        self.ui__txt_selected_result.Enable(False)
        #self.ui__txt_selected_result.Hide()

        ## parameter (hidden)
        self.ui__txt_launch_options_parameter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE)
        self.ui__txt_launch_options_parameter.SetFont(wx.Font(10, 74, 90, 92, False, 'Sans'))
        #self.ui__txt_launch_options_parameter.SetToolTipString(u'Parameter')
        self.ui__txt_launch_options_parameter.SetMinSize(wx.Size(150, 30))
        self.ui__txt_launch_options_parameter.SetMaxSize(wx.Size(150, 30))
        self.ui__txt_launch_options_parameter.SetEditable(False)
        self.ui__txt_launch_options_parameter.Enable(False)
        #self.ui__txt_launch_options_parameter.Hide()

        ## Version Information
        #self.txt_version_information = wx.StaticText(self, wx.ID_ANY, ' v'+APP_VERSION, wx.DefaultPosition, wx.DefaultSize, 0)
        #self.txt_version_information.Wrap(-1)
        #self.txt_version_information.SetFont(wx.Font(8, 74, 90, 90, False, 'Sans'))
        #self.txt_version_information.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))


        # ------------------------------------------------
        # Layout
        # ------------------------------------------------
        b_sizer = wx.BoxSizer(wx.VERTICAL)                              # define layout container
        b_sizer.Add(self.ui__bt_prefs, 0, wx.ALIGN_RIGHT, 100)          # preferences
        b_sizer.AddSpacer(10)                                           # spacer
        # horizontal sub-item 1
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self.ui__txt_result_counter, 0, wx.CENTRE)             # result counter
        box1.Add(self.search_and_result_combobox, 0, wx.CENTRE)         # combobox
        b_sizer.Add(box1, 0, wx.CENTRE)
        b_sizer.AddSpacer(10)                                           # spacer
        # horizontal sub-item 2
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(self.ui__bt_selected_result, 0, wx.CENTRE)             # launch button
        box2.Add(self.ui__bt_launch_options, 0, wx.CENTRE)              # options button
        b_sizer.Add(box2, 0, wx.CENTRE)
        # horizontal sub-item 3
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add(self.ui__txt_selected_result, 0, wx.CENTRE)            # launch text
        box3.Add(self.ui__txt_launch_options_parameter, 0, wx.CENTRE)   # option text
        b_sizer.Add(box3, 0, wx.CENTRE)
        #b_sizer.AddSpacer(30)                                           # spacer
        #b_sizer.Add(self.txt_version_information, 0, wx.CENTRE)         # version
        self.SetSizer(b_sizer)


        # ------------------------------------------------
        # Bind/Connect Events
        # ------------------------------------------------
        self.ui__bt_prefs.Bind(wx.EVT_BUTTON, self.on_clicked)

        ## combobox
        self.search_and_result_combobox.Bind(wx.EVT_KEY_UP, self.on_combobox_key_press)                 # Pressed any key
        self.search_and_result_combobox.Bind(wx.EVT_TEXT, self.on_combobox_text_changed)                # NEW: combobox text changes.
        self.search_and_result_combobox.Bind(wx.EVT_TEXT_ENTER, self.on_combobox_enter)                 # Pressed Enter
        self.search_and_result_combobox.Bind(wx.EVT_COMBOBOX, self.on_combobox_select_item)             # Item selected
        self.search_and_result_combobox.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.on_combobox_close)           # Popup closed

        ## option button
        self.ui__bt_launch_options.Bind(wx.EVT_BUTTON, self.on_clicked_option_button)


        # ------------------------------------------------
        # Statusbar (on bottom of window)
        # ------------------------------------------------
        #self.CreateStatusBar() # A Statusbar in the bottom of the window


        # ------------------------------------------------
        # Menubar
        # ------------------------------------------------
        ## Setting up the menu.
        #filemenu= wx.Menu()

        ## wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        #filemenu.Append(wx.ID_ABOUT, '&About',' Information about this program')
        #filemenu.AppendSeparator()
        #filemenu.Append(wx.ID_EXIT,'E&xit',' Terminate the program')

        ## Creating the menubar.
        #menuBar = wx.MenuBar()
        #menuBar.Append(filemenu,'&File') # Adding the "filemenu" to the MenuBar
        #self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        self.Center()                   # open window centered
        self.Show(True)                 # show main UI
        self.search_and_result_combobox.SetFocus()     # set focus to search
        self.SetTransparent(TRANSPARENCY_VALUE)       # 0-255


    def on_close_application(self, event):
        """Method to close the app"""
        print_debug_to_terminal('on_close_application')
        print_debug_to_terminal('\tEvent: '+str(event))
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()
        wx.GetApp().ExitMainLoop()
        event.Skip()


    def on_clicked_option_button(self, event):
        """If the launch option button was clicked"""
        print_debug_to_terminal('Clicked launch option button')
        print_debug_to_terminal('\tEvent: '+str(event))
        self.launch_external_application()


    def on_clicked(self, event):
        """General click handler - using label to find source"""
        print_debug_to_terminal('on_clicked')
        print_debug_to_terminal('\tEvent: '+str(event))
        btn = event.GetEventObject().GetLabel()
        if btn == 'Preferences':
            print_debug_to_terminal('\tPreferences')
            self.open_preference_window()


    def open_preference_window(self):
        """Opens the preference window"""
        print_debug_to_terminal('open_preference_window')
        self.new = PreferenceWindow(parent=None, id=-1)
        self.new.Show()


    def on_combobox_text_changed(self, event):
        """Triggered if the combobox text changes"""
        print_debug_to_terminal('on_combobox_text_changed')
        print_debug_to_terminal('\tEvent: '+str(event))

        if self.search_and_result_combobox.GetValue() == '':
            print_debug_to_terminal('\tSearch string is empty - could reset UI at that point - but cant so far because of endless loop')
            #self.reset_ui()
        else:
            global is_resetted
            is_resetted = False


    def on_combobox_enter(self, event):
        """Triggered if Enter was pressed in combobox"""
        print_debug_to_terminal('on_combobox_enter')
        print_debug_to_terminal('\tEvent: '+str(event))

        ## if we got a search string and 1 result in counter -> launch_external_application
        #if len(self.search_and_result_combobox.GetValue()) > 0 and self.ui__txt_result_counter.GetValue() == '1':
        if len(self.search_and_result_combobox.GetValue()) > 0:

            global is_resetted
            is_resetted = False

            global is_combobox_open
            if is_combobox_open == 0:
                self.launch_external_application()

            else: # enter was pressed to close the combobox ....
                print('\tcould launch app now ...combobox is still open')
                is_combobox_open = 0    # global var to keep track if dropdown is open or closed

                ## run search again after selecting the desired search string from dropdown
                self.parse_user_search_input(self.search_and_result_combobox.GetValue())
        else:
            print_debug_to_terminal('\tCombobox is empty, nothing to do here.')


    def on_combobox_select_item(self, event):
        """If an item of the result-list was selected"""
        print_debug_to_terminal('\n\non_combobox_select_item')
        print_debug_to_terminal('\tEvent: '+str(event))
        self.ui__txt_selected_result.SetValue(self.search_and_result_combobox.GetValue())   # write command to command text field
        self.search_and_result_combobox.SetInsertionPointEnd()


    def on_combobox_close(self, event):
        """If the popup of the combobox is closed"""
        print_debug_to_terminal('on_combobox_close')
        print_debug_to_terminal('\tEvent: '+str(event))
        print_debug_to_terminal('\tcombobox just got closed')


    def on_combobox_key_press(self, event):
        """If content of the searchfield of the combobox changes"""
        print_debug_to_terminal('on_combobox_key_press')
        print_debug_to_terminal('\tEvent: '+str(event))

        current_keycode = event.GetKeyCode()
        if current_keycode == 27: # ESC
            print_debug_to_terminal('\tESC in combobox')

            if(is_resetted is False):
                print_debug_to_terminal('\tLaunch reset method')
                self.reset_ui()
            else: # hide main window
                print_debug_to_terminal('\tUI is already resetted')
                self.tbicon.execute_tray_icon_left_click()

        elif current_keycode == 317:    # Arrow Down
            print_debug_to_terminal('\tARROW DOWN')
            self.search_and_result_combobox.Popup()

            ## global var to keep track if dropdown is open or closed
            global is_combobox_open
            is_combobox_open = 1
        else:
            current_search_string = self.search_and_result_combobox.GetValue()
            if len(current_search_string) == 0:
                print_debug_to_terminal("Search string is empty - doing nothing")
                self.reset_ui()
            else:
                print_debug_to_terminal('\tSearching: '+current_search_string)
                self.parse_user_search_input(current_search_string)


    def plugin__internet_search_prepare(self, current_search_string):
        """Plugin: Internet-Search - Updates the UI on trigger input"""
        print_debug_to_terminal('plugin__internet_search_prepare')

        if current_search_string.startswith('!a') is True:
            print_debug_to_terminal('\tPlugin Amazon activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_amazon_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Amazon')

        if current_search_string.startswith('!b') is True:
            print_debug_to_terminal('\tPlugin Bandcamp activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_bandcamp_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Bandcamp')

        if current_search_string.startswith('!g') is True:
            print_debug_to_terminal('\tPlugin Google activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_google_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Google')

        if current_search_string.startswith('!l') is True:
            print_debug_to_terminal('\tPlugin LastFM activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_lastfm_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('LastFM')

        if current_search_string.startswith('!r') is True:
            print_debug_to_terminal('\tPlugin Reddit activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_reddit_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Reddit')

        if current_search_string.startswith('!s') is True:
            print_debug_to_terminal('\tPlugin Soundcloud activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_soundcloud_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Soundcloud')

        if current_search_string.startswith('!t') is True:
            print_debug_to_terminal('\tPlugin Twitter activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_twitter_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Twitter')

        if current_search_string.startswith('!v') is True:
            print_debug_to_terminal('\tPlugin Vimeo activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_vimeo_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Vimeo')

        if current_search_string.startswith('!w') is True:
            print_debug_to_terminal('\tPlugin Wikipedia activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_wikipedia_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Wikipedia')

        if current_search_string.startswith('!y') is True:
            print_debug_to_terminal('\tPlugin YouTube activated')
            self.ui__img_selected_result = wx.Image('gfx/plugins/search/bt_youtube_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_result.SetToolTipString('Youtube')


        ## for all search plugin cases
        #
        ## update application button
        self.ui__bt_selected_result.Enable(True)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())

        ## update option button
        self.ui__img_launch_options = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.Enable(True)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.SetToolTipString('Search')

        ## set command
        self.ui__txt_selected_result.SetValue(current_search_string)

        ## set result-count
        self.ui__txt_result_counter.SetValue('1')


    def plugin__internet_search_execute(self, search_phrase, cur_searchphrase):
        """Plugin: Internet-Search - Execute the actual internet search call"""
        print_debug_to_terminal('plugin__internet_search_execute')

        if cur_searchphrase.startswith('!a') is True:                           # https://www.amazon.de/s/field-keywords=foobar
            remote_url = 'https://www.amazon.de/s/field-keywords='+search_phrase

        if cur_searchphrase.startswith('!b') is True:                           # https://bandcamp.com/search?q=foobar
            remote_url = 'https://bandcamp.com/search?q='+search_phrase

        if cur_searchphrase.startswith('!g') is True:                           # https://www.google.com/search?q=foobar
            remote_url = 'https://www.google.com/search?q='+search_phrase

        if cur_searchphrase.startswith('!l') is True:                           # https://www.last.fm/search?q=foobar
            remote_url = 'https://www.last.fm/search?q='+search_phrase

        if cur_searchphrase.startswith('!r') is True:                           # https://www.reddit.com/search?q=foobar
            remote_url = 'https://www.reddit.com/search?q='+search_phrase

        if cur_searchphrase.startswith('!s') is True:                           # https://soundcloud.com/search?q=foobar
            remote_url = 'https://soundcloud.com/search?q='+search_phrase

        if cur_searchphrase.startswith('!t') is True:                           # https://twitter.com/search?q=foobar
            remote_url = 'https://twitter.com/search?q='+search_phrase

        if cur_searchphrase.startswith('!v ') is True:                           # https://vimeo.com/search?q=foobar
            remote_url = 'https://vimeo.com/search?q='+search_phrase

        if cur_searchphrase.startswith('!w') is True:                           # https://en.wikipedia.org/w/index.php?search=foobar
            remote_url = 'https://en.wikipedia.org/w/index.php?search='+search_phrase

        if cur_searchphrase.startswith('!y') is True:
            remote_url = 'https://www.youtube.com/results?search_query='+search_phrase      # https://www.youtube.com/results?search_query=foobar

        ## for all:
        webbrowser.open(remote_url)  # open url

        ## update usage-statistics
        print_debug_to_terminal('\tUpdating statistics (plugin_executed)')
        current_plugin_executed_count = read_single_ini_value('Statistics', 'plugin_executed')          # get current value from ini
        write_single_ini_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1)    # update ini +1

        self.reset_ui()


    def process_plugin_session_lock(self):
        """Plugin Lock"""
        print_debug_to_terminal('\tPlugin lock activated')

        ## application buttons
        self.ui__img_selected_result = wx.Image('gfx/plugins/session/bt_lock_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result.Enable(True)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
        self.ui__bt_selected_result.SetToolTipString('Lock Session')

        ## option buttons
        self.ui__bt_launch_options.SetToolTipString('Launch')
        self.ui__img_launch_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.Enable(True) # Enable option button

        ## set command and parameter
        self.ui__txt_selected_result.SetValue('gnome-screensaver-command')
        self.ui__txt_launch_options_parameter.SetValue('--lock')

        ## set result-count
        self.ui__txt_result_counter.SetValue('1')


    def process_plugin_session_logout(self):
        """Plugin Logout"""
        print_debug_to_terminal('\tPlugin logout activated')

        ## application buttons
        self.ui__img_selected_result = wx.Image('gfx/plugins/session/bt_logout_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result.Enable(True)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
        self.ui__bt_selected_result.SetToolTipString('Logout Session')

        ## option buttons
        self.ui__bt_launch_options.SetToolTipString('Launch')
        self.ui__img_launch_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.Enable(True) # Enable option button

        ## set command and parameter
        self.ui__txt_selected_result.SetValue('gnome-session-quit')
        self.ui__txt_launch_options_parameter.SetValue('--logout')

        ## set result-count
        self.ui__txt_result_counter.SetValue('1')


    def process_plugin_session_shutdown(self):
        """Plugin Logout"""
        print_debug_to_terminal('\tPlugin shutdown activated')

        ## application buttons
        self.ui__img_selected_result = wx.Image('gfx/plugins/session/bt_shutdown_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result.Enable(True)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
        self.ui__bt_selected_result.SetToolTipString('Shutdown machine')

        ## option buttons
        self.ui__bt_launch_options.SetToolTipString('Launch')
        self.ui__img_launch_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.Enable(True) # Enable option button

        ## set command and parameter
        self.ui__txt_selected_result.SetValue('gnome-session-quit')
        self.ui__txt_launch_options_parameter.SetValue('--power-off')

        ## set result-count
        self.ui__txt_result_counter.SetValue('1')


    def process_plugin_session_hibernate(self):
        """Plugin Logout"""
        print_debug_to_terminal('\tPlugin hibernate activated')

        ## application buttons
        self.ui__img_selected_result = wx.Image('gfx/plugins/session/bt_hibernate_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result.Enable(True)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
        self.ui__bt_selected_result.SetToolTipString('Hibernate machine')

        ## option buttons
        self.ui__bt_launch_options.SetToolTipString('Launch')
        self.ui__img_launch_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.Enable(True) # Enable option button

        ## set command and parameter
        self.ui__txt_selected_result.SetValue('systemctl')
        self.ui__txt_launch_options_parameter.SetValue('suspend')

        ## set result-count
        self.ui__txt_result_counter.SetValue('1')


    def process_plugin_session_reboot(self):
        """Plugin Reboot"""
        print_debug_to_terminal('\tPlugin reboot activated')

        ## application buttons
        self.ui__img_selected_result = wx.Image('gfx/plugins/session/bt_reboot_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result.Enable(True)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
        self.ui__bt_selected_result.SetToolTipString('Reboot machine')

        ## option buttons
        self.ui__bt_launch_options.SetToolTipString('Launch')
        self.ui__img_launch_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
        self.ui__bt_launch_options.Enable(True) # Enable option button

        ## set command and parameter
        self.ui__txt_selected_result.SetValue('gnome-screensaver-command')
        self.ui__txt_launch_options_parameter.SetValue('--reboot')

        ## set result-count
        self.ui__txt_result_counter.SetValue('1')


    def parse_user_search_input(self, current_search_string):
        """ Method to search applications and/or plugin commands to fill the results """
        print_debug_to_terminal('parse_user_search_input')
        if current_search_string != '':

            ## Plugin: Session
            ## Lock
            if current_search_string == '!lock':
                self.process_plugin_session_lock()
                return

            ## Logout
            if current_search_string == '!logout':
                self.process_plugin_session_logout()
                return

            ## Shutdown
            if current_search_string == '!shutdown':
                self.process_plugin_session_shutdown()
                return

            ## Hibernate
            if current_search_string == '!hibernate' or current_search_string == '!sleep':
                self.process_plugin_session_hibernate()
                return

            ## Reboot
            if current_search_string == '!reboot' or current_search_string == '!restart':
                self.process_plugin_session_reboot()
                return

            ## Plugin: Internet-Search
            ##
            if \
            (current_search_string.startswith('!a') is True) or \
            (current_search_string.startswith('!b') is True) or \
            (current_search_string.startswith('!g') is True) or \
            (current_search_string.startswith('!l') is True) or \
            (current_search_string.startswith('!r') is True) or \
            (current_search_string.startswith('!s') is True) or \
            (current_search_string.startswith('!t') is True) or \
            (current_search_string.startswith('!v') is True) or \
            (current_search_string.startswith('!w') is True) or \
            (current_search_string.startswith('!y') is True):

                self.plugin__internet_search_prepare(current_search_string)
                return

            ## Default case
            print_debug_to_terminal('\tSearching executables for the following string: '+current_search_string)
            search_results = fnmatch.filter(os.listdir('/usr/bin'), '*'+current_search_string+'*')     # search for executables matching users searchstring

            ## Sort results
            search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

            self.ui__txt_result_counter.SetValue(str(len(search_results))) # update result count
            self.search_and_result_combobox.SetItems(search_results) # update combobox

            if len(search_results) == 0:
                print_debug_to_terminal('Found 0 applications')

                ## update launch button icon
                self.ui__img_selected_result = wx.Image('gfx/core/bt_result_sad_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())

                ## update option button
                self.ui__img_launch_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())

                ## set command and parameter
                self.ui__txt_selected_result.SetValue('')
                self.ui__txt_launch_options_parameter.SetValue('')

            elif len(search_results) == 1: # if we got 1 search-results
                print_debug_to_terminal('\tFound 1 matching application')

                ## application buttons
                self.ui__bt_selected_result.Enable(True) # Enable application button
                self.ui__bt_selected_result.SetToolTipString(search_results[0]) # set tooltip

                ## options buttons
                self.ui__img_launch_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
                self.ui__bt_launch_options.Enable(True) # Enable option button
                self.ui__bt_launch_options.SetToolTipString('Launch') # set tooltip

                ## update labels
                self.ui__txt_selected_result.SetValue(search_results[0])
                self.ui__txt_launch_options_parameter.SetValue('')

                # Icon search - http://www.pygtk.org/pygtk2reference/class-gtkicontheme.html
                #
                ## get app-icon for selected application from operating system
                icon_theme = gtk.icon_theme_get_default()
                ## check what icon sizes are available and choose best size
                available_icon_sizes = icon_theme.get_icon_sizes(search_results[0])
                if not available_icon_sizes: # if we got no list of available icon sizes - Fallback: try to get a defined size
                    max_icon_size = 64
                    icon_info = icon_theme.lookup_icon(search_results[0], max_icon_size, 0)
                else:
                    print_debug_to_terminal('\tFound several icon sizes: '+str(available_icon_sizes))
                    ## pick the biggest
                    max_icon_size = max(available_icon_sizes)
                    print_debug_to_terminal('\tPicking the following icon size: '+str(max_icon_size))
                    icon_info = icon_theme.lookup_icon(search_results[0], max_icon_size, 0)

                icon_path = icon_info.get_filename()

                if icon_path != '': # found icon
                    if '.svg' not in icon_path:
                        new_app_icon = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)    # define new image
                        #new_app_iconWidth=new_app_icon.GetWidth()                   # get icon width
                        print_debug_to_terminal('\tFound icon: '+icon_path+' ('+str(max_icon_size)+'px)')
                        if TARGET_ICON_SIZE == max_icon_size: # if icon has expected size
                            print_debug_to_terminal('\tIcon size is as expected')
                        else: # resize icon
                            print_debug_to_terminal('\tIcon size does not match, starting re-scaling.')
                            new_app_icon.Rescale(128, 128)                             # rescale image
                    else: # found unsupported icon format
                        print_debug_to_terminal('\tSVG icons can not be used so far. Using a dummy icon for now')
                        new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
                else: # no icon
                    print_debug_to_terminal('\tFound no icon')
                    new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)

                self.ui__bt_selected_result.SetBitmap(new_app_icon.ConvertToBitmap())    # set icon to button
                return search_results[0] # return the 1 result - for launch
            else: # got several hits
                print_debug_to_terminal('\tFound '+str(len(search_results))+' matching application')

                ## update launch button icon
                self.ui__img_selected_result = wx.Image('gfx/core/bt_result_happy_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())
                self.ui__bt_selected_result.Enable(False)
                self.ui__bt_selected_result.SetToolTipString(u'')

                self.ui__img_launch_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())
                self.ui__bt_launch_options.Enable(False)                                  # Enable option button
                self.ui__bt_launch_options.SetToolTipString(u'')

                ## update labels
                self.ui__txt_selected_result.SetValue('')
                self.ui__txt_launch_options_parameter.SetValue('')

        else: # search string is empty
            print_debug_to_terminal('\tEmpty search string')


    def launch_external_application(self):
        """Launches the actual external process"""
        print_debug_to_terminal('launch_external_application')
        cur_searchphrase = self.ui__txt_selected_result.GetValue()
        cur_searchphrase_parameter = self.ui__txt_launch_options_parameter.GetValue()

        if \
        (cur_searchphrase.startswith('!a ') is True) or \
        (cur_searchphrase.startswith('!b ') is True) or \
        (cur_searchphrase.startswith('!g ') is True) or \
        (cur_searchphrase.startswith('!l ') is True) or \
        (cur_searchphrase.startswith('!r ') is True) or \
        (cur_searchphrase.startswith('!s ') is True) or \
        (cur_searchphrase.startswith('!t ') is True) or \
        (cur_searchphrase.startswith('!v ') is True) or \
        (cur_searchphrase.startswith('!w ') is True) or \
        (cur_searchphrase.startswith('!y ') is True):
            search_phrase = cur_searchphrase[3:] # remove trigger '!y ' or '!g ' or '!w '....

            self.plugin__internet_search_execute(search_phrase, cur_searchphrase)
            return

        #if cur_searchphrase != '' or cur_searchphrase != 'None':
        if cur_searchphrase is not None: # Check if the dropdown contains something at all or not
            print_debug_to_terminal('\tShould execute: "'+cur_searchphrase+'" with parameter: "'+cur_searchphrase_parameter+'"')
            ## check if name exists and is executable
            executable_exists = cmd_exists(cur_searchphrase)
            if executable_exists is True:
                ## update usage-statistics
                print_debug_to_terminal('\tUpdating statistics (command_executed)')
                current_commands_executed_count = read_single_ini_value('Statistics', 'command_executed')          # get current value from ini

                ## update ini +1
                write_single_ini_value('Statistics', 'command_executed', \
                                             int(current_commands_executed_count)+1)

                print_debug_to_terminal('\tExecutable: "'+cur_searchphrase+'" exists')
                # https://docs.python.org/2/library/subprocess.html
                if cur_searchphrase_parameter == '':
                    #subprocess.Popen(["rm","-r","some.file"])
                    subprocess.Popen([cur_searchphrase])
                    print_debug_to_terminal('\tExecuted: '+cur_searchphrase)
                else:
                    subprocess.Popen([cur_searchphrase, cur_searchphrase_parameter, ""])
                    print_debug_to_terminal('\tExecuted: '+cur_searchphrase+' '+cur_searchphrase_parameter)

                self.reset_ui()

                ## if enabled in ini - hide the Main UI after executing the command
                cur_ini_value_for_hide_ui_after_command_execution = read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
                if cur_ini_value_for_hide_ui_after_command_execution == "True":
                    self.tbicon.execute_tray_icon_left_click()

            else:
                print_debug_to_terminal('\tERROR >> Checking the executable failed')
        else:
            print_debug_to_terminal('\tWARNING >> cur_searchphrase is empty, aborting')


    def open_app_url(self):
        """Method to open the application URL  (GitHub project)"""
        print_debug_to_terminal('open_app_url')
        print_debug_to_terminal('\tOpening '+APP_URL+' in default browser')
        webbrowser.open(APP_URL)  # Go to github


    def reset_ui(self):
        """Method to reset the User-Interface of the Apps main-window"""
        print_debug_to_terminal('reset_ui')
        ## reset the combobox
        self.search_and_result_combobox.SetFocus() # set focus to search
        self.search_and_result_combobox.Clear() # clear all list values
        self.search_and_result_combobox.SetValue('') # clear search field

        ## reset the applications button
        self.ui__img_selected_result = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_result.Enable(False)
        self.ui__bt_selected_result.SetBitmap(self.ui__img_selected_result.ConvertToBitmap())

        ## reset the option buttons
        self.ui__img_launch_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_launch_options.Enable(False)
        self.ui__bt_launch_options.SetBitmap(self.ui__img_launch_options.ConvertToBitmap())

        ## reset the command and parameter elements
        self.ui__txt_selected_result.SetValue('')
        self.ui__txt_launch_options_parameter.SetValue('')

        ## reset the result counter
        self.ui__txt_result_counter.SetValue('') # Reset result counter

        global is_resetted
        is_resetted = True

        print_debug_to_terminal('\tFinished resetting UI')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PREFERENCE WINDOW - TABS - # https://pythonspot.com/wxpython-tabs/
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define the tab content as class
class UITabGeneral(wx.Panel):

    """Preference Window - Tab: General"""

    def __init__(self, parent):
        """Inits the general tab"""
        wx.Panel.__init__(self, parent)

        ## show language
        cur_ini_value_for_language = read_single_ini_value('Language', 'lang')          # get current value from ini
        t = wx.StaticText(self, -1, "Language: "+cur_ini_value_for_language, (20, 20))

        ## Hide UI
        self.cb_enable_hide_ui = wx.CheckBox(self, -1, 'Hide UI after command execution ', (20, 60))
        cur_ini_value_for_hide_ui_after_command_execution = read_single_ini_value('General', 'hide_ui_after_command_execution')          # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == "False":
            self.cb_enable_hide_ui.SetValue(False)
        else:
            self.cb_enable_hide_ui.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_hide_ui.GetId(), self.prefs_general_toggle_hide_ui)

        ## Enable debug output
        self.cb_enable_debug = wx.CheckBox(self, -1, 'Enable debug output in commandline ', (20, 90))
        cur_ini_value_for_enable_debug = read_single_ini_value('General', 'enable_debug_output')          # get current value from ini
        if cur_ini_value_for_enable_debug == "False":
            self.cb_enable_debug.SetValue(False)
        else:
            self.cb_enable_debug.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_debug.GetId(), self.prefs_general_toggle_enable_debug)


    def prefs_general_toggle_hide_ui(self, event):
        """Toggle the general pref: hide_ui"""
        print_debug_to_terminal('Preference - General - Hide UI: '+str(event))
        if self.cb_enable_hide_ui.GetValue() is True:
            print_debug_to_terminal('Enabled')
            write_single_ini_value('General', 'hide_ui_after_command_execution', "True") # update preference value
        else:
            print_debug_to_terminal('Disabled')
            write_single_ini_value('General', 'hide_ui_after_command_execution', "False") # update preference value


    def prefs_general_toggle_enable_debug(self, event):
        """Toggle the general pref: enable_debug"""
        print_debug_to_terminal('Preference - General - Enable Debug: '+str(event))
        if self.cb_enable_debug.GetValue() is True:
            print_debug_to_terminal('Enabled')
            write_single_ini_value('General', 'enable_debug_output', "True") # update preference value
        else:
            print_debug_to_terminal('Disabled')
            write_single_ini_value('General', 'enable_debug_output', "False") # update preference value


class UITabStatistics(wx.Panel):

    """Preference Window - Tab: Statistics - Shows usage stats"""

    def __init__(self, parent):
        """Inits the statistics tab"""
        wx.Panel.__init__(self, parent)

        ## show app start counter
        cur_ini_value_for_apparat_started = read_single_ini_value('Statistics', 'apparat_started')          # get current value from ini
        t = wx.StaticText(self, -1, "Apparat started:\t\t\t"+cur_ini_value_for_apparat_started, (20, 20))

        ## show execute counter
        cur_ini_value_for_command_executed = read_single_ini_value('Statistics', 'command_executed')          # get current value from ini
        t = wx.StaticText(self, -1, "Command executed:\t\t"+cur_ini_value_for_command_executed, (20, 40))

        ## show plugin trigger count
        cur_ini_value_for_plugin_executed = read_single_ini_value('Statistics', 'plugin_executed')          # get current value from ini
        t = wx.StaticText(self, -1, "Plugin executed:\t\t\t"+cur_ini_value_for_plugin_executed, (20, 60))


class UITabPluginCommands(wx.Panel):

    """Preference Window - Tab: Commands- Shows available plugin commands"""

    def __init__(self, parent):
        """Inits the plugin-commands tab"""
        wx.Panel.__init__(self, parent)

        h1_plugin_session = wx.StaticText(self, -1, "Session", (20, 20))
        h1_plugin_session.SetFont(FONT_BIG)

        plugin_session_cmd_list = wx.StaticText(self, -1, "!lock      = Lock session\n!logout    = Logout session\n!shutdown  = Shutdown machine\n!hibernate = Hibernate machine\n!reboot    = Reboot machine", (20, 60))
        plugin_session_cmd_list.SetFont(FONT_NORMAL_MONO)

        h1_plugin_internet_search = wx.StaticText(self, -1, "Internet-Search", (20, 100))
        h1_plugin_internet_search.SetFont(FONT_BIG)

        plugin_internet_search_cmd_list = wx.StaticText(self, -1, "!a = Amazon\n!b = Bandcamp\n!g = Google\n!l = LastFM\n!r = Reddit\n!s = SoudCloud\n!t = Twitter\n!v = Vimeo\n!w = Wikipedia\n!y = YouTube", (20, 140))
        plugin_internet_search_cmd_list.SetFont(FONT_NORMAL_MONO)

        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)
        pref_sizer.Add(h1_plugin_session, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_session_cmd_list, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(30)
        pref_sizer.Add(h1_plugin_internet_search, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_internet_search_cmd_list, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(100)
        self.SetSizer(pref_sizer)


class UITabAbout(wx.Panel):

    """Preference Window - Tab: About"""

    def __init__(self, parent):
        """Inits the About Tab"""
        wx.Panel.__init__(self, parent)

        about_app_icon = wx.Bitmap('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_BMP)
        about_app_icon_static = wx.StaticBitmap(self, -1, about_app_icon)

        about_app_name = wx.StaticText(self, -1, APP_NAME, (20, 20))
        about_app_name.SetFont(FONT_BIG)

        about_app_description = wx.StaticText(self, -1, "An application launcher for Linux", (20, 20))
        about_app_description.SetFont(FONT_NORMAL_MONO)

        about_app_version = wx.StaticText(self, -1, "You are currently using the version "+APP_VERSION, (20, 60))
        about_app_version.SetFont(FONT_NORMAL_MONO)

        about_app_license = wx.StaticText(self, -1, "Licensed under "+APP_LICENSE, (20, 80))
        about_app_license.SetFont(FONT_NORMAL_MONO)

        about_app_url = wx.HyperlinkCtrl(self, id=-1, label='GitHub', url=APP_URL, pos=(20, 140))
        about_app_url.SetFont(FONT_NORMAL_MONO)

        pref_about_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_about_sizer.AddSpacer(20)
        pref_about_sizer.Add(about_app_icon_static, flag=wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(10)
        pref_about_sizer.Add(about_app_name, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(20)
        pref_about_sizer.Add(about_app_description, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(50)
        pref_about_sizer.Add(about_app_version, 0, wx.ALIGN_CENTER)
        pref_about_sizer.Add(about_app_license, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(80)
        pref_about_sizer.Add(about_app_url, 0, wx.ALIGN_CENTER)
        self.SetSizer(pref_about_sizer)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PREFERENCE WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PreferenceWindow(wx.Frame):

    """Class for Preference Window"""

    def __init__(self, parent, id):
        """Initialize the preference window"""
        ## define style of preference window
        pref_window_style = (wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        wx.Frame.__init__(self, parent, id, APP_NAME+' Preferences', size=(600, 500), style=pref_window_style)

        ## Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        ## Create the tab windows
        tab1 = UITabGeneral(nb)
        tab2 = UITabStatistics(nb)
        tab3 = UITabPluginCommands(nb)
        tab4 = UITabAbout(nb)

        ## Add the windows to tabs and name them.
        nb.AddPage(tab1, "General ")
        nb.AddPage(tab2, "Statistics ")
        nb.AddPage(tab3, "Plugin Commands ")
        nb.AddPage(tab4, "About ")

        ## Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        wx.Frame.CenterOnScreen(self) # center the pref window

        self.Bind(wx.EVT_CLOSE, self.close_preference_ui)


    def close_preference_ui(self, event):
        """Closes the preference window"""
        print_debug_to_terminal("close_preference_ui")
        self.Destroy() # close the pref UI

        # TODO:
        # set focus to mainwindow


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY-MENU
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_menu_item(menu, label, func):
    """Generates single menu items for the tray icon popup menu"""
    print_debug_to_terminal('create_menu_item: '+label)
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# APP_TRAY_ICON
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TaskBarIcon(wx.TaskBarIcon, MyFrame):

    """Class for the Task Bar Icon"""

    def __init__(self, frame):
        """Method to initialize the tray icon"""
        print_debug_to_terminal('init (TaskBarIcon)')
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_tray_icon(APP_TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_app_tray_icon_left_click)
        print_debug_to_terminal('\tTask icon is ready now')


    def CreatePopupMenu(self):
        """Method to generate a Popupmenu for the TrayIcon (do NOT rename)"""
        print_debug_to_terminal('CreatePopupMenu')
        menu = wx.Menu()
        create_menu_item(menu, 'Preferences', self.on_tray_popup_select_preferences)
        create_menu_item(menu, 'GitHub', self.on_tray_popup_select_github)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_tray_popup_select_exit)
        return menu


    def set_tray_icon(self, path):
        """Method to set the icon for the TrayIconMenu item"""
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, APP_TRAY_TOOLTIP)


    def on_app_tray_icon_left_click(self, event):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        print_debug_to_terminal('on_app_tray_icon_left_click')
        print_debug_to_terminal('\tEvent: '+str(event))
        self.execute_tray_icon_left_click()


    def execute_tray_icon_left_click(self):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        print_debug_to_terminal('execute_tray_icon_left_click')
        if self.frame.IsIconized(): # if main window is minimized
            print_debug_to_terminal('\tMainWindow was minimized - should show it now')
            self.frame.Raise()
        else: # if main window is shown
            print_debug_to_terminal('\tMainWindow was shown - should minimize it now')
            self.frame.Iconize(True)


    def on_tray_popup_select_preferences(self, event):
        """Method to handle click in the Preferences tray menu item"""
        print_debug_to_terminal('on_tray_popup_select_preferences')
        print_debug_to_terminal('\tEvent: '+str(event))
        self.open_preference_window()


    def on_tray_popup_select_exit(self, event):
        """Method to handle click in the Exit tray menu item"""
        print_debug_to_terminal('on_tray_popup_select_exit')
        print_debug_to_terminal('\tEvent: '+str(event))
        wx.CallAfter(self.frame.Close)


    def on_tray_popup_select_github(self, event):
        """Method to handle click on the GitHub tray menu item"""
        print_debug_to_terminal('on_tray_popup_select_github')
        print_debug_to_terminal('\tEvent: '+str(event))
        print_debug_to_terminal('\tOpening: '+APP_URL)
        webbrowser.open(APP_URL) # Go to github


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(wx.App):

    """Class App"""

    def OnInit(self):
        """While starting the app (checks for already running instances)"""
        self.name = APP_NAME
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning(): # allow only 1 instance of apparat
            wx.MessageBox("An instance of "+APP_NAME+" is already running. Aborting", "Error", wx.OK | wx.ICON_WARNING)
            return False
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """Main"""
    app = App(False)
    check_platform() # Check if platform is supported at all, otherwise abort
    check_linux_requirements()
    frame = MyFrame(None, APP_NAME) # Main UI window
    app.MainLoop()


if __name__ == '__main__':
    print_debug_to_terminal('__main__')
    main()

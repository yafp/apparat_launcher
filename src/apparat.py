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
# Icons Font Awesome                    Color: #7f8c8d


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
    import datetime                     # for timestamp in debug output
    import difflib                      # for intelligent list sort
    import fnmatch                      # for searching applications
    import os                           # for searching applications
    import subprocess                   # for checking if cmd_exists
    import platform                     # to detect the platform the script is executed on
    import webbrowser                   # for opening urls (example: github project page)
    import wx                           # for all the WX GUI items

    ## project imports
    import constants
    import config
    import ini


# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
DEBUG = True                    # True or False - overwritten by Preference Window
is_combobox_open = 0
is_resetted = True


# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HELPER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cmd_exists(cmd):
    """Method to check if a command exists."""
    print_debug_to_terminal('cmd_exists', 'starting')
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def print_debug_to_terminal(source, message):
    """Method to print debug messages (if debug = True)."""
    if DEBUG is True or DEBUG == "True":
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        print("debug # "+timestamp+" # "+source+" # "+message)


def check_platform():
    """Method to check the platform (supported or not)"""
    print_debug_to_terminal('check_platform', 'starting')

    ## Linux
    if platform == "linux" or platform == "linux2":
        print_debug_to_terminal('check_platform', 'Detected linux')

    ## Mac OS
    elif platform == "darwin":
        print_debug_to_terminal('check_platform', 'Detected unsupported platform (darwin)')
        wx.MessageBox('Unsupported platform detected, aborting '+constants.APP_NAME+' startup now.', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()

    ## Windows
    elif platform == "win32":
        print_debug_to_terminal('check_platform', 'Detected unsupported platform (windows)')
        wx.MessageBox('Unsupported platform detected, aborting '+constants.APP_NAME+' startup now.', 'Error', wx.OK | wx.ICON_ERROR) # error dialog
        exit()


def check_linux_requirements():
    """Method to check the used linux packages on app start"""
    ## needed for session commands
    #
    # gnome-screensaver-command
    # gnome-session-quit
    # systemctl
    if which('gnome-screensaver-command') is None:
        wx.MessageBox('gnome-screensaver-command is missing', 'Error', wx.OK | wx.ICON_ERROR) # error dialog
        exit()

    if which('gnome-session-quit') is None:
        wx.MessageBox('gnome-session-quit is missing', 'Error', wx.OK | wx.ICON_ERROR) # error dialog
        exit()

    if which('systemctl') is None:
        wx.MessageBox('systemctl', 'Error', wx.OK | wx.ICON_ERROR) # error dialog
        exit()


def which(program):
    """Method to check if executable exists"""
    print_debug_to_terminal('which', program)
    def is_exe(fpath):
        """foo"""
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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN-WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MyFrame(wx.Frame):

    """Class for MainWindow"""

    def __init__(self, parent, title):
        """Initialize the MainWindow"""

        ## Update Statistics (ini) - Apparat launched
        print_debug_to_terminal('__init__', 'Updating statistics (apparat_started)')
        cur_app_start_count = ini.read_single_ini_value('Statistics', 'apparat_started')          # get current value from ini
        ini.write_single_ini_value('Statistics', 'apparat_started', int(cur_app_start_count)+1)    # update ini +1

        ## check debug setting
        print_debug_to_terminal('__init__', 'Reading Debug settings from .ini (enable_debug_output)')
        global DEBUG
        DEBUG = ini.read_single_ini_value('General', 'enable_debug_output')          # get current value from ini

        ## define fonts
        global FONT_BIG
        FONT_BIG = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD) # family, style, weight
        global FONT_NORMAL_MONO
        FONT_NORMAL_MONO = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')

        ## Define the style of the frame
        style = (wx.MINIMIZE_BOX | wx.CLIP_CHILDREN | wx.NO_BORDER | wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR)

        self.mainUI = wx.Frame.__init__(self, parent, title=title, size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT), style=style)              # Custom Frame
        self.SetSizeHintsSz(wx.Size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT), wx.Size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT))         # forcing min and max size to same values - prevents resizing option
        self.tbicon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close_application)

        ## define and set an application icon
        app_icon = wx.Icon('gfx/core/bt_appIcon_16.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(app_icon)

        # ------------------------------------------------
        # Define UI Elements
        # ------------------------------------------------

        ## Preference button
        self.ui__bt_prefs_img = wx.Bitmap('gfx/core/bt_prefs_16.png', wx.BITMAP_TYPE_BMP)
        self.ui__bt_prefs = wx.BitmapButton(self, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=self.ui__bt_prefs_img, size=(self.ui__bt_prefs_img.GetWidth()+10, self.ui__bt_prefs_img.GetHeight()+10))
        self.ui__bt_prefs.SetLabel('Preferences')
        self.ui__bt_prefs.SetToolTipString(u'Preferences')

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
        self.ui__search_and_result_combobox = wx.ComboBox(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(265, 30), search_results, style=combo_box_style)

        ## selected result button
        self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(150, 150), wx.BU_AUTODRAW)
        self.ui__bt_selected_app.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetLabel('Applications')
        self.ui__bt_selected_app.Enable(False)

        ## launch options button
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(150, 150), wx.BU_AUTODRAW)
        self.ui__bt_selected_parameter.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_selected_parameter.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.SetLabel('Options')
        self.ui__bt_selected_parameter.Enable(False)

        ## command (hidden)
        self.ui__txt_selected_app = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_app.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_app.SetToolTipString(u'Command')
        self.ui__txt_selected_app.SetMinSize(wx.Size(150, 20))
        self.ui__txt_selected_app.SetMaxSize(wx.Size(150, 20))
        self.ui__txt_selected_app.SetEditable(False)
        self.ui__txt_selected_app.Enable(False)
        self.ui__txt_selected_app.SetBackgroundColour(wx.Colour(237, 237, 237))
        #self.ui__txt_selected_app.Hide()

        ## parameter (hidden)
        self.ui__txt_selected_parameter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_parameter.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_parameter.SetToolTipString(u'Parameter')
        self.ui__txt_selected_parameter.SetMinSize(wx.Size(150, 20))
        self.ui__txt_selected_parameter.SetMaxSize(wx.Size(150, 20))
        self.ui__txt_selected_parameter.SetEditable(False)
        self.ui__txt_selected_parameter.Enable(False)
        self.ui__txt_selected_parameter.SetBackgroundColour(wx.Colour(237, 237, 237))
        #self.ui__txt_selected_parameter.Hide()

        ## Plugin Information
        self.ui__txt_plugin_information = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_plugin_information.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_plugin_information.SetToolTipString(u'Activated plugin')
        self.ui__txt_plugin_information.SetMinSize(wx.Size(300, 20))
        self.ui__txt_plugin_information.SetMaxSize(wx.Size(300, 20))
        self.ui__txt_plugin_information.SetEditable(False)
        self.ui__txt_plugin_information.Enable(False)
        self.ui__txt_plugin_information.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## Version Information
        self.ui__txt_version_information = wx.StaticText(self, wx.ID_ANY, ' v'+config.APP_VERSION, wx.DefaultPosition, wx.DefaultSize, 0)
        self.ui__txt_version_information.Wrap(-1)
        self.ui__txt_version_information.SetFont(wx.Font(7, 74, 90, 90, False, 'Sans'))
        self.ui__txt_version_information.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))


        # ------------------------------------------------
        # Layout/Sizer
        # ------------------------------------------------
        b_sizer = wx.BoxSizer(wx.VERTICAL)                              # define layout container

        b_sizer.Add(self.ui__bt_prefs, 0, wx.ALIGN_RIGHT, 100)          # preferences
        b_sizer.AddSpacer(0)                                           # spacer

        # horizontal sub-item 1
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self.ui__txt_result_counter, 0, wx.CENTRE)             # result counter
        box1.Add(self.ui__search_and_result_combobox, 0, wx.CENTRE)         # combobox
        b_sizer.Add(box1, 0, wx.CENTRE)
        b_sizer.AddSpacer(5)                                           # spacer

        # horizontal sub-item 2
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(self.ui__bt_selected_app, 0, wx.CENTRE)             # launch button
        box2.Add(self.ui__bt_selected_parameter, 0, wx.CENTRE)              # options button
        b_sizer.Add(box2, 0, wx.CENTRE)

        # horizontal sub-item 3
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add(self.ui__txt_selected_app, 0, wx.CENTRE)            # command
        box3.Add(self.ui__txt_selected_parameter, 0, wx.CENTRE)   # parameter
        b_sizer.Add(box3, 0, wx.CENTRE)

        b_sizer.AddSpacer(0)                                           # spacer
        b_sizer.Add(self.ui__txt_plugin_information, 0, wx.CENTRE)         # plugin info
        b_sizer.AddSpacer(10)

        b_sizer.Add(self.ui__txt_version_information, 0, wx.CENTRE)         # version
        self.SetSizer(b_sizer)


        # ------------------------------------------------
        # Bind/Connect Events
        # ------------------------------------------------
        self.ui__bt_prefs.Bind(wx.EVT_BUTTON, self.on_clicked)

        ## combobox
        self.ui__search_and_result_combobox.Bind(wx.EVT_KEY_UP, self.on_combobox_key_press)                 # Pressed any key
        self.ui__search_and_result_combobox.Bind(wx.EVT_TEXT, self.on_combobox_text_changed)                # NEW: combobox text changes.
        self.ui__search_and_result_combobox.Bind(wx.EVT_TEXT_ENTER, self.on_combobox_enter)                 # Pressed Enter
        self.ui__search_and_result_combobox.Bind(wx.EVT_COMBOBOX, self.on_combobox_select_item)             # Item selected
        self.ui__search_and_result_combobox.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.on_combobox_close)           # Popup closed
        # TODO: EVT_COMBOBOX_DROPDOWN

        ## option button
        self.ui__bt_selected_parameter.Bind(wx.EVT_BUTTON, self.on_clicked_option_button)


        # ------------------------------------------------
        # foo
        # ------------------------------------------------
        self.Center()                   # open window centered
        self.Show(True)                 # show main UI
        self.ui__search_and_result_combobox.SetFocus()     # set focus to search
        self.SetTransparent(config.TRANSPARENCY_VALUE)       # 0-255

        ## GTK vs WX is a mess - Issue: #15
        #
        ## It helps to import GTK after having created the WX app
        global gtk
        import gtk


    def on_close_application(self, event):
        """Method to close the app"""
        print_debug_to_terminal('on_close_application', 'starting')
        print_debug_to_terminal('on_close_application', 'Event: '+str(event))
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()
        wx.GetApp().ExitMainLoop()
        event.Skip()


    def on_clicked_option_button(self, event):
        """If the launch option button was clicked"""
        print_debug_to_terminal('on_clicked_option_button', 'starting')
        print_debug_to_terminal('on_clicked_option_button', 'Event: '+str(event))
        self.launch_external_application()


    def on_clicked(self, event):
        """General click handler - using label to find source"""
        print_debug_to_terminal('on_clicked', 'starting')
        print_debug_to_terminal('on_clicked', 'Event: '+str(event))
        btn = event.GetEventObject().GetLabel()
        if btn == 'Preferences':
            print_debug_to_terminal('on_clicked', 'Preferences')
            self.open_preference_window()


    def open_preference_window(self):
        """Opens the preference window"""
        print_debug_to_terminal('open_preference_window', 'starting')
        self.new = PreferenceWindow(parent=None, id=-1)
        self.new.Show()


    def on_combobox_text_changed(self, event):
        """Triggered if the combobox text changes"""
        print_debug_to_terminal('on_combobox_text_changed', 'starting')
        print_debug_to_terminal('on_combobox_text_changed', 'Event: '+str(event))

        if self.ui__search_and_result_combobox.GetValue() == '':
            print_debug_to_terminal('on_combobox_text_changed', 'Search string is empty - could reset UI at that point - but cant so far because of endless loop')
            #self.reset_ui()
        else:
            global is_resetted
            is_resetted = False


    def on_combobox_enter(self, event):
        """Triggered if Enter was pressed in combobox"""
        print_debug_to_terminal('on_combobox_enter', 'starting')
        print_debug_to_terminal('on_combobox_enter', 'Event: '+str(event))

        ## if we got a search string and 1 result in counter -> launch_external_application
        #if len(self.ui__search_and_result_combobox.GetValue()) > 0 and self.ui__txt_result_counter.GetValue() == '1':
        if len(self.ui__search_and_result_combobox.GetValue()) > 0:

            global is_resetted
            is_resetted = False

            global is_combobox_open
            if is_combobox_open == 0:
                self.launch_external_application()

            else: # enter was pressed to close the combobox
                print_debug_to_terminal('on_combobox_enter', 'Pressed enter to close the open combobox')
                is_combobox_open = 0    # global var to keep track if dropdown is open or closed

                ## run search again after selecting the desired search string from dropdown
                self.parse_user_search_input(self.ui__search_and_result_combobox.GetValue())
        else:
            print_debug_to_terminal('on_combobox_enter', 'Combobox is empty, nothing to do here.')


    def on_combobox_select_item(self, event):
        """If an item of the result-list was selected"""
        print_debug_to_terminal('on_combobox_select_item', 'starting')
        print_debug_to_terminal('on_combobox_select_item', 'Event: '+str(event))
        self.ui__txt_selected_app.SetValue(self.ui__search_and_result_combobox.GetValue())   # write command to command text field

        # get icon for selected executable
        self.get_icon_for_executable(self.ui__search_and_result_combobox.GetValue())

        # set cursor to end of string
        self.ui__search_and_result_combobox.SetInsertionPointEnd()


    def on_combobox_close(self, event):
        """If the popup of the combobox is closed"""
        print_debug_to_terminal('on_combobox_close', 'starting')
        print_debug_to_terminal('on_combobox_close', 'Event: '+str(event))
        print_debug_to_terminal('on_combobox_close', 'combobox just got closed')


    def on_combobox_key_press(self, event):
        """If content of the searchfield of the combobox changes"""
        print_debug_to_terminal('on_combobox_key_press', 'starting')
        print_debug_to_terminal('on_combobox_key_press', 'Event: '+str(event))

        current_keycode = event.GetKeyCode()
        print_debug_to_terminal('on_combobox_key_press', 'KeyCode: '+str(current_keycode))

        if current_keycode == 27: # ESC
            print_debug_to_terminal('on_combobox_key_press', 'ESC in combobox')

            if(is_resetted is False):
                print_debug_to_terminal('on_combobox_key_press', 'Launch reset method')
                self.reset_ui()
            else: # hide main window
                print_debug_to_terminal('on_combobox_key_press', 'UI is already resetted')
                self.tbicon.execute_tray_icon_left_click()

        elif current_keycode == 317:    # Arrow Down
            print_debug_to_terminal('on_combobox_key_press', 'ARROW DOWN')
            self.ui__search_and_result_combobox.Popup()

            ## global var to keep track if dropdown is open or closed
            global is_combobox_open
            is_combobox_open = 1

        elif current_keycode == 13: # Enter
            print_debug_to_terminal('on_combobox_key_press', 'Enter was pressed - ignoring it because of "on_combobox_enter"')
            global is_combobox_open
            is_combobox_open = 0

        else:
            current_search_string = self.ui__search_and_result_combobox.GetValue()
            if len(current_search_string) == 0:
                print_debug_to_terminal('on_combobox_key_press', 'Search string is empty - doing nothing')
                self.reset_ui()
            else:
                print_debug_to_terminal('on_combobox_key_press', 'Searching: '+current_search_string)
                self.parse_user_search_input(current_search_string)


    def get_icon_for_executable(self, full_executable_name):
        """Tries to get an icon for an selected executable"""
        ## Icon search - http://www.pygtk.org/pygtk2reference/class-gtkicontheme.html
        #
        ## get app-icon for selected application from operating system
        icon_theme = gtk.icon_theme_get_default()
        ## check what icon sizes are available and choose best size
        available_icon_sizes = icon_theme.get_icon_sizes(full_executable_name)
        if not available_icon_sizes: # if we got no list of available icon sizes - Fallback: try to get a defined size
            max_icon_size = 64
            icon_info = icon_theme.lookup_icon(full_executable_name, max_icon_size, 0)
        else:
            print_debug_to_terminal('get_icon_for_executable', 'Found several icon sizes: '+str(available_icon_sizes))
            ## pick the biggest
            max_icon_size = max(available_icon_sizes)
            print_debug_to_terminal('get_icon_for_executable', 'Picking the following icon size: '+str(max_icon_size))
            icon_info = icon_theme.lookup_icon(full_executable_name, max_icon_size, 0)

        if icon_info is None:
            new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
        else:
            icon_path = icon_info.get_filename()

            if icon_path != '': # found icon
                if '.svg' not in icon_path:
                    new_app_icon = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)    # define new image
                    #new_app_iconWidth=new_app_icon.GetWidth()                   # get icon width
                    print_debug_to_terminal('get_icon_for_executable', 'Found icon: '+icon_path+' ('+str(max_icon_size)+'px)')
                    if config.TARGET_ICON_SIZE == max_icon_size: # if icon has expected size
                        print_debug_to_terminal('get_icon_for_executable', 'Icon size is as expected')
                    else: # resize icon
                        print_debug_to_terminal('get_icon_for_executable', 'Icon size does not match, starting re-scaling.')
                        new_app_icon.Rescale(128, 128)                             # rescale image
                else: # found unsupported icon format
                    print_debug_to_terminal('get_icon_for_executable', 'SVG icons ('+icon_path+') can not be used so far. Using a dummy icon for now')
                    new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
            else: # no icon
                print_debug_to_terminal('get_icon_for_executable', 'Found no icon')
                new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)

        # application button
        self.ui__bt_selected_app.SetBitmap(new_app_icon.ConvertToBitmap())    # set icon to button
        self.ui__bt_selected_app.Enable(True) # Enable the Button

        ## option buttons
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.Enable(True) # Enable option button
        self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip


    def plugin__internet_search_prepare(self, current_search_string):
        """Plugin: Internet-Search - Updates the UI on trigger input"""
        print_debug_to_terminal('plugin__internet_search_prepare', 'starting')

        if(self.ui__txt_selected_app.GetValue() != ''):
            ## show searchstring in parameter field
            cur_searchphrase_parameter = current_search_string[3:] # remove trigger '!y ' or '!g ' or '!w '
            self.ui__txt_selected_parameter.SetValue(cur_searchphrase_parameter)

        ## check if there is NO space after the trigger - abort this function and reset some parts of the UI
        #
        if(len(current_search_string) == 3) and (current_search_string[2] != " "):
            print_debug_to_terminal('plugin__internet_search_prepare', 'No space after trigger - should reset icons')

            # application button
            self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())

            ## option button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.SetToolTipString('')

            # command
            self.ui__txt_selected_app.SetValue('')

            # parameter
            self.ui__txt_selected_parameter.SetValue('')

            # plugin info
            self.set_ui_plugin_information('')
            return

        ## If search-string > 2 - abort - as all the work is already done
        #
        if(len(current_search_string) > 2):
            return # we can stop here - nothing more to do as plugin should be already activated

        ## Prepare UI for plugin
        #
        if current_search_string.startswith('!a') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Amazon activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_amazon_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Amazon')

        if current_search_string.startswith('!b') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Bandcamp activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_bandcamp_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Bandcamp')

        if current_search_string.startswith('!e') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Stack-Exchange activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_stack-exchange_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Stack-Exchange')

        if current_search_string.startswith('!g') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Google activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_google_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Google')

        if current_search_string.startswith('!l') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin LastFM activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_lastfm_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('LastFM')

        if current_search_string.startswith('!o') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Stack-Overflow activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_stack-overflow_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Stack-Overflow')

        if current_search_string.startswith('!r') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Reddit activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_reddit_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Reddit')

        if current_search_string.startswith('!s') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Soundcloud activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_soundcloud_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('SoundCloud')

        if current_search_string.startswith('!t') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Twitter activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_twitter_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Twitter')

        if current_search_string.startswith('!v') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Vimeo activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_vimeo_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Vimeo')

        if current_search_string.startswith('!w') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin Wikipedia activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_wikipedia_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('Wikipedia')

        if current_search_string.startswith('!y') is True:
            print_debug_to_terminal('plugin__internet_search_prepare', 'Plugin YouTube activated')
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_youtube_128.png', wx.BITMAP_TYPE_PNG)
            self.set_ui_plugin_information('YouTube')


        ## for all search plugin cases
        #
        ## update application button
        self.ui__bt_selected_app.Enable(True)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())

        ## update option button
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.Enable(True)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.SetToolTipString('Search')


    def plugin__internet_search_execute(self, command, parameter):
        """Plugin: Internet-Search - Execute the actual internet search call"""
        print_debug_to_terminal('plugin__internet_search_execute', 'starting')

        if command == '!a':                             # https://www.amazon.de/s/field-keywords=foobar
            remote_url = 'https://www.amazon.de/s/field-keywords='+parameter

        if command == ('!b'):                           # https://bandcamp.com/search?q=foobar
            remote_url = 'https://bandcamp.com/search?q='+parameter

        if command == ('!e'):                           # https://stackexchange.com/search?q=foobar
            remote_url = 'https://stackexchange.com/search?q='+parameter

        if command == ('!g'):                           # https://www.google.com/search?q=foobar
            remote_url = 'https://www.google.com/search?q='+parameter

        if command == ('!l'):                           # https://www.last.fm/search?q=foobar
            remote_url = 'https://www.last.fm/search?q='+parameter

        if command == ('!o'):                           # https://stackoverflow.com/search?q=foobar
            remote_url = 'https://stackoverflow.com/search?q='+parameter

        if command == ('!r'):                           # https://www.reddit.com/search?q=foobar
            remote_url = 'https://www.reddit.com/search?q='+parameter

        if command == ('!s'):                            # https://soundcloud.com/search?q=foobar
            remote_url = 'https://soundcloud.com/search?q='+parameter

        if command == ('!t'):                           # https://twitter.com/search?q=foobar
            remote_url = 'https://twitter.com/search?q='+parameter

        if command == ('!v '):                          # https://vimeo.com/search?q=foobar
            remote_url = 'https://vimeo.com/search?q='+parameter

        if command == ('!w'):                           # https://en.wikipedia.org/w/index.php?search=foobar
            remote_url = 'https://en.wikipedia.org/w/index.php?search='+parameter

        if command == ('!y'):
            remote_url = 'https://www.youtube.com/results?search_query='+parameter      # https://www.youtube.com/results?search_query=foobar

        ## for all - open the URL
        webbrowser.open(remote_url)

        ## update usage-statistics
        print_debug_to_terminal('plugin__internet_search_execute', 'Updating statistics (plugin_executed)')
        current_plugin_executed_count = ini.read_single_ini_value('Statistics', 'plugin_executed')          # get current value from ini
        ini.write_single_ini_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1)    # update ini +1

        self.reset_ui()

        ## if enabled in ini - hide the Main UI after executing the command
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == "True":
            self.tbicon.execute_tray_icon_left_click()


    def set_ui_plugin_information(self, plugin_name):
        """set some general UI values after having a plugin triggered"""
        print_debug_to_terminal('set_ui_plugin_information', 'started')

        if(plugin_name != ''):
            # application buttons
            self.ui__bt_selected_app.Enable(True)

            ## Option button
            self.ui__bt_selected_parameter.Enable(True) # Enable option button

            ## set result-count
            self.ui__txt_result_counter.SetValue('1')

            ## update search command
            self.ui__txt_selected_app.SetValue(self.ui__search_and_result_combobox.GetValue()[:2])

            # Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue('Plugin: '+plugin_name)

        else:
            # application buttons
            self.ui__bt_selected_app.Enable(False)

            ## Option button
            self.ui__bt_selected_parameter.Enable(False) # Enable option button

            # Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue(plugin_name)

        # tooltip
        self.ui__bt_selected_app.SetToolTipString(plugin_name)


    def process_plugin_session_lock(self):
        """Plugin Lock"""
        print_debug_to_terminal('process_plugin_session_lock', 'starting')

        ## update plugin info
        self.set_ui_plugin_information('Lock')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_lock_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Lock Session')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-screensaver-command')
        self.ui__txt_selected_parameter.SetValue('--lock')


    def process_plugin_session_logout(self):
        """Plugin Logout"""
        print_debug_to_terminal('process_plugin_session_logout', 'starting')

        ## update plugin info
        self.set_ui_plugin_information('Logout')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_logout_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Logout Session')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-session-quit')
        self.ui__txt_selected_parameter.SetValue('--logout')


    def process_plugin_session_shutdown(self):
        """Plugin Logout"""
        print_debug_to_terminal('process_plugin_session_shutdown', 'starting')

        ## update plugin info
        self.set_ui_plugin_information('Shutdown')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_shutdown_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Shutdown machine')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-session-quit')
        self.ui__txt_selected_parameter.SetValue('--power-off')


    def process_plugin_session_hibernate(self):
        """Plugin Logout"""
        print_debug_to_terminal('process_plugin_session_hibernate', 'starting')

        ## update plugin info
        self.set_ui_plugin_information('Hibernate')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_hibernate_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Hibernate machine')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('systemctl')
        self.ui__txt_selected_parameter.SetValue('suspend')


    def process_plugin_session_reboot(self):
        """Plugin Reboot"""
        print_debug_to_terminal('process_plugin_session_reboot', 'starting')

        ## update plugin info
        self.set_ui_plugin_information('Reboot')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_reboot_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Reboot machine')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-screensaver-command')
        self.ui__txt_selected_parameter.SetValue('--reboot')


    def parse_user_search_input(self, current_search_string):
        """ Method to search applications and/or plugin commands to fill the results """
        print_debug_to_terminal('parse_user_search_input', 'starting')

        if current_search_string != '':

            ## Plugin: Session
            ##
            if current_search_string in constants.APP_PLUGINS_SESSION_TRIGGER:
                print_debug_to_terminal('parse_user_search_input', 'Plugin Session')

                ## Hibernate
                if current_search_string == '!hibernate' or current_search_string == '!sleep':
                    self.process_plugin_session_hibernate()

                ## Lock
                elif current_search_string == '!lock':
                    self.process_plugin_session_lock()

                ## Logout
                elif current_search_string == '!logout':
                    self.process_plugin_session_logout()

                ## Reboot
                elif current_search_string == '!reboot' or current_search_string == '!restart':
                    self.process_plugin_session_reboot()

                ## Shutdown
                elif current_search_string == '!shutdown':
                    self.process_plugin_session_shutdown()

                else:
                    print("Error")
                return


            ## Plugin: Internet-Search
            ##
            if current_search_string.startswith(constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER):
                print_debug_to_terminal('parse_user_search_input', 'Plugin Internet-Search')
                self.plugin__internet_search_prepare(current_search_string)
                return


            ## Default case / search for executable
            ##
            # reset plugin name field
            self.set_ui_plugin_information('')

            print_debug_to_terminal('parse_user_search_input', 'Searching executables for the following string: '+current_search_string)
            search_results = fnmatch.filter(os.listdir('/usr/bin'), '*'+current_search_string+'*')     # search for executables matching users searchstring

            ## Sort results - http://stackoverflow.com/questions/17903706/how-to-sort-list-of-strings-by-best-match-difflib-ratio
            search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

            self.ui__txt_result_counter.SetValue(str(len(search_results))) # update result count
            self.ui__search_and_result_combobox.SetItems(search_results) # update combobox

            if len(search_results) == 0: # 0 search results
                print_debug_to_terminal('parse_user_search_input', 'Found 0 applications')

                ## update launch button icon
                if current_search_string.startswith("!"): # starting input for plugins
                    self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
                else: # no result - so sad
                    self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_result_sad_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())

                ## update option button
                self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

                ## set command
                self.ui__txt_selected_app.SetValue('')

                ## set parameter
                self.ui__txt_selected_parameter.SetValue('')

            elif len(search_results) == 1: # 1 search-result
                print_debug_to_terminal('parse_user_search_input', 'Found 1 matching application')

                # combobox - autocomplete
                #self.ui__search_and_result_combobox.SetValue(search_results[0])

                ## application buttons
                self.ui__bt_selected_app.Enable(True) # Enable application button
                self.ui__bt_selected_app.SetToolTipString(search_results[0]) # set tooltip

                ## options buttons
                self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
                self.ui__bt_selected_parameter.Enable(True) # Enable option button
                self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip

                ## update command
                self.ui__txt_selected_app.SetValue(search_results[0])

                ## update parameter
                self.ui__txt_selected_parameter.SetValue('')

                ## Icon search
                self.get_icon_for_executable(str(search_results[0]))

                #return search_results[0] # return the 1 result - for launch

            else: # > 1 search results
                print_debug_to_terminal('parse_user_search_input', 'Found '+str(len(search_results))+' matching application')

                ## update launch button
                self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_list_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
                self.ui__bt_selected_app.Enable(False)
                self.ui__bt_selected_app.SetToolTipString(u'')

                # update launch-options button
                self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
                self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
                self.ui__bt_selected_parameter.Enable(False)                                  # Enable option button
                self.ui__bt_selected_parameter.SetToolTipString(u'')

                ## update command
                self.ui__txt_selected_app.SetValue('')

                ## update parameter
                self.ui__txt_selected_parameter.SetValue('')

        else: # search string is empty
            print_debug_to_terminal('parse_user_search_input', 'Empty search string')


    def launch_external_application(self):
        """Launches the actual external process"""
        print_debug_to_terminal('launch_external_application', 'starting')

        command = self.ui__txt_selected_app.GetValue()
        parameter = self.ui__txt_selected_parameter.GetValue()

        ## Plugin: Internet-Search
        ##
        if command in constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER:
            self.plugin__internet_search_execute(command, parameter)
            return


        ## Plugin: Session OR normal application
        ##
        if command is not None: # Check if the dropdown contains something at all or not
            print_debug_to_terminal('launch_external_application', 'Should execute: "'+command+'" with parameter: "'+parameter+'"')

            ## check if name exists and is executable
            executable_exists = cmd_exists(command)
            if executable_exists is True:
                ## update usage-statistics
                print_debug_to_terminal('launch_external_application', 'Updating statistics (command_executed)')
                current_commands_executed_count = ini.read_single_ini_value('Statistics', 'command_executed')          # get current value from ini

                ## update ini +1
                ini.write_single_ini_value('Statistics', 'command_executed', int(current_commands_executed_count)+1)

                print_debug_to_terminal('launch_external_application', 'Executable: "'+command+'" exists')
                # https://docs.python.org/2/library/subprocess.html
                # TODO: check: check_output - https://docs.python.org/2/library/subprocess.html#subprocess.check_output
                if parameter == '':
                    #subprocess.Popen(["rm","-r","some.file"])
                    subprocess.Popen([command])
                    print_debug_to_terminal('launch_external_application', 'Executed: '+command)
                else:
                    subprocess.Popen([command, parameter, ""])
                    print_debug_to_terminal('launch_external_application', 'Executed: '+command+' '+parameter)

                self.reset_ui()

                ## if enabled in ini - hide the Main UI after executing the command
                cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
                if cur_ini_value_for_hide_ui_after_command_execution == "True":
                    self.tbicon.execute_tray_icon_left_click()

            else:
                print_debug_to_terminal('launch_external_application', 'ERROR >> Checking the executable failed')
        else:
            print_debug_to_terminal('launch_external_application', 'WARNING >> command is empty, aborting')


    def open_app_url(self):
        """Method to open the application URL  (GitHub project)"""
        print_debug_to_terminal('open_app_url', 'starting')
        print_debug_to_terminal('open_app_url', 'Opening '+constants.APP_URL+' in default browser')
        webbrowser.open(constants.APP_URL)  # Go to github


    def reset_ui(self):
        """Method to reset the User-Interface of the Apps main-window"""
        print_debug_to_terminal('reset_ui', 'starting')

        ## reset the combobox
        self.ui__search_and_result_combobox.SetFocus() # set focus to search
        self.ui__search_and_result_combobox.Clear() # clear all list values
        self.ui__search_and_result_combobox.SetValue('') # clear search field

        ## reset the applications button
        self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.Enable(False)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())

        ## reset the option buttons
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.Enable(False)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## reset command
        self.ui__txt_selected_app.SetValue('')

        ## reset parameter
        self.ui__txt_selected_parameter.SetValue('')

        # reset plugin name field
        self.ui__txt_plugin_information.SetValue('')

        ## reset the result counter
        self.ui__txt_result_counter.SetValue('') # Reset result counter

        global is_resetted
        is_resetted = True

        print_debug_to_terminal('reset_ui', 'Finished resetting UI')


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
        cur_ini_value_for_language = ini.read_single_ini_value('Language', 'lang')          # get current value from ini
        t = wx.StaticText(self, -1, "Language: "+cur_ini_value_for_language, (20, 20))

        ## Hide UI
        self.cb_enable_hide_ui = wx.CheckBox(self, -1, 'Hide UI after command execution ', (20, 60))
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution')          # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == "False":
            self.cb_enable_hide_ui.SetValue(False)
        else:
            self.cb_enable_hide_ui.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_hide_ui.GetId(), self.prefs_general_toggle_hide_ui)

        ## Enable debug output
        self.cb_enable_debug = wx.CheckBox(self, -1, 'Enable debug output in commandline ', (20, 90))
        cur_ini_value_for_enable_debug = ini.read_single_ini_value('General', 'enable_debug_output')          # get current value from ini
        if cur_ini_value_for_enable_debug == "False":
            self.cb_enable_debug.SetValue(False)
        else:
            self.cb_enable_debug.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_debug.GetId(), self.prefs_general_toggle_enable_debug)


    def prefs_general_toggle_hide_ui(self, event):
        """Toggle the general pref: hide_ui"""
        print_debug_to_terminal('prefs_general_toggle_hide_ui', 'Preference - General - Hide UI: '+str(event))
        if self.cb_enable_hide_ui.GetValue() is True:
            print_debug_to_terminal('prefs_general_toggle_hide_ui', 'Enabled')
            ini.write_single_ini_value('General', 'hide_ui_after_command_execution', "True") # update preference value
        else:
            print_debug_to_terminal('prefs_general_toggle_hide_ui', 'Disabled')
            ini.write_single_ini_value('General', 'hide_ui_after_command_execution', "False") # update preference value


    def prefs_general_toggle_enable_debug(self, event):
        """Toggle the general pref: enable_debug"""
        print_debug_to_terminal('prefs_general_toggle_enable_debug', 'Preference - General - Enable Debug: '+str(event))
        if self.cb_enable_debug.GetValue() is True:
            print_debug_to_terminal('prefs_general_toggle_enable_debug', 'Enabled')
            ini.write_single_ini_value('General', 'enable_debug_output', "True") # update preference value
        else:
            print_debug_to_terminal('prefs_general_toggle_enable_debug', 'Disabled')
            ini.write_single_ini_value('General', 'enable_debug_output', "False") # update preference value


class UITabStatistics(wx.Panel):

    """Preference Window - Tab: Statistics - Shows usage stats"""

    def __init__(self, parent):
        """Inits the statistics tab"""
        wx.Panel.__init__(self, parent)

        ## show app start counter
        cur_ini_value_for_apparat_started = ini.read_single_ini_value('Statistics', 'apparat_started')          # get current value from ini
        t = wx.StaticText(self, -1, "Apparat started:\t\t\t"+cur_ini_value_for_apparat_started, (20, 20))

        ## show execute counter
        cur_ini_value_for_command_executed = ini.read_single_ini_value('Statistics', 'command_executed')          # get current value from ini
        t = wx.StaticText(self, -1, "Command executed:\t\t"+cur_ini_value_for_command_executed, (20, 40))

        ## show plugin trigger count
        cur_ini_value_for_plugin_executed = ini.read_single_ini_value('Statistics', 'plugin_executed')          # get current value from ini
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

        plugin_internet_search_cmd_list = wx.StaticText(self, -1, "!a = Amazon\n!b = Bandcamp\n!e = Stack-Exchange\n!g = Google\n!l = LastFM\n!o = Stack-Overflow\n!r = Reddit\n!s = SoudCloud\n!t = Twitter\n!v = Vimeo\n!w = Wikipedia\n!y = YouTube", (20, 140))
        plugin_internet_search_cmd_list.SetFont(FONT_NORMAL_MONO)

        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)
        pref_sizer.Add(h1_plugin_session, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_session_cmd_list, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(10)
        pref_sizer.Add(h1_plugin_internet_search, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_internet_search_cmd_list, 0, wx.ALL, border=10)
        #pref_sizer.AddSpacer(100)
        self.SetSizer(pref_sizer)


class UITabAbout(wx.Panel):

    """Preference Window - Tab: About"""

    def __init__(self, parent):
        """Inits the About Tab"""
        wx.Panel.__init__(self, parent)

        about_app_icon = wx.Bitmap('gfx/core/bt_appIcon_128.png', wx.BITMAP_TYPE_BMP)
        about_app_icon_static = wx.StaticBitmap(self, -1, about_app_icon)

        about_app_name = wx.StaticText(self, -1, constants.APP_NAME, (20, 20))
        about_app_name.SetFont(FONT_BIG)

        about_app_description = wx.StaticText(self, -1, "An application launcher for Linux", (20, 20))
        about_app_description.SetFont(FONT_NORMAL_MONO)

        about_app_version = wx.StaticText(self, -1, "Version: "+config.APP_VERSION, (20, 60))
        about_app_version.SetFont(FONT_NORMAL_MONO)

        about_app_license = wx.StaticText(self, -1, "License: "+constants.APP_LICENSE, (20, 80))
        about_app_license.SetFont(FONT_NORMAL_MONO)

        about_app_github_icon = wx.Bitmap('gfx/core/bt_github_32.png', wx.BITMAP_TYPE_BMP)
        about_app_github_icon_static = wx.StaticBitmap(self, -1, about_app_github_icon)

        about_app_url = wx.HyperlinkCtrl(self, id=-1, label=constants.APP_URL, url=constants.APP_URL, pos=(20, 140))
        about_app_url.SetFont(FONT_NORMAL_MONO)

        pref_about_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_about_sizer.AddSpacer(20)
        pref_about_sizer.Add(about_app_icon_static, flag=wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(10)
        pref_about_sizer.Add(about_app_name, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(20)
        pref_about_sizer.Add(about_app_description, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(20)
        pref_about_sizer.Add(about_app_version, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(20)
        pref_about_sizer.Add(about_app_license, 0, wx.ALIGN_CENTER)
        pref_about_sizer.AddSpacer(80)
        pref_about_sizer.Add(about_app_github_icon_static, 0, wx.ALIGN_CENTER)
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
        wx.Frame.__init__(self, parent, id, constants.APP_NAME+' Preferences', size=(600, 500), style=pref_window_style)

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
        print_debug_to_terminal('close_preference_ui', 'starting')
        print_debug_to_terminal('close_preference_ui', 'Event: '+str(event))
        self.Destroy() # close the pref UI

        # TODO: set focus to mainwindow


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY-MENU
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_menu_item(menu, label, func):
    """Generates single menu items for the tray icon popup menu"""
    print_debug_to_terminal('create_menu_item', 'Menuitem: '+label)
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
        print_debug_to_terminal('__init__ (TaskBarIcon)', 'starting')
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_tray_icon(constants.APP_TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_app_tray_icon_left_click)
        print_debug_to_terminal('__init__ (TaskBarIcon)', 'Task icon is ready now')


    def CreatePopupMenu(self):
        """Method to generate a Popupmenu for the TrayIcon (do NOT rename)"""
        print_debug_to_terminal('CreatePopupMenu', 'starting')
        menu = wx.Menu()
        create_menu_item(menu, 'Preferences', self.on_tray_popup_click_preferences)
        create_menu_item(menu, 'GitHub', self.on_tray_popup_click_github)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_tray_popup_click_exit)
        return menu


    def set_tray_icon(self, path):
        """Method to set the icon for the TrayIconMenu item"""
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, constants.APP_TRAY_TOOLTIP)


    def on_app_tray_icon_left_click(self, event):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        print_debug_to_terminal('on_app_tray_icon_left_click', 'starting')
        print_debug_to_terminal('on_app_tray_icon_left_click', 'Event: '+str(event))
        self.execute_tray_icon_left_click()


    def execute_tray_icon_left_click(self):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        print_debug_to_terminal('execute_tray_icon_left_click', 'starting')
        if self.frame.IsIconized(): # if main window is minimized
            print_debug_to_terminal('execute_tray_icon_left_click', 'MainWindow was minimized - should show it now')
            self.frame.Raise()
        else: # if main window is shown
            print_debug_to_terminal('execute_tray_icon_left_click', 'MainWindow was shown - should minimize it now')
            self.frame.Iconize(True)


    def on_tray_popup_click_preferences(self, event):
        """Method to handle click in the 'Preferences' tray menu item"""
        print_debug_to_terminal('on_tray_popup_click_preferences', 'starting')
        print_debug_to_terminal('on_tray_popup_click_preferences', 'Event: '+str(event))
        self.open_preference_window()


    def on_tray_popup_click_exit(self, event):
        """Method to handle click in the 'Exit' tray menu item"""
        print_debug_to_terminal('on_tray_popup_click_exit', 'starting')
        print_debug_to_terminal('on_tray_popup_click_exit', 'Event: '+str(event))
        wx.CallAfter(self.frame.Close)


    def on_tray_popup_click_github(self, event):
        """Method to handle click on the 'GitHub' tray menu item"""
        print_debug_to_terminal('on_tray_popup_click_github', 'starting')
        print_debug_to_terminal('on_tray_popup_click_github', 'Event: '+str(event))
        print_debug_to_terminal('on_tray_popup_click_github', 'Opening: '+constants.APP_URL)
        webbrowser.open(constants.APP_URL) # Go to github


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(wx.App):

    """Class App"""

    def OnInit(self):
        """While starting the app (checks for already running instances)"""
        self.name = constants.APP_NAME
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning(): # allow only 1 instance of apparat
            wx.MessageBox("An instance of "+constants.APP_NAME+" is already running. Aborting", "Error", wx.OK | wx.ICON_WARNING)
            return False
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """Main"""
    app = App(False)
    #helperFunctions.external_func_test() # test function from external .py file
    check_platform() # Check if platform is supported at all, otherwise abort
    check_linux_requirements()
    frame = MyFrame(None, constants.APP_NAME) # Main UI window
    app.MainLoop()


if __name__ == '__main__':
    print_debug_to_terminal('__main__', 'starting')
    main()

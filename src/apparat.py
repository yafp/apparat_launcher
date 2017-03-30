#!/usr/bin/python
"""apparat - an application launcher for linux"""

# NAME:         apparat
# DESCRIPTION:  an application launcher for linux
# AUTHOR:       yafp
# URL:          https://github.com/yafp/apparat


# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------
import sys                          # to show python version used

if sys.version_info >= (3, 0):
    sys.stdout.write('Python version used: '+sys.version) ## show python version
    sys.stdout.write('Sorry, requires Python 2.x, not Python 3.x. Code might not work on Python3\n')
    sys.exit(1)

else: # python 2.x
    ## built-in modules
    import difflib                      # for intelligent list sort
    import fnmatch                      # for searching applications
    import os                           # for searching applications
    import platform
    import subprocess                   # for checking if cmd_exists
    import webbrowser                   # for opening urls (example: github project page)
    import wx                           # for all the WX GUI items

    ## projects internal modules
    import constants                    # contains some constants
    import config                       # contains some config values
    import ini                          # ini file handling
    import prefs
    import tools                        # contains helper-tools
    import plugin_search_local
    import plugin_search_internet
    import plugin_screenshot
    import plugin_nautilus
    import plugin_session

    ## GTK vs WX is a mess - Issue: #15 - It helps to import GTK after having created the WX app (at least for Ubuntu, not for Fedora)
    #
    # Ubuntu (import gtk) vs Fedora (from gi.repository import Gtk)
    if 'Ubuntu' in platform.linux_distribution():
        pass
        #print ('Ubuntu') # tested on 16.04
        #import gtk # after wx init

    elif 'Fedora' in platform.linux_distribution():
        #print ('Fedora') # tested on 25
        #gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk

    else:
        print('Here be dragons (untested distribution)')



# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
is_combobox_open = 0
is_resetted = True


# -----------------------------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------------------------


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN-WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MyFrame(wx.Frame):

    """Class for MainWindow"""

    def __init__(self, parent, title):
        """Initialize the MainWindow"""
        ## Update Statistics (ini) - Apparat launched
        tools.debug_output('__init__', 'Updating statistics (apparat_started)')
        cur_app_start_count = ini.read_single_value('Statistics', 'apparat_started')          # get current value from ini
        ini.write_single_value('Statistics', 'apparat_started', int(cur_app_start_count)+1)    # update ini +1

        ## Define the style of the frame
        main_ui_style = (wx.MINIMIZE_BOX | wx.CLIP_CHILDREN | wx.NO_BORDER | wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR)

        self.mainUI = wx.Frame.__init__(self, parent, title=title, size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT), style=main_ui_style) # Custom Frame
        self.SetSizeHintsSz(wx.Size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT), wx.Size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)) # forcing min and max size to same values - prevents resizing option
        self.tbicon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close_application)

        ## define and set an application icon
        app_icon = wx.Icon('gfx/core/bt_appIcon_16.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(app_icon)

        # ------------------------------------------------
        # Define UI Elements
        # ------------------------------------------------
        # Some general bitmaps which might be needed for some button states
        self.ui_bt_img_search = wx.Bitmap('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_BMP)
        self.ui_bt_img_blank = wx.Bitmap('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_BMP)
        self.ui_bt_img_execute_black = wx.Bitmap('gfx/core/bt_execute_128_black.png', wx.BITMAP_TYPE_BMP)

        ## Preference button
        self.ui__bt_prefs_img = wx.Bitmap('gfx/core/bt_prefs_16.png', wx.BITMAP_TYPE_BMP)
        self.ui__bt_prefs_img_focus = wx.Bitmap('gfx/core/bt_prefs_16_black.png', wx.BITMAP_TYPE_BMP) # #c0392b
        self.ui__bt_prefs = wx.BitmapButton(self, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=self.ui__bt_prefs_img, size=(self.ui__bt_prefs_img.GetWidth()+10, self.ui__bt_prefs_img.GetHeight()+10))
        self.ui__bt_prefs.SetBitmapFocus(self.ui__bt_prefs_img_focus)
        self.ui__bt_prefs.SetBitmapHover(self.ui__bt_prefs_img_focus)
        self.ui__bt_prefs.SetLabel('Preferences')
        self.ui__bt_prefs.SetToolTipString(u'Preferences')

        ## result counter
        self.ui__txt_result_counter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE)
        self.ui__txt_result_counter.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_result_counter.SetToolTipString(u'Results')
        self.ui__txt_result_counter.SetMinSize(wx.Size(50, 50))
        self.ui__txt_result_counter.SetMaxSize(wx.Size(50, 50))
        self.ui__txt_result_counter.SetEditable(False)
        self.ui__txt_result_counter.Enable(False)
        self.ui__txt_result_counter.SetValue('0')

        ## Search & Results as comboBox
        search_results = []
        combo_box_style = wx.TE_PROCESS_ENTER
        self.ui__cb_search = wx.ComboBox(self, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size(550, 50), search_results, style=combo_box_style)
        self.ui__cb_search.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        # TODO: check if wx.ComboCtrl is better

        ## Plugin Information
        self.ui__txt_plugin_information = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE | wx.TE_RICH2)
        self.ui__txt_plugin_information.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_plugin_information.SetMinSize(wx.Size(600, 18))
        self.ui__txt_plugin_information.SetMaxSize(wx.Size(600, 18))
        self.ui__txt_plugin_information.Enable(False)
        self.ui__txt_plugin_information.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## app button
        self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(300, 300), wx.BU_AUTODRAW)
        self.ui__bt_selected_app.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmapDisabled(self.ui_bt_img_search)
        #self.ui__bt_selected_app.SetBitmapSelected(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetLabel('Applications')
        self.ui__bt_selected_app.Enable(False)

        ## parameter button
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(300, 300), wx.BU_AUTODRAW)
        self.ui__bt_selected_parameter.SetBitmapFocus(wx.NullBitmap) # image when in focus
        self.ui__bt_selected_parameter.SetBitmapHover(self.ui_bt_img_execute_black) # image on hover
        self.ui__bt_selected_parameter.SetBitmapDisabled(self.ui_bt_img_blank)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.SetLabel('Options')
        self.ui__bt_selected_parameter.Enable(False)

        ## app text
        self.ui__txt_selected_app = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_app.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_app.SetToolTipString(u'Command')
        self.ui__txt_selected_app.SetMinSize(wx.Size(300, 18))
        self.ui__txt_selected_app.SetMaxSize(wx.Size(300, 18))
        self.ui__txt_selected_app.Enable(False)
        self.ui__txt_selected_app.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## parameter text
        self.ui__txt_selected_parameter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_parameter.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_parameter.SetToolTipString(u'Parameter')
        self.ui__txt_selected_parameter.SetMinSize(wx.Size(300, 18))
        self.ui__txt_selected_parameter.SetMaxSize(wx.Size(300, 18))
        self.ui__txt_selected_parameter.Enable(False)
        self.ui__txt_selected_parameter.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## Version Information
        self.ui__txt_version_information = wx.StaticText(self, wx.ID_ANY, ' v'+config.APP_VERSION, wx.DefaultPosition, wx.DefaultSize, 0)
        self.ui__txt_version_information.Wrap(-1)
        self.ui__txt_version_information.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_version_information.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))


        # ------------------------------------------------
        # Layout/Sizer
        # ------------------------------------------------
        b_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container

        b_sizer.Add(self.ui__bt_prefs, 0, wx.ALIGN_RIGHT, 100) # preferences icon button
        b_sizer.AddSpacer(5)

        # horizontal sub-item 1
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self.ui__txt_result_counter, 0, wx.CENTRE) # result counter
        box1.Add(self.ui__cb_search, 0, wx.CENTRE) # combobox
        b_sizer.Add(box1, 0, wx.CENTRE)
        b_sizer.AddSpacer(5)

        b_sizer.Add(self.ui__txt_plugin_information, 0, wx.CENTRE) # plugin info
        b_sizer.AddSpacer(5)

        # horizontal sub-item 2
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(self.ui__bt_selected_app, 0, wx.CENTRE) # application button
        box2.Add(self.ui__bt_selected_parameter, 0, wx.CENTRE) # parameter button
        b_sizer.Add(box2, 0, wx.CENTRE)

        # horizontal sub-item 3
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add(self.ui__txt_selected_app, 0, wx.CENTRE) # command
        box3.Add(self.ui__txt_selected_parameter, 0, wx.CENTRE) # parameter
        b_sizer.Add(box3, 0, wx.CENTRE)

        b_sizer.AddSpacer(10)

        b_sizer.Add(self.ui__txt_version_information, 0, wx.CENTRE) # version
        self.SetSizer(b_sizer)


        # ------------------------------------------------
        # Bind/Connect Events
        # ------------------------------------------------
        self.ui__bt_prefs.Bind(wx.EVT_BUTTON, self.on_clicked)

        ## combobox
        self.ui__cb_search.Bind(wx.EVT_KEY_UP, self.on_combobox_key_press)                 # Pressed any key
        self.ui__cb_search.Bind(wx.EVT_TEXT, self.on_combobox_text_changed)                # combobox text changes.
        self.ui__cb_search.Bind(wx.EVT_TEXT_ENTER, self.on_combobox_enter)                 # Pressed Enter
        self.ui__cb_search.Bind(wx.EVT_COMBOBOX, self.on_combobox_select_item)             # Item selected
        self.ui__cb_search.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_combobox_popup_open)     # Popup opened
        self.ui__cb_search.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.on_combobox_popup_close)     # Popup closed

        ## parameter button
        self.ui__bt_selected_parameter.Bind(wx.EVT_BUTTON, self.on_clicked_option_button)


        ## Handle clicks outside of the expected area 8main ui or none
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        # ------------------------------------------------
        # show the UI
        # ------------------------------------------------
        self.SetTransparent(config.TRANSPARENCY_VALUE)       # 0-255
        self.ui__cb_search.SetFocus()     # set focus to search
        self.Center()                   # open window centered
        self.Show(True)                 # show main UI

        if 'Ubuntu' in platform.linux_distribution():
            import gtk
            global gtk


    def on_key_down(self, event):
        """On Key Down in main ui"""
        tools.debug_output('OnKeyDown', 'starting with event: '+str(event))
        tools.debug_output('OnKeyDown', 'Currently focus is at: '+str(self.FindFocus()))
        self.ui__cb_search.SetFocus() # set focus to search
        self.ui__cb_search.SetInsertionPointEnd() # set cursor to end of string
        tools.debug_output('OnKeyDown', 'Set focus back to search.')


    def on_close_application(self, event):
        """Method to close the app"""
        tools.debug_output('on_close_application', 'starting with event: '+str(event))
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()
        wx.GetApp().ExitMainLoop()
        event.Skip()


    def on_clicked_option_button(self, event):
        """If the launch option button was clicked"""
        tools.debug_output('on_clicked_option_button', 'starting with event: '+str(event))
        self.do_execute()
        self.ui__cb_search.SetFocus()


    def on_clicked(self, event):
        """General click handler - using label to find source"""
        tools.debug_output('on_clicked', 'starting with event: '+str(event))
        btn = event.GetEventObject().GetLabel()
        if btn == 'Preferences':
            tools.debug_output('on_clicked', 'Preferences')
            self.open_preference_window()
        else:
            tools.debug_output('on_clicked', 'Something else got clicked')


    def open_preference_window(self):
        """Opens the preference window"""
        tools.debug_output('open_preference_window', 'starting')
        self.prefWindow = prefs.PreferenceWindow(parent=None, id=-1)
        self.prefWindow.Show()


    def on_combobox_text_changed(self, event):
        """Triggered if the combobox text changes"""
        tools.debug_output('on_combobox_text_changed', 'starting with event:'+str(event))

        if self.ui__cb_search.GetValue() == '': #searchstring is empty
            tools.debug_output('on_combobox_text_changed', 'Searchstring: <empty>. Nothing do to')
        else:
            tools.debug_output('on_combobox_text_changed', 'Searchstring: '+self.ui__cb_search.GetValue())
            global is_resetted
            is_resetted = False


    def on_combobox_enter(self, event):
        """Triggered if Enter was pressed in combobox"""
        tools.debug_output('on_combobox_enter', 'starting with event: '+str(event))

        if len(self.ui__cb_search.GetValue()) > 0:
            global is_resetted
            is_resetted = False

            global is_combobox_open
            if is_combobox_open == 0:
                self.do_execute()

            else: # enter was pressed to close the combobox
                tools.debug_output('on_combobox_enter', 'Pressed enter to close the open combobox')
                is_combobox_open = 0    # global var to keep track if dropdown is open or closed

                ## run search again after selecting the desired search string from dropdown
                self.parse_user_search_input(self.ui__cb_search.GetValue())
        else:
            tools.debug_output('on_combobox_enter', 'Combobox is empty, nothing to do here.')


    def on_combobox_select_item(self, event):
        """If an item of the result-list was selected"""
        tools.debug_output('on_combobox_select_item', 'starting with event: '+str(event))

        if(self.ui__txt_plugin_information.GetValue() == 'Plugin: Local Search'): # Local search is always using xdg-open - special case
            self.ui__txt_selected_parameter.SetValue(self.ui__cb_search.GetValue())   # write command to command text field
        else: # default-case
            self.ui__txt_selected_app.SetValue(self.ui__cb_search.GetValue())   # write command to command text field
            self.get_icon_for_executable(self.ui__cb_search.GetValue()) # get icon for selected executable
        self.ui__cb_search.SetInsertionPointEnd() # set cursor to end of string
        tools.debug_output('on_combobox_select_item', 'finished')


    def on_combobox_popup_open(self, event):
        """If the popup of the combobox gets opened"""
        tools.debug_output('on_combobox_popup_open', 'starting with event: '+str(event))
        global is_combobox_open
        is_combobox_open = True

        ## select the first item from list
        self.ui__cb_search.SetSelection(0) # is default
        if 'Ubuntu' in platform.linux_distribution():
            subprocess.Popen(["xdotool", "key", "Down"]) # simulate key press to highlight the choosen value as well

        tools.debug_output('on_combobox_popup_open', 'finished')


    def on_combobox_popup_close(self, event):
        """If the popup of the combobox is closed"""
        tools.debug_output('on_combobox_popup_close', 'starting with event: '+str(event))
        tools.debug_output('on_combobox_popup_close', 'combobox just got closed')
        self.get_icon_for_executable(self.ui__cb_search.GetValue()) # get icon for selected executable
        global is_combobox_open
        is_combobox_open = False
        tools.debug_output('on_combobox_popup_close', 'finished')


    def on_combobox_key_press(self, event):
        """If content of the searchfield of the combobox changes"""
        tools.debug_output('on_combobox_key_press', 'starting with event: '+str(event))
        global is_combobox_open

        current_keycode = event.GetKeyCode()
        tools.debug_output('on_combobox_key_press', 'KeyCode: '+str(current_keycode))

        if current_keycode == 27: # ESC
            tools.debug_output('on_combobox_key_press', 'ESC in combobox')
            if(is_resetted is False):
                tools.debug_output('on_combobox_key_press', 'Launch reset method')
                self.reset_ui()
            else: # hide main window
                tools.debug_output('on_combobox_key_press', 'UI is already resetted')
                self.tbicon.execute_tray_icon_left_click()

        elif current_keycode == 317:    # Arrow Down
            tools.debug_output('on_combobox_key_press', 'ARROW DOWN in combobox')
            if(self.ui__txt_result_counter.GetValue() != '0'):
                self.ui__cb_search.Popup()
                tools.debug_output('on_combobox_key_press', 'Opening dropdown')
                is_combobox_open = 1
            else:
                tools.debug_output('on_combobox_key_press', 'No result, so no need to open the dropdown')
                is_combobox_open = 0

        elif current_keycode == 13: # Enter
            tools.debug_output('on_combobox_key_press', 'ENTER was pressed - ignoring it because of "on_combobox_enter"')
            self.parse_user_search_input(self.ui__cb_search.GetValue())
            is_combobox_open = 0

        else:
            current_search_string = self.ui__cb_search.GetValue()
            if len(current_search_string) == 0:
                tools.debug_output('on_combobox_key_press', 'Searchstring: <empty>. Nothing do to')
                self.reset_ui()
            else:
                tools.debug_output('on_combobox_key_press', 'Searching: '+current_search_string)
                self.parse_user_search_input(current_search_string)


    def get_icon_for_executable(self, full_executable_name):
        """Tries to get an icon for an selected executable"""
        # Abort if a plugin is activated
        if(self.ui__txt_plugin_information.GetValue() != ''):
            return

        ## Icon search - http://www.pygtk.org/pygtk2reference/class-gtkicontheme.html
        #
        ## get app-icon for selected application from operating system

        # Ubuntu
        if 'Ubuntu' in platform.linux_distribution():
            icon_theme = gtk.icon_theme_get_default()

        # Fedora
        if 'Fedora' in platform.linux_distribution():
            icon_theme = Gtk.IconTheme.get_default()

        ## check what icon sizes are available and choose best size
        available_icon_sizes = icon_theme.get_icon_sizes(full_executable_name)
        if not available_icon_sizes: # if we got no list of available icon sizes - Fallback: try to get a defined size
            max_icon_size = 64
            icon_info = icon_theme.lookup_icon(full_executable_name, max_icon_size, 0)
        else:
            tools.debug_output('get_icon_for_executable', 'Found several icon sizes: '+str(available_icon_sizes))
            max_icon_size = max(available_icon_sizes) ## pick the biggest
            tools.debug_output('get_icon_for_executable', 'Picking the following icon size: '+str(max_icon_size))
            icon_info = icon_theme.lookup_icon(full_executable_name, max_icon_size, 0)

        if icon_info is None:
            new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
        else:
            icon_path = icon_info.get_filename()

            if icon_path != '': # found icon
                if '.svg' not in icon_path:
                    new_app_icon = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)    # define new image
                    #new_app_iconWidth=new_app_icon.GetWidth()                   # get icon width
                    tools.debug_output('get_icon_for_executable', 'Found icon: '+icon_path+' ('+str(max_icon_size)+'px)')
                    if config.TARGET_ICON_SIZE == max_icon_size: # if icon has expected size
                        tools.debug_output('get_icon_for_executable', 'Icon size is as expected')
                    else: # resize icon
                        tools.debug_output('get_icon_for_executable', 'Icon size does not match, starting re-scaling to '+str(config.TARGET_ICON_SIZE)+'px')
                        new_app_icon.Rescale(config.TARGET_ICON_SIZE, config.TARGET_ICON_SIZE) # rescale image
                else: # found unsupported icon format
                    tools.debug_output('get_icon_for_executable', 'SVG icons ('+icon_path+') can not be used so far. Using a dummy icon for now')
                    new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
            else: # no icon
                tools.debug_output('get_icon_for_executable', 'Found no icon')
                new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)

        ## application button
        self.ui__bt_selected_app.SetBitmap(new_app_icon.ConvertToBitmap()) # set icon to button
        self.ui__bt_selected_app.Enable(True) # Enable the Button

        ## option buttons
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.Enable(True) # Enable option button
        self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip


    def plugin__internet_search_execute(self, command, parameter):
        """Plugin: Internet-Search - Execute the actual internet search call"""
        tools.debug_output('plugin__internet_search_execute', 'starting')

        if command == '!a':
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_A+parameter

        elif command == ('!b'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_B+parameter

        elif command == ('!e'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_E+parameter

        elif command == ('!g'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_G+parameter

        elif command == ('!l'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_L+parameter

        elif command == ('!m'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_M+parameter

        elif command == ('!o'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_O+parameter

        elif command == ('!r'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_R+parameter

        elif command == ('!s'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_S+parameter

        elif command == ('!t'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_T+parameter

        elif command == ('!v'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_V+parameter

        elif command == ('!w'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_W+parameter

        elif command == ('!y'):
            remote_url = constants.PLUGIN_INTERNET_SEARCH_URL_Y+parameter

        else:
            tools.debug_output('plugin__internet_search_execute', 'Error: unexpected case in "plugin__internet_search_execute"')

        ## for all - open the URL
        webbrowser.open(remote_url)

        ## update usage-statistics
        tools.debug_output('plugin__internet_search_execute', 'Updating statistics (plugin_executed)')
        current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed')          # get current value from ini
        ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1)    # update ini +1

        self.reset_ui()

        ## if enabled in ini - hide the Main UI after executing the command
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == 'True':
            self.tbicon.execute_tray_icon_left_click()


    def plugin__update_general_ui_information(self, plugin_name):
        """set some general UI values after having a plugin triggered"""
        tools.debug_output('plugin__update_general_ui_information', 'started')

        if(plugin_name != ''):
            # application buttons
            self.ui__bt_selected_app.Enable(True)

            ## parameter button
            self.ui__bt_selected_parameter.Enable(True) # Enable option button

            ## set result-count
            self.ui__txt_result_counter.SetValue('1')

            ## update command (Example: !g)
            self.ui__txt_selected_app.SetValue(self.ui__cb_search.GetValue()[:2])

            # Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue('Plugin: '+plugin_name)

            tools.debug_output('plugin__update_general_ui_information', 'Plugin '+plugin_name+' activated')

        else:
            # application buttons
            self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
            self.ui__bt_selected_app.Enable(False)

            ## parameter button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.SetToolTipString('')
            self.ui__bt_selected_parameter.Enable(False) # Enable option button

            ## set result-count
            self.ui__txt_result_counter.SetValue('0')

            # Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue(plugin_name)

            self.ui__txt_selected_app.SetValue('')
            self.ui__txt_selected_parameter.SetValue('')


    def prepare_plugin_misc_open(self):
        """Plugin Misc - Open"""
        tools.debug_output('prepare_plugin_misc_open', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Misc (Open)')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/misc/bt_open_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Open')

        if(self.ui__cb_search.GetValue()[6:] != ''):
            ## parameter buttons
            self.ui__bt_selected_parameter.SetToolTipString('Open')
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

            # set parameter
            self.ui__txt_selected_parameter.SetValue(self.ui__cb_search.GetValue()[6:])

        ## set command
        self.ui__txt_selected_app.SetValue('xdg-open')


    def prepare_plugin_shell(self):
        """Plugin Shell"""
        tools.debug_output('prepare_plugin_shell', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Shell')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/shell/bt_shell_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Lock Session')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        ## http://askubuntu.com/questions/484993/run-command-on-anothernew-terminal-window
        self.ui__txt_selected_app.SetValue('xterm')
        self.ui__txt_selected_parameter.SetValue(self.ui__cb_search.GetValue()[4:])


    def parse_user_search_input(self, current_search_string):
        """Method to search applications and/or plugin commands to fill the results"""
        tools.debug_output('parse_user_search_input', 'starting')

        #self.SetCursor(wx.StockCursor(wx.CURSOR_WATCH)) # change cursor

        if current_search_string != '': # if there is a search string

            ## Reset UI partly if search is just !
            #
            if current_search_string == '!':
                tools.debug_output('parse_user_search_input', 'Case: !')
                self.plugin__update_general_ui_information('')
                return

            ## Plugin: Misc
            ##
            if  current_search_string.startswith(constants.APP_PLUGINS_MISC_TRIGGER):
                tools.debug_output('parse_user_search_input', 'Case: Plugin Misc')
                if current_search_string.startswith('!open'):
                    tools.debug_output('parse_user_search_input', 'Case: Plugin Misc - Open')
                    self.prepare_plugin_misc_open()
                    return
                else:
                    tools.debug_output('parse_user_search_input', 'Error: unexpected misc plugin command')
                    return


            ## Plugin: Screenshot
            ##
            if  current_search_string in constants.APP_PLUGINS_SCREENSHOT_TRIGGER:
                plugin_screenshot.prepare_general(current_search_string, self)
                return


            ## Plugin: Nautilus
            ##
            if current_search_string in constants.APP_PLUGINS_NAUTILUS_TRIGGER or current_search_string.startswith('!goto'):
                plugin_nautilus.prepare_general(current_search_string, self)
                return


            ## Plugin: Session
            ##
            if current_search_string in constants.APP_PLUGINS_SESSION_TRIGGER:
                plugin_session.prepare_general(current_search_string, self)
                return


            ## Plugin: Shell
            ##user alias in linux like mac
            if  current_search_string.startswith(constants.APP_PLUGINS_SHELL_TRIGGER):
                tools.debug_output('parse_user_search_input', 'Case: Plugin Shell')
                if current_search_string.startswith('!sh'):
                    self.prepare_plugin_shell()
                    return
                else:
                    tools.debug_output('parse_user_search_input', 'Error: unexpected shell plugin command')
                    return


            ## Plugin: Internet-Search
            ##
            if current_search_string.startswith(constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER):
                tools.debug_output('parse_user_search_input', 'Case: Plugin Internet-Search')
                plugin_search_internet.plugin__internet_search_prepare(self, current_search_string)
                return


            ## Search for local files
            #
            if current_search_string.startswith(constants.APP_PLUGINS_SEARCH_LOCAL_TRIGGER):
            #if current_search_string.startswith('?'):
                tools.debug_output('parse_user_search_input', 'Case: Plugin Local-Search')
                plugin_search_local.search_user_files(self, current_search_string)
                return


            ## Search for executables
            #
            self.search_executables(current_search_string)


        else: # search string is empty
            tools.debug_output('parse_user_search_input', 'Empty search string')


    def search_executables(self, current_search_string):
        """Searches for executables"""
        self.plugin__update_general_ui_information('')

        tools.debug_output('search_executables', 'Searching executables for the following string: '+current_search_string)
        search_results = fnmatch.filter(os.listdir('/usr/bin'), '*'+current_search_string+'*')     # search for executables matching users searchstring

        ## Sort results - http://stackoverflow.com/questions/17903706/how-to-sort-list-of-strings-by-best-match-difflib-ratio
        search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

        self.ui__txt_result_counter.SetValue(str(len(search_results))) # update result count
        self.ui__cb_search.SetItems(search_results) # update combobox

        tools.debug_output('search_executables', 'Found '+str(len(search_results))+' matching application')
        if len(search_results) == 0: # 0 result
            ## update launch button icon
            self.ui__bt_selected_app.Enable(True)
            if current_search_string.startswith('!'): # starting input for plugins
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

        elif len(search_results) == 1: # 1 result
            # combobox - autocomplete if it makes sense
            #
            #if(search_results[0].startswith(current_search_string)): # if only result starts with search_string - autocomplete and mark critical completed part
                #self.ui__cb_search.SetValue(search_results[0])
                #self.ui__cb_search.SetInsertionPoint(len(current_search_string))
                #self.ui__cb_search.SetMark(len(current_search_string)-1, len(search_results[0]))
                #self.ui__cb_search.SetMark(len(current_search_string), len(search_results[0]))

            ## application buttons
            self.ui__bt_selected_app.Enable(True) # Enable application button
            self.ui__bt_selected_app.SetToolTipString(search_results[0]) # set tooltip

            ## options buttons
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.Enable(True) # Enable option button
            self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip

            ## update command
            self.ui__txt_selected_app.SetValue(search_results[0])

            ## update parameter
            self.ui__txt_selected_parameter.SetValue('')

            ## Icon search
            self.get_icon_for_executable(str(search_results[0]))

        else: # > 1 search

            ## application button
            self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_list_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_app.Enable(True)
            self.ui__bt_selected_app.SetToolTipString(search_results[0])

            # update launch-options button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.Enable(False)                                  # Enable option button
            self.ui__bt_selected_parameter.SetToolTipString('Launch')

            ## update parameter
            self.ui__txt_selected_parameter.SetValue('')

            # get icon for primary search result
            self.get_icon_for_executable(search_results[0])

            # assume first search result is the way to go
            self.ui__txt_selected_app.SetValue(search_results[0])


    def do_execute(self):
        """Launches the actual task"""
        # get command and parameter inforations
        command = self.ui__txt_selected_app.GetValue()
        parameter = self.ui__txt_selected_parameter.GetValue()

        if(command == ''):
            tools.debug_output('do_execute', 'Nothing to do - empty command')
            return

        tools.debug_output('do_execute', 'starting with command: "'+command+'" and parameter: "'+parameter+'"')


        ## Plugin: Misc - Open
        ##
        if self.ui__txt_plugin_information.GetValue() == 'Plugin: Misc (Open)':
            if parameter == '':
                return


        ## Plugin: Shell
        ##
        #if self.ui__txt_plugin_information.GetValue() == 'Plugin: Shell':
            #command = command +' '+ parameter
            #parameter = ''


        ## Plugin: Internet-Search
        ##
        if command in constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER:
            self.plugin__internet_search_execute(command, parameter)
            return


        ## Plugin: Session/Screenshot/Nautilus OR normal application
        ##
        if command is not None: # Check if the dropdown contains something at all or not
            tools.debug_output('do_execute', 'Should execute: "'+command+'" with parameter: "'+parameter+'"')

            ## check if name exists and is executable
            executable_exists = tools.cmd_exists(command)
            if executable_exists is True:
                tools.debug_output('do_execute', 'Executable: "'+command+'" exists')

                ## update usage-statistics
                #
                ## commands executed
                tools.debug_output('do_execute', 'Updating statistics (command_executed)')
                current_commands_executed_count = ini.read_single_value('Statistics', 'command_executed')          # get current value from ini
                ini.write_single_value('Statistics', 'command_executed', int(current_commands_executed_count)+1) # update ini +1

                ## update plugin execution count
                if self.ui__txt_plugin_information != '':
                    tools.debug_output('do_execute', 'Updating statistics (plugins_executed)')
                    current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed')          # get current value from ini
                    ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

                if parameter == '':
                    #subprocess.Popen(["rm","-r","some.file"])
                    subprocess.Popen([command])
                    tools.debug_output('do_execute', 'Executed: "'+command+'"')

                else:
                    subprocess.Popen([command, parameter])
                    tools.debug_output('do_execute', 'Executed: "'+command+'" with parameter: "'+parameter+'"')

                self.reset_ui()

                ## if enabled in ini - hide the Main UI after executing the command
                cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
                if cur_ini_value_for_hide_ui_after_command_execution == 'True':
                    self.tbicon.execute_tray_icon_left_click()

            else:
                tools.debug_output('do_execute', 'ERROR >> Checking the executable failed')
        else:
            tools.debug_output('do_execute', 'WARNING >> command is empty, aborting')


    def open_app_url(self):
        """Method to open the application URL  (GitHub project)"""
        tools.debug_output('open_app_url', 'starting')
        tools.debug_output('open_app_url', 'Opening '+constants.APP_URL+' in default browser')
        webbrowser.open(constants.APP_URL)  # Go to github
        tools.debug_output('open_app_url', 'finished')


    def reset_ui(self):
        """Method to reset the User-Interface of the Apps main-window"""
        tools.debug_output('reset_ui', 'starting')

        ## reset the combobox
        self.ui__cb_search.SetFocus() # set focus to search
        self.ui__cb_search.Clear() # clear all list values
        self.ui__cb_search.SetValue('') # clear search field

        ## reset the applications button
        self.ui__bt_selected_app.Enable(False)

        ## reset the option buttons
        self.ui__bt_selected_parameter.Enable(False)
        self.ui__bt_selected_parameter.SetToolTipString('')

        ## reset txt command
        self.ui__txt_selected_app.SetValue('')

        ## reset txt parameter
        self.ui__txt_selected_parameter.SetValue('')

        # reset plugin name field
        self.ui__txt_plugin_information.SetValue('')

        ## reset the result counter
        self.ui__txt_result_counter.SetValue('0')

        global is_resetted
        is_resetted = True

        tools.debug_output('reset_ui', 'Finished resetting UI')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY-MENU
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_menu_item(menu, label, func):
    """Generates single menu items for the tray icon popup menu"""
    tools.debug_output('create_menu_item', 'Menuitem: '+label)
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
        tools.debug_output('__init__ (TaskBarIcon)', 'starting')
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_tray_icon(constants.APP_TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_app_tray_icon_left_click)
        tools.debug_output('__init__ (TaskBarIcon)', 'Task icon is ready now')


    def CreatePopupMenu(self):
        """Method to generate a Popupmenu for the TrayIcon (do NOT rename)"""
        tools.debug_output('CreatePopupMenu', 'starting')
        menu = wx.Menu()
        #create_menu_item(menu, 'Show Mainwindow', self.on_app_tray_icon_left_click)
        create_menu_item(menu, 'Show', self.on_tray_popup_left_show)
        menu.AppendSeparator()
        create_menu_item(menu, 'Preferences', self.on_tray_popup_click_preferences)
        create_menu_item(menu, 'About', self.on_tray_popup_click_about)
        create_menu_item(menu, 'GitHub', self.on_tray_popup_click_github)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_tray_popup_click_exit)
        tools.debug_output('CreatePopupMenu', 'finished')
        return menu


    def set_tray_icon(self, path):
        """Method to set the icon for the TrayIconMenu item"""
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, constants.APP_TRAY_TOOLTIP)


    def on_app_tray_icon_left_click(self, event):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        tools.debug_output('on_app_tray_icon_left_click', 'starting with event: '+str(event))
        self.execute_tray_icon_left_click()


    def execute_tray_icon_left_click(self):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        tools.debug_output('execute_tray_icon_left_click', 'starting')
        if self.frame.IsIconized(): # if main window is minimized
            tools.debug_output('execute_tray_icon_left_click', 'MainWindow is now displayed')
            self.frame.Raise()
        else: # if main window is shown
            tools.debug_output('execute_tray_icon_left_click', 'MainWindow is now hidden/minimized')
            self.frame.Iconize(True)


    def on_tray_popup_left_show(self, event):
        """Method to handle click in the 'Show mainwindow' tray menu item"""
        tools.debug_output('on_tray_popup_left_show', 'starting with event: '+str(event))
        if self.frame.IsIconized(): # if main window is minimized
            tools.debug_output('execute_tray_icon_left_click', 'MainWindow is now displayed')
            self.frame.Raise()
        else: # if main window is shown
            tools.debug_output('execute_tray_icon_left_click', 'MainWindow is already shown, nothing to do here')


    def on_tray_popup_click_preferences(self, event):
        """Method to handle click in the 'Preferences' tray menu item"""
        tools.debug_output('on_tray_popup_click_preferences', 'starting with event: '+str(event))
        self.open_preference_window()


    def on_tray_popup_click_about(self, event):
        """Method to handle click in the 'About' tray menu item"""
        tools.debug_output('on_tray_popup_click_about', 'starting with event: '+str(event))

        aboutInfo = wx.AboutDialogInfo()
        aboutInfo.SetName(constants.APP_NAME)
        aboutInfo.SetVersion(config.APP_VERSION)
        aboutInfo.SetDescription((constants.APP_DESCRIPTION))
        #aboutInfo.SetLicense(open("COPYING").read())
        aboutInfo.SetLicense(open("../LICENSE").read())
        aboutInfo.SetWebSite(constants.APP_URL)
        aboutInfo.SetIcon(wx.Icon("gfx/core/bt_appIcon_128.png", wx.BITMAP_TYPE_PNG, 128, 128))
        aboutInfo.AddDeveloper("yafp")
        #aboutInfo.AddDeveloper('random example') # additional devs

        wx.AboutBox(aboutInfo)


    def on_tray_popup_click_exit(self, event):
        """Method to handle click in the 'Exit' tray menu item"""
        tools.debug_output('on_tray_popup_click_exit', 'starting with event: '+str(event))
        wx.CallAfter(self.frame.Close)


    def on_tray_popup_click_github(self, event):
        """Method to handle click on the 'GitHub' tray menu item"""
        tools.debug_output('on_tray_popup_click_github', 'starting with event: '+str(event))
        tools.debug_output('on_tray_popup_click_github', 'Opening: '+constants.APP_URL)
        webbrowser.open(constants.APP_URL) # Go to github


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(wx.App):

    """Class App"""

    def OnInit(self):
        """While starting the app (checks for already running instances)"""
        self.name = constants.APP_NAME+'.lock'
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning(): # allow only 1 instance of apparat
            tools.debug_output('OnInit', 'An instance is already running. Aborting')
            wx.MessageBox(constants.APP_NAME+' is already running', 'Error', wx.OK | wx.ICON_WARNING)
            return False
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """main"""
    app = App(False)
    tools.check_arguments() # check launch parameter / arguments
    tools.check_platform() # Check if platform is supported at all, otherwise abort
    tools.check_linux_requirements()
    ini.validate()

    frame = MyFrame(None, constants.APP_NAME) # Main UI window
    tools.debug_output('main', 'Frame: '+str(frame))
    app.MainLoop()


if __name__ == '__main__':
    tools.debug_output('__main__', 'starting')
    main()

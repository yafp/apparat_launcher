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
    ## general
    import difflib                      # for intelligent list sort
    import fnmatch                      # for searching applications
    import os                           # for searching applications
    import platform                     # check platform & linux distribution
    import psutil                       # check for running processes
    import subprocess                   # for checking if cmd_exists
    import webbrowser                   # for opening urls (example: github project page)
    import wx                           # for all the WX GUI items
    import xdg                          # for icon & icon-theme handling
    import xdg.IconTheme                # for icon & icon-theme handling

    ## apparat
    import constants                    # contains some constants
    import config                       # contains some config values
    import ini                          # ini file handling
    import prefs                        # preference window
    import plugin_misc
    import plugin_nautilus
    import plugin_screenshot
    import plugin_search_internet
    import plugin_search_local
    import plugin_session
    import plugin_shell
    import tools                        # contains helper-tools
    import version


    ## GTK vs WX is a mess - Issue: #15 - It helps to import GTK after having created the WX app (at least for Ubuntu, not for Fedora)
    #
    # Ubuntu (import gtk) vs Fedora (from gi.repository import Gtk)
    """
    if 'Ubuntu' in platform.linux_distribution():
        import gtk # after wx init
        gtk.remove_log_handlers()

    elif 'Fedora' in platform.linux_distribution():
        #gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk

    elif os.path.exists('/etc/arch-release'): # platform.linux_distribution doesnt work for arch linux
        import gtk
        gtk.remove_log_handlers()

    else:
        print('Here be dragons (untested distribution)')
    """




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
class MyFrame(wx.Frame): # pylint:disable=too-many-instance-attributes

    """Class for MainWindow"""

    def __init__(self, parent, title): # pylint:disable=too-many-statements
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
        app_icon = wx.Icon('gfx/core/16/appIcon.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(app_icon)

        # ------------------------------------------------
        # Define UI Elements
        # ------------------------------------------------
        # Some general bitmaps which might be needed for some button states
        self.ui__bt_img_search = wx.Bitmap('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/search.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_img_blank = wx.Bitmap('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_img_execute_black = wx.Bitmap('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute_black.png', wx.BITMAP_TYPE_PNG)

        ## status button
        self.ui__bt_status_img = wx.Bitmap('gfx/core/16/status_ok_green.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_status = wx.BitmapButton(self, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=self.ui__bt_status_img, size=(self.ui__bt_status_img.GetWidth()+15, self.ui__bt_status_img.GetHeight()+15))
        self.ui__bt_status.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_status.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_status.SetLabel('Status')
        self.ui__bt_status.SetToolTipString(u'Status OK')
        self.ui__bt_status.Enable(True)

        ## Preference button
        self.ui__bt_prefs_img = wx.Bitmap('gfx/core/16/prefs.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_prefs_img_focus = wx.Bitmap('gfx/core/16/prefs_black.png', wx.BITMAP_TYPE_PNG) # #c0392b
        self.ui__bt_prefs = wx.BitmapButton(self, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=self.ui__bt_prefs_img, size=(self.ui__bt_prefs_img.GetWidth()+15, self.ui__bt_prefs_img.GetHeight()+15))
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

        ## Plugin Information
        self.ui__txt_plugin_information = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE | wx.TE_RICH2)
        self.ui__txt_plugin_information.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_plugin_information.SetMinSize(wx.Size(600, 18))
        self.ui__txt_plugin_information.SetMaxSize(wx.Size(600, 18))
        self.ui__txt_plugin_information.Enable(False)
        self.ui__txt_plugin_information.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## primary button
        self.ui__bt_selected_app_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(300, 300), wx.BU_AUTODRAW)
        self.ui__bt_selected_app.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmapDisabled(self.ui__bt_img_blank)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetLabel('Applications')
        self.ui__bt_selected_app.Enable(False)

        ## secondary button
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(300, 300), wx.BU_AUTODRAW)
        #self.ui__bt_selected_parameter.SetBitmapFocus(self.ui__bt_img_search) # image when in focus
        self.ui__bt_selected_parameter.SetBitmapFocus(wx.NullBitmap) # image when in focus
        self.ui__bt_selected_parameter.SetBitmapHover(self.ui__bt_img_execute_black) # image on hover
        self.ui__bt_selected_parameter.SetBitmapDisabled(self.ui__bt_img_blank)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.SetLabel('Options')
        self.ui__bt_selected_parameter.Enable(False)

        ## primary text
        self.ui__txt_selected_app = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_app.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_app.SetMinSize(wx.Size(300, 18))
        self.ui__txt_selected_app.SetMaxSize(wx.Size(300, 18))
        self.ui__txt_selected_app.Enable(False)
        self.ui__txt_selected_app.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## secondary text
        self.ui__txt_selected_parameter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_parameter.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_parameter.SetMinSize(wx.Size(300, 18))
        self.ui__txt_selected_parameter.SetMaxSize(wx.Size(300, 18))
        self.ui__txt_selected_parameter.Enable(False)
        self.ui__txt_selected_parameter.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## Version Information
        self.ui__txt_version_information = wx.StaticText(self, wx.ID_ANY, ' v'+version.APP_VERSION, wx.DefaultPosition, wx.DefaultSize, 0)
        self.ui__txt_version_information.Wrap(-1)
        self.ui__txt_version_information.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_version_information.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))


        ## ------------------------------------------------
        ## Layout/Sizer
        ## ------------------------------------------------
        b_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        # line 1
        box0 = wx.BoxSizer(wx.HORIZONTAL)
        box0.Add(self.ui__bt_status, 0, wx.ALIGN_LEFT, 100) # status icon button
        box0.AddStretchSpacer(1)
        box0.Add(self.ui__bt_prefs, 0, wx.ALIGN_RIGHT, 100) # preferences icon button
        b_sizer.Add(box0, 0, wx.EXPAND)
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


        ## ------------------------------------------------
        ## Bind/Connect Events
        ## ------------------------------------------------
        self.ui__bt_prefs.Bind(wx.EVT_BUTTON, self.on_clicked)

        ## status buttons -> on key -> back to search
        self.ui__bt_status.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        ## preference buttons -> on key -> back to search
        self.ui__bt_prefs.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        
        ## combobox on key
        self.ui__cb_search.Bind(wx.EVT_KEY_UP, self.on_combobox_key_press)                 # Pressed any key
        self.ui__cb_search.Bind(wx.EVT_TEXT, self.on_combobox_text_changed)                # combobox text changes.
        self.ui__cb_search.Bind(wx.EVT_TEXT_ENTER, self.on_combobox_enter)                 # Pressed Enter
        self.ui__cb_search.Bind(wx.EVT_COMBOBOX, self.on_combobox_select_item)             # Item selected
        self.ui__cb_search.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_combobox_popup_open)     # Popup opened
        self.ui__cb_search.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.on_combobox_popup_close)     # Popup closed

        ## parameter button
        self.ui__bt_selected_parameter.Bind(wx.EVT_BUTTON, self.on_clicked_option_button)

        ## Handle clicks outside of the expected area main ui or none
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        ## ------------------------------------------------
        ## show the UI
        ## ------------------------------------------------
        self.SetTransparent(config.TRANSPARENCY_VALUE)       # 0-255
        self.ui__cb_search.SetFocus()     # set focus to search
        self.Center()                   # open window centered
        self.Show(True)                 # show main UI


    def on_key_down(self, event):
        """On Key Down in main ui"""
        tools.debug_output('on_key_down', 'starting with event: '+str(event))
        tools.debug_output('on_key_down', 'Currently focus is at: '+str(self.FindFocus()))
        self.ui__cb_search.SetFocus() # set focus to search
        self.ui__cb_search.SetInsertionPointEnd() # set cursor to end of string
        tools.debug_output('on_key_down', 'Set focus back to search.')


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
        self.prefWindow = prefs.PreferenceWindow(parent=None, idd=-1)
        self.prefWindow.Show()


    def on_combobox_text_changed(self, event):
        """Triggered if the combobox text changes"""
        tools.debug_output('on_combobox_text_changed', 'starting with event:'+str(event))
        if self.ui__cb_search.GetValue() == '': #searchstring is empty
            tools.debug_output('on_combobox_text_changed', 'Searchstring: <empty>. Nothing do to')
        else:
            tools.debug_output('on_combobox_text_changed', 'Searchstring: '+self.ui__cb_search.GetValue().lower())
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

            else: ## enter was pressed to close the combobox
                tools.debug_output('on_combobox_enter', 'Pressed enter to close the open combobox')
                is_combobox_open = 0    # global var to keep track if dropdown is open or closed

                ## run search again after selecting the desired search string from dropdown
                self.parse_user_input(self.ui__cb_search.GetValue().lower())
        else:
            tools.debug_output('on_combobox_enter', 'Combobox is empty, nothing to do here.')


    def on_combobox_select_item(self, event):
        """If an item of the result-list was selected"""
        tools.debug_output('on_combobox_select_item', 'starting with event: '+str(event))

        if(self.ui__txt_plugin_information.GetValue() == 'Plugin: Local Search'): # Local search is always using xdg-open - special case
            self.ui__txt_selected_parameter.SetValue(self.ui__cb_search.GetValue().lower())   # write command to command text field
        else: # default-case
            self.ui__txt_selected_app.SetValue(self.ui__cb_search.GetValue().lower())   # write command to command text field
            self.get_icon(self.ui__cb_search.GetValue().lower) # get icon for selected executable

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
        self.get_icon(self.ui__cb_search.GetValue().lower()) # get icon for selected executable
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
            self.parse_user_input(self.ui__cb_search.GetValue().lower())
            is_combobox_open = 0

        else:
            current_search_string = self.ui__cb_search.GetValue().lower()
            if len(current_search_string) == 0:
                tools.debug_output('on_combobox_key_press', 'Searchstring: <empty>. Nothing do to')
                self.reset_ui()
            else:
                tools.debug_output('on_combobox_key_press', 'Searching: '+current_search_string)
                self.parse_user_input(current_search_string)


    def get_icon(self, full_executable_name): # pylint:disable=too-many-branches,too-many-statements
        """Tries to get an icon for an executable by name"""
        tools.debug_output('get_icon', 'Starting for: '+full_executable_name)

        # Abort if a plugin is activated
        if(self.ui__txt_plugin_information.GetValue() != ''):
            return

        # detect users current icontheme-name
        theme = os.popen('gsettings get org.gnome.desktop.interface icon-theme').read() # via: https://ubuntuforums.org/showthread.php?t=2100795
        theme = theme.partition("'")[-1].rpartition("'")[0] # build substring

        if theme is None:
            theme = xdg.Config.icon_theme # hicolor

        #foo1 = xdg.IconTheme.getIconPath(full_executable_name, size=None, theme=None, extensions=['png', 'svg', 'xpm'])
        icon = xdg.IconTheme.getIconPath(full_executable_name, size=128, theme=theme, extensions=['png', 'xpm'])
        #print icon

        if(icon is None): # use default dummy icon
            new_app_icon = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/missingAppIcon.png', wx.BITMAP_TYPE_PNG)
        else:
            new_app_icon = wx.Image(icon, wx.BITMAP_TYPE_ANY)    # define new image
            new_app_icon.Rescale(config.TARGET_ICON_SIZE, config.TARGET_ICON_SIZE) # rescale image

        ## application button
        self.ui__bt_selected_app.SetBitmap(new_app_icon.ConvertToBitmap()) # set icon to button
        self.ui__bt_selected_app.Enable(True) # Enable the Button

        ## option buttons
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.Enable(True) # Enable option button
        self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip


    def plugin__update_general_ui_information(self, plugin_name):
        """set some general UI values after having a plugin triggered"""
        tools.debug_output('plugin__update_general_ui_information', 'started')
        if(plugin_name != ''):
            self.ui__bt_selected_app.Enable(True) # enable application button
            self.ui__bt_selected_parameter.Enable(True) # Enable option button
            self.ui__txt_result_counter.SetValue('1') ## set result-count
            self.ui__txt_selected_app.SetValue(self.ui__cb_search.GetValue().lower()[:2]) ## update command (Example: !g)
            self.ui__txt_plugin_information.SetValue('Plugin: '+plugin_name) # Plugin Name in specific field
            tools.debug_output('plugin__update_general_ui_information', 'Plugin '+plugin_name+' activated')
        else:
            ## primary buttons
            self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
            self.ui__bt_selected_app.Enable(False)

            ## secondary button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.SetToolTipString('')
            self.ui__bt_selected_parameter.Enable(False) # Enable option button

            ## set result-count
            self.ui__txt_result_counter.SetValue('0')

            ## Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue(plugin_name)

            ## reset command and parameter
            self.ui__txt_selected_app.SetValue('')
            self.ui__txt_selected_parameter.SetValue('')


    def parse_user_input(self, current_search_string): # pylint:disable=too-many-return-statements
        """Takes the current user input and parses it for matching plugins or general application search"""
        tools.debug_output('parse_user_input', 'starting')
        if current_search_string != '': # if there is a search string

            ## Reset UI partly if search is just !
            if current_search_string == '!':
                tools.debug_output('parse_user_input', 'Case: !')
                self.plugin__update_general_ui_information('')
                return

            ## Plugin: Misc
            if  current_search_string.startswith(plugin_misc.TRIGGER):
                plugin_misc.prepare_general(current_search_string, self)
                return

            ## Plugin: Screenshot
            if  current_search_string in plugin_screenshot.TRIGGER:
                plugin_screenshot.prepare_general(current_search_string, self)
                return

            ## Plugin: Nautilus
            if current_search_string in plugin_nautilus.TRIGGER or current_search_string.startswith('!goto'):
                plugin_nautilus.prepare_general(current_search_string, self)
                return

            ## Plugin: Session
            if current_search_string in plugin_session.TRIGGER:
                plugin_session.prepare_general(current_search_string, self)
                return

            ## Plugin: Shell
            if  current_search_string.startswith(plugin_shell.TRIGGER):
                plugin_shell.prepare_general(current_search_string, self)
                return

            ## Plugin: Internet-Search
            if current_search_string.startswith(plugin_search_internet.TRIGGER):
                tools.debug_output('parse_user_input', 'Case: Plugin Internet-Search')
                plugin_search_internet.prepare_internet_search(self, current_search_string)
                return

            ## Search for local files
            if current_search_string.startswith(plugin_search_local.TRIGGER):
                tools.debug_output('parse_user_input', 'Case: Plugin Local-Search')
                plugin_search_local.search_user_files(self, current_search_string)
                return

            ## Search for executables
            if current_search_string[:1] != '!':
                self.search_executables(current_search_string)
                return

            ## Nothing matched (no plugin and no executable -> display error
            self.status_notification_display_error('Invalid input')

        else: ## search string is empty
            tools.debug_output('parse_user_input', 'Empty search string. Doing nothing.')


    def search_executables(self, current_search_string):
        """Searches for executables"""
        self.plugin__update_general_ui_information('') # get rid of all plugin UI-artefacts

        tools.debug_output('search_executables', 'Searching executables for the following string: '+current_search_string)
        search_results = fnmatch.filter(os.listdir('/usr/bin'), '*'+current_search_string+'*')     # search for executables matching users searchstring
        search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

        self.ui__txt_result_counter.SetValue(str(len(search_results))) # update result count
        self.ui__cb_search.SetItems(search_results) # update combobox

        tools.debug_output('search_executables', 'Found '+str(len(search_results))+' matching application')
        if len(search_results) == 0: # 0 results
            ## update status button
            self.status_notification_display_error('No matching executables found')

            ## update launch button icon
            self.ui__bt_selected_app.Enable(True)
            if current_search_string.startswith('!'): # starting input for plugins
                self.ui__bt_selected_app_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
            else: # no result - so sad
                self.ui__bt_selected_app_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/noResult.png', wx.BITMAP_TYPE_PNG)

            self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
            self.ui__bt_selected_app.SetToolTipString("") # set tooltip

            ## update secondary button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

            self.ui__txt_selected_app.SetValue('') ## set command

            self.ui__txt_selected_parameter.SetValue('') ## set parameter

        elif len(search_results) == 1: # 1 result
            ## status notification
            self.status_notification_reset()

            ## primary button
            self.ui__bt_selected_app.Enable(True) # Enable application button
            self.ui__bt_selected_app.SetToolTipString(search_results[0]) # set tooltip

            ## secondary button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.Enable(True) # Enable option button
            self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip

            self.ui__txt_selected_app.SetValue(search_results[0]) ## update command

            self.ui__txt_selected_parameter.SetValue('') ## update parameter

            self.get_icon(str(search_results[0])) ## Icon search

            # check if application is already running
            # should offer an option to change to this instance besides starting a new one
            self.check_for_existing_app_instances(search_results[0])

        else: # > 1 results
            ## status notification
            self.status_notification_reset()

            ## primary button
            self.ui__bt_selected_app_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/list.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_app.Enable(True)
            self.ui__bt_selected_app.SetToolTipString(search_results[0])

            ## secondary button
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
            self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
            self.ui__bt_selected_parameter.Enable(False)                                  # Enable option button
            self.ui__bt_selected_parameter.SetToolTipString('Launch')
            self.ui__txt_selected_parameter.SetValue('')             ## update parameter
            self.get_icon(search_results[0]) # get icon for primary search result
            self.ui__txt_selected_app.SetValue(search_results[0])             # assume first search result is the way to go


    def check_for_existing_app_instances(self, application_name):
        """checks if there are alrady existing instances of an given app"""
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == application_name:
                tools.debug_output('check_for_existing_app_instances', "Found instance of: "+ str(p.cmdline())+" ### Details: "+str(p))


    def do_execute(self): # pylint:disable=too-many-branches
        """Launches the actual task"""
        ## get command and parameter informations
        command = self.ui__txt_selected_app.GetValue()
        parameter = self.ui__txt_selected_parameter.GetValue()

        if(command == ''):
            tools.debug_output('do_execute', 'Command is empty, nothing to do. Aborting')
            return

        tools.debug_output('do_execute', 'starting with command: "'+command+'" and parameter: "'+parameter+'"')

        ## Plugin: Misc - Open
        if self.ui__txt_plugin_information.GetValue() == 'Plugin: Misc (Open)':
            if parameter == '':
                self.status_notification_display_error('No parameter supplied for !open')
                return
            else: # check if parameter-path exists
                tools.debug_output('do_execute', '!open - check if parameter is valid')
                # is parameter a file or folder
                if os.path.isfile(parameter) or os.path.isdir(parameter):
                    tools.debug_output('do_execute', '!open - parameter is valid')
                else:
                    tools.debug_output('do_execute', '!open - parameter is not valid')
                    self.status_notification_display_error('Invalid parameter')
                    return

        ## Plugin: Internet-Search
        if command in plugin_search_internet.TRIGGER:
            plugin_search_internet.execute_internet_search(self, command, parameter)
            return

        ## Plugin: Session/Screenshot/Nautilus OR normal application
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
                    if(' ' in parameter): # if parameter contains at least 1 space, there are most likely several parameters
                        subprocess.Popen([command+" "+parameter], shell=True) # using shell=True as hack for handling several parameters (i.e. for !fs)
                        tools.debug_output('do_execute', 'Executed: "'+command+'" with parameter: "'+parameter+'" (with shell=True)')
                    else:
                        subprocess.Popen([command, parameter])
                        tools.debug_output('do_execute', 'Executed: "'+command+'" with parameter: "'+parameter+'"')

                self.reset_ui()

                ## if enabled in ini - hide the Main UI after executing the command
                cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
                if cur_ini_value_for_hide_ui_after_command_execution == 'True':
                    tools.debug_output('do_execute', 'Hide Main UI after executing a command')
                    self.tbicon.execute_tray_icon_left_click()
            else:
                tools.debug_output('do_execute', 'ERROR >> Checking the executable failed')
                self.status_notification_display_error('Checking the executable failed')
        else:
            tools.debug_output('do_execute', 'WARNING >> command is empty, aborting')


    def status_notification_display_error(self, error_string):
        """displays an error string and symbol in the status area"""
        tools.debug_output('status_notification_display_error', 'Show error: '+error_string)
        self.ui__bt_status.SetToolTipString(error_string)
        self.ui__bt_status_img = wx.Bitmap('gfx/core/16/status_error_red.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_status.SetBitmap(self.ui__bt_status_img)
        self.Refresh()


    def status_notification_reset(self):
        """resets the status notification """
        tools.debug_output('status_notification_reset', 'Reset notification area back to OK')
        self.ui__bt_status.SetToolTipString('Status OK')
        self.ui__bt_status_img = wx.Bitmap('gfx/core/16/status_ok_green.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_status.SetBitmap(self.ui__bt_status_img)
        self.Refresh()


    def open_app_url(self):
        """Method to open the application URL  (GitHub project)"""
        tools.debug_output('open_app_url', 'starting')
        tools.debug_output('open_app_url', 'Opening '+constants.APP_URL+' in default browser')
        webbrowser.open(constants.APP_URL+'#top')  # Go to github
        tools.debug_output('open_app_url', 'finished')


    def reset_ui(self):
        """Method to reset the User-Interface of the Apps main-window"""
        tools.debug_output('reset_ui', 'starting')

        ## reset the status notification
        self.status_notification_reset()

        ## reset the combobox
        self.ui__cb_search.SetFocus() # set focus to search
        self.ui__cb_search.Clear() # clear all list values
        self.ui__cb_search.SetValue('') # clear search field

        self.ui__bt_selected_app.Enable(False) ## reset primary button by disabling it
        self.ui__bt_selected_app.SetToolTipString("") # set tooltip

        ## reset secondary button
        self.ui__bt_selected_parameter.Enable(False)
        self.ui__bt_selected_parameter.SetToolTipString('')

        self.ui__txt_selected_app.SetValue('') ## reset txt command
        self.ui__txt_selected_parameter.SetValue('') ## reset txt parameter
        self.ui__txt_plugin_information.SetValue('') # reset plugin name field
        self.ui__txt_result_counter.SetValue('0') ## reset the result counter

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
class TaskBarIcon(wx.TaskBarIcon, MyFrame): # pylint:disable=too-many-ancestors

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
        aboutInfo.SetVersion(version.APP_VERSION)
        aboutInfo.SetDescription((constants.APP_DESCRIPTION))
        #aboutInfo.SetLicense(open("COPYING").read())
        aboutInfo.SetLicense(open("../LICENSE").read())
        aboutInfo.SetWebSite(constants.APP_URL)
        aboutInfo.SetIcon(wx.Icon('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/appIcon.png', wx.BITMAP_TYPE_PNG, 128, 128))
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
    tools.check_linux_requirements() # check if needed linux packages are available/installed
    ini.validate() # validate ini file

    frame = MyFrame(None, constants.APP_NAME) # Main UI window
    tools.debug_output('main', 'Frame: '+str(frame))
    app.MainLoop()

if __name__ == '__main__':
    tools.debug_output('__main__', 'starting')
    main()

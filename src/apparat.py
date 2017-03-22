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
    sys.stdout.write('Sorry, requires Python 2.x, not Python 3.x\n')
    sys.exit(1)
else:
    import difflib                      # for intelligent list sort
    import fnmatch                      # for searching applications
    import os                           # for searching applications
    import subprocess                   # for checking if cmd_exists
    import webbrowser                   # for opening urls (example: github project page)
    import wx                           # for all the WX GUI items

    ## apparat imports
    import constants                    # contains some constants
    import config                       # contains some config values
    import ini                          # ini file handling
    import prefs
    import tools                        # contains helper-tools



# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
is_combobox_open = 0
is_resetted = True


# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN-WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MyFrame(wx.Frame):

    """Class for MainWindow"""

    def __init__(self, parent, title):
        """Initialize the MainWindow"""
        ## Update Statistics (ini) - Apparat launched
        tools.print_debug_to_terminal('__init__', 'Updating statistics (apparat_started)')
        cur_app_start_count = ini.read_single_value('Statistics', 'apparat_started')          # get current value from ini
        ini.write_single_value('Statistics', 'apparat_started', int(cur_app_start_count)+1)    # update ini +1

        ## define fonts
        global FONT_BIG
        FONT_BIG = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD) # family, style, weight
        global FONT_NORMAL_MONO
        FONT_NORMAL_MONO = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')

        ## Define the style of the frame
        style = (wx.MINIMIZE_BOX | wx.CLIP_CHILDREN | wx.NO_BORDER | wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR)

        self.mainUI = wx.Frame.__init__(self, parent, title=title, size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT), style=style) # Custom Frame
        self.SetSizeHintsSz(wx.Size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT), wx.Size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)) # forcing min and max size to same values - prevents resizing option
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
        self.ui__txt_result_counter.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_result_counter.SetToolTipString(u'Results')
        self.ui__txt_result_counter.SetMinSize(wx.Size(50, 50))
        self.ui__txt_result_counter.SetMaxSize(wx.Size(50, 50))
        self.ui__txt_result_counter.SetEditable(False)
        self.ui__txt_result_counter.Enable(False)

        ## Search & Results as comboBox
        search_results = []
        combo_box_style = wx.TE_PROCESS_ENTER
        self.ui__search_and_result_combobox = wx.ComboBox(self, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size(550, 50), search_results, style=combo_box_style)
        self.ui__search_and_result_combobox.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))

        ## app button
        self.ui__bt_selected_app_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(300, 300), wx.BU_AUTODRAW)
        self.ui__bt_selected_app.SetBitmapFocus(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmapHover(wx.NullBitmap)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetLabel('Applications')
        self.ui__bt_selected_app.Enable(False)

        ## parameter button
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size(300, 300), wx.BU_AUTODRAW)
        self.ui__bt_selected_parameter.SetBitmapFocus(wx.NullBitmap) # TODO: image when in focus
        self.ui__bt_selected_parameter.SetBitmapHover(wx.NullBitmap) # TODO: image on hover
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.SetLabel('Options')
        self.ui__bt_selected_parameter.Enable(False)

        ## app text
        self.ui__txt_selected_app = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_app.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_app.SetToolTipString(u'Command')
        self.ui__txt_selected_app.SetMinSize(wx.Size(300, 15))
        self.ui__txt_selected_app.SetMaxSize(wx.Size(300, 15))
        self.ui__txt_selected_app.SetEditable(False)
        self.ui__txt_selected_app.Enable(False)
        self.ui__txt_selected_app.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## parameter text
        self.ui__txt_selected_parameter = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE)
        self.ui__txt_selected_parameter.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_selected_parameter.SetToolTipString(u'Parameter')
        self.ui__txt_selected_parameter.SetMinSize(wx.Size(300, 15))
        self.ui__txt_selected_parameter.SetMaxSize(wx.Size(300, 15))
        self.ui__txt_selected_parameter.SetEditable(False)
        self.ui__txt_selected_parameter.Enable(False)
        self.ui__txt_selected_parameter.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## Plugin Information
        self.ui__txt_plugin_information = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTRE | wx.BORDER_NONE | wx.TE_RICH2)
        self.ui__txt_plugin_information.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_plugin_information.SetToolTipString(u'Activated plugin')
        self.ui__txt_plugin_information.SetMinSize(wx.Size(600, 15))
        self.ui__txt_plugin_information.SetMaxSize(wx.Size(600, 15))
        self.ui__txt_plugin_information.SetEditable(False)
        self.ui__txt_plugin_information.Enable(False)
        self.ui__txt_plugin_information.SetBackgroundColour(wx.Colour(237, 237, 237))

        ## Version Information
        self.ui__txt_version_information = wx.StaticText(self, wx.ID_ANY, ' v'+config.APP_VERSION, wx.DefaultPosition, wx.DefaultSize, 0)
        self.ui__txt_version_information.Wrap(-1)
        self.ui__txt_version_information.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__txt_version_information.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))


        # ------------------------------------------------
        # Layout/Sizer
        # ------------------------------------------------
        b_sizer = wx.BoxSizer(wx.VERTICAL)                              # define layout container

        b_sizer.Add(self.ui__bt_prefs, 0, wx.ALIGN_RIGHT, 100) # preferences icon button
        b_sizer.AddSpacer(10)

        # horizontal sub-item 1
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self.ui__txt_result_counter, 0, wx.CENTRE) # result counter
        box1.Add(self.ui__search_and_result_combobox, 0, wx.CENTRE) # combobox
        b_sizer.Add(box1, 0, wx.CENTRE)
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

        b_sizer.Add(self.ui__txt_plugin_information, 0, wx.CENTRE) # plugin info
        b_sizer.AddSpacer(10)

        b_sizer.Add(self.ui__txt_version_information, 0, wx.CENTRE) # version
        self.SetSizer(b_sizer)


        # ------------------------------------------------
        # Bind/Connect Events
        # ------------------------------------------------
        self.ui__bt_prefs.Bind(wx.EVT_BUTTON, self.on_clicked)

        ## combobox
        self.ui__search_and_result_combobox.Bind(wx.EVT_KEY_UP, self.on_combobox_key_press)                 # Pressed any key
        self.ui__search_and_result_combobox.Bind(wx.EVT_TEXT, self.on_combobox_text_changed)                # combobox text changes.
        self.ui__search_and_result_combobox.Bind(wx.EVT_TEXT_ENTER, self.on_combobox_enter)                 # Pressed Enter
        self.ui__search_and_result_combobox.Bind(wx.EVT_COMBOBOX, self.on_combobox_select_item)             # Item selected
        self.ui__search_and_result_combobox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_combobox_popup_open)     # Popup opened
        self.ui__search_and_result_combobox.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.on_combobox_popup_close)     # Popup closed

        ## parameter button
        self.ui__bt_selected_parameter.Bind(wx.EVT_BUTTON, self.on_clicked_option_button)
        self.ui__bt_selected_parameter.Bind(wx.EVT_SET_FOCUS, self.on_focus_parameter_button)

        ## TODO: check when events in the main ui gets triggered
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        #self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        #self.Bind(wx.EVT_CHAR, self.OnKeyDown)

        # ------------------------------------------------
        # show the UI
        # ------------------------------------------------
        self.SetTransparent(config.TRANSPARENCY_VALUE)       # 0-255
        self.ui__search_and_result_combobox.SetFocus()     # set focus to search
        self.Center()                   # open window centered
        self.Show(True)                 # show main UI

        ## GTK vs WX is a mess - Issue: #15 - It helps to import GTK after having created the WX app (at least for Ubuntu, not for Fedora)
        global gtk
        import gtk


    def on_focus_parameter_button(self, event):
        """On focus of parameter button"""
        tools.print_debug_to_terminal('on_focus_parameter_button', 'starting with event: '+str(event))


    #def OnKeyDown(self, event):
        #"""On Key Down in main ui"""
        #tools.print_debug_to_terminal('OnKeyDown', 'starting with event: '+str(event))


    def on_close_application(self, event):
        """Method to close the app"""
        tools.print_debug_to_terminal('on_close_application', 'starting with event: '+str(event))
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()
        wx.GetApp().ExitMainLoop()
        event.Skip()


    def on_clicked_option_button(self, event):
        """If the launch option button was clicked"""
        tools.print_debug_to_terminal('on_clicked_option_button', 'starting with event: '+str(event))
        self.launch_external_application()


    def on_clicked(self, event):
        """General click handler - using label to find source"""
        tools.print_debug_to_terminal('on_clicked', 'starting with event: '+str(event))
        btn = event.GetEventObject().GetLabel()
        if btn == 'Preferences':
            tools.print_debug_to_terminal('on_clicked', 'Preferences')
            self.open_preference_window()
        else:
            tools.print_debug_to_terminal('on_clicked', 'Something else got clicked')


    def open_preference_window(self):
        """Opens the preference window"""
        tools.print_debug_to_terminal('open_preference_window', 'starting')
        self.new = prefs.PreferenceWindow(parent=None, id=-1)
        self.new.Show()


    def on_combobox_text_changed(self, event):
        """Triggered if the combobox text changes"""
        tools.print_debug_to_terminal('on_combobox_text_changed', 'starting with event:'+str(event))

        if self.ui__search_and_result_combobox.GetValue() == '': #searchstring is empty
            tools.print_debug_to_terminal('on_combobox_text_changed', 'Searchstring: <empty> - could reset UI at that point - but cant so far because of endless loop')
        else:
            tools.print_debug_to_terminal('on_combobox_text_changed', 'Searchstring: '+self.ui__search_and_result_combobox.GetValue())
            global is_resetted
            is_resetted = False


    def on_combobox_enter(self, event):
        """Triggered if Enter was pressed in combobox"""
        tools.print_debug_to_terminal('on_combobox_enter', 'starting with event: '+str(event))

        if len(self.ui__search_and_result_combobox.GetValue()) > 0:
            global is_resetted
            is_resetted = False

            global is_combobox_open
            if is_combobox_open == 0:
                self.launch_external_application()

            else: # enter was pressed to close the combobox
                tools.print_debug_to_terminal('on_combobox_enter', 'Pressed enter to close the open combobox')
                is_combobox_open = 0    # global var to keep track if dropdown is open or closed

                ## run search again after selecting the desired search string from dropdown
                self.parse_user_search_input(self.ui__search_and_result_combobox.GetValue())
        else:
            tools.print_debug_to_terminal('on_combobox_enter', 'Combobox is empty, nothing to do here.')


    def on_combobox_select_item(self, event):
        """If an item of the result-list was selected"""
        tools.print_debug_to_terminal('on_combobox_select_item', 'starting with event: '+str(event))
        self.ui__txt_selected_app.SetValue(self.ui__search_and_result_combobox.GetValue())   # write command to command text field
        self.ui__search_and_result_combobox.SetInsertionPointEnd() # set cursor to end of string
        self.parse_user_search_input(self.ui__search_and_result_combobox.GetValue()) ## run search again after selecting the desired search string from dropdown
        self.get_icon_for_executable(self.ui__search_and_result_combobox.GetValue()) # get icon for selected executable


    def on_combobox_popup_open(self, event):
        """If the popup of the combobox gets opened"""
        tools.print_debug_to_terminal('on_combobox_popup_open', 'starting with event: '+str(event))
        tools.print_debug_to_terminal('on_combobox_popup_open', 'combobox just got opened')
        global is_combobox_open
        is_combobox_open = True
        tools.print_debug_to_terminal('on_combobox_popup_open', 'finished')


    def on_combobox_popup_close(self, event):
        """If the popup of the combobox is closed"""
        tools.print_debug_to_terminal('on_combobox_popup_close', 'starting with event: '+str(event))
        tools.print_debug_to_terminal('on_combobox_popup_close', 'combobox just got closed')
        self.get_icon_for_executable(self.ui__search_and_result_combobox.GetValue()) # get icon for selected executable
        global is_combobox_open
        is_combobox_open = False
        tools.print_debug_to_terminal('on_combobox_popup_close', 'finished')


    def on_combobox_key_press(self, event):
        """If content of the searchfield of the combobox changes"""
        tools.print_debug_to_terminal('on_combobox_key_press', 'starting with event: '+str(event))
        global is_combobox_open

        current_keycode = event.GetKeyCode()
        tools.print_debug_to_terminal('on_combobox_key_press', 'KeyCode: '+str(current_keycode))

        if current_keycode == 27: # ESC
            tools.print_debug_to_terminal('on_combobox_key_press', 'ESC in combobox')
            if(is_resetted is False):
                tools.print_debug_to_terminal('on_combobox_key_press', 'Launch reset method')
                self.reset_ui()
            else: # hide main window
                tools.print_debug_to_terminal('on_combobox_key_press', 'UI is already resetted')
                self.tbicon.execute_tray_icon_left_click()

        elif current_keycode == 317:    # Arrow Down
            tools.print_debug_to_terminal('on_combobox_key_press', 'ARROW DOWN in combobox')
            if(self.ui__txt_result_counter.GetValue() != ''):
                self.ui__search_and_result_combobox.Popup()
                tools.print_debug_to_terminal('on_combobox_key_press', 'Opening dropdown')
                is_combobox_open = 1
            else:
                ## global var to keep track if dropdown is open or closed
                tools.print_debug_to_terminal('on_combobox_key_press', 'No result, so no need to open the dropdown')
                is_combobox_open = 0

        elif current_keycode == 13: # Enter
            tools.print_debug_to_terminal('on_combobox_key_press', 'ENTER was pressed - ignoring it because of "on_combobox_enter"')
            is_combobox_open = 0

        else:
            current_search_string = self.ui__search_and_result_combobox.GetValue()
            if len(current_search_string) == 0:
                tools.print_debug_to_terminal('on_combobox_key_press', 'Search string is empty - doing nothing')
                #self.reset_ui()
            else:
                tools.print_debug_to_terminal('on_combobox_key_press', 'Searching: '+current_search_string)
                self.parse_user_search_input(current_search_string)


    def get_icon_for_executable(self, full_executable_name):
        """Tries to get an icon for an selected executable"""
        # Abort if a plugin is activated
        if(self.ui__txt_plugin_information.GetValue() != ''):
            return

        ## Icon search - http://www.pygtk.org/pygtk2reference/class-gtkicontheme.html
        ## get app-icon for selected application from operating system
        icon_theme = gtk.icon_theme_get_default()
        ## check what icon sizes are available and choose best size
        available_icon_sizes = icon_theme.get_icon_sizes(full_executable_name)
        if not available_icon_sizes: # if we got no list of available icon sizes - Fallback: try to get a defined size
            max_icon_size = 64
            icon_info = icon_theme.lookup_icon(full_executable_name, max_icon_size, 0)
        else:
            tools.print_debug_to_terminal('get_icon_for_executable', 'Found several icon sizes: '+str(available_icon_sizes))
            ## pick the biggest
            max_icon_size = max(available_icon_sizes)
            tools.print_debug_to_terminal('get_icon_for_executable', 'Picking the following icon size: '+str(max_icon_size))
            icon_info = icon_theme.lookup_icon(full_executable_name, max_icon_size, 0)

        if icon_info is None:
            new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
        else:
            icon_path = icon_info.get_filename()

            if icon_path != '': # found icon
                if '.svg' not in icon_path:
                    new_app_icon = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)    # define new image
                    #new_app_iconWidth=new_app_icon.GetWidth()                   # get icon width
                    tools.print_debug_to_terminal('get_icon_for_executable', 'Found icon: '+icon_path+' ('+str(max_icon_size)+'px)')
                    if config.TARGET_ICON_SIZE == max_icon_size: # if icon has expected size
                        tools.print_debug_to_terminal('get_icon_for_executable', 'Icon size is as expected')
                    else: # resize icon
                        tools.print_debug_to_terminal('get_icon_for_executable', 'Icon size does not match, starting re-scaling.')
                        new_app_icon.Rescale(128, 128)                             # rescale image
                else: # found unsupported icon format
                    tools.print_debug_to_terminal('get_icon_for_executable', 'SVG icons ('+icon_path+') can not be used so far. Using a dummy icon for now')
                    new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)
            else: # no icon
                tools.print_debug_to_terminal('get_icon_for_executable', 'Found no icon')
                new_app_icon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)

        # application button
        self.ui__bt_selected_app.SetBitmap(new_app_icon.ConvertToBitmap())    # set icon to button
        self.ui__bt_selected_app.Enable(True) # Enable the Button

        ## option buttons
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.Enable(True) # Enable option button
        self.ui__bt_selected_parameter.SetToolTipString('Launch') # set tooltip


    def plugin__internet_search_prepare(self, current_search_string):
        """Plugin: Internet-Search - Updates the UI on trigger input"""
        tools.print_debug_to_terminal('plugin__internet_search_prepare', 'starting')

        ## show searchstring in parameter field
        if(self.ui__txt_selected_app.GetValue() != ''):
            cur_searchphrase_parameter = current_search_string[3:] # remove trigger '!y ' or '!g ' or '!w '
            self.ui__txt_selected_parameter.SetValue(cur_searchphrase_parameter)

        ## check if there is NO space after the trigger - abort this function and reset some parts of the UI
        if(len(current_search_string) >= 3) and (current_search_string[2] != " "):
            tools.print_debug_to_terminal('plugin__internet_search_prepare', 'No space after trigger - should reset icons')
            self.plugin__update_general_ui_information('')
            return

        ## If search-string > 2 - abort - as all the work is already done
        #
        if(len(current_search_string) > 2):
            return # we can stop here - nothing more to do as plugin should be already activated

        ## Prepare UI for plugin
        if current_search_string.startswith('!a') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_amazon_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Amazon')

        if current_search_string.startswith('!b') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_bandcamp_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Bandcamp')

        if current_search_string.startswith('!e') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_stack-exchange_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Stack-Exchange')

        if current_search_string.startswith('!g') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_google_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Google')

        if current_search_string.startswith('!l') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_lastfm_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('LastFM')

        if current_search_string.startswith('!m') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_maps_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Google-Maps')

        if current_search_string.startswith('!o') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_stack-overflow_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Stack-Overflow')

        if current_search_string.startswith('!r') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_reddit_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Reddit')

        if current_search_string.startswith('!s') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_soundcloud_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('SoundCloud')

        if current_search_string.startswith('!t') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_twitter_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Twitter')

        if current_search_string.startswith('!v') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_vimeo_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Vimeo')

        if current_search_string.startswith('!w') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_wikipedia_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('Wikipedia')

        if current_search_string.startswith('!y') is True:
            self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_youtube_128.png', wx.BITMAP_TYPE_PNG)
            self.plugin__update_general_ui_information('YouTube')

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
        tools.print_debug_to_terminal('plugin__internet_search_execute', 'starting')

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

        if command == ('!m'):                           # https://www.google.de/maps/place/foobar/
            remote_url = 'https://www.google.de/maps/place/'+parameter

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
        tools.print_debug_to_terminal('plugin__internet_search_execute', 'Updating statistics (plugin_executed)')
        current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed')          # get current value from ini
        ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1)    # update ini +1

        self.reset_ui()

        ## if enabled in ini - hide the Main UI after executing the command
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == 'True':
            self.tbicon.execute_tray_icon_left_click()


    def plugin__update_general_ui_information(self, plugin_name):
        """set some general UI values after having a plugin triggered"""
        tools.print_debug_to_terminal('plugin__update_general_ui_information', 'started')

        if(plugin_name != ''):
            # application buttons
            self.ui__bt_selected_app.Enable(True)

            ## parameter button
            self.ui__bt_selected_parameter.Enable(True) # Enable option button

            ## set result-count
            self.ui__txt_result_counter.SetValue('1')

            ## update search command
            self.ui__txt_selected_app.SetValue(self.ui__search_and_result_combobox.GetValue()[:2])

            # Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue('Plugin: '+plugin_name)
            tools.print_debug_to_terminal('plugin__update_general_ui_information', 'Plugin '+plugin_name+' activated')

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
            self.ui__txt_result_counter.SetValue('')

            # Plugin Name in specific field
            self.ui__txt_plugin_information.SetValue(plugin_name)

            self.ui__txt_selected_app.SetValue('')
            self.ui__txt_selected_parameter.SetValue('')


    def prepare_plugin_misc_open(self):
        """Plugin Misc - Open"""
        tools.print_debug_to_terminal('sprepare_plugin_misc_open', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Misc (Open)')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/misc/bt_open_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Open')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command
        self.ui__txt_selected_app.SetValue('xdg-open')

        # set parameter
        self.ui__txt_selected_parameter.SetValue(self.ui__search_and_result_combobox.GetValue()[6:])


    def prepare_plugin_nautilus_goto(self):
        """Plugin Nautilus - GoTo"""
        tools.print_debug_to_terminal('prepare_plugin_nautilus_goto', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Nautilus (GoTo)')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_goto_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Go to folder')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command
        self.ui__txt_selected_app.SetValue('nautilus')

        # set parameter
        self.ui__txt_selected_parameter.SetValue(self.ui__search_and_result_combobox.GetValue()[6:])


    def prepare_plugin_nautilus_show_network_devices(self):
        """Plugin Nautilus - Network"""
        tools.print_debug_to_terminal('prepare_plugin_nautilus_show_network_devices', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Nautilus (Network)')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_network_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Show network devices')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('nautilus')
        self.ui__txt_selected_parameter.SetValue('network://')


    def prepare_plugin_nautilus_show_recent(self):
        """Plugin Nautilus - Recent"""
        tools.print_debug_to_terminal('prepare_plugin_nautilus_show_recent', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Nautilus (Recent)')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_recent_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Show recent files')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('nautilus')
        self.ui__txt_selected_parameter.SetValue('recent://')


    def prepare_plugin_nautilus_open_trash(self):
        """Plugin Nautilus - Trash"""
        tools.print_debug_to_terminal('prepare_plugin_nautilus_open_trash', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Nautilus (Trash)')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/nautilus/bt_trash_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Open Trash')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('nautilus')
        self.ui__txt_selected_parameter.SetValue('trash://')

        # TODO: introduce multiple actions for 1 app
        # - open trash
        # - empty trash
        #self.ui__bt_selected_parameter.SetFocus()


    def prepare_plugin_shell(self):
        """Plugin Shell"""
        tools.print_debug_to_terminal('prepare_plugin_shell', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Shell')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/shell/bt_shell_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Lock Session')

        ## parameter buttons
        self.ui__bt_selected_parameter.SetToolTipString('Open')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        ## http://askubuntu.com/questions/484993/run-command-on-anothernew-terminal-window
        self.ui__txt_selected_app.SetValue('xterm')
        self.ui__txt_selected_parameter.SetValue(self.ui__search_and_result_combobox.GetValue()[4:])


    def prepare_plugin_session_lock(self):
        """Plugin Session - Lock"""
        tools.print_debug_to_terminal('prepare_plugin_session_lock', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Lock')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_lock_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Lock Session')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-screensaver-command')
        self.ui__txt_selected_parameter.SetValue('--lock')


    def prepare_plugin_session_logout(self):
        """Plugin Session - Logout"""
        tools.print_debug_to_terminal('prepare_plugin_session_logout', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Logout')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_logout_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Logout Session')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-session-quit')
        self.ui__txt_selected_parameter.SetValue('--logout')


    def prepare_plugin_session_shutdown(self):
        """Plugin Session - Shutdown"""
        tools.print_debug_to_terminal('prepare_plugin_session_shutdown', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Shutdown')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_shutdown_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Shutdown machine')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-session-quit')
        self.ui__txt_selected_parameter.SetValue('--power-off')


    def prepare_plugin_session_hibernate(self):
        """Plugin Session - Hibernate"""
        tools.print_debug_to_terminal('prepare_plugin_session_hibernate', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Hibernate')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_hibernate_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Hibernate machine')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('systemctl')
        self.ui__txt_selected_parameter.SetValue('suspend')


    def prepare_plugin_session_reboot(self):
        """Plugin Session - Reboot"""
        tools.print_debug_to_terminal('prepare_plugin_session_reboot', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Reboot')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/session/bt_reboot_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Reboot machine')

        ## option buttons
        self.ui__bt_selected_parameter.SetToolTipString('Launch')
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())

        ## set command and parameter
        self.ui__txt_selected_app.SetValue('gnome-screensaver-command')
        self.ui__txt_selected_parameter.SetValue('--reboot')


    def parse_user_search_input(self, current_search_string):
        """Method to search applications and/or plugin commands to fill the results"""
        tools.print_debug_to_terminal('parse_user_search_input', 'starting')

        if current_search_string != '': # if there is a search string

            ## Reset UI partly if search is just !
            #
            if current_search_string == '!':
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: !')
                self.plugin__update_general_ui_information('')
                return

            ## Plugin: Misc
            ##
            if  current_search_string.startswith(constants.APP_PLUGINS_MISC_TRIGGER):
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: Plugin Misc')
                if current_search_string.startswith('!open'):
                    self.prepare_plugin_misc_open()
                return

            ## Plugin: Nautilus
            ##
            if current_search_string in constants.APP_PLUGINS_NAUTILUS_TRIGGER or current_search_string.startswith('!goto'):
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: Plugin Nautilus')

                if current_search_string.startswith('!goto'):
                    self.prepare_plugin_nautilus_goto()
                    return

                if current_search_string == ('!recent'):
                    self.prepare_plugin_nautilus_show_recent()
                    return

                if current_search_string == ('!trash'):
                    self.prepare_plugin_nautilus_open_trash()
                    return

                if current_search_string == ('!network') or current_search_string == ('!net'):
                    self.prepare_plugin_nautilus_show_network_devices()
                    return

            ## Plugin: Shell
            ##
            if  current_search_string.startswith(constants.APP_PLUGINS_SHELL_TRIGGER):
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: Plugin Shell')
                if current_search_string.startswith('!sh'):
                    self.prepare_plugin_shell()
                return

            ## Plugin: Session
            ##
            if current_search_string in constants.APP_PLUGINS_SESSION_TRIGGER:
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: Plugin Session')

                ## Hibernate
                if current_search_string == '!hibernate' or current_search_string == '!sleep':
                    self.prepare_plugin_session_hibernate()

                ## Lock
                elif current_search_string == '!lock':
                    self.prepare_plugin_session_lock()

                ## Logout
                elif current_search_string == '!logout':
                    self.prepare_plugin_session_logout()

                ## Reboot
                elif current_search_string == '!reboot' or current_search_string == '!restart':
                    self.prepare_plugin_session_reboot()

                ## Shutdown
                elif current_search_string == '!shutdown' or current_search_string == '!halt':
                    self.prepare_plugin_session_shutdown()

                else:
                    tools.print_debug_to_terminal('parse_user_search_input', 'Error: Undefined session command')
                return

            ## Plugin: Internet-Search
            ##
            if current_search_string.startswith(constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER):
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: Plugin Internet-Search')
                self.plugin__internet_search_prepare(current_search_string)
                return

            ## Search for local files
            #
            if current_search_string.startswith('?'):
                tools.print_debug_to_terminal('parse_user_search_input', 'Case: Plugin Local-Search')
                self.search_user_files(current_search_string)
                return

            ## Search for executables
            #
            self.search_executables(current_search_string)


        else: # search string is empty
            tools.print_debug_to_terminal('parse_user_search_input', 'Empty search string')



    def search_user_files(self, current_search_string):
        """Search for user files"""
        tools.print_debug_to_terminal('search_user_files', 'starting')

        ## update plugin info
        self.plugin__update_general_ui_information('Local Search')

        ## application buttons
        self.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_app.SetBitmap(self.ui__bt_selected_app_img.ConvertToBitmap())
        self.ui__bt_selected_app.SetToolTipString('Search local user files')

        ## parameter buttons
        self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
        self.ui__bt_selected_parameter.SetBitmap(self.ui__bt_selected_parameter_img.ConvertToBitmap())
        self.ui__bt_selected_parameter.SetToolTipString('Search local user files')

        ## set command
        self.ui__txt_selected_app.SetValue('xdg-open')

        ## set parameter
        self.ui__txt_selected_parameter.SetValue('')


        if(len(current_search_string) > 4) and current_search_string.startswith('? '):
            current_search_string = current_search_string[2:] # get the real search term without trigger
            tools.print_debug_to_terminal('search_user_files', 'Searching local files for: '+current_search_string)
            root = os.environ['HOME']
            pattern = '*'+current_search_string+'*'

            search_results = []

            if(len(current_search_string) > 2): # if search string is long enough
                tools.print_debug_to_terminal('search_user_files', 'Searching local user files for the following string: '+current_search_string)
                for root, dirs, files in os.walk(root):
                    for filename in fnmatch.filter(files, pattern):
                        #print( os.path.join(root, filename))

                        # append to list
                        result = os.path.join(root, filename)
                        search_results.append(result)

                tools.print_debug_to_terminal('search_user_files', 'Got '+(str(len(search_results)))+' Results')

                if(len(search_results) > 0):
                    # update result count
                    self.ui__txt_result_counter.SetValue(str(len(search_results)))
                else:
                    self.ui__txt_result_counter.SetValue('')

                # update combobox
                self.ui__search_and_result_combobox.SetItems(search_results) # update combobox
        else:
            tools.print_debug_to_terminal('search_user_files', 'aborting search (string too short)')








    def search_executables(self, current_search_string):
        """Searches for executables"""
        self.plugin__update_general_ui_information('')

        tools.print_debug_to_terminal('search_executables', 'Searching executables for the following string: '+current_search_string)
        search_results = fnmatch.filter(os.listdir('/usr/bin'), '*'+current_search_string+'*')     # search for executables matching users searchstring

        ## Sort results - http://stackoverflow.com/questions/17903706/how-to-sort-list-of-strings-by-best-match-difflib-ratio
        search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

        self.ui__txt_result_counter.SetValue(str(len(search_results))) # update result count
        self.ui__search_and_result_combobox.SetItems(search_results) # update combobox

        tools.print_debug_to_terminal('search_executables', 'Found '+str(len(search_results))+' matching application')
        if len(search_results) == 0: # 0 result
            ## update launch button icon
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
            # combobox - autocomplete
            #self.ui__search_and_result_combobox.SetValue(search_results[0])

            ## application buttons
            self.ui__bt_selected_app.Enable(True) # Enable application button
            self.ui__bt_selected_app.SetToolTipString(search_results[0]) # set tooltip

            ## options buttons
            self.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_play_128.png', wx.BITMAP_TYPE_PNG)
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


    def launch_external_application(self):
        """Launches the actual external process"""
        command = self.ui__txt_selected_app.GetValue()
        parameter = self.ui__txt_selected_parameter.GetValue()

        if(command == ''):
            tools.print_debug_to_terminal('launch_external_application', 'Nothing to do - empty command')
            return

        tools.print_debug_to_terminal('launch_external_application', 'starting with command: "'+command+'" and parameter: "'+parameter+'"')

        ## Plugin: Shell
        ##
        #if self.ui__txt_plugin_information.GetValue() == 'Plugin: Shell':
            #command = parameter
            #parameter = ''


        ## Plugin: Local-Search
        ##
        if self.ui__txt_plugin_information.GetValue() == 'Plugin: Local Search':
            parameter = command
            command = 'xdg-open'


        ## Plugin: Internet-Search
        ##
        if command in constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER:
            self.plugin__internet_search_execute(command, parameter)
            return


        ## Plugin: Session OR normal application
        ##
        if command is not None: # Check if the dropdown contains something at all or not
            tools.print_debug_to_terminal('launch_external_application', 'Should execute: "'+command+'" with parameter: "'+parameter+'"')

            ## check if name exists and is executable
            executable_exists = tools.cmd_exists(command)
            if executable_exists is True:

                ## update usage-statistics
                #
                ## commands executed
                tools.print_debug_to_terminal('launch_external_application', 'Updating statistics (command_executed)')
                current_commands_executed_count = ini.read_single_value('Statistics', 'command_executed')          # get current value from ini
                ini.write_single_value('Statistics', 'command_executed', int(current_commands_executed_count)+1) # update ini +1

                ## update plugin execution count
                if self.ui__txt_plugin_information != '':
                    tools.print_debug_to_terminal('launch_external_application', 'Updating statistics (plugins_executed)')
                    current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed')          # get current value from ini
                    ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

                tools.print_debug_to_terminal('launch_external_application', 'Executable: "'+command+'" exists')
                # https://docs.python.org/2/library/subprocess.html
                # TODO: check: check_output - https://docs.python.org/2/library/subprocess.html#subprocess.check_output
                if parameter == '':
                    #subprocess.Popen(["rm","-r","some.file"])
                    
                    # 
                    subprocess.Popen([command])
                    tools.print_debug_to_terminal('launch_external_application', 'Executed: "'+command+'"')
                else:
                    subprocess.Popen([command, parameter])
                    tools.print_debug_to_terminal('launch_external_application', 'Executed: "'+command+'" with parameter "'+parameter+'"')

                self.reset_ui()

                ## if enabled in ini - hide the Main UI after executing the command
                cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
                if cur_ini_value_for_hide_ui_after_command_execution == 'True':
                    self.tbicon.execute_tray_icon_left_click()

            else:
                tools.print_debug_to_terminal('launch_external_application', 'ERROR >> Checking the executable failed')
        else:
            tools.print_debug_to_terminal('launch_external_application', 'WARNING >> command is empty, aborting')


    def open_app_url(self):
        """Method to open the application URL  (GitHub project)"""
        tools.print_debug_to_terminal('open_app_url', 'starting')
        tools.print_debug_to_terminal('open_app_url', 'Opening '+constants.APP_URL+' in default browser')
        webbrowser.open(constants.APP_URL)  # Go to github
        tools.print_debug_to_terminal('open_app_url', 'finished')


    def reset_ui(self):
        """Method to reset the User-Interface of the Apps main-window"""
        tools.print_debug_to_terminal('reset_ui', 'starting')

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
        self.ui__txt_result_counter.SetValue('')

        global is_resetted
        is_resetted = True

        tools.print_debug_to_terminal('reset_ui', 'Finished resetting UI')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY-MENU
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_menu_item(menu, label, func):
    """Generates single menu items for the tray icon popup menu"""
    tools.print_debug_to_terminal('create_menu_item', 'Menuitem: '+label)
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
        tools.print_debug_to_terminal('__init__ (TaskBarIcon)', 'starting')
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_tray_icon(constants.APP_TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_app_tray_icon_left_click)
        tools.print_debug_to_terminal('__init__ (TaskBarIcon)', 'Task icon is ready now')


    def CreatePopupMenu(self):
        """Method to generate a Popupmenu for the TrayIcon (do NOT rename)"""
        tools.print_debug_to_terminal('CreatePopupMenu', 'starting')
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
        tools.print_debug_to_terminal('on_app_tray_icon_left_click', 'starting')
        tools.print_debug_to_terminal('on_app_tray_icon_left_click', 'Event: '+str(event))
        self.execute_tray_icon_left_click()


    def execute_tray_icon_left_click(self):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        tools.print_debug_to_terminal('execute_tray_icon_left_click', 'starting')
        if self.frame.IsIconized(): # if main window is minimized
            tools.print_debug_to_terminal('execute_tray_icon_left_click', 'MainWindow was minimized - should show it now')
            self.frame.Raise()
        else: # if main window is shown
            tools.print_debug_to_terminal('execute_tray_icon_left_click', 'MainWindow was shown - should minimize it now')
            self.frame.Iconize(True)


    def on_tray_popup_click_preferences(self, event):
        """Method to handle click in the 'Preferences' tray menu item"""
        tools.print_debug_to_terminal('on_tray_popup_click_preferences', 'starting')
        tools.print_debug_to_terminal('on_tray_popup_click_preferences', 'Event: '+str(event))
        self.open_preference_window()


    def on_tray_popup_click_exit(self, event):
        """Method to handle click in the 'Exit' tray menu item"""
        tools.print_debug_to_terminal('on_tray_popup_click_exit', 'starting')
        tools.print_debug_to_terminal('on_tray_popup_click_exit', 'Event: '+str(event))
        wx.CallAfter(self.frame.Close)


    def on_tray_popup_click_github(self, event):
        """Method to handle click on the 'GitHub' tray menu item"""
        tools.print_debug_to_terminal('on_tray_popup_click_github', 'starting')
        tools.print_debug_to_terminal('on_tray_popup_click_github', 'Event: '+str(event))
        tools.print_debug_to_terminal('on_tray_popup_click_github', 'Opening: '+constants.APP_URL)
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
            tools.print_debug_to_terminal('OnInit', 'An instance is already running. Aborting')
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
    tools.print_debug_to_terminal('main', 'Frame: '+str(frame))
    app.MainLoop()


if __name__ == '__main__':
    tools.print_debug_to_terminal('__main__', 'starting')
    main()

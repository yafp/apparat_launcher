#!/usr/bin/python
"""preference UI"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules
import wx

## apparat
import constants
import ini
import requirements
import tools


# -----------------------------------------------------------------------------------------------
# PREFERENCE WINDOW
# -----------------------------------------------------------------------------------------------
class PreferenceWindow(wx.Frame):

    """Class for Preference Window"""

    def __init__(self, parent, idd):
        """Initialize the preference window"""
        ## define style of preference window
        pref_window_style = (wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        wx.Frame.__init__(self, parent, idd, constants.APP_NAME+' - Preferences', size=(500, 600), style=pref_window_style)

        ## Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        ## Create the tab windows
        tab1 = UITabGeneral(nb)
        tab2 = UITabPluginCommands(nb)
        tab3 = UITabStatistics(nb)

        ## Add the windows to tabs and name them.
        nb.AddPage(tab1, "General ")
        nb.AddPage(tab2, "Plugins ")
        nb.AddPage(tab3, "Statistics ")

        ## Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        wx.Frame.CenterOnScreen(self) # center the pref window

        self.Bind(wx.EVT_CLOSE, self.close_preference_ui)


    def close_preference_ui(self, event):
        """Closes the preference window"""
        tools.debug_output(__name__, 'close_preference_ui', 'starting', 1)
        tools.debug_output(__name__, 'close_preference_ui', 'Event: '+str(event), 1)
        self.Destroy() # close the pref UI


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PREFERENCE-TABS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class UITabGeneral(wx.Panel):

    """Preference Window - Tab: General"""

    def __init__(self, parent): # pylint:disable=too-many-statements
        """Inits the general tab"""
        wx.Panel.__init__(self, parent)

        ## show language
        ##
        cur_ini_value_for_language = ini.read_single_ini_value('Language', 'lang') # get current value from ini
        txt_language = wx.StaticText(self, -1, "Language: ", (20, 20))

        languages = [cur_ini_value_for_language]
        combo_box_style = wx.CB_READONLY
        ui__cb_languages = wx.ComboBox(self, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size(100, 30), languages, style=combo_box_style)
        ui__cb_languages.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        ui__cb_languages.SetValue(languages[0])

        # line_1
        line1 = wx.StaticLine(self, -1, size=(480, 1), style=wx.LI_HORIZONTAL)

        ## icon sizes
        ##
        cur_ini_value_for_iconsize = ini.read_single_ini_value('General', 'icon_size') # get current value from ini
        txt_iconsize = wx.StaticText(self, -1, "Icon Size: ", (20, 20))

        available_icon_sizes = ['128', '256']
        combo_box_style = wx.CB_READONLY
        self.ui__cb_iconsizes = wx.ComboBox(self, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size(100, 30), available_icon_sizes, style=combo_box_style)
        self.ui__cb_iconsizes.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__cb_iconsizes.SetValue(cur_ini_value_for_iconsize)
        self.ui__cb_iconsizes.Bind(wx.EVT_TEXT, self.on_change_icon_size) # changing

        # line_2
        line2 = wx.StaticLine(self, -1, size=(480, 1), style=wx.LI_HORIZONTAL)

        ## transparency
        ##
        cur_ini_value_for_transparency = ini.read_single_ini_value('General', 'transparency') # get current value from ini
        txt_transparency = wx.StaticText(self, -1, "UI transparency (default 255, needs restart) : ", (20, 20))

        available_transparency_values = ['255', '250', '245', '240', '235', '230', '225', '220', '215', '210', '205', '200']
        combo_box_style = wx.CB_READONLY
        self.ui__cb_transparency = wx.ComboBox(self, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size(100, 30), available_transparency_values, style=combo_box_style)
        self.ui__cb_transparency.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        self.ui__cb_transparency.SetValue(cur_ini_value_for_transparency)
        self.ui__cb_transparency.Bind(wx.EVT_TEXT, self.on_change_transparency) # changing

        # line_3
        line3 = wx.StaticLine(self, -1, size=(480, 1), style=wx.LI_HORIZONTAL)

        ## Hide UI
        ##
        self.cb_enable_hide_ui = wx.CheckBox(self, -1, 'Hide UI after command execution ', (20, 60))
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == "False":
            self.cb_enable_hide_ui.SetValue(False)
        else:
            self.cb_enable_hide_ui.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_hide_ui.GetId(), self.prefs_general_toggle_hide_ui)

        ## Layout
        ##
        general_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        general_sizer.AddSpacer(10)
        general_sizer.Add(txt_language, 0, wx.ALL, border=10)
        general_sizer.Add(ui__cb_languages, 0, wx.ALL, border=10)

        general_sizer.AddSpacer(30)
        general_sizer.Add(line1, 0, wx.CENTRE)
        general_sizer.AddSpacer(10)

        general_sizer.Add(txt_iconsize, 0, wx.ALL, border=10)
        general_sizer.Add(self.ui__cb_iconsizes, 0, wx.ALL, border=10)

        general_sizer.AddSpacer(30)
        general_sizer.Add(line2, 0, wx.CENTRE)
        general_sizer.AddSpacer(10)

        general_sizer.Add(txt_transparency, 0, wx.ALL, border=10)
        general_sizer.Add(self.ui__cb_transparency, 0, wx.ALL, border=10)

        general_sizer.AddSpacer(30)
        general_sizer.Add(line3, 0, wx.CENTRE)
        general_sizer.AddSpacer(10)

        general_sizer.Add(self.cb_enable_hide_ui, 0, wx.ALL, border=10)

        self.SetSizer(general_sizer)


    def on_change_icon_size(self, event):
        """Handles the value change of icon_size dropbox"""
        tools.debug_output(__name__, 'on_change_icon_size', 'Preference - General - change icon size: '+str(event), 1)
        tools.debug_output(__name__, 'on_change_icon_size', 'New icon size is set to: '+str(self.ui__cb_iconsizes.GetValue())+'px', 1)
        ini.write_single_ini_value('General', 'icon_size', self.ui__cb_iconsizes.GetValue()) # update preference value


    def on_change_transparency(self, event):
        """Handles the value change of transparency dropbox"""
        tools.debug_output(__name__, 'on_change_transparency', 'Preference - General - change transparency: '+str(event), 1)
        tools.debug_output(__name__, 'on_change_transparency', 'New transparency value is set to: '+str(self.ui__cb_transparency.GetValue()), 1)
        ini.write_single_ini_value('General', 'transparency', self.ui__cb_transparency.GetValue()) # update preference value


    def prefs_general_toggle_hide_ui(self, event):
        """Toggle the general pref: hide_ui"""
        tools.debug_output(__name__, 'prefs_general_toggle_hide_ui', 'Preference - General - Hide UI: '+str(event), 1)
        if self.cb_enable_hide_ui.GetValue() is True:
            tools.debug_output(__name__, 'prefs_general_toggle_hide_ui', 'Enabled', 1)
            ini.write_single_ini_value('General', 'hide_ui_after_command_execution', "True") # update preference value
        else:
            tools.debug_output(__name__, 'prefs_general_toggle_hide_ui', 'Disabled', 1)
            ini.write_single_ini_value('General', 'hide_ui_after_command_execution', "False") # update preference value


class UITabStatistics(wx.Panel):

    """Preference Window - Tab: Statistics - Shows usage stats"""

    def __init__(self, parent):
        """Inits the statistics tab"""
        wx.Panel.__init__(self, parent)

        ## show app start counter
        cur_ini_value_for_apparat_started = ini.read_single_ini_value('Statistics', 'apparat_started') # get current value from ini
        txt_stats__apparat_started = wx.StaticText(self, -1, "Apparat started:\t\t\t"+cur_ini_value_for_apparat_started, (20, 20))

        ## show execute counter
        cur_ini_value_for_command_executed = ini.read_single_ini_value('Statistics', 'command_executed') # get current value from ini
        txt_stats__command_executed = wx.StaticText(self, -1, "Command executed:\t\t"+cur_ini_value_for_command_executed, (20, 40))

        ## show plugin trigger count
        cur_ini_value_for_plugin_executed = ini.read_single_ini_value('Statistics', 'plugin_executed') # get current value from ini
        txt_stats__plugin_executed = wx.StaticText(self, -1, "Plugins executed:\t\t\t"+cur_ini_value_for_plugin_executed, (20, 60))

        ## Layout
        statistics_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        statistics_sizer.AddSpacer(10)
        statistics_sizer.Add(txt_stats__apparat_started, 0, wx.ALL, border=10)
        statistics_sizer.AddSpacer(10)
        statistics_sizer.Add(txt_stats__command_executed, 0, wx.ALL, border=10)
        statistics_sizer.AddSpacer(10)
        statistics_sizer.Add(txt_stats__plugin_executed, 0, wx.ALL, border=10)
        self.SetSizer(statistics_sizer)


class UITabPluginCommands(wx.Panel):

    """Preference Window - Tab: Commands- Shows available plugins"""

    def __init__(self, parent): # pylint:disable=too-many-statements, too-many-branches, too-many-locals
        """Inits the plugin-commands tab"""
        wx.Panel.__init__(self, parent)

        # Create a font using wx.FontInfo
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False)

        ## Plugin: core (can not be disabled)
        ##
        cb_enable_plugin_core = wx.CheckBox(self, -1, 'Core', (20, 60))
        cb_enable_plugin_core.SetLabel('core')
        cb_enable_plugin_core.SetToolTipString(u'Offers !help !prefs and !preferences.Plugin can not be disabled.')
        cb_enable_plugin_core.SetValue(True)
        cb_enable_plugin_core.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_click) # changing the checkbox change
        cb_enable_plugin_core.Enable(False)
        ## Plugin description
        txt_plugin_core = wx.StaticText(self, -1, "Offers !help !prefs and !preferences", (20, 40))
        txt_plugin_core.SetForegroundColour('#7f8c8d')
        #txt_plugin_core.SetFont(font)

        ## Plugin: Kill
        ##
        cb_enable_plugin_kill = wx.CheckBox(self, -1, 'Misc', (20, 60))
        cb_enable_plugin_kill.SetToolTipString(u'Enable other stuff')
        cb_enable_plugin_kill.SetLabel('kill')
        cur_ini_value_for_plugin_kill = ini.read_single_ini_value('Plugins', 'plugin_kill') # get current value from ini
        if cur_ini_value_for_plugin_kill == 'True':
            cb_enable_plugin_kill.SetValue(True)
        else:
            cb_enable_plugin_kill.SetValue(False)
        cb_enable_plugin_kill.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_kill = wx.StaticText(self, -1, "Kill graphical applications using xkill (requires xkill)", (20, 40))
        txt_plugin_kill.SetForegroundColour('#7f8c8d')
        txt_plugin_kill.SetFont(font)


        ## Plugin: Misc
        ##
        cb_enable_plugin_misc = wx.CheckBox(self, -1, 'Misc', (20, 60))
        cb_enable_plugin_misc.SetToolTipString(u'Enable other stuff')
        cb_enable_plugin_misc.SetLabel('misc')
        cur_ini_value_for_plugin_misc = ini.read_single_ini_value('Plugins', 'plugin_misc') # get current value from ini
        if cur_ini_value_for_plugin_misc == 'True':
            cb_enable_plugin_misc.SetValue(True)
        else:
            cb_enable_plugin_misc.SetValue(False)
        cb_enable_plugin_misc.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_misc = wx.StaticText(self, -1, "Enable other stuff", (20, 40))
        txt_plugin_misc.SetForegroundColour('#7f8c8d')
        txt_plugin_misc.SetFont(font)

        ## Plugin: Nautilus
        ##
        cb_enable_plugin_nautilus = wx.CheckBox(self, -1, 'Nautilus', (20, 60))
        cb_enable_plugin_nautilus.SetLabel('nautilus')
        cb_enable_plugin_nautilus.SetToolTipString(u'Enables quick access to some nautilus locations/places')
        cur_ini_value_for_plugin_nautilus = ini.read_single_ini_value('Plugins', 'plugin_nautilus') # get current value from ini
        if cur_ini_value_for_plugin_nautilus == 'True':
            cb_enable_plugin_nautilus.SetValue(True)
        else:
            cb_enable_plugin_nautilus.SetValue(False)
        cb_enable_plugin_nautilus.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_nautilus = wx.StaticText(self, -1, "Enables quick access to some nautilus locations/places", (20, 40))
        txt_plugin_nautilus.SetForegroundColour('#7f8c8d')
        txt_plugin_nautilus.SetFont(font)

        ## Plugin: PasswordGen
        ##
        cb_enable_plugin_passwordgen = wx.CheckBox(self, -1, 'Password Generator', (20, 60))
        cb_enable_plugin_passwordgen.SetLabel('passwordgen')
        cb_enable_plugin_passwordgen.SetToolTipString(u'Enables a simple password generator')
        cur_ini_value_for_plugin_passwordgen = ini.read_single_ini_value('Plugins', 'plugin_passwordgen') # get current value from ini
        if cur_ini_value_for_plugin_passwordgen == 'True':
            cb_enable_plugin_passwordgen.SetValue(True)
        else:
            cb_enable_plugin_passwordgen.SetValue(False)
        cb_enable_plugin_passwordgen.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_passwordgen = wx.StaticText(self, -1, "Enables a simple password generator", (20, 40))
        txt_plugin_passwordgen.SetForegroundColour('#7f8c8d')
        txt_plugin_passwordgen.SetFont(font)

        ## Plugin: Screenshot
        ##
        cb_enable_plugin_screenshot = wx.CheckBox(self, -1, 'Screenshot', (20, 60))
        cb_enable_plugin_screenshot.SetLabel('screenshot')
        cb_enable_plugin_screenshot.SetToolTipString(u'Enables simple screenshot functions')
        cur_ini_value_for_plugin_screenshot = ini.read_single_ini_value('Plugins', 'plugin_screenshot') # get current value from ini
        if cur_ini_value_for_plugin_screenshot == 'True':
            cb_enable_plugin_screenshot.SetValue(True)
        else:
            cb_enable_plugin_screenshot.SetValue(False)
        cb_enable_plugin_screenshot.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_screenshot = wx.StaticText(self, -1, "Enables simple screenshot functions", (20, 40))
        txt_plugin_screenshot.SetForegroundColour('#7f8c8d')
        txt_plugin_screenshot.SetFont(font)

        ## Plugin: Internet search
        ##
        cb_enable_plugin_internet_search = wx.CheckBox(self, -1, 'Internet-Search', (20, 60))
        cb_enable_plugin_internet_search.SetLabel('search_internet')
        cb_enable_plugin_internet_search.SetToolTipString(u'Enables search for several popular web-services')
        cur_ini_value_for_plugin_search_internet = ini.read_single_ini_value('Plugins', 'plugin_search_internet') # get current value from ini
        if cur_ini_value_for_plugin_search_internet == 'True':
            cb_enable_plugin_internet_search.SetValue(True)
        else:
            cb_enable_plugin_internet_search.SetValue(False)
        cb_enable_plugin_internet_search.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_internet_search = wx.StaticText(self, -1, "Enables search for several popular web-services", (20, 40))
        txt_plugin_internet_search.SetForegroundColour('#7f8c8d')
        txt_plugin_internet_search.SetFont(font)

        ## Plugin: Local search
        ##
        cb_enable_plugin_local_search = wx.CheckBox(self, -1, 'Local-Search', (20, 60))
        cb_enable_plugin_local_search.SetLabel('search_local')
        cb_enable_plugin_local_search.SetToolTipString(u'Enables search for files and folders in users home directory')
        cur_ini_value_for_plugin_search_local = ini.read_single_ini_value('Plugins', 'plugin_search_local') # get current value from ini
        if cur_ini_value_for_plugin_search_local == 'True':
            cb_enable_plugin_local_search.SetValue(True)
        else:
            cb_enable_plugin_local_search.SetValue(False)
        cb_enable_plugin_local_search.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_local_search = wx.StaticText(self, -1, "Enables search for files and folders in users home directory", (20, 40))
        txt_plugin_local_search.SetForegroundColour('#7f8c8d')
        txt_plugin_local_search.SetFont(font)

        ## Plugin: Session
        ##
        cb_enable_plugin_session = wx.CheckBox(self, -1, 'Session', (20, 60))
        cb_enable_plugin_session.SetLabel('session')
        cb_enable_plugin_session.SetToolTipString(u'Enables several session commands')
        cur_ini_value_for_plugin_session = ini.read_single_ini_value('Plugins', 'plugin_session') # get current value from ini
        if cur_ini_value_for_plugin_session == 'True':
            cb_enable_plugin_session.SetValue(True)
        else:
            cb_enable_plugin_session.SetValue(False)
        cb_enable_plugin_session.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_session = wx.StaticText(self, -1, "Enables several session commands", (20, 40))
        txt_plugin_session.SetForegroundColour('#7f8c8d')
        txt_plugin_session.SetFont(font)

        ## Plugin: Shell
        cb_enable_plugin_shell = wx.CheckBox(self, -1, 'Shell', (20, 60))
        cb_enable_plugin_shell.SetLabel('shell')
        cb_enable_plugin_shell.SetToolTipString(u'Enable executing shell commands')
        cur_ini_value_for_plugin_shell = ini.read_single_ini_value('Plugins', 'plugin_shell') # get current value from ini
        if cur_ini_value_for_plugin_shell == 'True':
            cb_enable_plugin_shell.SetValue(True)
        else:
            cb_enable_plugin_shell.SetValue(False)
        cb_enable_plugin_shell.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change
        ## Plugin description
        txt_plugin_shell = wx.StaticText(self, -1, "Enable executing shell commands", (20, 40))
        txt_plugin_shell.SetForegroundColour('#7f8c8d')
        txt_plugin_shell.SetFont(font)


        ## Link to plugin commands description
        wxHyperlinkCtrl = wx.HyperlinkCtrl(self, -1, 'Plugin command details', constants.APP_URL+'#plugins')


        ## -----------------------
        ## Layout
        ## -----------------------
        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)

        ## core
        coreSizer = wx.BoxSizer(wx.HORIZONTAL)
        coreSizer.Add(cb_enable_plugin_core, 0, wx.ALL, border=10) # status icon button
        coreSizer.Add(txt_plugin_core, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(coreSizer, 0, wx.EXPAND)

        ## kill
        killSizer = wx.BoxSizer(wx.HORIZONTAL)
        killSizer.Add(cb_enable_plugin_kill, 0, wx.ALL, border=10) # status icon button
        killSizer.Add(txt_plugin_kill, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(killSizer, 0, wx.EXPAND)

        ## misc
        miscSizer = wx.BoxSizer(wx.HORIZONTAL)
        miscSizer.Add(cb_enable_plugin_misc, 0, wx.ALL, border=10) # status icon button
        miscSizer.Add(txt_plugin_misc, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(miscSizer, 0, wx.EXPAND)
        #pref_sizer.AddSpacer(5)

        ## Nautilus
        nautilusSizer = wx.BoxSizer(wx.HORIZONTAL)
        nautilusSizer.Add(cb_enable_plugin_nautilus, 0, wx.ALL, border=10) # status icon button
        nautilusSizer.Add(txt_plugin_nautilus, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(nautilusSizer, 0, wx.EXPAND)

        ## PasswordGen
        passwordgenSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordgenSizer.Add(cb_enable_plugin_passwordgen, 0, wx.ALL, border=10) # status icon button
        passwordgenSizer.Add(txt_plugin_passwordgen, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(passwordgenSizer, 0, wx.EXPAND)

        ## screenshot
        screenshotSizer = wx.BoxSizer(wx.HORIZONTAL)
        screenshotSizer.Add(cb_enable_plugin_screenshot, 0, wx.ALL, border=10) # status icon button
        screenshotSizer.Add(txt_plugin_screenshot, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(screenshotSizer, 0, wx.EXPAND)

        ## search internet
        searchinternetSizer = wx.BoxSizer(wx.HORIZONTAL)
        searchinternetSizer.Add(cb_enable_plugin_internet_search, 0, wx.ALL, border=10) # status icon button
        searchinternetSizer.Add(txt_plugin_internet_search, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(searchinternetSizer, 0, wx.EXPAND)

        ## search local
        searchlocalSizer = wx.BoxSizer(wx.HORIZONTAL)
        searchlocalSizer.Add(cb_enable_plugin_local_search, 0, wx.ALL, border=10) # status icon button
        searchlocalSizer.Add(txt_plugin_local_search, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(searchlocalSizer, 0, wx.EXPAND)

        ## Session
        sessionSizer = wx.BoxSizer(wx.HORIZONTAL)
        sessionSizer.Add(cb_enable_plugin_session, 0, wx.ALL, border=10) # status icon button
        sessionSizer.Add(txt_plugin_session, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(sessionSizer, 0, wx.EXPAND)

        ## Shell
        shellSizer = wx.BoxSizer(wx.HORIZONTAL)
        shellSizer.Add(cb_enable_plugin_shell, 0, wx.ALL, border=10) # status icon button
        shellSizer.Add(txt_plugin_shell, 0, wx.ALL, border=10) # preferences icon button
        pref_sizer.Add(shellSizer, 0, wx.EXPAND)

        pref_sizer.AddSpacer(10)

        ## Hyperlink to docs
        pref_sizer.Add(wxHyperlinkCtrl, 0, wx.ALL, border=10)

        self.SetSizer(pref_sizer)


    def on_plugin_checkbox_click(self, evt):
        """Handle plugin checkbox click - prevent changing values"""
        e_obj = evt.GetEventObject()
        e_obj.SetValue(not e_obj.GetValue()) # plugin checkboxes are always TRUE/checked
        wx.MessageBox('Plugin can not be disabled', 'Error', wx.OK | wx.ICON_WARNING)


    def on_plugin_checkbox_change(self, event):
        """Triggered if a checkbox state is changing and writes the new state to ini"""
        btn = event.GetEventObject().GetLabel() # button label
        value = event.GetEventObject().GetValue() # button value
        ui_element = event.GetEventObject() # object itself

        if value is True:
            check_requirements = requirements.check_plugin_requirements(btn) # check if requirements for this plugin are fulfilled, otherwise enabling doesnt make sense
            if check_requirements is True:
                tools.debug_output(__name__, 'on_plugin_checkbox_change', 'Enabled Plugin: '+btn, 1)
                ini.write_single_ini_value('Plugins', 'plugin_'+btn, 'True')
            else:
                tools.debug_output(__name__, 'on_plugin_checkbox_change', 'Can not enable plugin: '+btn+' due to missing requirements', 3)
                ui_element.SetValue(False)
                ini.write_single_ini_value('Plugins', 'plugin_'+btn, 'False')
                wx.MessageBox('Plugin can not be enabled because of missing requirements', 'Error', wx.OK | wx.ICON_WARNING)

        else:
            tools.debug_output(__name__, 'on_plugin_checkbox_change', 'Disabled Plugin: '+btn, 1)
            ini.write_single_ini_value('Plugins', 'plugin_'+btn, 'False')

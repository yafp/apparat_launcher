#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules
import wx

## apparat
import constants
import ini
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
        wx.Frame.__init__(self, parent, idd, constants.APP_NAME+' Preferences', size=(600, 700), style=pref_window_style)

        ## Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        ## Create the tab windows
        tab1 = UITabGeneral(nb)
        tab2 = UITabStatistics(nb)
        tab3 = UITabPluginCommands(nb)

        ## Add the windows to tabs and name them.
        nb.AddPage(tab1, "General ")
        nb.AddPage(tab2, "Statistics ")
        nb.AddPage(tab3, "Plugins ")

        ## Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        wx.Frame.CenterOnScreen(self) # center the pref window

        self.Bind(wx.EVT_CLOSE, self.close_preference_ui)


    def close_preference_ui(self, event):
        """Closes the preference window"""
        tools.debug_output('close_preference_ui', 'starting', 1)
        tools.debug_output('close_preference_ui', 'Event: '+str(event), 1)
        self.Destroy() # close the pref UI


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PREFERENCE-TABS- TABS - # https://pythonspot.com/wxpython-tabs/
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class UITabGeneral(wx.Panel):

    """Preference Window - Tab: General"""

    def __init__(self, parent):
        """Inits the general tab"""
        wx.Panel.__init__(self, parent)

        ## show language
        cur_ini_value_for_language = ini.read_single_value('Language', 'lang')          # get current value from ini
        t = wx.StaticText(self, -1, "Language: ", (20, 20))

        languages = [cur_ini_value_for_language]
        combo_box_style = wx.CB_READONLY
        ui__cb_languages = wx.ComboBox(self, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size(100, 30), languages, style=combo_box_style)
        ui__cb_languages.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans'))
        ui__cb_languages.SetValue(languages[0])

        ## Hide UI
        self.cb_enable_hide_ui = wx.CheckBox(self, -1, 'Hide UI after command execution ', (20, 60))
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution')          # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == "False":
            self.cb_enable_hide_ui.SetValue(False)
        else:
            self.cb_enable_hide_ui.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_hide_ui.GetId(), self.prefs_general_toggle_hide_ui)

        ## Layout
        general_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        general_sizer.AddSpacer(10)
        general_sizer.Add(t, 0, wx.ALL, border=10)
        general_sizer.Add(ui__cb_languages, 0, wx.ALL, border=10)
        general_sizer.AddSpacer(10)
        general_sizer.Add(self.cb_enable_hide_ui, 0, wx.ALL, border=10)
        self.SetSizer(general_sizer)


    def prefs_general_toggle_hide_ui(self, event):
        """Toggle the general pref: hide_ui"""
        tools.debug_output('prefs_general_toggle_hide_ui', 'Preference - General - Hide UI: '+str(event), 1)
        if self.cb_enable_hide_ui.GetValue() is True:
            tools.debug_output('prefs_general_toggle_hide_ui', 'Enabled', 1)
            ini.write_single_value('General', 'hide_ui_after_command_execution', "True") # update preference value
        else:
            tools.debug_output('prefs_general_toggle_hide_ui', 'Disabled', 1)
            ini.write_single_value('General', 'hide_ui_after_command_execution', "False") # update preference value



class UITabStatistics(wx.Panel):

    """Preference Window - Tab: Statistics - Shows usage stats"""

    def __init__(self, parent):
        """Inits the statistics tab"""
        wx.Panel.__init__(self, parent)

        ## show app start counter
        cur_ini_value_for_apparat_started = ini.read_single_value('Statistics', 'apparat_started')          # get current value from ini
        t1 = wx.StaticText(self, -1, "Apparat started:\t\t\t"+cur_ini_value_for_apparat_started, (20, 20))

        ## show execute counter
        cur_ini_value_for_command_executed = ini.read_single_value('Statistics', 'command_executed')          # get current value from ini
        t2 = wx.StaticText(self, -1, "Command executed:\t\t"+cur_ini_value_for_command_executed, (20, 40))

        ## show plugin trigger count
        cur_ini_value_for_plugin_executed = ini.read_single_value('Statistics', 'plugin_executed')          # get current value from ini
        t3 = wx.StaticText(self, -1, "Plugins executed:\t\t\t"+cur_ini_value_for_plugin_executed, (20, 60))

        statistics_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        statistics_sizer.AddSpacer(10)
        statistics_sizer.Add(t1, 0, wx.ALL, border=10)
        statistics_sizer.AddSpacer(10)
        statistics_sizer.Add(t2, 0, wx.ALL, border=10)
        statistics_sizer.AddSpacer(10)
        statistics_sizer.Add(t3, 0, wx.ALL, border=10)
        self.SetSizer(statistics_sizer)



class UITabPluginCommands(wx.Panel):

    """Preference Window - Tab: Commands- Shows available plugins"""

    def __init__(self, parent): # pylint:disable=too-many-statements
        """Inits the plugin-commands tab"""
        wx.Panel.__init__(self, parent)

        ## Plugin: core (can not be disabled)
        self.cb_enable_plugin_core = wx.CheckBox(self, -1, 'Core', (20, 60))
        self.cb_enable_plugin_core.SetLabel('core')
        self.cb_enable_plugin_core.SetToolTipString(u'Offers !help !prefs and !preferences.Plugin can not be disabled.')
        self.cb_enable_plugin_core.SetValue(True)
        self.cb_enable_plugin_core.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_click) # changing the checkbox change

        ## Plugin: Local search
        self.cb_enable_plugin_local_search = wx.CheckBox(self, -1, 'Local-Search', (20, 60))
        self.cb_enable_plugin_local_search.SetLabel('search_local')
        self.cb_enable_plugin_local_search.SetToolTipString(u'Enables search for files and folders in users home directory')
        cur_ini_value_for_plugin_search_local = ini.read_single_value('Plugins', 'enable_plugin_search_local')          # get current value from ini
        if cur_ini_value_for_plugin_search_local == 'True':
            self.cb_enable_plugin_local_search.SetValue(True)
        else:
            self.cb_enable_plugin_local_search.SetValue(False)
        self.cb_enable_plugin_local_search.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Plugin: Internet search
        self.cb_enable_plugin_internet_search = wx.CheckBox(self, -1, 'Internet-Search', (20, 60))
        self.cb_enable_plugin_internet_search.SetLabel('search_internet')
        self.cb_enable_plugin_internet_search.SetToolTipString(u'Enables search for several popular web-services')
        cur_ini_value_for_plugin_search_internet = ini.read_single_value('Plugins', 'enable_plugin_search_internet')          # get current value from ini
        if cur_ini_value_for_plugin_search_internet == 'True':
            self.cb_enable_plugin_internet_search.SetValue(True)
        else:
            self.cb_enable_plugin_internet_search.SetValue(False)
        self.cb_enable_plugin_internet_search.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Plugin: Nautilus
        self.cb_enable_plugin_nautilus = wx.CheckBox(self, -1, 'Nautilus', (20, 60))
        self.cb_enable_plugin_nautilus.SetLabel('nautilus')
        self.cb_enable_plugin_nautilus.SetToolTipString(u'Enables quick access to some nautilus locations/places')
        cur_ini_value_for_plugin_nautilus = ini.read_single_value('Plugins', 'enable_plugin_nautilus')          # get current value from ini
        if cur_ini_value_for_plugin_nautilus == 'True':
            self.cb_enable_plugin_nautilus.SetValue(True)
        else:
            self.cb_enable_plugin_nautilus.SetValue(False)
        self.cb_enable_plugin_nautilus.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Plugin: Screenshot
        self.cb_enable_plugin_screenshot = wx.CheckBox(self, -1, 'Screenshot', (20, 60))
        self.cb_enable_plugin_screenshot.SetLabel('screenshot')
        self.cb_enable_plugin_screenshot.SetToolTipString(u'Enables simple screenshot functions')
        cur_ini_value_for_plugin_screenshot = ini.read_single_value('Plugins', 'enable_plugin_screenshot')          # get current value from ini
        if cur_ini_value_for_plugin_screenshot == 'True':
            self.cb_enable_plugin_screenshot.SetValue(True)
        else:
            self.cb_enable_plugin_screenshot.SetValue(False)
        self.cb_enable_plugin_screenshot.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Plugin: Session
        self.cb_enable_plugin_session = wx.CheckBox(self, -1, 'Session', (20, 60))
        self.cb_enable_plugin_session.SetLabel('session')
        self.cb_enable_plugin_session.SetToolTipString(u'Enables several session commands')
        cur_ini_value_for_plugin_session = ini.read_single_value('Plugins', 'enable_plugin_session')          # get current value from ini
        if cur_ini_value_for_plugin_session == 'True':
            self.cb_enable_plugin_session.SetValue(True)
        else:
            self.cb_enable_plugin_session.SetValue(False)
        self.cb_enable_plugin_session.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Plugin: Shell
        self.cb_enable_plugin_shell = wx.CheckBox(self, -1, 'Shell', (20, 60))
        self.cb_enable_plugin_shell.SetLabel('shell')
        self.cb_enable_plugin_shell.SetToolTipString(u'Enable executing shell commands')
        cur_ini_value_for_plugin_shell = ini.read_single_value('Plugins', 'enable_plugin_shell')          # get current value from ini
        if cur_ini_value_for_plugin_shell == 'True':
            self.cb_enable_plugin_shell.SetValue(True)
        else:
            self.cb_enable_plugin_shell.SetValue(False)
        self.cb_enable_plugin_shell.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Plugin: Misc
        self.cb_enable_plugin_misc = wx.CheckBox(self, -1, 'Misc', (20, 60))
        self.cb_enable_plugin_misc.SetToolTipString(u'Enable other stuff')
        self.cb_enable_plugin_misc.SetLabel('misc')
        cur_ini_value_for_plugin_misc = ini.read_single_value('Plugins', 'enable_plugin_misc')          # get current value from ini
        if cur_ini_value_for_plugin_misc == 'True':
            self.cb_enable_plugin_misc.SetValue(True)
        else:
            self.cb_enable_plugin_misc.SetValue(False)
        self.cb_enable_plugin_misc.Bind(wx.EVT_CHECKBOX, self.on_plugin_checkbox_change) # changing the checkbox change

        ## Link to plugin commands description
        wxHyperlinkCtrl = wx.HyperlinkCtrl(self, -1, 'Plugin command details', constants.APP_URL+'#plugins')



        ## -----------------------
        ## Layout
        ## -----------------------
        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)

        ## core
        pref_sizer.Add(self.cb_enable_plugin_core, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## misc
        pref_sizer.Add(self.cb_enable_plugin_misc, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## Nautilus
        pref_sizer.Add(self.cb_enable_plugin_nautilus, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## screenshot
        pref_sizer.Add(self.cb_enable_plugin_screenshot, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## search internet
        pref_sizer.Add(self.cb_enable_plugin_internet_search, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## search local
        pref_sizer.Add(self.cb_enable_plugin_local_search, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## Session
        pref_sizer.Add(self.cb_enable_plugin_session, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)

        ## Shell
        pref_sizer.Add(self.cb_enable_plugin_shell, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(20)

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
        btn = event.GetEventObject().GetLabel()
        value = event.GetEventObject().GetValue()

        if value is True:
            tools.debug_output('on_plugin_checkbox_change', 'Enabled Plugin: '+btn, 1)
            ini.write_single_value('Plugins', 'enable_plugin_'+btn, 'True')
        else:
            tools.debug_output('on_plugin_checkbox_change', 'Disabled Plugin: '+btn, 1)
            ini.write_single_value('Plugins', 'enable_plugin_'+btn, 'False')

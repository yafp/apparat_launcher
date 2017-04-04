#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules
import wx
#import wx.grid

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
        tools.debug_output('close_preference_ui', 'starting')
        tools.debug_output('close_preference_ui', 'Event: '+str(event))
        self.Destroy() # close the pref UI
        # TODO: set focus back to main-window


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
        t = wx.StaticText(self, -1, "Language: "+cur_ini_value_for_language, (20, 20))

        ## Hide UI
        self.cb_enable_hide_ui = wx.CheckBox(self, -1, 'Hide UI after command execution ', (20, 60))
        cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution')          # get current value from ini
        if cur_ini_value_for_hide_ui_after_command_execution == "False":
            self.cb_enable_hide_ui.SetValue(False)
        else:
            self.cb_enable_hide_ui.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb_enable_hide_ui.GetId(), self.prefs_general_toggle_hide_ui)

        general_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        general_sizer.AddSpacer(10)
        general_sizer.Add(t, 0, wx.ALL, border=10)
        general_sizer.AddSpacer(10)
        general_sizer.Add(self.cb_enable_hide_ui, 0, wx.ALL, border=10)
        self.SetSizer(general_sizer)


    def prefs_general_toggle_hide_ui(self, event):
        """Toggle the general pref: hide_ui"""
        tools.debug_output('prefs_general_toggle_hide_ui', 'Preference - General - Hide UI: '+str(event))
        if self.cb_enable_hide_ui.GetValue() is True:
            tools.debug_output('prefs_general_toggle_hide_ui', 'Enabled')
            ini.write_single_value('General', 'hide_ui_after_command_execution', "True") # update preference value
        else:
            tools.debug_output('prefs_general_toggle_hide_ui', 'Disabled')
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

    """Preference Window - Tab: Commands- Shows available plugin commands"""

    def __init__(self, parent):
        """Inits the plugin-commands tab"""
        wx.Panel.__init__(self, parent)

        # Plugin: Local search
        cb_enable_plugin_local_search = wx.CheckBox(self, -1, 'Local-Search', (20, 60))
        cb_enable_plugin_local_search.SetToolTipString(u'Enables search for user home')
        cb_enable_plugin_local_search.SetValue(True)
        cb_enable_plugin_local_search.Disable()

        # Plugin: Internet search
        cb_enable_plugin_insernet_search = wx.CheckBox(self, -1, 'Internet-Search', (20, 60))
        cb_enable_plugin_insernet_search.SetToolTipString(u'Enables search for several popular web-services')
        cb_enable_plugin_insernet_search.SetValue(True)
        cb_enable_plugin_insernet_search.Disable()

        # Plugin: Nautilus
        cb_enable_plugin_nautilus = wx.CheckBox(self, -1, 'Nautilus', (20, 60))
        cb_enable_plugin_nautilus.SetToolTipString(u'Enables quick access to some nautilus locations/places')
        cb_enable_plugin_nautilus.SetValue(True)
        cb_enable_plugin_nautilus.Disable()

        # Plugin: Screenshot
        cb_enable_plugin_screenshot = wx.CheckBox(self, -1, 'Screenshot', (20, 60))
        cb_enable_plugin_screenshot.SetToolTipString(u'Enables simple screenshot functions')
        cb_enable_plugin_screenshot.SetValue(True)
        cb_enable_plugin_screenshot.Disable()

        # Plugin: Session
        cb_enable_plugin_session = wx.CheckBox(self, -1, 'Session', (20, 60))
        cb_enable_plugin_session.SetToolTipString(u'Enables several session commands')
        cb_enable_plugin_session.SetValue(True)
        cb_enable_plugin_session.Disable()

        ## Layout
        #
        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)

        # Local search
        pref_sizer.Add(cb_enable_plugin_local_search, 0, wx.ALL, border=10)

        # Spacer
        pref_sizer.AddSpacer(5)

        # Internet search
        pref_sizer.Add(cb_enable_plugin_insernet_search, 0, wx.ALL, border=10)

        # Spacer
        pref_sizer.AddSpacer(5)

        # Nautilus
        pref_sizer.Add(cb_enable_plugin_nautilus, 0, wx.ALL, border=10)

        # Spacer
        pref_sizer.AddSpacer(5)

        # Session
        pref_sizer.Add(cb_enable_plugin_screenshot, 0, wx.ALL, border=10)

        # Spacer
        pref_sizer.AddSpacer(5)

        # Session
        pref_sizer.Add(cb_enable_plugin_session, 0, wx.ALL, border=10)


        self.SetSizer(pref_sizer)

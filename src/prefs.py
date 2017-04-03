#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules
import wx

## projects internal modules
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
        nb.AddPage(tab3, "Plugin Commands ")

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

        FONT_BIG = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD) # family, style, weight
        FONT_NORMAL_MONO = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')

        # Plugin: Internet search
        plugin_internet_search_headline = wx.StaticText(self, -1, "Internet-Search", (20, 100))
        plugin_internet_search_headline.SetFont(FONT_BIG)
        plugin_internet_search_details = wx.StaticText(self, -1, "!a = Amazon\n!b = Bandcamp\n!e = Stack-Exchange\n!g = Google\n!l = LastFM\n!m = Google Maps\n!o = Stack-Overflow\n!r = Reddit\n!s = SoudCloud\n!t = Twitter\n!v = Vimeo\n!w = Wikipedia\n!y = YouTube", (20, 140))
        plugin_internet_search_details.SetFont(FONT_NORMAL_MONO)

        # Plugin: Nautilus
        plugin_nautilus_headline = wx.StaticText(self, -1, "Nautilus", (20, 20))
        plugin_nautilus_headline.SetFont(FONT_BIG)
        plugin_nautilus_details = wx.StaticText(self, -1, "!network = Show network devices in nautilus\n!goto    = Open custom path in nautilus\n!recent  = Show recent files in nautilus\n!trash   = Show trash in nautilus", (20, 60))
        plugin_nautilus_details.SetFont(FONT_NORMAL_MONO)

        # Plugin: Session
        plugin_session_headline = wx.StaticText(self, -1, "Session", (20, 20))
        plugin_session_headline.SetFont(FONT_BIG)
        plugin_session_details = wx.StaticText(self, -1, "!lock      = Lock session\n!logout    = Logout session\n!shutdown  = Shutdown machine\n!hibernate = Hibernate machine\n!reboot    = Reboot machine", (20, 60))
        plugin_session_details.SetFont(FONT_NORMAL_MONO)

        # Lines
        line1 = wx.StaticLine(self, -1, (25, 50), (600, 1))
        line2 = wx.StaticLine(self, -1, (25, 50), (600, 1))

        ## Layout
        #
        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)
        # Internet search
        pref_sizer.Add(plugin_internet_search_headline, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_internet_search_details, 0, wx.ALL, border=10)
        # Spacer
        pref_sizer.AddSpacer(5)
        pref_sizer.Add(line1, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)
        # Nautilus
        pref_sizer.Add(plugin_nautilus_headline, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_nautilus_details, 0, wx.ALL, border=10)
        # Spacer
        pref_sizer.AddSpacer(5)
        pref_sizer.Add(line2, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(5)
        # Session
        pref_sizer.Add(plugin_session_headline, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_session_details, 0, wx.ALL, border=10)

        self.SetSizer(pref_sizer)

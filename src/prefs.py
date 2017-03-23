#!/usr/bin/python
"""apparat - an application launcher for linux"""

# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

## built-in modules
import wx

## project’s internal modules
import config
import constants
import ini
import tools


# -----------------------------------------------------------------------------------------------
# PREFERENCE WINDOW
# -----------------------------------------------------------------------------------------------
class PreferenceWindow(wx.Frame):

    """Class for Preference Window"""

    def __init__(self, parent, id):
        """Initialize the preference window"""
        ## define style of preference window
        pref_window_style = (wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        wx.Frame.__init__(self, parent, id, constants.APP_NAME+' Preferences', size=(600, 700), style=pref_window_style)

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
        tools.print_debug_to_terminal('close_preference_ui', 'starting')
        tools.print_debug_to_terminal('close_preference_ui', 'Event: '+str(event))
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
        tools.print_debug_to_terminal('prefs_general_toggle_hide_ui', 'Preference - General - Hide UI: '+str(event))
        if self.cb_enable_hide_ui.GetValue() is True:
            tools.print_debug_to_terminal('prefs_general_toggle_hide_ui', 'Enabled')
            ini.write_single_value('General', 'hide_ui_after_command_execution', "True") # update preference value
        else:
            tools.print_debug_to_terminal('prefs_general_toggle_hide_ui', 'Disabled')
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

        h1_plugin_session = wx.StaticText(self, -1, "Session", (20, 20))
        h1_plugin_session.SetFont(FONT_BIG)

        plugin_session_cmd_list = wx.StaticText(self, -1, "!lock      = Lock session\n!logout    = Logout session\n!shutdown  = Shutdown machine\n!hibernate = Hibernate machine\n!reboot    = Reboot machine", (20, 60))
        plugin_session_cmd_list.SetFont(FONT_NORMAL_MONO)

        h1_plugin_internet_search = wx.StaticText(self, -1, "Internet-Search", (20, 100))
        h1_plugin_internet_search.SetFont(FONT_BIG)

        plugin_internet_search_cmd_list = wx.StaticText(self, -1, "!a = Amazon\n!b = Bandcamp\n!e = Stack-Exchange\n!g = Google\n!l = LastFM\n!o = Stack-Overflow\n!r = Reddit\n!s = SoudCloud\n!t = Twitter\n!v = Vimeo\n!w = Wikipedia\n!y = YouTube", (20, 140))
        plugin_internet_search_cmd_list.SetFont(FONT_NORMAL_MONO)

        h1_plugin_nautilus = wx.StaticText(self, -1, "Nautilus", (20, 20))
        h1_plugin_nautilus.SetFont(FONT_BIG)

        plugin_nautilus_cmd_list = wx.StaticText(self, -1, "!network = Show network devices in nautilus\n!goto    = Open custom path in nautilus\n!recent  = Show recent files in nautilus\n!trash   = Show trash in nautilus", (20, 60))
        plugin_nautilus_cmd_list.SetFont(FONT_NORMAL_MONO)

        pref_sizer = wx.BoxSizer(wx.VERTICAL) # define layout container
        pref_sizer.AddSpacer(10)
        pref_sizer.Add(h1_plugin_internet_search, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_internet_search_cmd_list, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(10)
        pref_sizer.Add(h1_plugin_nautilus, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_nautilus_cmd_list, 0, wx.ALL, border=10)
        pref_sizer.AddSpacer(10)
        pref_sizer.Add(h1_plugin_session, 0, wx.ALL, border=10)
        pref_sizer.Add(plugin_session_cmd_list, 0, wx.ALL, border=10)
        self.SetSizer(pref_sizer)



class UITabAbout(wx.Panel):

    """Preference Window - Tab: About"""

    def __init__(self, parent):
        """Inits the About Tab"""
        wx.Panel.__init__(self, parent)

        FONT_BIG = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD) # family, style, weight
        FONT_NORMAL_MONO = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')

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

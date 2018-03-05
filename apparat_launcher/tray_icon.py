#!/usr/bin/python
"""Handles the tray icon and tray menu"""


# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------
## general
import webbrowser
import wx


## apparat
import constants
import tools
import version
import prefs


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY-MENU
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_menu_item(menu, label, func, enable=True):
    """Generates single menu items for the tray icon popup menu"""
    tools.debug_output(__name__, 'create_menu_item', 'Menuitem: '+label, 1)
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    if enable is False:
        item.Enable(False)
    return item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# APP_TRAY_ICON
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TaskBarIcon(wx.TaskBarIcon): # pylint:disable=too-many-ancestors

    """Class for the Task Bar Icon"""

    def __init__(self, frame):
        """Method to initialize the tray icon"""
        tools.debug_output(__name__, '__init__ (TaskBarIcon)', 'starting', 1)
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_tray_icon(constants.APP_TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_app_tray_icon_left_click)
        tools.debug_output(__name__, '__init__ (TaskBarIcon)', 'Task icon is ready now', 1)


    def CreatePopupMenu(self): # pylint:disable=invalid-name
        """Method to generate a Popupmenu for the TrayIcon (do NOT rename)"""
        tools.debug_output(__name__, 'CreatePopupMenu', 'starting', 1)
        menu = wx.Menu()
        create_menu_item(menu, "Version "+version.APP_VERSION, self.on_tray_popup_click_github, enable=False) # disabled menu
        menu.AppendSeparator()
        create_menu_item(menu, 'Show', self.on_tray_popup_left_show)
        menu.AppendSeparator()
        create_menu_item(menu, 'Preferences', self.on_tray_popup_click_preferences)
        create_menu_item(menu, 'About', self.on_tray_popup_click_about)
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
        tools.debug_output(__name__, 'on_app_tray_icon_left_click', 'starting with event: '+str(event), 1)
        self.execute_tray_icon_left_click()


    def execute_tray_icon_left_click(self):
        """Method to handle left click on the tray icon - toggles visibility of the Main Window"""
        if self.frame.IsIconized(): # if main window is minimized
            tools.debug_output(__name__, 'execute_tray_icon_left_click', 'MainWindow is now visible', 1)
            self.frame.Raise()
        else: # if main window is shown
            tools.debug_output(__name__, 'execute_tray_icon_left_click', 'MainWindow is now hidden/minimized', 1)
            self.frame.Iconize(True)


    def on_tray_popup_left_show(self, event):
        """Method to handle click in the 'Show mainwindow' tray menu item"""
        tools.debug_output(__name__, 'on_tray_popup_left_show', 'starting with event: '+str(event), 1)
        if self.frame.IsIconized(): # if main window is minimized
            tools.debug_output(__name__, 'on_tray_popup_left_show', 'MainWindow is now visible', 1)
            self.frame.Raise()
        else: # if main window is shown
            tools.debug_output(__name__, 'on_tray_popup_left_show', 'MainWindow is already shown, nothing to do here', 1)


    def on_tray_popup_click_preferences(self, event):
        """Method to handle click in the 'Preferences' tray menu item"""
        tools.debug_output(__name__, 'on_tray_popup_click_preferences', 'starting with event: '+str(event), 1)
        self.open_preference_window()


    def on_tray_popup_click_about(self, event):
        """Method to handle click in the 'About' tray menu item"""
        tools.debug_output(__name__, 'on_tray_popup_click_about', 'starting with event: '+str(event), 1)
        aboutInfo = wx.AboutDialogInfo()
        aboutInfo.SetName(constants.APP_NAME)
        aboutInfo.SetVersion(version.APP_VERSION)
        aboutInfo.SetDescription((constants.APP_DESCRIPTION))
        aboutInfo.SetLicense(open("../LICENSE").read())
        aboutInfo.SetWebSite(constants.APP_URL)
        aboutInfo.SetIcon(wx.Icon('gfx/core/128/appIcon.png', wx.BITMAP_TYPE_PNG, 128, 128))
        aboutInfo.AddDeveloper("yafp")
        #aboutInfo.AddDeveloper('Name of other contributors') # additional devs/contributors
        wx.AboutBox(aboutInfo)


    def on_tray_popup_click_exit(self, event):
        """Method to handle click in the 'Exit' tray menu item"""
        tools.debug_output(__name__, 'on_tray_popup_click_exit', 'starting with event: '+str(event), 1)
        wx.CallAfter(self.frame.Close)


    def on_tray_popup_click_github(self, event):
        """Method to handle click on the 'GitHub' tray menu item"""
        tools.debug_output(__name__, 'on_tray_popup_click_github', 'starting with event: '+str(event), 1)
        tools.debug_output(__name__, 'on_tray_popup_click_github', 'Opening: '+constants.APP_URL, 1)
        webbrowser.open(constants.APP_URL) # Go to github


    # method exists in apprat_launcher & tray_icon right now - Baustelle
    def open_preference_window(self):
        """Opens the preference window"""
        tools.debug_output(__name__, 'open_preference_window', 'starting', 1)
        self.prefWindow = prefs.PreferenceWindow(parent=None, idd=-1)
        self.prefWindow.Show()


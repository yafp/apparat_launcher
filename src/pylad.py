#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# via: http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python


# -----------------------------------------------------------------------------------------------
# IMPORTING
# -----------------------------------------------------------------------------------------------
import wx                           # for all the WX items
import os, fnmatch                  # for searching applications
import webbrowser                   # for opening urls (example: github project page)
import gtk                          # for app-icon handling - crashes - reason: wx?
gtk.remove_log_handlers()           # if this line is removed - app is crashing as long as both WX and GTK are imported.
                                    # reference: https://groups.google.com/forum/#!topic/wxpython-users/KO_hmLxeDKA
from subprocess import call         # for calling external commands
import subprocess                   # for checking if cmd_exists



# -----------------------------------------------------------------------------------------------
# CONSTANTS (DEVELOPER)
# -----------------------------------------------------------------------------------------------
TRAY_TOOLTIP = 'pylad'
TRAY_ICON = 'gfx/bt_appIcon_16.png'
appName = 'pylad'
appURL = 'https://github.com/yafp/pylad'
targetIconSize = 128



# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
appVersion = '20170222.01'



# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------
def cmd_exists(cmd):
    print('Method: cmd_exists')
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0



class MyFrame(wx.Frame):
    # We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,330))
        self.SetSizeHintsSz( wx.Size( 400,330 ), wx.Size( 400,330 ) )   # forcing min and max size to same values - prevents resizing option

        # set an application icon
        appIcon = wx.Icon('gfx/bt_appIcon_16.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(appIcon)


        # ------------------------------------------------
        # Define UI Elements
        # ------------------------------------------------

        # Preference button
        img_preferences = wx.Bitmap('gfx/bt_prefs_16.png', wx.BITMAP_TYPE_BMP)
        #self.bt_preferences = wx.BitmapButton(self, id = wx.ID_ANY, bitmap = img_preferences, size = (img_preferences.GetWidth()+10, img_preferences.GetHeight()+10))
        self.bt_preferences = wx.BitmapButton(self, id = wx.ID_ANY, style=wx.NO_BORDER, bitmap = img_preferences, size = (img_preferences.GetWidth()+10, img_preferences.GetHeight()+10))
        self.bt_preferences.SetLabel('Preferences')
        self.bt_preferences.SetToolTipString( u'Open Preferences' )


        # Search & Search Results as comboBox
        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
        self.m_comboBox1.SetToolTipString( u'Search & Results' )
        
        
        # launchbutton
        self.img_application = wx.Image('gfx/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_application = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 156,156 ), wx.BU_AUTODRAW )
        self.bt_application.SetBitmapFocus( wx.NullBitmap )
        self.bt_application.SetBitmapHover( wx.NullBitmap )
        #self.bt_application.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        #self.bt_application.SetBackgroundColour( wx.Colour( 255, 0, 255 ) )
        self.bt_application.SetToolTipString( u'Launch' )
        self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
        self.bt_application.SetLabel('Launch')
        self.bt_application.Enable( False )
        
        
        # optionbutton
        self.img_options = wx.Image('gfx/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_options = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 156,156 ), wx.BU_AUTODRAW )
        self.bt_options.SetBitmapFocus( wx.NullBitmap )
        self.bt_options.SetBitmapHover( wx.NullBitmap )
        self.bt_options.SetToolTipString( u'Options' )
        self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
        self.bt_options.SetLabel('Options')
        self.bt_options.Enable( False )
        
        
        # label 1
        self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_CENTRE|wx.NO_BORDER, size=(100, -1), pos=(10, 10) )
        self.m_textCtrl3.SetFont( wx.Font( 10, 74, 90, 92, False, 'Sans' ) )
        self.m_textCtrl3.SetToolTipString( u'Launch' )
        self.m_textCtrl3.SetMinSize( wx.Size( 156,30 ) )
        self.m_textCtrl3.SetMaxSize( wx.Size( 156,30 ) )
        self.m_textCtrl3.SetEditable(True)
        self.m_textCtrl3.Enable( True )
        
        
        # label 2
        self.m_textCtrl4 = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_CENTRE|wx.NO_BORDER, size=(100, -1), pos=(10, 10) )
        self.m_textCtrl4.SetFont( wx.Font( 10, 74, 90, 92, False, 'Sans' ) )
        self.m_textCtrl4.SetToolTipString( u'Launch' )
        self.m_textCtrl4.SetMinSize( wx.Size( 156,30 ) )
        self.m_textCtrl4.SetMaxSize( wx.Size( 156,30 ) )
        self.m_textCtrl4.SetEditable(True)
        self.m_textCtrl4.Enable( True )
        
        
        #  result counter
        #self.txt_resultCounter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_resultCounter = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_CENTRE|wx.NO_BORDER, size=(100, -1), pos=(10, 10) )
        self.txt_resultCounter.SetFont( wx.Font( 10, 74, 90, 92, False, 'Sans' ) )
        self.txt_resultCounter.SetToolTipString( u'Result count' )
        self.txt_resultCounter.SetMinSize( wx.Size( 100,30 ) )
        self.txt_resultCounter.SetMaxSize( wx.Size( 100,30 ) )
        self.txt_resultCounter.SetEditable(False)
        self.txt_resultCounter.Enable( False )
        
        
        # Version Information
        self.txt_versionInformation = wx.StaticText( self, wx.ID_ANY, ' v'+appVersion, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_versionInformation.Wrap( -1 )
        self.txt_versionInformation.SetFont( wx.Font( 8, 74, 90, 90, False, 'Sans' ) )
        self.txt_versionInformation.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        
        
        # ------------------------------------------------
        # Layout
        # ------------------------------------------------
        
        # define layout container
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer1.Add( self.bt_preferences, 0, wx.ALIGN_RIGHT, 100)           # preferences
        bSizer1.Add( self.m_comboBox1, 0, wx.EXPAND)                        # search / dropdown
        
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add( self.bt_application, 0, wx.CENTRE)                               # launch button
        box1.Add( self.bt_options, 0, wx.CENTRE)                               # options button
        bSizer1.Add( box1, 0, wx.CENTRE)                                   
        
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add( self.m_textCtrl3, 0, wx.CENTRE)                           # launch text
        box2.Add( self.m_textCtrl4, 0, wx.CENTRE)                           # option text
        bSizer1.Add( box2, 0, wx.CENTRE)
        
        bSizer1.Add( self.txt_resultCounter, 0, wx.CENTRE)                  # result count
        bSizer1.Add( self.txt_versionInformation, 0, wx.CENTRE )            # version
        
        self.SetSizer( bSizer1 )
        #self.Layout()

        self.Center() # open window centered


        # ------------------------------------------------
        # Bind/Connect Events
        # ------------------------------------------------
        self.m_comboBox1.Bind( wx.EVT_KEY_UP, self.onKeyPressInCombobox )               # ComboBox
        # image buttons - https://www.tutorialspoint.com/wxpython/wxpython_buttons.htm
        self.bt_preferences.Bind(wx.EVT_BUTTON, self.OnClicked) 
        


        # ------------------------------------------------
        # Statusbar (on bottom of window)
        # ------------------------------------------------
        #self.CreateStatusBar() # A Statusbar in the bottom of the window
        
        
        # ------------------------------------------------
        # Menubar
        # ------------------------------------------------
        ## Setting up the menu.
        #filemenu= wx.Menu()
        
        ## wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        #filemenu.Append(wx.ID_ABOUT, '&About',' Information about this program')
        #filemenu.AppendSeparator()
        #filemenu.Append(wx.ID_EXIT,'E&xit',' Terminate the program')

        ## Creating the menubar.
        #menuBar = wx.MenuBar()
        #menuBar.Append(filemenu,'&File') # Adding the "filemenu" to the MenuBar
        #self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        self.Show(True)
        
        self.m_comboBox1.SetFocus()     # set focus to search


    def OnClicked(self, event): 
        btn = event.GetEventObject().GetLabel() 
        print 'Label of pressed button = ',btn 
        if (btn =='Preferences'):
            print('\nOpen Preferences')
            self.m_comboBox1.SetFocus() # set focus back to search



    def onEnter(self, event):
        print('Enter in Search')



    def onKeyPressInCombobox(self, event):
        print('\nOn Key Press On Comboxbox')
        kc = event.GetKeyCode()
        if(kc == 13) : # Enter
            print('\tENTER')
            self.launchExternalApplication()
            
        elif(kc == 27) : # ESC
            print('\tESC in combobox')
            self.resetUI()
            
        elif(kc == 317):    # Arrow Down
            print('\tARROW DOWN')
            self.m_comboBox1.Popup()
        else:
            currentSearchString=self.m_comboBox1.GetValue()
            if(len(currentSearchString) == 0):
                self.resetUI()
            else:
                print('\tSearching: '+currentSearchString)
                self.searchApplications(currentSearchString)
        
    
    
    def launchExternalApplication(self):
        print('\nlaunchExternalApplication')
        currentSelectedAppName = self.searchApplications(self.m_comboBox1.GetValue())

        #if currentSelectedAppName != '' or currentSelectedAppName != 'None':
        if(currentSelectedAppName is not None): # Check if the dropdown contains something at all or not
            print("\tShould execute: "+currentSelectedAppName)
            checkExecutable = cmd_exists(currentSelectedAppName)                   # check if name exists and is executable
            if (checkExecutable == True):
                print('\tExecutable: '+currentSelectedAppName+' exists')
                # https://docs.python.org/2/library/subprocess.html
                #
                #call([currentSelectedAppName, ""])                                 # launch external command
                call([currentSelectedAppName])                                 # launch external command
                print('\tExecuted: '+currentSelectedAppName)
                self.resetUI()
            else:
                print ('\tERROR >> Checking the executable failed')
        else:
            print('\tWARNING >> currentSelectedAppName is empty, aborting')



    def openAppURL(self):
        print('\nopenAppURL')
        print('\tOpening '+appURL+' in default browser')
        webbrowser.open(appURL)  # Go to github



    def resetUI(self):
        print('\nresetUI')
        # combobox
        self.m_comboBox1.SetFocus()                                 # set focus to search
        self.m_comboBox1.SetValue('')                               # reset dropdown with search results
        
        # launch button
        self.img_application = wx.Image('gfx/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_application.Enable( False )
        self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
        self.bt_application.SetToolTipString( 'Launch')
        
        # option buttons
        self.img_options = wx.Image('gfx/bt_appIcon_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_options.Enable( False )
        self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
        self.bt_options.SetToolTipString( 'Options')
        
        # result counter
        self.txt_resultCounter.SetValue('')                               # Reset result counter
        print('\tFinished resetting UI')



    def searchApplications(self, currentSearchString):
        print('\nsearchApplications')
        if(currentSearchString != ''):
        
            # Plugin Session
            if(currentSearchString == '!s'):
                print('\tSession Plugin activated')
                self.bt_options.SetFocus()
                
                # option buttons
                self.img_options = wx.Image('gfx/bt_optionLock_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_options.Enable( True )
                self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
                self.bt_options.SetToolTipString( 'Lock')
                
                # gnome-screensaver-command', '--lock'])
                self.m_comboBox1.SetValue('')                               # reset dropdown with search results
                self.m_comboBox1.SetValue('gnome-screensaver-command -lock')
                
                return
                
        
            print('\tSearching executables for the following string: '+currentSearchString)
            searchResults = fnmatch.filter(os.listdir('/usr/bin'), '*'+currentSearchString+'*')     # search for executables matching users searchstring
            searchResults.sort() # sort search results (from a to z)
            
            self.txt_resultCounter.SetValue(str(len(searchResults)))  # update result count
        
            if(len(searchResults) == 0):
                print('Found 0 applications')
                self.m_comboBox1.SetItems(searchResults)
                
                # update launch button icon
                self.img_application = wx.Image('gfx/bt_result_sad_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())

            elif(len(searchResults) == 1):     # if we got 1 search-results
                print('\tFound 1 matching application')

                # update combobox
                self.m_comboBox1.SetItems(searchResults)
                #self.m_comboBox1.SetSelection(0)
                
                # update launch button
                self.bt_application.Enable( True ) # Enable new launch button
                self.bt_application.SetToolTipString( searchResults[0] )
                
                # update launch button
                self.bt_options.Enable( True ) # Enable new launch button
                self.bt_options.SetToolTipString( 'Launch' )
                
                # get app-icon for selected application from operating system
                icon_theme = gtk.icon_theme_get_default()
                icon_info = icon_theme.lookup_icon(searchResults[0], 16, 0)
                icon_path =icon_info.get_filename()

                if(icon_path <> ''): # found icon
                    if('.svg' not in icon_path ):
                        # define new image
                        newAppIcon = wx.Image(icon_path, wx.BITMAP_TYPE_PNG)

                        # get image size
                        newAppIconSize=newAppIcon.GetSize()
                        newAppIconWidth=newAppIcon.GetWidth()
                        print('\tFound icon: '+icon_path+' ('+str(newAppIconWidth)+'px)')

                        # icon might be to large or to small - resizing could make sense
                        if targetIconSize == newAppIconWidth:
                            print('\tIcon size is as expected')

                        else:
                            print('\tIcon size does not match, starting re-scaling.')
                            newAppIcon.Rescale(128,128)                             # rescale image
                            
                        self.bt_application.SetBitmap(newAppIcon.ConvertToBitmap())    # set icon to button
                    else:
                        print('\tSVG icons can not be used so far')
                        
                else: # no icon
                        print('\tFound no icon')

                return searchResults[0] # return the 1 result - for launch

            else:           # got several hits
                print('\tFound '+str(len(searchResults))+' matching application')
                #self.m_comboBox1.Enable( True )
                self.m_comboBox1.SetItems(searchResults)
                
                # update launch button icon
                self.img_application = wx.Image('gfx/bt_result_happy_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
        else:
            print('\tEmpty search string')



def create_menu_item(menu, label, func):
    print('\ncreate_menu_item')
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item



class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)



    def CreatePopupMenu(self):
        print('\nCreatePopupMenu')
        menu = wx.Menu()
        # preferences
        create_menu_item(menu, 'Preferences', self.on_hello)
        menu.AppendSeparator()
        # github
        create_menu_item(menu, 'GitHub', self.on_github)
        menu.AppendSeparator()
        # exit
        create_menu_item(menu, 'Exit', self.on_exit)
        
        # test: append items
        fitem = menu.Append(wx.ID_EXIT, 'Qu_it', 'Quit application')
        return menu



    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)



    def on_left_down(self, event):
        print('\non_left_down')
        print '\tTray icon was left-clicked.'
        print '\tShould open or close main UI'
        #WINDOW_REF.Show() 
        #MyFrame.Show(MyFrame, self) 




    def on_hello(self, event):
        print 'Dummy: Open Preference Window'



    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


    
    def on_github(self, event):
        print('Opening github in browser')
        webbrowser.open(appURL)  # Go to github
        #self.openAppURL()



class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True


def main():
    app = App(False)
    
    # Main UI window
    frame = MyFrame(None, appName)
    #frame = wx.Frame(None, wx.ID_ANY, appName) # A Frame is a top-level window.
    #frame.Show(True)     # Show the frame.
    app.MainLoop()



if __name__ == '__main__':
    main()

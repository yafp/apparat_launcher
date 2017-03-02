#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# -----------------------------------------------------------------------------------------------
# NAME:         apparat
# DESCRIPTION:  Python based application launcher
# AUTHOR:       yafp
# URL:          https://github.com/yafp/apparat


# -----------------------------------------------------------------------------------------------
# RESOURCES
# -----------------------------------------------------------------------------------------------
# TrayIcon:                                 http://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
# Icons - Font Awesome - Color: #7f8c8d     http://fontawesome.io/icons/
#                                           http://fa2png.io/
# Ini files                                 https://wiki.python.org/moin/ConfigParserExamples
# Frame Styles                              https://www.blog.pythonlibrary.org/2013/11/06/wxpython-101-using-frame-styles/
# Key Events                                https://wxpython.org/docs/api/wx.KeyEvent-class.html


# -----------------------------------------------------------------------------------------------
# REMINDER/OPEN
# -----------------------------------------------------------------------------------------------
# - global hotkey to bring running app in foreground        https://wxpython.org/docs/api/wx.Window-class.html#RegisterHotKey
#                                                           https://github.com/schurpf/pyhk                                                           
# - ui fade in on launch                                    https://www.blog.pythonlibrary.org/2008/04/14/doing-a-fade-in-with-wxpython/


# -----------------------------------------------------------------------------------------------
# IMPORTING
# -----------------------------------------------------------------------------------------------
import wx                           # for all the WX GUI items
import os, fnmatch                  # for searching applications
import webbrowser                   # for opening urls (example: github project page)
import subprocess                   # for checking if cmd_exists
import difflib                      # for intelligent list sort
import ConfigParser                 # to handle .ini/configuration files
from subprocess import call         # for calling external commands
from sys import platform            # to detect the platform the script is executed on

import gtk                          # for app-icon handling - crashes - reason: wx?
# helps on ubuntu - not on fedora
gtk.remove_log_handlers()           # if this line is removed - app is crashing as long as both WX and GTK are imported.
                                    # reference: https://groups.google.com/forum/#!topic/wxpython-users/KO_hmLxeDKA
gtk.disable_setlocale()


# -----------------------------------------------------------------------------------------------
# CONSTANTS (DEVELOPER)
# -----------------------------------------------------------------------------------------------
TRAY_TOOLTIP = 'apparat'
TRAY_ICON = 'gfx/core/bt_appIcon_16.png'
appName = 'apparat'
appURL = 'https://github.com/yafp/apparat'
targetIconSize = 128


# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
appVersion = '20170302.01'
debug = True                    # True or False
#debug = False                    # True or False

windowWidth=350
windowHeight=310


# -----------------------------------------------------------------------------------------------
# CONFIG (USER)
# -----------------------------------------------------------------------------------------------
transparency=255                # app transparency - Values: 0-255



# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HELPER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cmdExists(cmd):
    printDebugToTerminal('cmdExists')
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


# used to print debug-output if debug = TRUE
def printDebugToTerminal(string):
    if(debug == True):
        print ("debug >> "+string)


# used to detect the platform and exit if the platform is unsupported
def checkPlatform():
    printDebugToTerminal('checkPlatform')
    if platform == "linux" or platform == "linux2": # linux
        printDebugToTerminal('\tDetected linux')
    elif platform == "darwin":                      # OS X
        printDebugToTerminal('\tDetected unsupported platform (darwin)')
        wx.MessageBox('Unsupported platform detected, aborting '+appName+' startup now.', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()
    elif platform == "win32":                       # Windows...
        printDebugToTerminal('\tDetected unsupported platform (windows)')
        wx.MessageBox('Unsupported platform detected, aborting '+appName+' startup now.', 'Error', wx.OK | wx.ICON_ERROR)           # error dialog
        exit()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN-WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MyFrame(wx.Frame):                # We simply derive a new class of Frame. """
    def __init__(self, parent, title):

        # Update Statistics (ini) - Apparat launched
        printDebugToTerminal('\tUpdating statistics (apparat_started)')
        curAppStartCount = self.readSingleINIValue('Statistics','apparat_started')          # get current value from ini
        self.writeSingleINIValue('Statistics','apparat_started',int(curAppStartCount)+1)    # update ini +1
        
        # frame style
        style = ( wx.MINIMIZE_BOX | wx.CLIP_CHILDREN | wx.NO_BORDER | wx.FRAME_SHAPED  )
        
        #wx.Frame.__init__(self, parent, title=title, size=(windowWidth,windowHeight))                          # Default frame
        wx.Frame.__init__(self, parent, title=title, size=(windowWidth,windowHeight), style=style)              # Custom Frame 
        self.SetSizeHintsSz( wx.Size( windowWidth,windowHeight ), wx.Size( windowWidth,windowHeight ) )         # forcing min and max size to same values - prevents resizing option
        self.tbicon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        ## define and set an application icon
        appIcon = wx.Icon('gfx/core/bt_appIcon_16.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(appIcon)


        # ------------------------------------------------
        # Define UI Elements
        # ------------------------------------------------

        # Preference button
        img_preferences = wx.Bitmap('gfx/core/bt_prefs_16.png', wx.BITMAP_TYPE_BMP)
        #self.bt_preferences = wx.BitmapButton(self, id = wx.ID_ANY, bitmap = img_preferences, size = (img_preferences.GetWidth()+10, img_preferences.GetHeight()+10))
        self.bt_preferences = wx.BitmapButton(self, id = wx.ID_ANY, style=wx.NO_BORDER, bitmap = img_preferences, size = (img_preferences.GetWidth()+10, img_preferences.GetHeight()+10))
        self.bt_preferences.SetLabel('Preferences')
        self.bt_preferences.SetToolTipString( u'Open Preferences' )

        #  result counter
        #self.txt_resultCounter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_resultCounter = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_CENTRE )
        self.txt_resultCounter.SetFont( wx.Font( 10, 74, 90, 92, False, 'Sans' ) )
        self.txt_resultCounter.SetToolTipString( u'Result count' )
        self.txt_resultCounter.SetMinSize( wx.Size( 35,30 ) )
        self.txt_resultCounter.SetMaxSize( wx.Size( 35,30 ) )
        self.txt_resultCounter.SetEditable(False)
        self.txt_resultCounter.Enable( False )

        # Search & Search Results as comboBox
        searchResults = []
        self.m_comboBox1 = wx.ComboBox( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size( 265,30 ), searchResults, 0 )

        # launchbutton
        self.img_application = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_application = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 150,150 ), wx.BU_AUTODRAW )
        self.bt_application.SetBitmapFocus( wx.NullBitmap )
        self.bt_application.SetBitmapHover( wx.NullBitmap )
        self.bt_application.SetToolTipString( u'Search' )
        self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
        self.bt_application.SetLabel('Applications')
        self.bt_application.Enable( False )

        # optionbutton
        self.img_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_options = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 150,150 ), wx.BU_AUTODRAW )
        self.bt_options.SetBitmapFocus( wx.NullBitmap )
        self.bt_options.SetBitmapHover( wx.NullBitmap )
        #self.bt_options.SetToolTipString( u'Launch' )
        self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
        self.bt_options.SetLabel('Options')
        self.bt_options.Enable( False )

        # label - command (hidden)
        self.txt_command = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_CENTRE)
        self.txt_command.SetFont( wx.Font( 10, 74, 90, 92, False, 'Sans' ) )
        self.txt_command.SetToolTipString( u'Command' )
        self.txt_command.SetMinSize( wx.Size( 150,30 ) )
        self.txt_command.SetMaxSize( wx.Size( 150,30 ) )
        self.txt_command.SetEditable(False)
        self.txt_command.Enable( False )
        #self.txt_command.Hide()
        
        # label - parameter (hidden)
        self.txt_commandParameter = wx.TextCtrl( self, wx.ID_ANY, style=wx.TE_CENTRE )
        self.txt_commandParameter.SetFont( wx.Font( 10, 74, 90, 92, False, 'Sans' ) )
        self.txt_commandParameter.SetToolTipString( u'Parameter' )
        self.txt_commandParameter.SetMinSize( wx.Size( 150,30 ) )
        self.txt_commandParameter.SetMaxSize( wx.Size( 150,30 ) )
        self.txt_commandParameter.SetEditable(False)
        self.txt_commandParameter.Enable( False )
        #self.txt_commandParameter.Hide()

        # Version Information
        self.txt_versionInformation = wx.StaticText( self, wx.ID_ANY, ' v'+appVersion, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_versionInformation.Wrap( -1 )
        self.txt_versionInformation.SetFont( wx.Font( 8, 74, 90, 90, False, 'Sans' ) )
        self.txt_versionInformation.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )


        # ------------------------------------------------
        # Layout
        # ------------------------------------------------
        bSizer1 = wx.BoxSizer( wx.VERTICAL )                                # define layout container
        bSizer1.Add( self.bt_preferences, 0, wx.ALIGN_RIGHT, 100)           # preferences
        bSizer1.AddSpacer(10)                                               # spacer
        # horizontal sub-item 1
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add( self.txt_resultCounter, 0, wx.CENTRE)                     # result counter
        box1.Add( self.m_comboBox1, 0, wx.CENTRE)                           # combobox
        bSizer1.Add( box1, 0, wx.CENTRE)
        bSizer1.AddSpacer(10)                                               # spacer
        # horizontal sub-item 2
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add( self.bt_application, 0, wx.CENTRE)                        # launch button
        box2.Add( self.bt_options, 0, wx.CENTRE)                            # options button
        bSizer1.Add( box2, 0, wx.CENTRE)
        # horizontal sub-item 3
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add( self.txt_command, 0, wx.CENTRE)                           # launch text
        box3.Add( self.txt_commandParameter, 0, wx.CENTRE)                  # option text
        bSizer1.Add( box3, 0, wx.CENTRE)
        bSizer1.AddSpacer(30)                                               # spacer
        bSizer1.Add( self.txt_versionInformation, 0, wx.CENTRE )            # version
        self.SetSizer( bSizer1 )


        # ------------------------------------------------
        # Bind/Connect Events
        # ------------------------------------------------
        # image buttons - https://www.tutorialspoint.com/wxpython/wxpython_buttons.htm
        self.bt_preferences.Bind(wx.EVT_BUTTON, self.OnClicked) 
        
        # combobox
        self.m_comboBox1.Bind( wx.EVT_KEY_UP, self.onKeyPressInCombobox )               # ComboBox
        self.m_comboBox1.Bind( wx.EVT_TEXT_ENTER, self.onEnterInCombobox)               # ComboBox - doesnt trigger
        self.m_comboBox1.Bind( wx.EVT_COMBOBOX, self.onSelectInCombobox)                # ComboBox - does trigger
        
        # option button
        self.bt_options.Bind(wx.EVT_BUTTON, self.OnClickedOptionButton)


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
        
        self.Center()                   # open window centered
        self.Show(True)                 # show main UI
        self.m_comboBox1.SetFocus()     # set focus to search
        self.SetTransparent(transparency)       # 0-255

    #
    def OnCloseWindow(self, event):
        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()
        wx.GetApp().ExitMainLoop()
        event.Skip()


    '''
        Method to read a single value from the configuration file apparat.ini
    '''
    def readSingleINIValue(self, sectionName, keyName):
        Config = ConfigParser.ConfigParser() 
        Config.read("apparat.ini")                                              # read config file
        #print Config.sections()                                                # get available sections
        value = Config.get(sectionName, keyName)                                # get single value
        return(value)                                                           # return single value


    '''
        Method to write a single value to the configuration file apparat.ini
    '''
    def writeSingleINIValue(self, sectionName, keyName, value):
        Config = ConfigParser.ConfigParser() 
        Config.read("apparat.ini")                                              # read config file
        Config.set(sectionName, keyName, value )                                # write
        with open('apparat.ini', 'wb') as configfile:
            Config.write(configfile)                                            # save
        


    def OnClickedOptionButton(self, event): 
        printDebugToTerminal('Clicked Applications button')
        self.launchExternalApplication()


    def OnClicked(self, event): 
        printDebugToTerminal('OnClicked')
        btn = event.GetEventObject().GetLabel() 
        if (btn =='Preferences'):
            printDebugToTerminal('\tPreferences')
            # Open a preference window
            self.openPreferenceWindow()


    def openPreferenceWindow(self):
        printDebugToTerminal('openPreferenceWindow')
        self.new = NewWindow(parent=None, id=-1)
        self.new.Show()



    def onEnterInCombobox(self, event):
        print('\n\n\nEvent: enter in combobox')


    def onSelectInCombobox(self, event):
        print('\n\n\nEvent Event')

    '''
        If content of the searchfield of the combobox changes
    '''
    def onKeyPressInCombobox(self, event):
        printDebugToTerminal('On Key Press On Comboxbox')
        
        kc = event.GetKeyCode()
        #print kc
        
        ## Checking for key-combinations
        #
        if event.HasModifiers():            # either CTRL or ALT was pressed
            # Modifiers
            # 1 = alt
            # 2 = ctrl
            # 3 = alt + ctrl
            #print event.GetModifiers()
            
            # ctrl+alt+a
            if(event.GetModifiers() == 3) and (kc == 65):
                print('magic combo was pressed')
                # do something

        
        if(kc == 13) : # Enter
            printDebugToTerminal('\tENTER')
            # should check if combobox is open or not
            # not sure if possible with combobox - or if i need to use 'ComboCtrl' - as it has 'IsPopupShown'

            # if we got a search string and 1 result in counter -> launchExternalApplication
            if(len(self.m_comboBox1.GetValue()) > 0) and (self.txt_resultCounter.GetValue() == '1'):
                self.launchExternalApplication()
            else:
                printDebugToTerminal('\tCombobox is empty or resultcount is not 1, nothing to do here.')
            
        elif(kc == 27) : # ESC
            printDebugToTerminal('\tESC in combobox')
            self.resetUI()
            
        elif(kc == 317):    # Arrow Down
            printDebugToTerminal('\tARROW DOWN')
            self.m_comboBox1.Popup()
        else:
            currentSearchString=self.m_comboBox1.GetValue()
            if(len(currentSearchString) == 0):
                self.resetUI()
            else:
                printDebugToTerminal('\tSearching: '+currentSearchString)
                self.searchApplications(currentSearchString)


    def searchApplications(self, currentSearchString):
        printDebugToTerminal('searchApplications')
        if(currentSearchString != ''):
        
            if \
            (currentSearchString.startswith('!a') == True) or \
            (currentSearchString.startswith('!b') == True) or \
            (currentSearchString.startswith('!g') == True) or \
            (currentSearchString.startswith('!r') == True) or \
            (currentSearchString.startswith('!s') == True) or \
            (currentSearchString.startswith('!t') == True) or \
            (currentSearchString.startswith('!v') == True) or \
            (currentSearchString.startswith('!w') == True) or \
            (currentSearchString.startswith('!y') == True):

                # Amazon
                if(currentSearchString.startswith('!a') == True):
                    printDebugToTerminal('\tPlugin Amazon activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_amazon_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Amazon')
                    
                # Bandcamp
                if(currentSearchString.startswith('!b') == True):
                    printDebugToTerminal('\tPlugin Bandcamp activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_bandcamp_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Bandcamp')

                # Google
                if(currentSearchString.startswith('!g') == True):
                    printDebugToTerminal('\tPlugin Google activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_google_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Google')
                    
                # Reddit
                if(currentSearchString.startswith('!r') == True):
                    printDebugToTerminal('\tPlugin Reddit activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_reddit_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Reddit')
                
                # Soundcloud
                if(currentSearchString.startswith('!s') == True):
                    printDebugToTerminal('\tPlugin Soundcloud activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_soundcloud_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Soundcloud')
                
                # Twitter
                if(currentSearchString.startswith('!t') == True):
                    printDebugToTerminal('\tPlugin Twitter activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_twitter_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Twitter')
                
                # Vimeo
                if(currentSearchString.startswith('!v') == True):
                    printDebugToTerminal('\tPlugin Vimeo activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_vimeo_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Vimeo')

                # Wikipedia
                if(currentSearchString.startswith('!w') == True):
                    printDebugToTerminal('\tPlugin Wikipedia activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_wikipedia_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Wikipedia')

                # Youtube
                if(currentSearchString.startswith('!y') == True):
                    printDebugToTerminal('\tPlugin YouTube activated')
                    self.img_application = wx.Image('gfx/plugins/search/bt_youtube_128.png', wx.BITMAP_TYPE_PNG)
                    self.bt_application.SetToolTipString( 'Youtube')


                ## for all search plugin cases
                #
                # update application button
                self.bt_application.Enable( True )
                self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
                
                # update option button
                self.img_options = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_options.Enable( True )
                self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
                self.bt_options.SetToolTipString( 'Search')
                
                # set command
                self.txt_command.SetValue(currentSearchString)
                
                self.txt_resultCounter.SetValue('1') # set resultcount
                return

            # Plugin: Lock
            if(currentSearchString == '!l'):
                printDebugToTerminal('\tPlugin lock activated')
                
                # application buttons
                self.img_application = wx.Image('gfx/plugins/lock/bt_lock_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_application.Enable( True )
                self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
                self.bt_application.SetToolTipString( 'Lock Session')
                
                # option buttons
                self.bt_options.SetToolTipString( 'Launch')
                self.img_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
                self.bt_options.Enable( True )                                  # Enable option button
                
                # set command and parameter
                self.txt_command.SetValue('gnome-screensaver-command')
                self.txt_commandParameter.SetValue('--lock')
                
                self.txt_resultCounter.SetValue('1')        # set resultcount
                return

            ## Default case
            printDebugToTerminal('\tSearching executables for the following string: '+currentSearchString)
            searchResults = fnmatch.filter(os.listdir('/usr/bin'), '*'+currentSearchString+'*')     # search for executables matching users searchstring
            
            ## Sort results
            ## 1: from a to z
            #searchResults.sort() # sort search results (from a to z)
            ## 2: using difflib
            #print sorted(searchResults, key=lambda x: difflib.SequenceMatcher(None, x, currentSearchString).ratio(),reverse=True)
            searchResults=sorted(searchResults, key=lambda x: difflib.SequenceMatcher(None, x, currentSearchString).ratio(),reverse=True)

            self.txt_resultCounter.SetValue(str(len(searchResults)))            # update result count
            self.m_comboBox1.SetItems(searchResults)                            # update combobox

            if(len(searchResults) == 0):
                printDebugToTerminal('Found 0 applications')
                
                # update launch button icon
                self.img_application = wx.Image('gfx/core/bt_result_sad_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
                
                # update option button
                self.img_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
                
                # set command and parameter
                self.txt_command.SetValue('')
                self.txt_commandParameter.SetValue('')
                

            elif(len(searchResults) == 1):     # if we got 1 search-results
                printDebugToTerminal('\tFound 1 matching application')

                # application buttons
                self.bt_application.Enable( True )                              # Enable application button
                self.bt_application.SetToolTipString( searchResults[0] )        # set tooltip
                
                # options buttons
                self.img_options = wx.Image('gfx/core/bt_right_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
                self.bt_options.Enable( True )                                  # Enable option button
                self.bt_options.SetToolTipString( 'Launch' )                    # set tooltip
                
                # update labels
                self.txt_command.SetValue(searchResults[0])
                self.txt_commandParameter.SetValue('')
                
                # Icon search - http://www.pygtk.org/pygtk2reference/class-gtkicontheme.html
                #
                # get app-icon for selected application from operating system
                icon_theme = gtk.icon_theme_get_default()
                # check what icon sizes are available and choose best size
                availableIconSizes = icon_theme.get_icon_sizes(searchResults[0])
                if not availableIconSizes: # if we got no list of available icon sizes - Fallback: try to get a defined size
                    icon_info = icon_theme.lookup_icon(searchResults[0], 64, 0)
                    maxIconSize=64
                else:
                    printDebugToTerminal('\tFound several icon sizes: '+str(availableIconSizes))
                    # pick the biggest
                    maxIconSize=max(availableIconSizes)
                    printDebugToTerminal('\tPicking the following icon size: '+str(maxIconSize))
                    icon_info = icon_theme.lookup_icon(searchResults[0], maxIconSize, 0)
                    
                icon_path =icon_info.get_filename()

                if(icon_path <> ''):                                            # found icon
                    if('.svg' not in icon_path ):
                        
                        newAppIcon = wx.Image(icon_path, wx.BITMAP_TYPE_PNG)    # define new image
                        #newAppIconWidth=newAppIcon.GetWidth()                   # get icon width
                        printDebugToTerminal('\tFound icon: '+icon_path+' ('+str(maxIconSize)+'px)')
                        if targetIconSize == maxIconSize:                   # if icon has expected size
                            printDebugToTerminal('\tIcon size is as expected')
                        else:                                                   # resize icon
                            printDebugToTerminal('\tIcon size does not match, starting re-scaling.')
                            newAppIcon.Rescale(128,128)                             # rescale image
                    else:                                                       # found unsupported icon format
                        printDebugToTerminal('\tSVG icons can not be used so far')
                        newAppIcon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)      # use dummy icon
                else: # no icon
                        printDebugToTerminal('\tFound no icon')
                        newAppIcon = wx.Image('gfx/core/bt_missingAppIcon_128.png', wx.BITMAP_TYPE_PNG)      # use dummy icon
                self.bt_application.SetBitmap(newAppIcon.ConvertToBitmap())    # set icon to button
                return searchResults[0] # return the 1 result - for launch
            else:           # got several hits
                printDebugToTerminal('\tFound '+str(len(searchResults))+' matching application')

                # update launch button icon
                self.img_application = wx.Image('gfx/core/bt_result_happy_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
                self.bt_application.Enable( False )
                self.bt_application.SetToolTipString( u'' )
                
                self.img_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
                self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
                self.bt_options.Enable( False )                                  # Enable option button
                self.bt_options.SetToolTipString( u'' )
                
                # update labels
                self.txt_command.SetValue('')
                self.txt_commandParameter.SetValue('')
                
        else:                                                                                       # search string is empty
            printDebugToTerminal('\tEmpty search string')

    '''
        Launches the actual external process
    '''
    def launchExternalApplication(self):
        printDebugToTerminal('launchExternalApplication')
        currentSelectedAppName = self.txt_command.GetValue()
        currentSelectedAppNameParameter = self.txt_commandParameter.GetValue()

        if \
        (currentSelectedAppName.startswith('!a ') == True) or \
        (currentSelectedAppName.startswith('!b ') == True) or \
        (currentSelectedAppName.startswith('!g ') == True) or \
        (currentSelectedAppName.startswith('!r ') == True) or \
        (currentSelectedAppName.startswith('!s ') == True) or \
        (currentSelectedAppName.startswith('!t ') == True) or \
        (currentSelectedAppName.startswith('!v ') == True) or \
        (currentSelectedAppName.startswith('!w ') == True) or \
        (currentSelectedAppName.startswith('!y ') == True):
            searchPhrase=currentSelectedAppName[3:] # remove '!y ' or '!g ' or '!w '
            
            # Plugin: Amazon
            if(currentSelectedAppName.startswith('!a ') == True):                           # https://www.amazon.de/s/field-keywords=foobar
                remoteURL='https://www.amazon.de/s/field-keywords='+searchPhrase
            
            # Plugin: Bandcamp
            if(currentSelectedAppName.startswith('!b ') == True):                           # https://bandcamp.com/search?q=foobar
                remoteURL='https://bandcamp.com/search?q='+searchPhrase
            
            # Plugin: Google
            if(currentSelectedAppName.startswith('!g ') == True):                           # https://www.google.com/search?q=foobar
                remoteURL='https://www.google.com/search?q='+searchPhrase
                
            # Plugin: Reddit
            if(currentSelectedAppName.startswith('!r ') == True):                           # https://www.reddit.com/search?q=foobar
                remoteURL='https://www.reddit.com/search?q='+searchPhrase

            # Plugin: Soundcloud
            if(currentSelectedAppName.startswith('!s ') == True):                           # https://soundcloud.com/search?q=foobar
                remoteURL='https://soundcloud.com/search?q='+searchPhrase
            
            # Plugin: Twitter
            if(currentSelectedAppName.startswith('!t ') == True):                           # https://twitter.com/search?q=foobar
                remoteURL='https://twitter.com/search?q='+searchPhrase
            
            # Plugin: Vimeo
            if(currentSelectedAppName.startswith('!v ') == True):                           # https://vimeo.com/search?q=foobar
                remoteURL='https://vimeo.com/search?q='+searchPhrase
            
            # Plugin: Wikipedia
            if(currentSelectedAppName.startswith('!w ') == True):                           # https://en.wikipedia.org/w/index.php?search=foobar
                remoteURL='https://en.wikipedia.org/w/index.php?search='+searchPhrase
                
            # Plugin: Youtube
            if(currentSelectedAppName.startswith('!y ') == True):
                remoteURL='https://www.youtube.com/results?search_query='+searchPhrase      # https://www.youtube.com/results?search_query=foobar
            
            # for all  plugins:
            webbrowser.open(remoteURL)  # search youtube
            
            # update usage-statistics
            printDebugToTerminal('\tUpdating statistics (plugin_executed)')
            curPluginExecutedCount = self.readSingleINIValue('Statistics','plugin_executed')          # get current value from ini
            self.writeSingleINIValue('Statistics','plugin_executed',int(curPluginExecutedCount)+1)    # update ini +1
            
            self.resetUI()
            return

        #if currentSelectedAppName != '' or currentSelectedAppName != 'None':
        if(currentSelectedAppName is not None): # Check if the dropdown contains something at all or not
            printDebugToTerminal('\tShould execute: "'+currentSelectedAppName+'" with parameter: "'+currentSelectedAppNameParameter+'"')
            checkExecutable = cmdExists(currentSelectedAppName)                   # check if name exists and is executable
            if (checkExecutable == True):
                
                # update usage-statistics
                printDebugToTerminal('\tUpdating statistics (command_executed)')
                curCommandsExecutedCount = self.readSingleINIValue('Statistics','command_executed')          # get current value from ini
                self.writeSingleINIValue('Statistics','command_executed',int(curCommandsExecutedCount)+1)    # update ini +1
                
                printDebugToTerminal('\tExecutable: "'+currentSelectedAppName+'" exists')
                # https://docs.python.org/2/library/subprocess.html
                if(currentSelectedAppNameParameter == ''):
                    #subprocess.Popen(["rm","-r","some.file"])
                    subprocess.Popen([currentSelectedAppName])
                    printDebugToTerminal('\tExecuted: '+currentSelectedAppName)
                else:
                    subprocess.Popen([currentSelectedAppName,currentSelectedAppNameParameter,""])
                    printDebugToTerminal('\tExecuted: '+currentSelectedAppName+' '+currentSelectedAppNameParameter)

                self.resetUI()
            else:
                printDebugToTerminal ('\tERROR >> Checking the executable failed')
        else:
            printDebugToTerminal('\tWARNING >> currentSelectedAppName is empty, aborting')


    def openAppURL(self):
        printDebugToTerminal('openAppURL')
        printDebugToTerminal('\tOpening '+appURL+' in default browser')
        webbrowser.open(appURL)  # Go to github


    '''
        Reset the User-Interface of the Apps main-window
    '''
    def resetUI(self):
        printDebugToTerminal('resetUI')
        # reset the combobox
        self.m_comboBox1.SetFocus()                                 # set focus to search
        self.m_comboBox1.Clear()                                    # clear all list values
        self.m_comboBox1.SetValue('')                               # clear search field

        # reset the applications button
        self.img_application = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_application.Enable( False )
        self.bt_application.SetBitmap(self.img_application.ConvertToBitmap())
        self.bt_application.SetToolTipString( 'Search')

        # reset the option buttons
        self.img_options = wx.Image('gfx/core/bt_question_128.png', wx.BITMAP_TYPE_PNG)
        self.bt_options.Enable( False )
        self.bt_options.SetBitmap(self.img_options.ConvertToBitmap())
        self.bt_options.SetToolTipString( 'Launch')

        # reset the command and parameter elements
        self.txt_command.SetValue('')
        self.txt_commandParameter.SetValue('')

        # reset the result counter
        self.txt_resultCounter.SetValue('')                               # Reset result counter
        printDebugToTerminal('\tFinished resetting UI')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PREFERENCE WINDOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class NewWindow(wx.Frame):
    def __init__(self,parent,id):
        prefWindowStyle = ( wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR )
        
        wx.Frame.__init__(self, parent, id, 'Preferences', size=(500,300), style=prefWindowStyle)
        wx.Frame.CenterOnScreen(self)
        #self.new.Show(False)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY-MENU
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_menu_item(menu, label, func):
    printDebugToTerminal('create_menu_item: '+label)
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TRAY_ICON
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#class TaskBarIcon(wx.TaskBarIcon):
class TaskBarIcon(wx.TaskBarIcon, MyFrame):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.onTrayMenuLeftClick)


    def CreatePopupMenu(self):
        printDebugToTerminal('CreatePopupMenu')
        menu = wx.Menu()
        create_menu_item(menu, 'Preferences', self.onTrayMenuRightClickPreferences)     # preferences
        create_menu_item(menu, 'GitHub', self.onTrayMenuRightClickGitHub)               # github
        menu.AppendSeparator()                                                          # separator
        create_menu_item(menu, 'Exit', self.onTrayMenuRightClickExit)                   # exit
        return menu


    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)


    def onTrayMenuLeftClick(self, event):
        printDebugToTerminal('onTrayMenuLeftClick')
        # check if main window is minimized
        if self.frame.IsIconized():
            printDebugToTerminal('\tMainWindows was minimized - should show it now')
            self.frame.Raise()
            
        else:
            printDebugToTerminal('\tMainWindows was shown - should minimize it now')
            self.frame.Iconize(True)
            #self.frame.HideWithEffect(wx.SHOW_EFFECT_SLIDE_TO_RIGHT, timeout=3000)


    def onTrayMenuRightClickPreferences(self, event):
        printDebugToTerminal('onTrayMenuRightClickPreferences')
        self.openPreferenceWindow()


    def onTrayMenuRightClickExit(self, event):
        printDebugToTerminal('onTrayMenuRightClickExit')
        wx.CallAfter(self.frame.Close)


    def onTrayMenuRightClickGitHub(self, event):
        printDebugToTerminal('onTrayMenuRightClickGitHub')
        webbrowser.open(appURL)  # Go to github


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(wx.App):
    def OnInit(self):
        
        # allow only 1 instance of apparat
        self.name = appName
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox(
                "An instance of the application is already running", 
                "Error", 
                 wx.OK | wx.ICON_WARNING
            )
            return False
        return True
        
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        #TaskBarIcon(frame)
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    app = App(False)
    checkPlatform()                 # Check if platform is supported at all, otherwise abort
    frame = MyFrame(None, appName)  # Main UI window
    app.MainLoop()


if __name__ == '__main__':
    printDebugToTerminal('__main__')
    main()

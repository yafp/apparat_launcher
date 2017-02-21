#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# NAME:         pylad
# DESCRIPTION:  Python based application launcher
# AUTHOR:       yafp
# URL:          https://github.com/yafp/pylad


# -----------------------------------------------------------------------------------------------
# RESOURCES
# -----------------------------------------------------------------------------------------------
# General App tutorial:                     http://sebsauvage.net/python/gui/#our_project
# Tkinter:                                  https://docs.python.org/2/library/tkinter.html
# Dropdown:                                 https://www.reddit.com/r/learnpython/comments/2wn1w6/how_to_create_a_drop_down_list_using_tkinter/
# Search icon:                              http://fontawesome.io/icon/search/
# dropdown for results                      https://www.tutorialspoint.com/python/tk_menubutton.htm
# image on button                           https://www.daniweb.com/programming/software-development/code/216852/an-image-button-python-and-tk
# colors:                                   "white", "black", "red", "green", "blue", "cyan", "yellow", and "magenta" are default
# Event types:                              http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-types.html


# -----------------------------------------------------------------------------------------------
# REMINDER/OPEN
# -----------------------------------------------------------------------------------------------
# - global hotkey to bring running app in foreground
# - remember last window position           https://wiki.tcl-lang.org/14452
# - no window decoration -> keyword: overrideredirect -> broken
# - ui fade in on launch


# -----------------------------------------------------------------------------------------------
# CHANGES
# -----------------------------------------------------------------------------------------------
# - display application icon on linux
# - optimized icon search and display process (scale & subsample)
# - optimize tab-ability of UI
# - added error dialogs to platform detection
# - removed un-needed import of Gio


# -----------------------------------------------------------------------------------------------
# IMPORTING
# -----------------------------------------------------------------------------------------------
try:
    # Python2
    import Tkinter as tk            # for the UI
    import tkMessageBox             # for the pref dummy dialog
except ImportError:
    # Python3
    import tkinter as tk            # for the UI
    import tkMessageBox             # for the pref dummy dialog

# not yet documented
import os, fnmatch                  # for searching applications
from subprocess import call         # for calling external commands
import subprocess                   # for checking if cmd_exists

from sys import platform            # for checking platform
import webbrowser                   # for opening urls (example: github project page)
import gtk                          # for app-icon handling


# -----------------------------------------------------------------------------------------------
# CONSTANTS (DEVELOPER)
# -----------------------------------------------------------------------------------------------
appName = "pylad"
appURL = "https://github.com/yafp/pylad"


# -----------------------------------------------------------------------------------------------
# CONFIG (DEVELOPER)
# -----------------------------------------------------------------------------------------------
appVersion = "20170221.01"
debug = True                    # True or False
#debug = False                    # True or False
targetIconSize = 32


# -----------------------------------------------------------------------------------------------
# CONFIG (USER)
# -----------------------------------------------------------------------------------------------
appTransparency = 0.95           # 1.0 = not tranparet / 0.9 slighty


# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------

# Check if command exists
# via: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028
def cmd_exists(cmd):
    printDebugToTerminal('Method: cmd_exists')
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


# used to print debug-output if debug = TRUE
def printDebugToTerminal(string):
    if(debug == True):
        print ("debug >> "+string)


class simpleapp_tk(tk.Tk):

    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.checkPlatform()
        self.initialize()


    def checkPlatform(self):
        printDebugToTerminal('Method: checkPlatform - start')
        if platform == "linux" or platform == "linux2":             # linux
            printDebugToTerminal("\tDetected linux")
        elif platform == "darwin":                                  # OS X
            printDebugToTerminal("Unsupported platform, exiting.")
            tkMessageBox.showerror("Error", "Unsupported platform. Bye")
            quit() 
        elif platform == "win32":                                   # Windows
            printDebugToTerminal("Unsupported platform, exiting.")
            tkMessageBox.showerror("Error", "Unsupported platform. Bye")
            quit()
        printDebugToTerminal('Method: checkPlatform - end')


    def initUI(self):
        printDebugToTerminal('Method: initUI - start')
        self.grid()

        # define some images
        self.bt_IconExecute = tk.PhotoImage(file="bt_play.png")        # pick a (small) image file you have in the working directory
        self.bt_IconPreferences = tk.PhotoImage(file="bt_prefs.png")
        self.bt_IconGithub = tk.PhotoImage(file="bt_github.png") 

        # Search field
        printDebugToTerminal('\tConfiguring searchInputEntry')
        self.searchInputEntryVariable = tk.StringVar()
        self.searchInputEntryVariable.set(u"")                                 # set content on start = empty
        self.searchInputEntry = tk.Entry(self,textvariable=self.searchInputEntryVariable, width=6)
        self.searchInputEntry.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), ipady=0, ipadx=0, sticky='EW')  # set padding
        self.searchInputEntry.config(highlightbackground='gray')               # set border color
        
        # key bindings
        self.searchInputEntry.bind('<Return>', self.onSearchPressEnter)
        self.searchInputEntry.bind('<Down>', self.onSearchArrowDown)           # on Arrow Down
        self.searchInputEntry.bind('<KeyRelease>', self.getSearchString)       # on keypress release
        self.searchInputEntry.bind('<Escape>', self.onSearchPressESC)          # on ESC
        # input
        self.searchInputEntry.config(foreground="gray")         # font color
        self.searchInputEntry.config(background="lightgray")    # background
        # font
        self.searchInputEntry.config(font="Helvetica 32 bold")
        self.searchInputEntry.config(justify="center")
        # cursor
        self.searchInputEntry.config(insertbackground='gray')                   # cursor color
        self.searchInputEntry.config(insertofftime=512)                        # = 0 dont blink - integer value indicating the number of milliseconds the insertion cursor should remain ``off'' in each blink cycle
        self.searchInputEntry.config(insertontime=1024)                            # indicating the number of milliseconds the insertion cursor should remain ``on'' in each blink cycle. 
        self.searchInputEntry.config(insertwidth=4)                             # total width of the insertion cursor.
        # border
        self.searchInputEntry.config(highlightthickness=2)                      # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus. 
        self.searchInputEntry.config(highlightbackground="gray")                # Background color of the highlight region when the widget has focus.

        # Launch button
        printDebugToTerminal('\tConfiguring launchButton')
        self.launchButton = tk.Button(self,text=u"", image=self.bt_IconExecute, highlightthickness=0, compound="left", height=56, width=56, relief='raised', command=self.OnLaunchButtonClick)
        self.launchButton.configure(foreground='black')
        self.launchButton.bind('<Return>', self.OnLaunchButtonClick)
        self.launchButton['state'] = 'disabled'
        self.launchButton.grid(row=0, column=2, padx=(0,10), pady=(10,0))
        self.launchButton.image = self.bt_IconExecute # save the button's image from garbage collection

        # Dropdown (featuring results from search)
        printDebugToTerminal('\tConfiguring optionMenu/Dropdown')
        optionList = (' ')                                      #optionList = ('Result', 'Option 2', 'Option 3')
        self.v = tk.StringVar()
        self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
        self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
        self.om.bind('<Return>', self.onMenuPressEnter)
        self.om.bind('<Leave>', self.onMenuLeave)
        # testing
        self.om.bind('<Escape>', self.onMenuPressESC)               # on ESC - does not work - while it still closes the Menu
        self.om.bind("<FocusIn>", self.focusIn) # testing
        self.om.bind('<FocusOut>', self.focusOut) # testing
        
        self.om['state'] = 'disabled' # disable the dropdown at start
        self.om.config(bd=0)    # disable the border
        self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus. 

        # SearchResult-Count label
        printDebugToTerminal('\tConfiguring searchResultCount')
        self.searchResultCountVariable = tk.StringVar()
        #self.searchResultCountVariable.set('') # overwrite - to get rid of old content
        self.searchResultCountVariable.set('0') # set empty text
        self.searchResultCount = tk.Label(self,textvariable=self.searchResultCountVariable, anchor="center",fg="gray", takefocus=0)
        self.searchResultCount.grid(row=1, column=2, padx=5, pady=0)
        
        # Preference button
        printDebugToTerminal('\tConfiguring prefButton')
        self.prefButton = tk.Button(self,text=u"Prefs", image=self.bt_IconPreferences, highlightthickness=0, bd=0, command=self.OnPrefButtonClick, takefocus=0)
        self.prefButton.configure(foreground='black')
        self.prefButton['state'] = 'normal'
        self.prefButton.grid(row=2, column=2, padx=5, pady=0)
        self.prefButton.image = self.bt_IconPreferences # save the button's image from garbage collection

        # Version label
        printDebugToTerminal('\tConfiguring versionLabel')
        self.versionLabelVariable = tk.StringVar()
        self.versionLabel = tk.Label(self,textvariable=self.versionLabelVariable, anchor="center",fg="gray", takefocus=0)
        self.versionLabel.grid(row=3, column=0, columnspan=1, padx=5, pady=(0,5), sticky='EW')
        self.versionLabelVariable.set('Version '+appVersion)

        # Github button
        printDebugToTerminal('\tConfiguring githubButton')
        self.githubButton = tk.Button(self,text=u"Prefs", image=self.bt_IconGithub, highlightthickness=0, bd=0, command=self.OnGithubButtonClick, takefocus=0)
        self.githubButton.configure(foreground='black')
        self.githubButton['state'] = 'normal'
        self.githubButton.grid(row=3, column=2, padx=5, pady=(5,5))
        self.githubButton.image = self.bt_IconGithub     # save the button's image from garbage collection

        # misc
        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False) # make it un-resizeable
        #self.overrideredirect(True) # Buggy - Disable windows-decoration - as a result the window is not longer dragable
        self.update()
        
        self.searchInputEntry.focus_set()       # set cursor focus to search field

        printDebugToTerminal('Method: initUI - end')


    def setApplicationIcon(self):
        printDebugToTerminal('Method: setApplicationIcon - start')
        # set app icon
        img = tk.Image("photo", file="bt_play.png")
        self.tk.call('wm','iconphoto',self._w,img)
        printDebugToTerminal('Method: setApplicationIcon - end')


    def focusIn(self, event):
        print("-------------------------------")
        print("Focus In")
        print("-------------------------------")
        
        
    def focusOut(self, event):
        print("-------------------------------")
        print("Focus Out")
        print("-------------------------------")
        
        
    def onMenuLeave(self, event):
        printDebugToTerminal('Method: onMenuLeave - start')
        printDebugToTerminal('\tSetting focus back to search')
        self.searchInputEntry.focus_set()       # set cursor focus to search field
        printDebugToTerminal('Method: onMenuLeave - end')


    def centerUI(self):     # Window Size and Position
        printDebugToTerminal('Method: centerUI - start')
        printDebugToTerminal('\tConfiguring window size and position')
        #
        # v1:
        #self.geometry(self.geometry())
        #
        # v2:
        # Define window dimensions
        windowWidth = 600 # width for the Tk root
        windowHeight = 150 # height for the Tk root

        # get screen width and height
        screenWidth = self.winfo_screenwidth() # width of the screen
        screenheight = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (screenWidth/4) - (windowWidth/2) # ws/2 = default -> /4 because of dualscreen
        y = (screenheight/2) - (windowHeight/2)

        # set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        
        self.attributes("-alpha", appTransparency) # Transparent UI (1.0 = not transparent)
        
        #self.searchInputEntry.selection_range(0, tk.END)
        printDebugToTerminal('Method: centerUI - end')


    def initialize(self):
        printDebugToTerminal('Method: initialize - start')
        self.initUI()
        self.setApplicationIcon()
        self.centerUI()
        printDebugToTerminal('Method: initialize - end')


    def OptionMenu_SelectionEvent(self, event): # I'm not sure on the arguments here, it works though
        printDebugToTerminal('Method: OptionMenu_SelectionEvent - start')
        printDebugToTerminal('\tSearch-field: got focus')
        self.searchInputEntry.focus_set() # set focus to search field
        printDebugToTerminal('\tLaunch-button: enabled')
        self.launchButton['state'] = 'normal'                 # enabling Launch Button
        printDebugToTerminal('Method: OptionMenu_SelectionEvent - end')


    # search matching application for the current searchstring
    def searchingApplication(self, string):
        printDebugToTerminal('Method: searchingApplication - start')
        string = string.lower() # lowercase search-string
        lengthOfSearchString =  len(string) # detect length of search string
        
        if lengthOfSearchString < 1:
            printDebugToTerminal('\tSearch string is empty')
            self.initUI()
        else:
            printDebugToTerminal('\tSearching:\t"'+string+'" ('+str(lengthOfSearchString)+')') # Print search string and length of it
            searchResults = fnmatch.filter(os.listdir('/usr/bin'), '*'+string+'*')     # search for executables matching users searchstring
            searchResults.sort() # sort search results (from a to z)

            self.searchResultCountVariable.set(len(searchResults)) # show number of search results

            if(len(searchResults) == 0):
                # search field
                self.searchInputEntry.config(background="white")           # set background color
                self.searchInputEntry.config(foreground="gray")            # set font color
                self.searchInputEntry.config(highlightbackground="red")    # set border color

                # launch button
                printDebugToTerminal('\tLaunch-Button: disabled')
                self.launchButton['state'] = 'disabled'               # disabling Launch Button

                # dropdown
                optionList = (' ')
                self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
                self.om.grid(row=1, column=0, columnspan=2, padx=100, pady=0, sticky='EW')
                self.v.set(optionList[0])                                   # select 1 menu-item
                self.om['state'] = 'disabled'
                
                self.searchResultCount.config(fg='red') # colorize search results count label

            elif(len(searchResults) == 1):     # if we got 1 search-results
                #printDebugToTerminal('\tGot 1 search result')
                printDebugToTerminal('\tAutocompleting search field to: '+searchResults[0])

                # search field
                self.searchInputEntry.config(background="white")           # set background color
                self.searchInputEntry.config(highlightbackground="green")  # set border color
                self.searchInputEntry.focus_set()
                #self.searchInputEntryVariable.set(searchResults[0])           # bad idea - if someone wants to delete the content or parts
                self.searchInputEntry.icursor(tk.END)                      # set cursor to end


                # launch button
                #
                self.launchButton.image.blank() # reset current image
                #
                # get app-icon for selected application from operating system
                icon_theme = gtk.icon_theme_get_default()
                icon_info = icon_theme.lookup_icon(searchResults[0], 16, 0)
                print(icon_info)
                icon_path =icon_info.get_filename()
                if(icon_path <> ""): # found icon
                    self.curAppIcon = tk.PhotoImage(file=icon_path)
                    curIconSize=self.curAppIcon.width() # detect icon size
                    printDebugToTerminal('\tFound '+str(curIconSize)+'px icon at: '+icon_path)
                    # icon might be to large or to small - resizing could make sense
                    if targetIconSize == curIconSize:
                        printDebugToTerminal("\tIcon size matches - no resizing needed")
                        self.launchButton.configure(image= self.curAppIcon) # set button-icon
                    else:
                        printDebugToTerminal("\tIcon size does not match, resizing needed.")
                        if(curIconSize > targetIconSize): # icon is to big - shrink it
                            printDebugToTerminal("\tAdjusting icon using subsample")
                            self.curAppIcon = self.curAppIcon.subsample(curIconSize/targetIconSize) 
                            self.launchButton.configure(image= self.curAppIcon) # set button-icon
                        else: # icon is too small -> zoom it
                            printDebugToTerminal("\tAdjusting icon using zoom")
                            scale_w = targetIconSize/curIconSize
                            scale_h = targetIconSize/curIconSize
                            self.curAppIcon = self.curAppIcon.zoom(scale_w, scale_h)
                            self.launchButton.configure(image= self.curAppIcon) # set button-icon
                else: # no icon
                    printDebugToTerminal("\tNo icon found")

                printDebugToTerminal('\tLaunch-Button: enabled')
                self.launchButton['state'] = 'normal'                 # enabling Launch Button

                # dropdown
                self.om['state'] = 'disabled'
                # Update Dropdown
                optionList = searchResults
                self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
                self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
                self.v.set(optionList[0]) # select first search-result

                # change color of searchResultCount
                self.searchResultCount.config(fg='green')    # Change color of search result count label

            else:           # got several hits
                # search field
                self.searchInputEntry.config(background="white")           # set background color
                self.searchInputEntry.config(foreground="gray")            # set font color
                self.searchInputEntry.config(highlightbackground="red")    # set border color

                # dropdown
                self.om['state'] = 'normal'
                optionList = searchResults
                self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
                self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')

                # change color of searchResultCount
                self.searchResultCount.config(fg='red') # adjust colors
                
                # CONSTRUCTION SITE
                #self.openSearchResultList() # open search result list
                #self.searchInputEntry.focus_set()

            # OptionMenu should be non eye-catchy
            self.om.config(bd=0) # disable the border
            self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus.

            # Update Dropdown
            #optionList = searchResults
            #self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
            #self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
            #self.v.set(optionList[0]) # select first search-result

            printDebugToTerminal('\tSearch-Results:\t'+str(len(searchResults)))
        printDebugToTerminal('Method: searchingApplication - end')


    # On Pressing Launch button
    def OnLaunchButtonClick(self):
        printDebugToTerminal('Method: OnLaunchButtonClick - start')
        self.launchExternalApp()                                          # reset the UI
        printDebugToTerminal('Method: OnLaunchButtonClick - end')


    # On Pressing Preferences button
    def OnPrefButtonClick(self):
        printDebugToTerminal('Method: OnPrefButtonClick - start')
        printDebugToTerminal('\tOpening the preference dialog')
        self.messageBox = tkMessageBox.showinfo("pylad Preferences", "not yet implemented")
        printDebugToTerminal('Method: OnPrefButtonClick - end')


    # On Pressing GitHub button
    def OnGithubButtonClick(self):
        printDebugToTerminal('Method: OnGithubButtonClick - start')
        printDebugToTerminal('\tOpening project URL ('+appURL+') in default browser')
        webbrowser.open(appURL)  # Go to github
        printDebugToTerminal('Method: OnGithubButtonClick - end')


    # launching external application
    def launchExternalApp(self):
        printDebugToTerminal('Method: launchExternalApp - start')
        selectedApplicationName = self.v.get()          # get value of OptionMenu
        if selectedApplicationName != "":
            checkExecutable = cmd_exists(selectedApplicationName)                   # check if name exists and is executable
            if (checkExecutable == True):
                call([selectedApplicationName, ""])                                 # launch external command
                self.initUI()
            else:
                print ('\tERROR >> Checking the executable failed....')
        else:
            printDebugToTerminal('\tNo application selected')
        printDebugToTerminal('Method: launchExternalApp - end')


    # On Pressing ENTER
    def onMenuPressEnter(self,event):
        printDebugToTerminal('Method: onMenuPressEnter - start')
        self.launchExternalApp()
        printDebugToTerminal('Method: onMenuPressEnter - end')


    # On Search Pressing ENTER
    def onSearchPressEnter(self,event):
        printDebugToTerminal('Method: onSearchPressEnter - start')
        self.launchExternalApp()
        printDebugToTerminal('Method: onSearchPressEnter - end')


    # On ESC in Search
    def onSearchPressESC(self, event):
        printDebugToTerminal('Method: onSearchPressESC - start')
        self.initUI()
        printDebugToTerminal('Method: onSearchPressESC - end')


    # On Menu/Dropdown press ESC (is not triggered)
    def onMenuPressESC(self, event):
        printDebugToTerminal('Method: onMenuPressESC - start')
        printDebugToTerminal('Method: onMenuPressESC - end')


    # update current search string and trigger app search
    def getSearchString(self, event):
        printDebugToTerminal('Method: getSearchString - start')
        if event.char != '': # if not ARROW DOWN then
            curString = self.searchInputEntryVariable.get()                         # get current search string
            if(len(curString) > 0):                                                 # if current string exists
                print(len(curString))
                self.searchingApplication(curString)                                # start search for this string
            else:                                                                   # if search string is empty
                self.initUI()                                                       # reset UI
        printDebugToTerminal('Method: getSearchString - end')
        

    def openSearchResultList(self):
        printDebugToTerminal('Method: openSearchResultList - start')
        curSearchResults = self.searchResultCountVariable.get()     # check if we got searchResults at all - otherwise do nothing
        if(curSearchResults)==str(0):    # we got no search results - so opening the OptionMenu makes no sense at all
            printDebugToTerminal('\tArray-Down without search results is stupid. Lets stop here')
            printDebugToTerminal('\tSetting focus back to search')
            self.searchInputEntry.focus_set()             # Set focus to search
        else:
            printDebugToTerminal('\tSetting focus to dropdown')
            self.om.focus_set()             # Set focus to OpionMenu / Dropdown
            printDebugToTerminal('\tSimulate space key')
            self.om.event_generate('<space>')  # Open the OptionMenu by simulating a keypress
            #
            #self.searchInputEntry.focus_set()             # Set focus back to search field
        printDebugToTerminal('Method: openSearchResultList - end')


    # Arrow Down in Search field should list
    def onSearchArrowDown(self, event):
        printDebugToTerminal('Method: onSearchArrowDown - start')
        self.openSearchResultList()
        printDebugToTerminal('Method: onSearchArrowDown - end')


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title(appName)
    app.mainloop()

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



# -----------------------------------------------------------------------------------------------
# REMINDER/OPEN
# -----------------------------------------------------------------------------------------------
# - global hotkey to bring running app in foreground
# - remember last window position           https://wiki.tcl-lang.org/14452
# - no window decoration -> keyword: overrideredirect
# - show related icon of selected application if possible (in dropdown / optionmenu)


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

import os, fnmatch                  # for searching applications
from subprocess import call         # for calling external commands
import subprocess                   # for checking if cmd_exists
from sys import platform            # for checking platform

import webbrowser                   # for opening urls (example: github project page)



# -----------------------------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------------------------
appName = "pylad"
appVersion = "20170218.01"
appURL = "https://github.com/yafp/pylad"

debug = True                    # True or False
#debug = False                    # True or False



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
        printDebugToTerminal('Method: checkPlatform')
        if platform == "linux" or platform == "linux2":             # linux
            printDebugToTerminal("\tDetected linux")
        elif platform == "darwin":                                  # OS X
            printDebugToTerminal("Unsupported platform, exiting.")
            quit() 
        elif platform == "win32":                                   # Windows
            printDebugToTerminal("Unsupported platform, exiting.")
            quit() 


    def initialize(self):
        printDebugToTerminal('Method: initialize')
        self.grid()

        # define some images
        bt_IconExecute = tk.PhotoImage(file="bt_play.png")        # pick a (small) image file you have in the working directory
        bt_IconPreferences = tk.PhotoImage(file="bt_prefs.png")
        bt_IconGithub = tk.PhotoImage(file="bt_github.png") 

        # Search field
        self.searchInputEntryVariable = tk.StringVar()
        self.searchInputEntry = tk.Entry(self,textvariable=self.searchInputEntryVariable)
        #self.searchInputEntry.config(background='white')                      # set background color
        #self.searchInputEntry.config(foreground='gray')                       # set font color
        self.searchInputEntry.config(highlightbackground='gray')               # set border color
        self.searchInputEntry.bind('<Return>', self.OnSearchPressEnter)
        self.searchInputEntry.bind('<Down>', self.OnSearchArrowDown)           # on Arrow Down
        self.searchInputEntry.bind('<KeyRelease>', self.getSearchString)       # on keypress release
        self.searchInputEntry.bind('<Escape>', self.OnSearchPressESC)          # on ESC
        self.searchInputEntry.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), ipady=0, ipadx=0, sticky='EW')  # set padding
        self.searchInputEntryVariable.set(u"")                                 # set content on start = empty

        # Launch button
        self.launchButton = tk.Button(self,text=u"Launch", image=bt_IconExecute, highlightthickness=0, compound="left", command=self.OnLaunchButtonClick)
        self.launchButton.configure(foreground='black')
        self.launchButton.bind('<Return>', self.OnLaunchButtonClick)
        self.launchButton['state'] = 'disabled'
        self.launchButton.grid(row=0, column=2, padx=(0,10), pady=(10,0))
        self.launchButton.image = bt_IconExecute # save the button's image from garbage collection

        # Dropdown (featuring results from search)
        optionList = (' ')                                      #optionList = ('Result', 'Option 2', 'Option 3')
        self.v = tk.StringVar()
        #self.v.set(optionList[0])                              # select 1 item of list
        #self.om = tk.OptionMenu(self, self.v, *optionList)
        self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
        self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
        self.om.bind('<Escape>', self.OnMenuPressESC)               # on ESC - does not work - while it still closes the Menu
        self.om.bind("<Return>", self.OnMenuPressEnter)
        self.om['state'] = 'disabled' # disable the dropdown at start
        self.om.config(bd=0)    # disable the border
        self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus. 

        # SearchResult-Count label
        self.searchResultCountVariable = tk.StringVar()
        self.searchResultCount = tk.Label(self,textvariable=self.searchResultCountVariable, anchor="center",fg="gray")
        self.searchResultCount.grid(row=1, column=2, padx=5, pady=0)
        self.searchResultCountVariable.set(u"") # set empty text

        # Preference button
        self.prefButton = tk.Button(self,text=u"Prefs", image=bt_IconPreferences, highlightthickness=0, bd=0, command=self.OnPrefButtonClick)
        self.prefButton.configure(foreground='black')
        self.prefButton['state'] = 'normal'
        self.prefButton.grid(row=2, column=2, padx=5, pady=0)
        self.prefButton.image = bt_IconPreferences # save the button's image from garbage collection

        # Version label
        self.versionLabelVariable = tk.StringVar()
        self.versionLabel = tk.Label(self,textvariable=self.versionLabelVariable, anchor="center",fg="gray")
        self.versionLabel.grid(row=3, column=0, columnspan=1, padx=5, pady=(0,5), sticky='EW')
        self.versionLabelVariable.set("Version "+appVersion)

        # Github button
        self.githubButton = tk.Button(self,text=u"Prefs", image=bt_IconGithub, highlightthickness=0, bd=0, command=self.OnGithubButtonClick)
        self.githubButton.configure(foreground='black')
        self.githubButton['state'] = 'normal'
        self.githubButton.grid(row=3, column=2, padx=5, pady=(5,5))
        self.githubButton.image = bt_IconGithub     # save the button's image from garbage collection

        # misc
        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False) # make it un-resizeable
        #self.overrideredirect(True) # Buggy - Disable windows-decoration - as a result the window is not longer dragable
        self.update()
        # Min size: http://stackoverflow.com/questions/10448882/how-do-i-set-a-minimum-window-size-in-tkinter
        self.minsize(self.winfo_width()+200, self.winfo_height())
        
        # Window Size and Position
        #
        # v1:
        #self.geometry(self.geometry())
        #
        # v2:
        #
        # Define window dimensions
        windowWidth = 500 # width for the Tk root
        windowHeight = 100 # height for the Tk root
        #
        # get screen width and height
        screenWidth = self.winfo_screenwidth() # width of the screen
        screenheight = self.winfo_screenheight() # height of the screen
        #
        # calculate x and y coordinates for the Tk root window
        x = (screenWidth/4) - (windowWidth/2) # ws/2 = default -> /4 because of dualscreen
        y = (screenheight/2) - (windowHeight/2)
        #
        # set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        
        
        self.attributes("-alpha", 0.9) # Transparent UI (1.0 = not transparent)
        
        self.searchInputEntry.focus_set()       # set cursor focus to search field
        #self.searchInputEntry.selection_range(0, tk.END)


    def OptionMenu_SelectionEvent(self, event): # I'm not sure on the arguments here, it works though
        printDebugToTerminal('Method: OptionMenu_SelectionEvent')
        printDebugToTerminal('\tSearch-field: got focus')
        self.searchInputEntry.focus_set() # set focus to search field
        printDebugToTerminal('\tLaunch-button: enabled')
        self.launchButton['state'] = 'normal'                 # enabling Launch Button


    # search matching application for the current searchstring
    def searchingApplication(self, string):
        printDebugToTerminal('Method: searchingApplication')
        string = string.lower() # lowercase search-string
        lengthOfSearchString =  len(string) # detect length of search string
        
        if lengthOfSearchString < 1:
            printDebugToTerminal('\tSearch string is empty')
            self.resetUI()
        else:
            printDebugToTerminal('\tSearching:\t"'+string+'" ('+str(lengthOfSearchString)+')') # Print search string and length of it
            searchResults = fnmatch.filter(os.listdir('/usr/bin'), '*'+string+'*')     # search for executables featuring *string*
            searchResults.sort() # sort search results (from a to z)

            self.searchResultCountVariable.set(len(searchResults)) # show number of search results

            if(len(searchResults) == 0):
                #printDebugToTerminal('\tGot 0 results')
                
                # search field
                self.searchInputEntry.config(background="white")           # set background color
                self.searchInputEntry.config(foreground="gray")            # set font color
                self.searchInputEntry.config(highlightbackground="red")    # set border color

                # launch button
                printDebugToTerminal('\tLaunch-Button: disabled')
                self.launchButton['state'] = 'disabled'               # disabling Launch Button

                # dropdown
                optionList = (' ')
                #self.om = tk.OptionMenu(self, self.v, *optionList)
                self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
                self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
                self.v.set(optionList[0])                                   # select 1 menu-item
                self.om['state'] = 'disabled'
                self.om.config(bd=0) # disable the border
                self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus.
                


                # search results count label
                self.searchResultCount.config(fg='red')

            elif(len(searchResults) == 1):     # if we got 1 search-results
                #printDebugToTerminal('\tGot 1 result')
                printDebugToTerminal('\tAutocompleting search field')
                printDebugToTerminal(searchResults[0])

                # search field
                self.searchInputEntry.config(background="white")           # set background color
                self.searchInputEntry.config(foreground="green")           # set font color
                self.searchInputEntry.config(highlightbackground="green")  # set border color
                self.searchInputEntry.focus_set()
                #self.searchInputEntry.selection_range(0, tk.END)      # select entire field content
                #self.searchInputEntryVariable.set(searchResults[0])           # bad idea - if someone wants to delete the content or parts
                self.searchInputEntry.icursor(tk.END)                      # set cursor to end

                # launch button
                printDebugToTerminal('\tLaunch-Button: enabled')
                self.launchButton['state'] = 'normal'                 # enabling Launch Button

                # dropdown
                self.om['state'] = 'disabled'
                # Update Dropdown
                optionList = searchResults
                self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
                self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
                self.v.set(optionList[0]) # select first search-result
                self.om.config(bd=0) # disable the border
                self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus.

                # search result count label
                self.searchResultCount.config(fg='green')    # Change color of search result count label

            else:           # got several hits
                #printDebugToTerminal('\tGot >1 results')
                # search field
                self.searchInputEntry.config(background="white")           # set background color
                self.searchInputEntry.config(foreground="gray")            # set font color
                self.searchInputEntry.config(highlightbackground="red")    # set border color

                # dropdown
                self.om['state'] = 'normal'
                # Update Dropdown
                optionList = searchResults
                self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
                self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
                #self.v.set(optionList[0]) # select first search-result
                self.om.config(bd=0) # disable the border
                self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus.

                # search result count
                self.searchResultCount.config(fg='red') # adjust colors
                
                # CONSTRUCTION SITE
                #
                #self.openSearchResultList() # open search result list
                
                self.searchInputEntry.focus_set()
                
                

            # Update Dropdown
            #optionList = searchResults
            #self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
            #self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
            #self.v.set(optionList[0]) # select first search-result

            printDebugToTerminal('\tResults:\t'+str(len(searchResults)))


    # On Pressing Launch button
    def OnLaunchButtonClick(self):
        printDebugToTerminal('Method: OnLaunchButtonClick')
        self.launchExternalApp()                                          # reset the UI


    # On Pressing Preferences button
    def OnPrefButtonClick(self):
        printDebugToTerminal('Method: OnPrefButtonClick')
        printDebugToTerminal('\tOpening the preference dialog')
        self.messageBox = tkMessageBox.showinfo("pylad Preferences", "not yet implemented")


    # On Pressing GitHub button
    def OnGithubButtonClick(self):
        printDebugToTerminal('Method: OnGithubButtonClick')
        printDebugToTerminal('\tOpening project URL ('+appURL+') in default browser')
        webbrowser.open(appURL)  # Go to github


    # launching external application
    def launchExternalApp(self):
        printDebugToTerminal('Method: launchExternalApp')
        selectedApplicationName = self.v.get()          # get value of OptionMenu
        if selectedApplicationName != "":
            checkExecutable = cmd_exists(selectedApplicationName)                  # check if name exists and is executable
            if (checkExecutable == True):
                #call([self.searchInputEntryVariable.get(), ""])                    # launch external command
                call([selectedApplicationName, ""])                    # launch external command
                self.resetUI()                                          # reset the UI
            else:
                print ('\tERROR >> Checking the executable failed....')
        else:
            printDebugToTerminal('\tNo application selected')


    # On Pressing ENTER
    def OnMenuPressEnter(self,event):
        printDebugToTerminal('Method: OnMenuPressEnter')
        self.launchExternalApp()


    # On Search Pressing ENTER
    def OnSearchPressEnter(self,event):
        printDebugToTerminal('Method: OnSearchPressEnter')
        self.launchExternalApp()


    # On ESC in Search
    def OnSearchPressESC(self, event):
        printDebugToTerminal('Method: OnSearchPressESC')
        self.resetUI()


    # On Menu/Dropdown press ESC (is not triggered)
    def OnMenuPressESC(self, event):
        printDebugToTerminal('Method: OnMenuPressESC')


    # update current search string and trigger app search
    def getSearchString(self, event):
        printDebugToTerminal('Method: getSearchString')
        if event.char != '': # if not ARRAY DOWN then
            curString = self.searchInputEntryVariable.get()                        # get current search string
            self.searchingApplication(curString)                        # start search for this string


    def openSearchResultList(self):
        printDebugToTerminal('Method: openSearchResultList')
        # check if we got searchResults at all - otherwise do nothing
        curSearchResults = self.searchResultCountVariable.get()
        if(len(curSearchResults))==0:    # we got no search results - so opening the OptionMenu makes no sense at all
            printDebugToTerminal('\tArray-Down without search results is stupid. Lets stop here')
        else:
            printDebugToTerminal('\tSetting focus to dropdown')
            self.om.focus_set()             # Set focus to OpionMenu / Dropdown
            printDebugToTerminal('\tSimulate space key')
            self.event_generate('<space>')  # Open the OptionMenu by simulating a keypress
            return;


    # Arrow Down in Search field should list
    def OnSearchArrowDown(self, event):
        printDebugToTerminal('Method: OnSearchArrowDown')
        self.openSearchResultList()


    # reset the UI back to default
    def resetUI(self):
        printDebugToTerminal('Method: resetUI')

        # search field
        self.searchInputEntry.config(background="white")                       # set background color
        self.searchInputEntry.config(foreground="gray")                        # set foreground color
        self.searchInputEntry.config(highlightbackground="gray")               # set border color
        self.searchInputEntryVariable.set(u"")                                 # Empty search
        self.searchInputEntry.focus_set()                                      # set focus to search field
        #self.searchInputEntry.selection_range(0, tk.END)

        # dropdown
        optionList = (' ')
        self.om = tk.OptionMenu(self, self.v, *optionList, command = self.OptionMenu_SelectionEvent)
        self.om.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='EW')
        self.v.set(optionList[0])                                   # select 1 menu-item
        self.om['state'] = 'disabled'
        self.om.config(bd=0)                                        # disable border
        self.om.config(highlightthickness=0)    # Specifies a non-negative value indicating the width of the highlight rectangle to draw around the outside of the widget when it has the input focus.

        # launch button
        self.launchButton['state'] = 'disabled'                           # disable launch-button

        # search results count label
        self.searchResultCountVariable.set("")                                  # empty search-results-count label
        self.searchResultCount.config(fg='gray')                 # reset search-results-count-label colors


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title(appName)
    app.mainloop()

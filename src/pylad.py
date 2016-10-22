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




# -----------------------------------------------------------------------------------------------
# TODO
# -----------------------------------------------------------------------------------------------
# - global hotkey
# - remember last window position           https://wiki.tcl-lang.org/14452
# - image on button                         https://www.daniweb.com/programming/software-development/code/216852/an-image-button-python-and-tk


# -----------------------------------------------------------------------------------------------
# IMPORTING
# -----------------------------------------------------------------------------------------------
try:
    # Python2
    import Tkinter as tk            # for the UI
except ImportError:
    # Python3
    import tkinter as tk            # for the UI

import os, fnmatch                  # for searching applications
from subprocess import call         # for calling external commands
import subprocess                   # for checking if cmd_exists

import webbrowser                   # for opening urls (github project page)

# dropdown
#from Tkinter import *
#import Tkinter as ttk
#from ttk import *


# -----------------------------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------------------------
appName = "pylad"
appVersion = "20161022.02"
appURL = "https://github.com/yafp/pylad"

debug = True                    # True or False
#debug = False                    # True or False



# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------

# Check if command exists
#
# via: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028
def cmd_exists(cmd):
    printDebugToTerminal('Executing method cmd_exists')
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


# used to enable or disable debug output to terminal
def printDebugToTerminal(str):
    if(debug == True):
        print ("debug >> "+str)


class simpleapp_tk(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        # Search field
        #
        self.entryVariable = tk.StringVar()
        self.entry = tk.Entry(self,textvariable=self.entryVariable)
        self.entry.config(background='white')                       # set background color
        self.entry.config(foreground='gray')                       # set font color
        self.entry.config(highlightbackground='gray')               # set border color
        self.entry.bind('<Return>', self.OnPressEnter)
        #self.entry.bind("<Return>", self.launchExternalApp)
        self.entry.bind('<Down>', self.OnArrowDown)                 # on Arrow Down
        #self.entry.bind('<Key>', self.OnPressKey)                   # on keypress
        self.entry.bind('<KeyRelease>', self.getSearchString)       # on keypress release
        self.entry.bind('<Escape>', self.OnPressESC)                # on ESC
        self.entry.grid(row=0, column=0, columnspan=2, padx=5, pady=0, sticky='EW')  # set padding
        self.entryVariable.set(u"")                                 # set content on start = empty

        # Launch button
        self.button = tk.Button(self,text=u"Launch", command=self.OnButtonClick)
        self.button.configure(foreground='black')
        self.button.bind('<Return>', self.OnButtonClick)
        self.button['state'] = 'disabled'
        self.button.grid(row=0, column=2, padx=5, pady=0)

        # Dropdown (featuring results from search)
        #
        #optionList = ('Result', 'Option 2', 'Option 3')
        optionList = (' ')
        self.v = tk.StringVar()
        #self.v.set(optionList[0])                              # select 1 item of list
        self.om = tk.OptionMenu(self, self.v, *optionList)
        self.om.grid(row=1, column=0, columnspan=2, padx=5, pady=0, sticky='EW')
        self.om.bind('<Escape>', self.OnPressESC)                # on ESC
        self.om.bind("<Return>", self.OnPressEnter)
        self.om['state'] = 'disabled'

        # Status label
        self.labelVariable = tk.StringVar()
        self.label = tk.Label(self,textvariable=self.labelVariable, anchor="center",fg="gray")
        self.label.grid(row=1, column=2, padx=5, pady=0)
        self.labelVariable.set(u"") # set empty text


        # Github button
        #
        # pick a (small) image file you have in the working directory ...
        photo2 = tk.PhotoImage(file="g.png")
        #
        self.githubButton = tk.Button(self,text=u"Prefs", image=photo2, highlightthickness=0,bd=0, command=self.OnGithubButtonClick)
        #self.githubButton = tk.Button(self,text=u"Prefs", command=self.OnPrefButtonClick)
        self.githubButton.configure(foreground='black')
        self.githubButton.bind('<Return>', self.OnPrefButtonClick)
        self.githubButton['state'] = 'normal'
        self.githubButton.grid(row=3, column=2, padx=5, pady=0)
        #
        # save the button's image from garbage collection (needed?)
        self.githubButton.image = photo2

        # Version label
        self.labelVersionVariable = tk.StringVar()
        self.labelVersion = tk.Label(self,textvariable=self.labelVersionVariable, anchor="center",fg="gray")
        self.labelVersion.grid(row=3, column=0, columnspan=1, sticky='EW')
        self.labelVersionVariable.set("Version "+appVersion)

        # Preference button
        #
        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="f.png")
        #
        self.prefButton = tk.Button(self,text=u"Prefs", image=photo1, highlightthickness=0,bd=0, command=self.OnPrefButtonClick)
        #self.prefButton = tk.Button(self,text=u"Prefs", command=self.OnPrefButtonClick)
        self.prefButton.configure(foreground='black')
        self.prefButton.bind('<Return>', self.OnPrefButtonClick)
        self.prefButton['state'] = 'normal'
        self.prefButton.grid(row=2, column=2, padx=5, pady=0)
        #
        # save the button's image from garbage collection (needed?)
        self.prefButton.image = photo1

        # misc
        self.grid_columnconfigure(0,weight=1)
        #self.resizable(True,False) # make it resizeable in width only - not in height
        self.resizable(False,False) # make it un-resizeable
        self.update()

        # Min size: http://stackoverflow.com/questions/10448882/how-do-i-set-a-minimum-window-size-in-tkinter
        self.minsize(self.winfo_width()+200, self.winfo_height())

        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)



    # search matching application for the current searchstring
    def searchingApplication(self, str):
        lengthOfSearchString =  len(str)

        if lengthOfSearchString < 1:
            printDebugToTerminal('Search string is empty')
            self.resetUI()
            return;
        else:
            print ('\n')
            printDebugToTerminal('Searching matching application for: '+str)
            searchResults = fnmatch.filter(os.listdir('/usr/bin'), '*'+str+'*')     # search for executables featuring *str*


            self.labelVariable.set(len(searchResults)) # show number of search results in status label

            if(len(searchResults) == 0):
                # search field
                self.entry.config(background="white")           # set background color
                self.entry.config(foreground="gray")            # set font color
                self.entry.config(highlightbackground="red")    # set border color

                # launch button
                self.button['state'] = 'disabled'               # disabling Launch Button

                # dropdown
                optionList = (' ')
                self.om = tk.OptionMenu(self, self.v, *optionList)
                self.om.grid(row=1, column=0, padx=5, pady=0, sticky='EW')
                self.v.set(optionList[0])                                   # select 1 menu-item
                self.om['state'] = 'disabled'

                # label
                self.label.config(fg='red',bg="lightgray")

            elif(len(searchResults) == 1):     # if we got 1 search-results
                printDebugToTerminal(searchResults[0])
                printDebugToTerminal('Autocompleting search field')

                # search field
                self.entry.config(background="white")           # set background color
                self.entry.config(foreground="green")           # set font color
                self.entry.config(highlightbackground="green")  # set border color
                #self.entryVariable.set(searchResults[0])        # Display name of executable in search field
                self.entry.focus_set()
                #self.entry.selection_range(0, tk.END)      # select entire field content
                self.entry.icursor(tk.END)                      # set cursor to end

                # launch button
                self.button['state'] = 'normal'                 # enabling Launch Button

                # dropdown
                self.om['state'] = 'disabled'

                #status label
                self.label.config(fg='green',bg="lightgray")    # Change color of status label

            else:           # got several hits
                printDebugToTerminal('Results:')

                self.entry.config(background="white")           # set background color
                self.entry.config(foreground="gray")            # set font color
                self.entry.config(highlightbackground="red")    # set border color
                # launch button
                self.button['state'] = 'disabled'               # disabling Launch Button

                # drpdowm
                self.om['state'] = 'normal'

                #status label
                self.label.config(fg='red',bg="lightgray")

            # Update Dropdown
            #optionList = ('one', 'two', 'three')
            optionList = searchResults
            self.om = tk.OptionMenu(self, self.v, *optionList)
            self.om.grid(row=1, column=0, padx=5, pady=0, sticky='EW')
            self.v.set(optionList[0])

            print(len(searchResults))
            print(searchResults)
            return;


    # On Pressing button
    def OnButtonClick(self):
        #self.labelVariable.set( self.entryVariable.get()+" (Clicked the button)" )
        printDebugToTerminal('----------- Clicked the button ------------')
        self.launchExternalApp()                                          # reset the UI

    # On Pressing button
    def OnPrefButtonClick(self):
        printDebugToTerminal('----------- Clicked the preference button ------------')

    # On Pressing button
    def OnGithubButtonClick(self):
        printDebugToTerminal('----------- Clicked the github button ------------')
        webbrowser.open('https://github.com/yafp/pylad')  # Go to github

    # launching external application
    def launchExternalApp(self):
        printDebugToTerminal('launching external application')
        #self.labelVariable.set( self.entryVariable.get()+" (Clicked the button)" )
        selectedApplicationName = self.v.get()          # get value of OptionMenu
        if selectedApplicationName != "":
            checkExecutable = cmd_exists(selectedApplicationName)                  # check if name exists and is executable
            if (checkExecutable == True):
                #call([self.entryVariable.get(), ""])                    # launch external command
                call([selectedApplicationName, ""])                    # launch external command
                self.resetUI()                                          # reset the UI
            else:
                print ('ERROR >> Checking the executable failed....')
        else:
            printDebugToTerminal('No application selected')

    # On Pressing ENTER
    def OnPressEnter(self,event):
        #self.labelVariable.set( self.entryVariable.get()+" (Pressed ENTER)" )
        printDebugToTerminal('----------- Pressed Enter ------------')
        self.launchExternalApp()


    # On KeyPress in search field
    #def OnPressKey(self, event):
        #print('Last Keypress:\t {k!r}'.format(k = event.char))     # output last keypress event
        #printDebugToTerminal('Last Keypress:\t {k!r}'.format(k = event.char))  # output last keypress event


    # On ESC
    def OnPressESC(self, event):
        printDebugToTerminal('Pressed ESC')
        self.resetUI()
        return;


    # update current search string and trigger app search
    def getSearchString(self, event):
        if event.char != '': # if not ARRAY DOWN then
            curString = self.entryVariable.get()                        # get current search string
            #printDebugToTerminal('Search-String:\t '+curString)         # output current content of search field
            self.searchingApplication(curString)                        # start search for this string


    # Arrow Down in Search field should list
    def OnArrowDown(self, event):
        #printDebugToTerminal("Arrow down pressed - should option Option list and set focus to it")
        self.om.focus_set()
        self.event_generate('<space>') # - Open the OptionMenu by simulating a keypress
        return;


    # reset the UI back to default
    def resetUI(self):
        print ("\n")
        #printDebugToTerminal('Resetting UI')

        # search field
        self.entry.config(background="white")                       # set background color
        self.entry.config(foreground="gray")                        # set foreground color
        self.entry.config(highlightbackground="gray")               # set border color
        self.entryVariable.set(u"")                                 # Empty search
        self.entry.focus_set()                                      # set focus to search field
        self.entry.selection_range(0, tk.END)

        # dropdown
        optionList = (' ')
        self.om = tk.OptionMenu(self, self.v, *optionList)
        self.om.grid(row=1, column=0, padx=5, pady=0, sticky='EW')
        self.v.set(optionList[0])                                   # select 1 menu-item
        self.om['state'] = 'disabled'

        # button
        self.button['state'] = 'disabled'                           # disable launch-button

        # status label
        self.labelVariable.set("")                                  # empty status label
        self.label.config(fg='gray',bg="lightgray")                 # reset status label colors


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title(appName)
    app.mainloop()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

"""This is pylad - a python based application launcher"""

# General App tutorial:                     http://sebsauvage.net/python/gui/#our_project
# Dropdown:                                 https://www.reddit.com/r/learnpython/comments/2wn1w6/how_to_create_a_drop_down_list_using_tkinter/


# -----------------------------------------------------------------------------------------------
# IMPORTING
# -----------------------------------------------------------------------------------------------
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk



#import Tkinter                      # for the UI
import os, fnmatch                  # for searching applications
from subprocess import call         # for calling external commands
import subprocess


# -----------------------------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------------------------
appName = "pylad"
appVersion = "20161020.01"

debug = True                    # True or False
#debug = False                    # True or False



# -----------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------

# via: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028
#
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
        self.entryVariable = tk.StringVar()
        self.entry = tk.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
    
        self.entry.bind("<Return>", self.OnPressEnter)
        #self.entry.bind("<Return>", self.launchExternalApp)
        
        self.entry.grid(row=0, column=0, padx=5, pady=0)            # set padding
        self.entry.config(background="white")                       # set background color
        self.entry.config(foreground="black")                       # set font color
        self.entry.config(highlightbackground="gray")               # set border color
        
        self.entry.bind('<Key>', self.OnPressKey)                   # on keypress
        self.entry.bind('<KeyRelease>', self.getSearchString)       # on keypress release
        self.entry.bind('<Escape>', self.OnPressESC)                # on ESC
        self.entryVariable.set(u"")                                 # set content on start = empty

        # Launch button
        self.button = tk.Button(self,text=u"Launch", command=self.OnButtonClick)
        self.button.grid(row=0, column=0, padx=5, pady=0)
        self.button.configure(foreground="black")
        self.button.bind("<Return>", self.OnButtonClick)
        self.button['state'] = 'disabled'
        self.button.grid(column=1,row=0)

        # Status label
        self.labelVariable = tk.StringVar()
        
        self.label = tk.Label(self,textvariable=self.labelVariable, anchor="w",fg="gray",bg="lightgray")
        #self.label.grid(row=0, column=0, padx=5, pady=0)            # set padding
        self.label.grid(column=0,row=1,columnspan=2,sticky='EW',padx=5, pady=0)
        self.labelVariable.set(u"") # set empty text
        
        # Version label        
        self.labelVersionVariable = tk.StringVar()
        self.labelVersion = tk.Label(self,textvariable=self.labelVersionVariable, anchor="center",fg="gray",bg="lightgray")
        self.labelVersion.grid(column=0,row=2,columnspan=2,sticky='EW')
        self.labelVersionVariable.set("r"+appVersion)

        # misc
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False) # make it resizeable in width only - not in height
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
            printDebugToTerminal('Searching matching application for: '+str)
            searchResults = fnmatch.filter(os.listdir('/usr/bin'), '*'+str+'*')     # search for executables featuring *str*
            
            numberOfSearchResults = len(searchResults)  #
            
            self.labelVariable.set(numberOfSearchResults)
            if(numberOfSearchResults == 1):     # got 1 hit
                printDebugToTerminal('Got 1 hit, autocompleting search field')
                printDebugToTerminal(searchResults[0])
                
                self.label.config(fg='green',bg="lightgray")        # Change color of status label
                self.button['state'] = 'normal'                 # enabling Launch Button
                
                self.entry.config(background="white")           # set background color
                self.entry.config(foreground="green")           # set font color
                self.entry.config(highlightbackground="green")   # set border color
                self.entryVariable.set(searchResults[0])        # Display name of executable in search field 
                self.entry.focus_set()
                #self.entry.selection_range(0, tk.END)      # select entire field content
                
                 # set cursor to end
                # MISSING

            else:           # got several hits
                printDebugToTerminal('Got several possible application matches')
                self.entry.config(background="white")           # set background color
                self.entry.config(foreground="black")           # set font color
                self.entry.config(highlightbackground="red")    # set border color
                self.button['state'] = 'disabled'               # disabling Launch Button
                self.label.config(fg='red',bg="lightgray")
            
            print(numberOfSearchResults)
            print(searchResults)
            return;


    # On Pressing button
    def OnButtonClick(self):
        self.labelVariable.set( self.entryVariable.get()+" (Clicked the button)" )
        printDebugToTerminal('----------- Clicked the button ------------')
        self.launchExternalApp()                                          # reset the UI


    # launching external application
    def launchExternalApp(self):
        printDebugToTerminal('launching external application')
        self.labelVariable.set( self.entryVariable.get()+" (Clicked the button)" )
        
        checkExecutable = cmd_exists(self.entryVariable.get())                  # check if name exists and is executable
        if (checkExecutable == True):
            call([self.entryVariable.get(), ""])                    # launch external command
            self.resetUI()                                          # reset the UI
        else:
            print "ERROR >> Checking the executable failed...."


    # On Pressing ENTER
    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (Pressed ENTER)" )
        printDebugToTerminal('----------- Pressed Enter ------------')
        self.launchExternalApp()


    # On KeyPress in search field
    def OnPressKey(self, event):
        #print('Last Keypress:\t {k!r}'.format(k = event.char))     # output last keypress event 
        printDebugToTerminal('Last Keypress:\t {k!r}'.format(k = event.char))  # output last keypress event 


    # On ESC
    def OnPressESC(self, event):
        printDebugToTerminal('Pressed ESC')
        self.resetUI()
        return;


    # update current search string and trigger app search
    def getSearchString(self, event):
        curString = self.entryVariable.get()
        printDebugToTerminal('Search-String:\t '+curString)         # output current content of search field
        self.searchingApplication(curString)


    # reset the UI back to default
    def resetUI(self):
        print "\n"
        printDebugToTerminal('Resetting UI')
        # search field
        self.entry.config(background="white")
        self.entry.config(foreground="black")
        self.entry.config(highlightbackground="gray")               # set border color
        self.entryVariable.set(u"")                                 # Empty search
        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)
        # button
        self.button['state'] = 'disabled'
        # status label
        self.labelVariable.set("")                                  # empty status label
        self.label.config(fg='grey',bg="lightgray")                 # reset status label colors


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title(appName)
    
    
    # WINDOW POSITION AND SIZE
    #
    #w = 400 # width for the Tk root
    #h = 150 # height for the Tk root
    #ws = app.winfo_screenwidth() # width of the screen
    #hs = app.winfo_screenheight() # height of the screen
    #
    # calculate x and y coordinates for the Tk root window
    #x = (ws/2) - (w/2)
    #y = (hs/2) - (h/2)
    #
    #app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #app.geometry(app.geometry())
    
    
    app.mainloop()

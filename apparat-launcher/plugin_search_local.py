#!/usr/bin/python
"""apparat - plugin: search-internet"""

## general
import difflib # for intelligent list sort
import fnmatch
import os
import wx

## apparat
import config
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------

TRIGGER = ('?')


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------

def search_user_files(main_window, current_search_string):
    """Search for user files"""
    tools.debug_output('search_user_files', 'starting', 1)

    # Reset status notification back to OK
    main_window.status_notification_reset()

    ## reset combobox
    search_results = []
    main_window.ui__cb_search.SetItems(search_results) # update combobox

    ## update plugin info
    main_window.plugin__update_general_ui_information('Local Search')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/'+str(config.TARGET_ICON_SIZE)+'/search.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Search local user files')

    ## parameter buttons
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/blank.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())
    main_window.ui__bt_selected_parameter.SetToolTipString('Search local user files')

    ## set command
    main_window.ui__txt_selected_app.SetValue('xdg-open')

    ## set parameter
    main_window.ui__txt_selected_parameter.SetValue('')

    if(len(current_search_string) > 4) and current_search_string.startswith('? '):
        current_search_string = current_search_string[2:] # get the real search term without trigger
        tools.debug_output('search_user_files', 'Searching local files for: '+current_search_string, 1)
        root = os.environ['HOME']
        pattern = '*'+current_search_string+'*'

        search_results = []

        if(len(current_search_string) > 2): # if search string is long enough
            tools.debug_output('search_user_files', 'Searching local user files for the following string: '+current_search_string, 1)

            exclude = set(['.cache', '.dbus', '.dropbox', '.dropbox-dist', '.local/share/Trash']) # exclude list for file search in home dir
            for root, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d not in exclude]
                for filename in fnmatch.filter(files, pattern):
                    result = os.path.join(root, filename) # append to list
                    search_results.append(result)

            tools.debug_output('search_user_files', 'Got '+(str(len(search_results)))+' Results', 1)

            ## sort search results
            search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

            # update result count
            main_window.ui__txt_result_counter.SetValue(str(len(search_results)))

            if(len(search_results) > 1):
                ## update application button
                main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/'+str(config.TARGET_ICON_SIZE)+'/files.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

            elif(len(search_results) == 1):
                ## update application button
                main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/'+str(config.TARGET_ICON_SIZE)+'/file.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

                ## parameter buttons
                main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/execute.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

                main_window.ui__txt_selected_app.SetValue('xdg-open')
                main_window.ui__txt_selected_parameter.SetValue(search_results[0])

            else: ## no results
                main_window.ui__txt_result_counter.SetValue('0') # overwrite

                ## update application button
                main_window.ui__bt_selected_app_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/noResult.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

            ## update combobox
            main_window.ui__cb_search.SetItems(search_results) # update combobox
        else:
            tools.debug_output('search_user_files', 'aborting search (string too short)', 2)
            main_window.ui__txt_result_counter.SetValue('0')
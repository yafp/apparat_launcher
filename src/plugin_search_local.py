#!/usr/bin/python
"""apparat - plugin: search-internet"""

import difflib                      # for intelligent list sort
import os
import fnmatch
import tools
import wx

def search_user_files(main_window, current_search_string):
    """Search for user files"""
    tools.debug_output('search_user_files', 'starting')

    # reset combobox
    search_results = []
    main_window.ui__cb_search.SetItems(search_results) # update combobox

    ## update plugin info
    main_window.plugin__update_general_ui_information('Local Search')

    ## application buttons
    main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/bt_search_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())
    main_window.ui__bt_selected_app.SetToolTipString('Search local user files')

    ## parameter buttons
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_blank_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())
    main_window.ui__bt_selected_parameter.SetToolTipString('Search local user files')

    ## set command
    main_window.ui__txt_selected_app.SetValue('xdg-open')

    ## set parameter
    main_window.ui__txt_selected_parameter.SetValue('')

    if(len(current_search_string) > 4) and current_search_string.startswith('? '):
        current_search_string = current_search_string[2:] # get the real search term without trigger
        tools.debug_output('search_user_files', 'Searching local files for: '+current_search_string)
        root = os.environ['HOME']
        pattern = '*'+current_search_string+'*'

        search_results = []

        if(len(current_search_string) > 2): # if search string is long enough
            tools.debug_output('search_user_files', 'Searching local user files for the following string: '+current_search_string)

            exclude = set(['.cache', '.dbus', '.dropbox', '.dropbox-dist', '.local/share/Trash']) # exclude list for file search in home dir
            for root, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d not in exclude]
                #for filename in fnmatch.filter(files, pattern):
                for filename in fnmatch.filter(files, pattern):
                    #print( os.path.join(root, filename))
                    result = os.path.join(root, filename) # append to list
                    search_results.append(result)

            tools.debug_output('search_user_files', 'Got '+(str(len(search_results)))+' Results')

            ## sort search results
            search_results = sorted(search_results, key=lambda x: difflib.SequenceMatcher(None, x, current_search_string).ratio(), reverse=True) # better sorting

            # update result count
            main_window.ui__txt_result_counter.SetValue(str(len(search_results)))

            if(len(search_results) > 1):
                # update application button
                main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/bt_files_128.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

            elif(len(search_results) == 1):
                # update application button
                main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_local/bt_file_128.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

                ## parameter buttons
                main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_execute_128.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())

                main_window.ui__txt_selected_app.SetValue('xdg-open')
                main_window.ui__txt_selected_parameter.SetValue(search_results[0])

            else: # no results
                main_window.ui__txt_result_counter.SetValue('0') # overwrite

                # update application button
                main_window.ui__bt_selected_app_img = wx.Image('gfx/core/bt_result_sad_128.png', wx.BITMAP_TYPE_PNG)
                main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

            # update combobox
            main_window.ui__cb_search.SetItems(search_results) # update combobox
        else:
            tools.debug_output('search_user_files', 'aborting search (string too short)')
            main_window.ui__txt_result_counter.SetValue('0')

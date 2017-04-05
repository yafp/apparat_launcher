#!/usr/bin/python
"""apparat - plugin: search-internet"""

# general
import webbrowser
import wx

# apparat
import constants
import ini
import tools


def prepare_internet_search(main_window, current_search_string):
    """Updates the UI according to the matching internet-search trigger"""
    tools.debug_output('prepare_internet_search', 'starting')

    ## show searchstring in parameter field
    if(main_window.ui__txt_selected_app.GetValue() != ''):
        cur_searchphrase_parameter = current_search_string[3:] # remove trigger - example: '!y '
        main_window.ui__txt_selected_parameter.SetValue(cur_searchphrase_parameter)

    ## check if there is NO space after the trigger - abort this function and reset some parts of the UI
    if(len(current_search_string) >= 3) and (current_search_string[2] != " "):
        tools.debug_output('prepare_internet_search', 'No space after trigger - should reset icons')
        main_window.plugin__update_general_ui_information('')
        return

    ## If search-string > 2 - abort - as all the work is already done
    #
    if(len(current_search_string) > 2):
        return # we can stop here - nothing more to do as plugin should be already activated

    ## Prepare UI for plugin
    if current_search_string.startswith('!a') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_amazon_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Amazon)')

    if current_search_string.startswith('!b') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_bandcamp_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Bandcamp)')

    if current_search_string.startswith('!e') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_stack-exchange_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Stack-Exchange)')

    if current_search_string.startswith('!g') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_google_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Google)')

    if current_search_string.startswith('!l') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_lastfm_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (LastFM)')

    if current_search_string.startswith('!m') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_maps_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Google-Maps)')

    if current_search_string.startswith('!o') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_stack-overflow_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Stack-Overflow)')

    if current_search_string.startswith('!r') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_reddit_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Reddit)')

    if current_search_string.startswith('!s') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_soundcloud_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (SoundCloud)')

    if current_search_string.startswith('!t') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_twitter_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Twitter)')

    if current_search_string.startswith('!v') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_vimeo_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Vimeo)')

    if current_search_string.startswith('!w') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_wikipedia_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Wikipedia)')

    if current_search_string.startswith('!y') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search_internet/bt_youtube_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (YouTube)')

    ## update application button
    main_window.ui__bt_selected_app.Enable(True)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

    ## update option button
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.Enable(True)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())
    main_window.ui__bt_selected_parameter.SetToolTipString('Search')


def execute_internet_search(main_window, command, parameter):
    """Plugin: Internet-Search - Execute the actual internet search call"""
    tools.debug_output('execute_internet_search', 'starting')

    # get tuple position of command
    index = constants.APP_PLUGINS_INTERNET_SEARCH_TRIGGER.index(command)

    # get url based on tuple index
    remote_url = constants.APP_PLUGINS_INTERNET_SEARCH_URLS[index]

    if(len(parameter) == 0): # if so searchphrase/parameter was supplied - open the main url (Issue #22)
        tools.debug_output('execute_internet_search', 'No searchphrase supplied, trunc to main-url') # Issue #22
        remote_url = tools.trunc_at(remote_url, "/")

    ## open the URL
    webbrowser.open(remote_url)

    ## update usage-statistics
    tools.debug_output('execute_internet_search', 'Updating statistics (plugin_executed)')
    current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed') # get current value from ini
    ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

    # reset the UI
    main_window.reset_ui()

    ## if enabled in ini - hide the UI after executing the command
    cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
    if cur_ini_value_for_hide_ui_after_command_execution == 'True':
        main_window.tbicon.execute_tray_icon_left_click()

#!/usr/bin/python
"""apparat - plugin: search-internet"""

# general
import wx

# project
import tools


def plugin__internet_search_prepare(main_window, current_search_string):
    """Plugin: Internet-Search - Updates the UI on trigger input"""
    tools.debug_output('plugin__internet_search_prepare', 'starting')

    ## show searchstring in parameter field
    if(main_window.ui__txt_selected_app.GetValue() != ''):
        cur_searchphrase_parameter = current_search_string[3:] # remove trigger - example: '!y '
        main_window.ui__txt_selected_parameter.SetValue(cur_searchphrase_parameter)

    ## check if there is NO space after the trigger - abort this function and reset some parts of the UI
    if(len(current_search_string) >= 3) and (current_search_string[2] != " "):
        tools.debug_output('plugin__internet_search_prepare', 'No space after trigger - should reset icons')
        main_window.plugin__update_general_ui_information('')
        return

    ## If search-string > 2 - abort - as all the work is already done
    #
    if(len(current_search_string) > 2):
        return # we can stop here - nothing more to do as plugin should be already activated

    ## Prepare UI for plugin
    if current_search_string.startswith('!a') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_amazon_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Amazon)')

    if current_search_string.startswith('!b') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_bandcamp_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Bandcamp)')

    if current_search_string.startswith('!e') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_stack-exchange_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Stack-Exchange)')

    if current_search_string.startswith('!g') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_google_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Google)')

    if current_search_string.startswith('!l') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_lastfm_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (LastFM)')

    if current_search_string.startswith('!m') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_maps_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Google-Maps)')

    if current_search_string.startswith('!o') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_stack-overflow_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Stack-Overflow)')

    if current_search_string.startswith('!r') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_reddit_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Reddit)')

    if current_search_string.startswith('!s') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_soundcloud_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (SoundCloud)')

    if current_search_string.startswith('!t') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_twitter_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Twitter)')

    if current_search_string.startswith('!v') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_vimeo_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Vimeo)')

    if current_search_string.startswith('!w') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_wikipedia_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (Wikipedia)')

    if current_search_string.startswith('!y') is True:
        main_window.ui__bt_selected_app_img = wx.Image('gfx/plugins/search/bt_youtube_128.png', wx.BITMAP_TYPE_PNG)
        main_window.plugin__update_general_ui_information('Internet-Search (YouTube)')


    ## for all search plugin cases
    #
    ## update application button
    main_window.ui__bt_selected_app.Enable(True)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

    ## update option button
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/bt_search_128.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.Enable(True)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())
    main_window.ui__bt_selected_parameter.SetToolTipString('Search')

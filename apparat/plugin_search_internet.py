#!/usr/bin/python
"""apparat - plugin: search-internet"""

# general
import webbrowser
import wx

# apparat
import config
import ini
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------

TRIGGER = ('!a', '!b', '!e', '!g', '!l', '!m', '!o', '!r', '!s', '!t', '!v', '!w', '!y')

URLS = (
    'https://www.amazon.de/s/field-keywords=',
    'https://bandcamp.com/search?q=',
    'https://stackexchange.com/search?q=',
    'https://www.google.com/search?q=',
    'https://www.last.fm/search?q=',
    'http://www.maps.google.de/maps/place/',
    'https://stackoverflow.com/search?q=',
    'https://www.reddit.com/search?q=',
    'https://soundcloud.com/search?q=',
    'https://twitter.com/search?q=',
    'https://vimeo.com/search?q=',
    'https://en.wikipedia.org/w/index.php?search=',
    'https://www.youtube.com/results?search_query='
)

ICONS = (
    'amazon.png',
    'bandcamp.png',
    'stack-exchange.png',
    'google.png',
    'lastfm.png',
    'maps.png',
    'stack-overflow.png',
    'reddit.png',
    'soundcloud.png',
    'twitter.png',
    'vimeo.png',
    'wikipedia.png',
    'youtube.png'
)

DESCRIPTIONS = (
    'Internet-Search (Amazon)',
    'Internet-Search (Bandcamp)',
    'Internet-Search (Stack-Exchange)',
    'Internet-Search (Google)',
    'Internet-Search (LastFM)',
    'Internet-Search (Google-Maps)',
    'Internet-Search (Stack-Overflow)',
    'Internet-Search (Reddit)',
    'Internet-Search (SoundCloud)',
    'Internet-Search (Twitter)',
    'Internet-Search (Vimeo)',
    'Internet-Search (Wikipedia)',
    'Internet-Search (YouTube)'
)


# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------

def prepare_internet_search(main_window, current_search_string):
    """Updates the UI according to the matching internet-search trigger"""
    tools.debug_output('prepare_internet_search', 'starting', 1)

    ## show searchstring in parameter field
    if(main_window.ui__txt_selected_app.GetValue() != ''):
        cur_searchphrase_parameter = current_search_string[3:] # remove trigger - example: '!y '
        main_window.ui__txt_selected_parameter.SetValue(cur_searchphrase_parameter)

    ## check if there is NO space after the trigger - abort this function and reset some parts of the UI
    if(len(current_search_string) >= 3) and (current_search_string[2] != " "):
        tools.debug_output('prepare_internet_search', 'No space after trigger - should reset icons', 1)
        main_window.plugin__update_general_ui_information('')
        return

    ## If search-string > 2 - abort - as all the work is already done
    #
    if(len(current_search_string) > 2):
        return # we can stop here - nothing more to do as plugin should be already activated

    # get tuple position of command
    index = TRIGGER.index(current_search_string)

    # get icon-name based on tuple index
    icon = 'gfx/plugins/search_internet/'+str(config.TARGET_ICON_SIZE)+'/'+ICONS[index]

    # get description based on tuple index
    description = DESCRIPTIONS[index]

    # update UI with icon and description
    main_window.ui__bt_selected_app_img = wx.Image(icon, wx.BITMAP_TYPE_PNG)
    main_window.plugin__update_general_ui_information(description)

    ## update application button
    main_window.ui__bt_selected_app.Enable(True)
    main_window.ui__bt_selected_app.SetBitmap(main_window.ui__bt_selected_app_img.ConvertToBitmap())

    ## update option button
    main_window.ui__bt_selected_parameter_img = wx.Image('gfx/core/'+str(config.TARGET_ICON_SIZE)+'/search.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_selected_parameter.Enable(True)
    main_window.ui__bt_selected_parameter.SetBitmap(main_window.ui__bt_selected_parameter_img.ConvertToBitmap())
    main_window.ui__bt_selected_parameter.SetToolTipString('Search')


def execute_internet_search(main_window, command, parameter):
    """Plugin: Internet-Search - Execute the actual internet search call"""
    tools.debug_output('execute_internet_search', 'starting', 1)

    # get tuple position of command
    index = TRIGGER.index(command)

    # get url based on tuple index
    remote_url = URLS[index]+parameter

    if(len(parameter) == 0): # if so searchphrase/parameter was supplied - open the main url (Issue #22)
        tools.debug_output('execute_internet_search', 'No searchphrase supplied, trunc to main-url', 2) # Issue #22
        remote_url = tools.trunc_at(remote_url, "/")

    ## open the URL
    webbrowser.open(remote_url)

    ## update usage-statistics
    tools.debug_output('execute_internet_search', 'Updating statistics (plugin_executed)', 1)
    current_plugin_executed_count = ini.read_single_value('Statistics', 'plugin_executed') # get current value from ini
    ini.write_single_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

    # reset the UI
    main_window.reset_ui()

    ## if enabled in ini - hide the UI after executing the command
    cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_value('General', 'hide_ui_after_command_execution') # get current value from ini
    if cur_ini_value_for_hide_ui_after_command_execution == 'True':
        main_window.tbicon.execute_tray_icon_left_click()

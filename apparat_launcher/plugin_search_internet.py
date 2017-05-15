#!/usr/bin/python
"""apparat_launcher - plugin: search-internet"""

# general
import webbrowser
import sys
import wx

# apparat
import ini
import tools


# -----------------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------------

TRIGGER = ('!am', '!au', '!bc', '!dd', '!fb', '!fl', '!gh', '!gi', '!gk', '!gm', '!gn', '!gs', '!la', '!re', '!sc', '!se', '!so', '!tu', '!tw', '!vi', '!wi', '!yt',)

URLS = (
    'https://www.amazon.de/s/field-keywords=',
    'https://askubuntu.com/search?q=',
    'https://bandcamp.com/search?q=',
    'https://duckduckgo.com/?q=',
    'https://m.facebook.com/search/?&query=',
    'https://www.flickr.com/search/?text=',
    'https://github.com/search?q=',
    'https://www.google.de/search?&tbm=isch&q=',
    'https://keep.google.com/',
    'http://www.maps.google.de/maps/place/',
    'https://www.google.de/search?&tbm=nws&q=',
    'https://www.google.com/search?q=',
    'https://www.last.fm/search?q=',
    'https://www.reddit.com/search?q=',
    'https://soundcloud.com/search?q=',
    'https://stackexchange.com/search?q=',
    'https://stackoverflow.com/search?q=',
    'https://www.tumblr.com/search/',
    'https://twitter.com/search?q=',
    'https://vimeo.com/search?q=',
    'https://en.wikipedia.org/w/index.php?search=',
    'https://www.youtube.com/results?search_query='
)

ICONS = (
    'amazon.png',
    'stack-exchange.png',
    'bandcamp.png',
    'duckduckgo.png',
    'facebook.png',
    'flickr.png',
    'github.png',
    'google.png',
    'google.png',
    'maps.png',
    'google.png',
    'google.png',
    'lastfm.png',
    'reddit.png',
    'soundcloud.png',
    'stack-exchange.png',
    'stack-overflow.png',
    'tumblr.png',
    'twitter.png',
    'vimeo.png',
    'wikipedia.png',
    'youtube.png'
)

DESCRIPTIONS = (
    'Internet-Search (Amazon)',
    'Internet-Search (Ask Ubuntu)',
    'Internet-Search (BandCamp)',
    'Internet-Search (DuckDuckGo)',
    'Internet-Search (FaceBook)',
    'Internet-Search (Flickr)',
    'Internet-Search (GitHub)',
    'Internet-Search (Google Images)',
    'Internet-Search (Google Keep/Notes)',
    'Internet-Search (Google Maps)',
    'Internet-Search (Google News)',
    'Internet-Search (Google Search)',
    'Internet-Search (LastFM)',
    'Internet-Search (Reddit)',
    'Internet-Search (SoundCloud)',
    'Internet-Search (Stack-Exchange)',
    'Internet-Search (Stack-Overflow)',
    'Internet-Search (Tumbler)',
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
    tools.debug_output('prepare_internet_search', 'starting', 1, __name__)

    ## Reset status notification back to OK
    main_window.status_notification_got_distinct_result()

    icon_size = ini.read_single_ini_value('General', 'icon_size') # get preference value

    ## show searchstring in parameter field
    if(main_window.ui__txt_command.GetValue() != ''):
        cur_searchphrase_parameter = current_search_string[3:] # remove trigger - example: '!y '
        main_window.ui__txt_parameter.SetValue(cur_searchphrase_parameter)

    ## check if there is NO space after the trigger - abort this function and reset some parts of the UI
    if(len(current_search_string) >= 4) and (current_search_string[3] != " "):
        tools.debug_output('prepare_internet_search', 'No space after trigger - should reset icons', 1, __name__)
        main_window.plugin__update_general_ui_information('')
        main_window.status_notification_display_error('Invalid input')
        return

    ## If search-string > 3 - abort - as all the work is already done
    #
    if(len(current_search_string) > 3):
        return # we can stop here - nothing more to do as plugin should be already activated

    # get tuple position of command
    index = TRIGGER.index(current_search_string)

    # get icon-name based on tuple index
    icon = 'gfx/plugins/search_internet/'+icon_size+'/'+ICONS[index]

    # get description based on tuple index
    description = DESCRIPTIONS[index]

    # update UI with icon and description
    main_window.ui__bt_command_img = wx.Image(icon, wx.BITMAP_TYPE_PNG)
    main_window.plugin__update_general_ui_information(description)

    ## command button
    main_window.ui__bt_command.Enable(True)
    main_window.ui__bt_command.SetBitmap(main_window.ui__bt_command_img.ConvertToBitmap())

    ## parameter button
    main_window.ui__bt_parameter_img = wx.Image('gfx/core/'+icon_size+'/search.png', wx.BITMAP_TYPE_PNG)
    main_window.ui__bt_parameter.Enable(True)
    main_window.ui__bt_parameter.SetBitmap(main_window.ui__bt_parameter_img.ConvertToBitmap())
    main_window.ui__bt_parameter.SetToolTipString('Search')


def execute_internet_search(main_window, command, parameter):
    """Plugin: Internet-Search - Execute the actual internet search call"""
    tools.debug_output('execute_internet_search', 'starting', 1, __name__)

    # get tuple position of command
    index = TRIGGER.index(command)

    # get url based on tuple index
    remote_url = URLS[index]+parameter

    if(len(parameter) == 0): # if so searchphrase/parameter was supplied - open the main url (Issue #22)
        tools.debug_output('execute_internet_search', 'No searchphrase supplied, trunc to main-url', 2, __name__) # Issue #22
        remote_url = tools.trunc_at(remote_url, "/")

    ## open the URL
    webbrowser.open(remote_url)

    ## update usage-statistics
    tools.debug_output('execute_internet_search', 'Updating statistics (plugin_executed)', 1, __name__)
    current_plugin_executed_count = ini.read_single_ini_value('Statistics', 'plugin_executed') # get current value from ini
    ini.write_single_ini_value('Statistics', 'plugin_executed', int(current_plugin_executed_count)+1) # update ini +1

    # reset the UI
    main_window.reset_ui()

    ## if enabled in ini - hide the UI after executing the command
    cur_ini_value_for_hide_ui_after_command_execution = ini.read_single_ini_value('General', 'hide_ui_after_command_execution') # get current value from ini
    if cur_ini_value_for_hide_ui_after_command_execution == 'True':
        main_window.tbicon.execute_tray_icon_left_click()

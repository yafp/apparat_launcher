Changelog
==========

![logo](https://raw.githubusercontent.com/yafp/apparat_launcher/master/apparat_launcher/gfx/core/128/appIcon.png)


# 20170602
* Plugin Password Generator: changed default button to OK (memorable or not)


# 20170530
* Moved trayicon and traymenu code to new file tray_icon.py
* UI: reduced main window height from 460px to 430px
* UI: Text command has now a highlight for the user input string
* Plugins: Optimized plugin-commands-search regarding when to autocomplete and when not
* Plugin Internet Search: adding support for blog.fefe.de
* tools.py: Added general support for syslog in debug_output                            (Issue: #68)


# 20170523
* Reworking requirements check (is now plugin specific)                                 (Issue: #67)
* Adding first version of apidoc (using epydoc)


# 20170519
* Reset UI function takes now care about icon-size as well
* Project is now using Travis CI for building etc...                                    (Issue: #51)


# 20170518
* Plugins: Added new plugin Kill (using xkill)                                          (Issue: #66)
* Optimized code to detect running application processes


# 20170515
* Plugin-command-search now features only commands from enabled plugins                 (Issue: #62)
* Plugin-command-search is now sorted                                                   (Issue: #63)
* Plugin-command-search got autocomplete now                                            (Issue: #64)
* Plugin-command-search does no autocomplete if user is pressing BackSpace
* Plugin Password Generator: UI is now always resetted after finishing the function
* Debug Output: Now shows the source (.py) file as well, not only function name)        (Issue: #65)


# 20170511
* Plugins: Fill searchresults with matching plugin-triggers (if input starts with !)    (Issue: #59)
* Plugin Password Generator: Add support for memorable passwords                        (Issue: #60)
* Plugin Password Generator: Now generates 5 passwords on execution to offer a choice   (Issue: #61)
* Renamed apparatHotkeyHelper.sh to hotkeyHelperForApparatLauncher


# 20170509
* Plugin Internet Search: Add support for Google Keep/Notes (!gk)                       (Issue: #53)
* Plugin Password Generator: Added initial version of new plugin                        (Issue: #54)
* Plugins: Fix wrong result count while incomplete plugin command                       (Issue: #55)
* Command button is now displaying appIcon if disabled                                  (Issue: #56)
* Parameter button is now showing search-icon if disabled                               (Issue: #57)
* Parameter button now shows execute icon if search results > 1 (formerly blank)        (ISsue: #58)


# 20170508
* Fix left-over from #50 in apparat.py (get_icon) and plugin_nautilus.py
* Finishing rename to apparat_launcher.py                                               (Issue: #42)
* UI: Transparency change now via preferences (before: config.py)                       (Issue: #52)


# 20170506
* Minor fix for apparatHotkeyHelper.sh
* Minor changes based on pylint
* Plugin Shell:
    Moved from xterm to x-terminal-emulator as default
    Opens now a new default terminal and executes the related command
* Optimized method get_icon in apparat-launcher.py
* Readme.md: Fixing landscape link                                                      (Issue: #42)
* Ini: Adjusted ini folder and ini file to new project name                             (Issue: #42)
* Project: renaming once again from apparat-launcher to apparat_launcher                (Issue: #42)
    (apparat-launcher conflicts with naming conventions)
* UI: Status icon is hidden by default. Only displayed if there is an OK or ERROR state
* UI: Icon size change now via preferences (before: config.py)                          (Issue: #50)


# 20170427
* Add requirements check to apparatHotkeyHelper.sh
* Plugin Internet Search: Move from single to dual-letter triggers                      (Issue: #40)
* Plugin Internet Search: Add support for Ask Ubuntu via !au                            (Issue: #41)
* Plugin Internet Search: Add support for GitHub via !gh                                (Issue: #39)
* Plugin Internet Search: Add support for Facebook via !fb                              (Issue: #43)
* Renamed project from apparat to apparat-launcher                                      (Issue: #42)
* Plugin Internet Search: Add support for Flickr via !fl                                (Issue: #44)
* Plugin Internet Search: Add support for Google Images via !gi                         (Issue: #45)
* Plugin Internet Search: Add support for Google News via !gn                           (Issue: #46)
* Plugin Internet Search: Add support for DuckDuckGo Search via !dd                     (Issue: #47)
* Plugin Internet Search: Add support for tumblr via !tu                                (Issue: #48)
* Preferences: Add description text for each plugin on plugin-preference-tab1           (Issue: #49)


# 20170415
* Prefs: Plugins can now be enabled or disabled.                                        (Issue: #37)
* Plugins: Create new plugin core which handles !prefs, !preferences and !helper        (Issue: #38)


# 20170413
* Plugin Misc: Added ~ support for !open command                                        (Issue: #35)
* Plugin Nautilus: Added ~ support for !goto command                                    (Issue: #36)
* Improved check for required linux packages
* Improved get_icon method in case of .svg results


# 20170412
* Preferences: Checkboxes on plugin-tab are not longer disabled,
    but state can't be changed. All plugins are always enabled.                         (Issue: #33)
* Ini: Added basic validation (existing sections and options)                           (Issue: #13)
* Tools: Enhanced readability of debug output by adding spaces to source (same width)   (Issue: #34)
* Tools: Add support for colored debug output                                           (Issue: #32)


# 20170410
* Replaced Gtk/gtk with xdg (icon search)                                               (Issue: #15)
* Adding status notifier to main ui                                                     (Issue: #29)
* Plugin Internet-Search: Bugfix regarding missing searchparameter                      (Issue: #30)
* Plugin Misc: Closing UI if configured after running ! help                            (Issue: #31)


# 20170407
* Plugins: Moved plugin-specific constants from constant.py to plugin_PLUGINNAME.py
* Plugins: Moved plugin_shell and plugin_misc code to separate files
* Plugin Session: Added new !screensaver/!saver command                                 (Issue: #26)
* Plugin Misc: Add new !help command                                                    (Issue: #27)
* Plugin Misc: Added new !preferences command                                           (Issue: #28)


# 20170406
* Plugin Internet Search: Simplified plugin code (reduced complexity)
* Added project wide support for 2 different icon sizes (128px & 256px)                 (Issue: #25)
* Documentation: Added CHANGELOG.md to repo


# 20170405
* Added check for desktop-environment to tools.check_platform() -                       (Issue: #24)
* Search & case-sensitivity - user input is now lowercased before used for search       (Issue: #23)


# 20170403
* Plugin Internet Search: Added support for empty searchphrase                          (Issue: #22)


# before
* undocumented

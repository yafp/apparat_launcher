Changelog
==========

![logo](https://raw.githubusercontent.com/yafp/apparat/master/apparat/gfx/core/128/appIcon.png)


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

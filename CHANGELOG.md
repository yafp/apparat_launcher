apparat changelog
==========

![logo](https://raw.githubusercontent.com/yafp/apparat/master/apparat/gfx/core/128/appIcon.png)

# 20170412
* Preferences: Checkboxes on plugin-tab are not longer disabled,
    but state can't be changed. All plugins are always enabled.                         Issue: #33
* Ini: Added basic validation (existing sections and options)                           Issue: #13
* Tools: Enhanced readability of debug output by adding spaces to source (same width)   Issue: #34
* Tools: Add support for colored debug output                                           Issue: #32


# 20170410
* Replaced Gtk/gtk with xdg (icon search)                                               Issue: #15
* Adding status notifier to main ui                                                     Issue: #29
* Plugin Internet-Search: Bugfix regarding missing searchparameter                      Issue: #30
* Plugin Misc: Closing UI if configured after running ! help                            Issue: #31


# 20170407
* Plugins: Moved plugin-specific constants from constant.py to plugin_PLUGINNAME.py
* Plugins: Moved plugin_shell and plugin_misc code to separate files
* Plugin Session: Added new !screensaver/!saver command                                 Issue: #26
* Plugin Misc: Add new !help command                                                    Issue: #27
* Plugin Misc: Added new !preferences command                                           Issue: #28


# 20170406
* Plugin Internet Search: Simplified plugin code (reduced complexity)
* Added project wide support for 2 different icon sizes (128px & 256px)                 Issue: #25
* Documentation: Added CHANGELOG.md to repo


# 20170405
* Added check for desktop-environment to tools.check_platform() -                       Issue: #24
* Search & case-sensitivity - user input is now lowercased before used for search       Issue: #23


# 20170403
* Plugin Internet Search: Added support for empty searchphrase                          Issue: #22


# before
* undocumented

<!---
[![Code Health](https://landscape.io/github/yafp/apparat_launcher/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/apparat_launcher/master)
-->
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/yafp/apparat_launcher.svg)](https://github.com/yafp/apparat_launcher/issues)
[![Issues Closed](https://img.shields.io/github/issues-closed/yafp/apparat_launcher.svg)](https://github.com/yafp/apparat_launcher/issues?q=is%3Aclosed)
[![Build Status](https://travis-ci.org/yafp/apparat_launcher.svg?branch=master)](https://travis-ci.org/yafp/apparat_launcher)


# <a name="top"> apparat_launcher

![logo](https://raw.githubusercontent.com/yafp/apparat_launcher/master/apparat_launcher/gfx/core/128/appIcon.png)


## Important notice
This program is currently in a very early development state.


## <a name="toc">Table of Contents

  * [Description](#description)
  * [Screenshots](#screenshots)
  * [Installation](#installation)
    * [Requirements](rRequirements)
  * [Usage](#usage)
    * [Parameter](#parameter)
    * [Hotkey](#hotkey)
  * [Plugins](#plugins)
    * [Core](#core)
    * [Kill](#kill)
    * [Misc](#misc)
    * [Nautilus](#nautilus)
    * [Password Generator](#passwordgen)
    * [Screenshot](#screenshot)
    * [Search-Internet](#search-internet)
    * [Search-Local](#search-local)
    * [Session](#session)
    * [Shell](#shell)
  * [Contributing](#contributing)
  * [Credits](#credits)


## <a name="description">Description

__apparat_launcher__ is an application launcher for linux. It is developed and tested for Gnome Desktop environments.


## <a name="screenshots">Screenshots
*Launcher UI*

![screenshot](https://raw.githubusercontent.com/yafp/apparat_launcher/master/docs/screenshots_ui/screenshot_ui.png)


*Tray-Icon (Gnome)*

![screenshot](https://raw.githubusercontent.com/yafp/apparat_launcher/master/docs/screenshots_ui/screenshot_trayicon.png)


## <a name="installation">Installation
There is no installation routine so far.

#### <a name="requirements">Requirements
##### Python modules

- ```difflib```
- ```fnmatch```
- ```os```
- ```platform```
- ```psutil```
- ```subprocess```
- ```sys```
- ```webbrowser```
- ```wx```
- ```xdg```
- ```xdg.IconTheme```

##### Linux packages
The following packages are needed:

- ```gnome-screensaver-command```
- ```gnome-session-quit```
- ```systemctl```
- ```xdg-open```
- ```xdotool```


## <a name="usage">Usage
Simply run:
```
./apparat_launcher.py
```


#### <a name="parameter">Parameter
The following command line parameters are available:

| Parameter     | Alias          | Function            |
| ------------- |:---------------| :-------------------|
| ```-d```      | ```--debug```  | Show debug output   |
| ```-h```      | ```--help```   | Show help           |
| ```-v```      | ```--version```| Show version        |

*Debug output*

![screenshot](https://raw.githubusercontent.com/yafp/apparat_launcher/master/docs/screenshots_ui/screenshot_debug_output.png)


#### <a name="hotkey">Hotkey
If you want to use a global/system-wide hotkey to trigger ```apparat_launcher``` (starting, focusing and minimizing) consider using the script ```hotkeyHelperForApparatLauncher.sh```. Simply define a system-wide hotkey which triggers ```hotkeyHelperForApparatLauncher.sh```.

Hotkey definition in [Gnome](https://help.gnome.org/users/gnome-help/stable/keyboard-shortcuts-set.html.en)
* Open the **Activities** overview and start typing Keyboard.
* Click on **Keyboard** to open the panel.
* Select the **Shortcuts** tab.
* Select a category in the left pane, and the row for the desired action (launching ```hotkeyHelperForApparatLauncher.sh```)  on the right. The current shortcut definition will change to **New accelerator…**
* Hold down the desired key combination, or press Backspace to clear.


## <a name="plugins">Plugins
#### <a name="core">Core
Core plugin (can not be disabled)

| Trigger            | Alias              | Parameter      | Function                                        |
|--------------------|:------------------ |:---------------|:------------------------------------------------|
| ```!help```        |                    |                | Open apparat_launcher online documentation      |
| ```!preferences``` | ```!prefs```       |                | Open apparat_launcher preferences               |


#### <a name="kill">Kill
Optional plugin to kill graphical applications using xkill

| Trigger            | Alias              | Parameter      | Function                                        |
|--------------------|:------------------ |:---------------|:------------------------------------------------|
| ```!xkill```       | ```!kill```        |                | Starts xkill                                    |


#### <a name="misc">Misc
Optional plugin

| Trigger            | Alias              | Parameter      | Function                                        |
|--------------------|:------------------ |:---------------|:------------------------------------------------|
| ```!open```        |                    | _path_         | Open file or folder using default application   |


#### <a name="nautilus">Nautilus
Optional plugin which offers quick access to some locations in nautilus

| Trigger          | Alias          | Parameter      | Function                         |
|------------------|:-------------- |:---------------|:---------------------------------|
| ```!goto```      |                | _path_         | Open directory in nautilus       |
| ```!network```   | ```!net```     |                | Show network devices in nautilus |
| ```!recent```    |                |                | Show recent files in nautilus    |
| ```!trash```     |                |                | Show trash in nautilus           |


#### <a name="passwordgen">Password Generator
Optional plugin which offers a simple password generator

| Trigger          | Alias          | Parameter      | Function                         |
|------------------|:-------------- |:---------------|:---------------------------------|
| ```!pw```        | ```!password```|                | A simple password generator      |


#### <a name="screenshot">Screenshot
Optional plugin which offers screenshot functionality

| Trigger          | Alias              | Parameter      | Function                              |
|------------------|:------------------ |:---------------|:--------------------------------------|
| ```!ss```        |                    |                | Selective screenshot (window or area) |
| ```!fs```        |                    |                | Full screenshot                       |


#### <a name="search-internet">Search-Internet
Optional plugin which offers easy access to some popular web-services

| Trigger          | Alias          | Parameter      | Function               |
|------------------|:---------------|:---------------|:---------------------- |
| ```!am```        |                | _searchstring_ | Amazon                 |
| ```!au```        |                | _searchstring_ | Ask Ubuntu             |
| ```!bc```        |                | _searchstring_ | BandCamp               |
| ```!dd```        |                | _searchstring_ | DuckDuckGo             |
| ```!fb```        |                | _searchstring_ | FaceBook               |
| ```!fe```        |                | _searchstring_ | Fefe                   |
| ```!fl```        |                | _searchstring_ | Flickr                 |
| ```!gh```        |                | _searchstring_ | GitHub                 |
| ```!gi```        |                | _searchstring_ | Google Images          |
| ```!gk```        |                | _searchstring_ | Google Keep/Notes      |
| ```!gm```        |                | _searchstring_ | Google Maps            |
| ```!gn```        |                | _searchstring_ | Google News            |
| ```!gs```        |                | _searchstring_ | Google Search          |
| ```!la```        |                | _searchstring_ | LastFM                 |
| ```!re```        |                | _searchstring_ | Reddit                 |
| ```!sc```        |                | _searchstring_ | SoundCloud             |
| ```!se```        |                | _searchstring_ | Stack-Exchange         |
| ```!so```        |                | _searchstring_ | Stack-Overflow         |
| ```!tu```        |                | _searchstring_ | Tumblr                 |
| ```!tw```        |                | _searchstring_ | Twitter                |
| ```!vi```        |                | _searchstring_ | Vimeo                  |
| ```!wi```        |                | _searchstring_ | Wikipedia              |
| ```!yt```        |                | _searchstring_ | YouTube                |


#### <a name="search-local">Search-Local
Optional plugin which offers a file search for $HOME

| Trigger          | Alias          | Parameter      | Function                      |
|------------------|:---------------|:---------------|:----------------------------- |
| ```?```          |                | _searchstring_ | Filesearch for home directory |


#### <a name="session">Session
Optional plugin which offers access to some session commands

| Trigger            | Alias          | Parameter      | Function                    |
|--------------------|:-------------- |:---------------|:----------------------------|
| ```!hibernate```   | ```!sleep```   |                | hibernate the machine       |
| ```!lock```        |                |                | locks the current session   |
| ```!logout```      |                |                | logout from current session |
| ```!reboot```      | ```!restart``` |                | reboot the machine          |
| ```!shutdown```    | ```!halt```    |                | shutdown the machine        |
| ```!screensaver``` | ```!saver```   |                | start screensaver           |


#### <a name="shell">Shell
Optional plugin which allows running terminal commands from within the launcher

| Trigger          | Alias              | Parameter      | Function                            |
|------------------|:------------------ |:---------------|:------------------------------------|
| ```!sh```        |                    | _path_         | Run terminal commands in new window |


## <a name="contributing">Contributing
Please check the [Contribution guidelines for this project](.github/CONTRIBUTING.md)

![bomb](https://raw.githubusercontent.com/yafp/apparat_launcher/master/docs/bomb.gif)


## <a name="credits">Credits
* Icons [Details](docs/icons.md)
  * [Font Awesome](http://fontawesome.io)
  * [Foundation Icons](http://zurb.com/playground/foundation-icon-fonts-3)
  * [FA2PNG](http://fa2png.io/)
* Colors
  * Gray (#7f8c8d or 127, 140, 141)
  * Red (#b92c0c or 185, 44, 12)
  * Green (#269c58 or 38, 156, 88)

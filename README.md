# <a name="top"> apparat


![logo](https://raw.githubusercontent.com/yafp/apparat/master/apparat/gfx/core/128/appIcon.png)

[![Code Health](https://landscape.io/github/yafp/apparat/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/apparat/master)


## <a name="toc">Table of Contents

  * [Description](#description)
  * [Screenshots](#screenshots)
  * [Installation](#installation)
    * [Requirements](rRequirements)
  * [Usage](#usage)
    * [Parameter](#parameter)
    * [Hotkey](#hotkey)
  * [Plugins](#plugins)
    * [Local-Search](#local-search)
    * [Internet-Search](#internet-search)
    * [Nautilus](#nautilus)
    * [Session](#session)
    * [Screenshot](#screenshot)
    * [Shell](#shell)
    * [Misc](#misc)
  * [Contributing](#contributing)
  * [Credits](#credits)
  * [License](#license)


## <a name="description">Description

__apparat__ is an application launcher for linux. It is developed and tested for Gnome Desktop environments.


## <a name="screenshots">Screenshots
![screenshot](https://raw.githubusercontent.com/yafp/apparat/master/docs/screenshots_ui/screenshot_ui.png)

*User-Interace*


![screenshot](https://raw.githubusercontent.com/yafp/apparat/master/docs/screenshots_ui/screenshot_trayicon.png)

*Tray-Icon in Gnome*

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
./apparat.py
```


#### <a name="parameter">Parameter
The following command line parameters are available:

| Parameter     | Alias          | Function            |
| ------------- |:---------------| :-------------------|
| ```-d```      | ```--debug```  | Show debug output   |
| ```-h```      | ```--help```   | Show help           |
| ```-v```      | ```--version```| Show version        |


#### <a name="hotkey">Hotkey
If you want to use a global/system-wide hotkey to trigger ```apparat``` (starting, focusing and minimizing) consider using the script ```apparatHotkeyHelper.sh```. Simply define a system-wide hotkey which triggers ```apparatHotkeyHelper.sh```.

Hotkey definition in [Gnome](https://help.gnome.org/users/gnome-help/stable/keyboard-shortcuts-set.html.en)
* Open the **Activities** overview and start typing Keyboard.
* Click on **Keyboard** to open the panel.
* Select the **Shortcuts** tab.
* Select a category in the left pane, and the row for the desired action (launching ```apparatHotkeyHelper.sh```)  on the right. The current shortcut definition will change to **New accelerator…**
* Hold down the desired key combination, or press Backspace to clear.



## <a name="plugins">Plugins
#### <a name="local-search">Local-Search
| Trigger          | Alias          | Parameter      | Function                      |
|------------------|:---------------|:---------------|:----------------------------- |
| ```?```          |                | _searchstring_ | Filesearch for home directory |


#### <a name="internet-search">Internet-Search
| Trigger          | Alias          | Parameter      | Function       |
|------------------|:---------------|:---------------|:-------------- |
| ```!a```         |                | _searchstring_ | Amazon         |
| ```!b```         |                | _searchstring_ | Bandcamp       |
| ```!e```         |                | _searchstring_ | Stack-Exchange |
| ```!g```         |                | _searchstring_ | Google         |
| ```!l```         |                | _searchstring_ | LastFM         |
| ```!m```         |                | _searchstring_ | Google-Maps    |
| ```!o```         |                | _searchstring_ | Stack-Overflow |
| ```!r```         |                | _searchstring_ | Reddit         |
| ```!s```         |                | _searchstring_ | SoundCloud     |
| ```!t```         |                | _searchstring_ | Twitter        |
| ```!v```         |                | _searchstring_ | Vimeo          |
| ```!w```         |                | _searchstring_ | Wikipedia      |
| ```!y```         |                | _searchstring_ | YouTube        |


#### <a name="nautilus">Nautilus
| Trigger          | Alias          | Parameter      | Function                         |
|------------------|:-------------- |:---------------|:---------------------------------|
| ```!goto```      |                | _path_         | Open directory in nautilus       |
| ```!network```   | ```!net```     |                | Show network devices in nautilus |
| ```!recent```    |                |                | Show recent files in nautilus    |
| ```!trash```     |                |                | Show trash in nautilus           |


#### <a name="session">Session
| Trigger            | Alias          | Parameter      | Function                    |
|--------------------|:-------------- |:---------------|:----------------------------|
| ```!hibernate```   | ```!sleep```   |                | hibernate the machine       |
| ```!lock```        |                |                | locks the current session   |
| ```!logout```      |                |                | logout from current session |
| ```!reboot```      | ```!restart``` |                | reboot the machine          |
| ```!shutdown```    | ```!halt```    |                | shutdown the machine        |
| ```!screensaver``` | ```!saver```   |                | start screensaver           |


#### <a name="screenshot">Screenshot
| Trigger          | Alias              | Parameter      | Function                              |
|------------------|:------------------ |:---------------|:--------------------------------------|
| ```!ss```        |                    |                | Selective screenshot (window or area) |
| ```!fs```        |                    |                | Full screenshot                       |


#### <a name="shell">Shell
| Trigger          | Alias              | Parameter      | Function                            |
|------------------|:------------------ |:---------------|:------------------------------------|
| ```!sh```        |                    | path           | Run terminal commands in new window |


#### <a name="misc">Misc
| Trigger            | Alias              | Parameter      | Function                         |
|--------------------|:------------------ |:---------------|:---------------------------------|
| ```!help```        |                    |                | Open apparat online help         |
| ```!open```        |                    | path           | Open using default application   |
| ```!preferences``` | ```!prefs```       |                | Open apparat preferences         |




## <a name="contributing">Contributing
Please check the [Contribution guidelines for this project](.github/CONTRIBUTING.md)



## <a name="credits">Credits
* Icons
  * [Font Awesome](http://fontawesome.io)
  * [FA2PNG](http://fa2png.io/)
  * Color:
    * Gray: #7f8c8d
    * Red: #b92c0c
    * Green: #269c58


## <a name="license">License
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)

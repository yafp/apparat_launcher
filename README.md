# <a name="top"> apparat-launcher


![logo](https://raw.githubusercontent.com/yafp/apparat-launcher/master/apparat-launcher/gfx/core/128/appIcon.png)

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
    * [Core](#core)
    * [Misc](#misc)
    * [Nautilus](#nautilus)
    * [Screenshot](#screenshot)
    * [Search-Internet](#search-internet)
    * [Search-Local](#search-local)
    * [Session](#session)
    * [Shell](#shell)
  * [Contributing](#contributing)
  * [Credits](#credits)
  * [License](#license)


## <a name="description">Description

__apparat-launcher__ is an application launcher for linux. It is developed and tested for Gnome Desktop environments.


## <a name="screenshots">Screenshots
*Launcher UI*

![screenshot](https://raw.githubusercontent.com/yafp/apparat-launcher/master/docs/screenshots_ui/screenshot_ui.png)


*Tray-Icon (Gnome)*

![screenshot](https://raw.githubusercontent.com/yafp/apparat-launcher/master/docs/screenshots_ui/screenshot_trayicon.png)


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
./apparat-launcher.py
```


#### <a name="parameter">Parameter
The following command line parameters are available:

| Parameter     | Alias          | Function            |
| ------------- |:---------------| :-------------------|
| ```-d```      | ```--debug```  | Show debug output   |
| ```-h```      | ```--help```   | Show help           |
| ```-v```      | ```--version```| Show version        |


#### <a name="hotkey">Hotkey
If you want to use a global/system-wide hotkey to trigger ```apparat-launcher``` (starting, focusing and minimizing) consider using the script ```apparatHotkeyHelper.sh```. Simply define a system-wide hotkey which triggers ```apparatHotkeyHelper.sh```.

Hotkey definition in [Gnome](https://help.gnome.org/users/gnome-help/stable/keyboard-shortcuts-set.html.en)
* Open the **Activities** overview and start typing Keyboard.
* Click on **Keyboard** to open the panel.
* Select the **Shortcuts** tab.
* Select a category in the left pane, and the row for the desired action (launching ```apparatHotkeyHelper.sh```)  on the right. The current shortcut definition will change to **New accelerator…**
* Hold down the desired key combination, or press Backspace to clear.



## <a name="plugins">Plugins
#### <a name="core">Core
| Trigger            | Alias              | Parameter      | Function                                        |
|--------------------|:------------------ |:---------------|:------------------------------------------------|
| ```!help```        |                    |                | Open apparat online documentation               |
| ```!preferences``` | ```!prefs```       |                | Open apparat preferences                        |


#### <a name="misc">Misc
| Trigger            | Alias              | Parameter      | Function                                        |
|--------------------|:------------------ |:---------------|:------------------------------------------------|
| ```!open```        |                    | _path_         | Open file or folder using default application   |


#### <a name="nautilus">Nautilus
| Trigger          | Alias          | Parameter      | Function                         |
|------------------|:-------------- |:---------------|:---------------------------------|
| ```!goto```      |                | _path_         | Open directory in nautilus       |
| ```!network```   | ```!net```     |                | Show network devices in nautilus |
| ```!recent```    |                |                | Show recent files in nautilus    |
| ```!trash```     |                |                | Show trash in nautilus           |


#### <a name="screenshot">Screenshot
| Trigger          | Alias              | Parameter      | Function                              |
|------------------|:------------------ |:---------------|:--------------------------------------|
| ```!ss```        |                    |                | Selective screenshot (window or area) |
| ```!fs```        |                    |                | Full screenshot                       |


#### <a name="search-internet">Search-Internet
| Trigger          | Alias          | Parameter      | Function               |
|------------------|:---------------|:---------------|:---------------------- |
| ```!am```        |                | _searchstring_ | Amazon                 |
| ```!au```        |                | _searchstring_ | Ask Ubuntu             |
| ```!bc```        |                | _searchstring_ | BandCamp               |
| ```!dd```        |                | _searchstring_ | DuckDuckGo             |
| ```!fb```        |                | _searchstring_ | FaceBook               |
| ```!fl```        |                | _searchstring_ | Flickr                 |
| ```!gh```        |                | _searchstring_ | GitHub                 |
| ```!gi```        |                | _searchstring_ | Google Images          |
| ```!gm```        |                | _searchstring_ | Google Maps            |
| ```!gn```        |                | _searchstring_ | Google News            |
| ```!go```        |                | _searchstring_ | Google                 |
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
| Trigger          | Alias          | Parameter      | Function                      |
|------------------|:---------------|:---------------|:----------------------------- |
| ```?```          |                | _searchstring_ | Filesearch for home directory |


#### <a name="session">Session
| Trigger            | Alias          | Parameter      | Function                    |
|--------------------|:-------------- |:---------------|:----------------------------|
| ```!hibernate```   | ```!sleep```   |                | hibernate the machine       |
| ```!lock```        |                |                | locks the current session   |
| ```!logout```      |                |                | logout from current session |
| ```!reboot```      | ```!restart``` |                | reboot the machine          |
| ```!shutdown```    | ```!halt```    |                | shutdown the machine        |
| ```!screensaver``` | ```!saver```   |                | start screensaver           |


#### <a name="shell">Shell
| Trigger          | Alias              | Parameter      | Function                            |
|------------------|:------------------ |:---------------|:------------------------------------|
| ```!sh```        |                    | _path_         | Run terminal commands in new window |



## <a name="contributing">Contributing
Please check the [Contribution guidelines for this project](CONTRIBUTING.md)



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

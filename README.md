[![Code Health](https://landscape.io/github/yafp/apparat/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/apparat/master)

apparat
==========

![logo](https://raw.githubusercontent.com/yafp/apparat/master/src/gfx/core/bt_appIcon_128.png)


## Table of Contents

  * [Description](#description)
  * [Screenshot](#Screenshot)
  * [Installation](#Installation)
    * [Requirements](#Requirements)
  * [Usage](#Usage)
    * [Parameter](#Parameter)
    * [Hotkey](#Hotkey)
  * [Plugins](#Plugins)
  * [Contributing](#Contributing)
  * [Credits](#Credits)
  * [License](#License)


## <a name="description">Description

__apparat__ is an application launcher for linux. It is developed and tested for Gnome Desktop environments.


## Screenshot
![screenshot](https://raw.githubusercontent.com/yafp/apparat/master/docs/screenshot_ui.png)


## Installation
There is no installation routine so far

#### Requirements
- python2
- python-wxtools
- gtk

## Usage
Simply run:
```
./apparat.py
```


#### Parameter
The following command line parameters are available:

| Parameter     | Alias          | Function            |
| ------------- |:---------------| :-------------------|
| ```-d```      | ```--debug```  | Show debug output   |
| ```-h```      | ```--help```   | Show help           |
| ```-v```      | ```--version```| Show version        |


#### Hotkey
If you want to use a global hotkey to trigger ```apparat``` consider using ```apparatHotkeyHelper.sh```. Define a system-wide hotkey which triggers ```apparatHotkeyHelper.sh```.

Gnome:
* Open the Activities overview and start typing Keyboard.
* Click on Keyboard to open the panel.
* Select the Shortcuts tab.
* Select a category in the left pane, and the row for the desired action (launching ```apparatHotkeyHelper.sh```)  on the right. The current shortcut definition will change to New accelerator…
* Hold down the desired key combination, or press Backspace to clear.

More details about [global hotkeys in Gnome](https://help.gnome.org/users/gnome-help/stable/keyboard-shortcuts-set.html.en).

## Plugins
#### Search local
| Trigger          | Alias         | Parameter      | Function                      |
| ---------------- |:--------------| :--------------|:----------------------------- |
| ```?```          |               | searchstring   | Filesearch for home directory |

#### Internet Search
| Trigger          | Alias         | Parameter      | Function       |
| ---------------- |:--------------| :--------------|:-------------- |
| ```!a```         |               | _searchstring_ | Amazon         |
| ```!b```         |               | _searchstring_ | Bandcamp       |
| ```!e```         |               | _searchstring_ | Stack-Exchange |
| ```!g```         |               | _searchstring_ | Google         |
| ```!l```         |               | _searchstring_ | LastFM         |
| ```!m```         |               | _searchstring_ | Google-Maps    |
| ```!o```         |               | _searchstring_ | Stack-Overflow |
| ```!r```         |               | _searchstring_ | Reddit         |
| ```!s```         |               | _searchstring_ | SoundCloud     |
| ```!t```         |               | _searchstring_ | Twitter        |
| ```!v```         |               | _searchstring_ | Vimeo          |
| ```!w```         |               | _searchstring_ | Wikipedia      |
| ```!y```         |               | _searchstring_ | YouTube        |


#### Nautilus
| Trigger          | Alias          | Parameter           | Function                         |
| ---------------- |:-------------- | :-------------------|:---------------------------------|
| ```!goto```      |                | _path_              | Open directory in nautilus       |
| ```!network```   | ```!net```     |                     | Show network devices in nautilus |
| ```!recent```    |                |                     | Show recent files in nautilus    |
| ```!trash```     |                |                     | Show trash in nautilus           |


#### Session
| Trigger          | Alias          | Function                    |
| ---------------- |:-------------- | :---------------------------|
| ```!hibernate``` | ```!sleep```   | hibernate the machine       |
| ```!lock```      |                | locks the current session   |
| ```!logout```    |                | logout from current session |
| ```!reboot```    | ```!restart``` | reboot the machine          |
| ```!shutdown```  | ```!halt```    | shutdown the machine        |


#### Misc
| Trigger          | Alias          | Parameter           | Function                         |
| ---------------- |:-------------- | :-------------------|:---------------------------------|
| ```!open```      |                | path                | Open using default application   |


## Contributing
Please check the [Contribution guidelines for this project](.github/CONTRIBUTING.md)


## Credits
* Icons via [Font Awesome](http://fontawesome.io) (Color: #7f8c8d)

## License
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)

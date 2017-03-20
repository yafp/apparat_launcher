[![Code Health](https://landscape.io/github/yafp/apparat/master/landscape.svg?style=flat)](https://landscape.io/github/yafp/apparat/master)
[![License](https://img.shields.io/badge/license-GPL3-brightgreen.svg)](LICENSE)


![logo](https://raw.githubusercontent.com/yafp/apparat/master/src/gfx/core/bt_appIcon_128.png)
apparat
==========

## About
apparat is an application launcher for linux


## Requirements
- python2
- python-wxtools
- gtk

## Parameter
The following command line parameters are available:

| Parameter     | Alias          | Function            |
| ------------- |:---------------| :-------------------|
| ```-d```      | ```--debug```  | Show debug output   |
| ```-h```      | ```--help```   | Show help           |
| ```-v```      | ```--version```| Show version        |


## Plugins
### Internet-Search

Usage:
```trigger + SPACE + searchphrase```

| Trigger       | Alias         | Function       |
| ------------- |:--------------| :--------------|
| ```!a```      |               | Amazon         |
| ```!b```      |               | Bandcamp       |
| ```!e```      |               | Stack-Exchange |
| ```!g```      |               | Google         |
| ```!l```      |               | LastFM         |
| ```!m```      |               | Google-Maps    |
| ```!o```      |               | Stack-Overflow |
| ```!r```      |               | Reddit         |
| ```!s```      |               | SoundCloud     |
| ```!t```      |               | Twitter        |
| ```!v```      |               | Vimeo          |
| ```!w```      |               | Wikipedia      |
| ```!y```      |               | YouTube        |


### Nautilus

| Trigger       | Alias          | Function                     |
| ------------- |:-------------- | :----------------------------|
| ```!recent``` |                | Opens trash in nautilus      |
| ```!trash```  |                | Show recent files in nautilus|


### Session

| Trigger          | Alias          | Function                    |
| ---------------- |:-------------- | :---------------------------|
| ```!hibernate``` | ```!sleep```   | hibernate the machine       |
| ```!lock```      |                | locks the current session   |
| ```!logout```    |                | logout from current session |
| ```!reboot```    | ```!restart``` | reboot the machine          |
| ```!shutdown```  | ```!halt```    | shutdown the machine        |


## Development
Please check the [Contribution guidelines for this project](.github/CONTRIBUTING.md)


## Credits
* All icons used in Apparat are from [Font Awesome](http://fontawesome.io) - Color: #7f8c8d


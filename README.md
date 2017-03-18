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

| Parameter     | Alias          | Function            |
| ------------- |:---------------| :-------------------|
| ```-d```      | ```--debug```  | Show debug output   |
| ```-h```      | ```--help```   | Show help           |
| ```-v```      | ```--version```| Show version        |

## Plugins
### Internet-Search

Usage:
```trigger + SPACE + searchphrase```

| Trigger       | Alias         | Function   |
| ------------- |:--------------| :----------|
| ```!a```      |               | Amazon     |
| ```!b```      |               | Bandcamp   |
| ```!e```      |               | Exchange   |
| ```!g```      |               | Google     |
| ```!l```      |               | LastFM     |
| ```!o```      |               | Overflow   |
| ```!r```      |               | Reddit     |
| ```!s```      |               | SoundCloud |
| ```!t```      |               | Twitter    |
| ```!v```      |               | Vimeo      |
| ```!w```      |               | Wikipedia  |
| ```!y```      |               | YouTube    |


### Session

| Trigger          | Alias          | Function                    |
| ---------------- |:-------------- | :---------------------------|
| ```!hibernate``` | ```!sleep```   | hibernate the machine       |
| ```!lock```      |                | locks the current session   |
| ```!logout```    |                | logout from current session |
| ```!reboot```    | ```!restart``` | reboot the machine          |
| ```!shutdown```  |                | shutdown the machine        |


## Development
Please check the [Contribution guidelines for this project](.github/CONTRIBUTING.md)

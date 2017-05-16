#!/usr/bin/python
"""test - an application launcher for linux"""

# NAME:         test
# DESCRIPTION:  an application launcher for linux
# AUTHOR:       yafp
# URL:          https://github.com/yafp/apparat



import dbus

## A list of available DBus services
#
print('\n\nSYSTEMBUS')
for service in dbus.SystemBus().list_names():
    print(service)

print('\n\nSESSIONBUS')
for service in dbus.SessionBus().list_names():
    print(service)



## playing with dbus
#
session_bus = dbus.SessionBus()
system_bus = dbus.SystemBus()


## example 1
#proxy = system_bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager/Devices/eth0') # proxy is a dbus.proxies.ProxyObject
#print(proxy)


## example 2
#eth0 = system_bus.get_object('org.freedesktop.NetworkManager','/org/freedesktop/NetworkManager/Devices/eth0')
#props = eth0.getProperties(dbus_interface='org.freedesktop.NetworkManager.Devices') # props is a tuple of properties, the first of which is the object path
#print(props)



bus = dbus.SessionBus()
dbus_proxy = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
names = dbus_proxy.ListNames()
for name in names:
    if name.startswith(':'):
        try:
            proxy = bus.get_object(name, '/')
            ident_method = proxy.get_dbus_method("Identity", dbus_interface="org.freedesktop.MediaPlayer")

            print ident_method()

        except dbus.exceptions.DBusException:
            pass




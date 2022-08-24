# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 00:19:12 2022

@author: javapak
"""
from pyWinCoreAudio import (
    ON_DEVICE_ADDED,
    ON_DEVICE_REMOVED,
    ON_ENDPOINT_VOLUME_CHANGED,
    ON_ENDPOINT_DEFAULT_CHANGED,
    ON_SESSION_CREATED,
    ON_SESSION_NAME_CHANGED,
    ON_SESSION_GROUPING_CHANGED,
    ON_SESSION_ICON_CHANGED,
    ON_SESSION_DISCONNECT,
    ON_SESSION_VOLUME_CHANGED,
)

import tkinter as tk
from tkinter import ttk
import sv_ttk
from model import DevicesModel
from view import View
from PIL import Image
from pyWinCoreAudio import utils as utils
import codecs 
from PyQt6.QtWidgets import QApplication
import sys


class Controller(object):
    model = DevicesModel()
    view = View(tk.Tk())
    
    def instantiate_endpoints(self): #testing purposes currently...
        self.provide_icons()
        device_and_sessions_dict = self.provide_endpoints_and_sessions()
        i = 0
        for key in device_and_sessions_dict.keys():
            print()
            for value in device_and_sessions_dict.values():
                if i < len(self.view.icons):
                    self.view.session_slider_and_image(i, value[0])
                    i += 1
             
                
    
    
    def run(self):
        self.instantiate_endpoints()
        self.view.pack()
        self.view.mainloop()

        
#Implementation of IMMNotificationClient and IAudioSessionEvents per the Microsoft docs. Need to make sure to unregister on close of the application or problems may arise. Glad I found this library. Much more robust and complete bindings and less confusing than Rust or C# bindings.
    def on_device_added(signal, device):
        print('Device added:', device.name)


    _on_device_added = ON_DEVICE_ADDED.register(on_device_added) #method from library to register event callback methods.


    def on_device_removed(signal, name):
        print('Device removed:', name)


    _on_device_removed = ON_DEVICE_REMOVED.register(on_device_removed)

  
    def on_endpoint_volume_changed(signal, device, endpoint, is_muted, master_volume,  channel_volumes):
        print('Endpoint volume changed:', device.name + '.' + endpoint.name)
        print('mute:', is_muted)
        print('volume:', master_volume)
        for i, channel in enumerate(channel_volumes):
            print('channel:', i)
            print('volume:', channel)


    _on_endpoint_volume_changed = ON_ENDPOINT_VOLUME_CHANGED.register(on_endpoint_volume_changed)


    def on_endpoint_default_changed(signal, device, endpoint, role, flow):
        print('Default changed:', device.name + '.' + endpoint.name, 'role:', role, 'flow:', flow)


    _on_endpoint_default_changed = ON_ENDPOINT_DEFAULT_CHANGED.register(on_endpoint_default_changed)



    def on_session_created(signal, device, endpoint, session):
        print('Session created:', device.name + '.' + endpoint.name + '.' + session.name)


    _on_session_created = ON_SESSION_CREATED.register(on_session_created)


    def on_session_name_changed(signal, device, endpoint, session, old_name, new_name):
        print('Session name changed:', device.name + '.' + endpoint.name + '.' + old_name, new_name)


    _on_session_name_changed = ON_SESSION_NAME_CHANGED.register(on_session_name_changed)


    def on_session_grouping_changed(signal, device, endpoint, session, new_grouping_param):
        print('Session grouping changed:', device.name + '.' + endpoint.name + '.' + session.name, new_grouping_param)


    _on_session_grouping_changed = ON_SESSION_GROUPING_CHANGED.register(on_session_grouping_changed)


    def on_session_icon_changed(signal, device, endpoint, session, old_icon, new_icon):
        print('Session icon changed:', device.name + '.' + endpoint.name + '.' + session.name, 'old:', old_icon, 'new:', new_icon)


    _on_session_icon_changed = ON_SESSION_ICON_CHANGED.register(on_session_icon_changed)


    def on_session_disconnect(signal, device, endpoint, name, reason):
        print('Session disconnected:', device.name + '.' + endpoint.name + '.' + name, reason)


    _on_session_disconnect = ON_SESSION_DISCONNECT.register(on_session_disconnect)


    def on_session_volume_changed(signal, device, endpoint, session, new_volume, new_mute):
        print('Session volume changed:', device.name + '.' + endpoint.name + '.' + session.name, 'volume:', new_volume, 'mute:', new_mute)
        if new_volume <= 15.0:
            print('setting session volume', session.volume.level)
            session.volume.level = 50.0
            print('new session volume =', session.volume.level)


    _on_session_volume_changed = ON_SESSION_VOLUME_CHANGED.register(on_session_volume_changed)


    def provide_endpoints_and_sessions(self): #indirectly provide model data to the view, do not want to directly expose model to the view. 
        return self.model.sessions_info_dev_name_dict()
    
    def provide_icons(self):
        self.view.icons = self.model.icons
Controller().run()
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 00:19:12 2022

@author: javapak
"""
from importlib.resources import path
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
    ON_DEVICE_PROPERTY_CHANGED
)
from model import DevicesModel
from view import View
from eqview import EqualizerView
from pyWinCoreAudio import utils as utils
from PySide6 import QtWidgets
import sys
import json
import os
from threading import Thread

class Controller():

    def __init__(self):
        self.model = DevicesModel()
        self.app = QtWidgets.QApplication(sys.argv) 
        self.view = View()
        self.config_header = "Include: example.txt\nPreamp: -6.2dB\nGraphicEQ: "
        if not os.path.exists("/config/config.json"):
            self.bandfrequencies = ["25 0; ", "40 0; ", "63 0; ", "100 0; ", "160 0; ", "250 0; ", "400 0; ", "630 0; ", "1000 0; ", "1600 0; ", "2500 0; ", "4000 0; ", "6300 0; ", "10000 0; ", "16000 0; "]
        self.eq_view = EqualizerView()      

    def toJSON(self):
        return json.dumps(self, default=lambda self: self.__dict__, 
            sort_keys=True, indent=4)      
            
    def setBand(self, i, val):
        valstring = self.bandfrequencies[i]
        valstring = valstring.split(' ')
        valstring = valstring[0]
        split_done = valstring + " " + str(val) + "; "
        self.bandfrequencies[i] = split_done
        config = ''.join(self.bandfrequencies)
        config_w_head = self.config_header + config 
        print(split_done)
        with open(self.model.equalizer_apo.strip('"'), 'w') as f:
            f.seek(0)
            f.truncate()
            f.write(config_w_head)



    def instantiate_endpoints(self): #testing purposes currently...
        self.provide_icons() 
        endpoint_dict = self.model.endpoint_sess_obj()
        
        for endpoint in endpoint_dict.values():
            i = 0
            print(endpoint.sessions)
            self.view.endpoint_view(endpoint.endpoint_ref.name, endpoint.endpoint_ref.id, endpoint.endpoint_ref.volume.level, self.all_purpose_control_thread_end)

            for sess in endpoint.sessions.values():
                self.view.session_slider_view(sess.name, sess.endpoint.id, sess.id, sess.volume.level, self.all_purpose_control_thread_sess, self.model.mute)
                i += 1

                                           
    def run(self): 
        self.model.equalizer_apo = self.view.if_equalizer_apo(self.show_eq)
        self.eq_view.slider_view(self.bandfrequencies, self.setBand)
        self.instantiate_endpoints()
        print(self.model.equalizer_apo)
        self.view.snap_to_br()
        self.view.show()
        self.app.exec()

    def show_eq(self):
        self.eq_view.connect(self.setBand)
        self.eq_view.snap_to_br()
        self.eq_view.show()


    def all_purpose_control_thread_end(self, id, val):
        self.model.change_vol_end(id, val)

    def provide_endpoints_and_sessions(self): #indirectly provide model data to the view, do not want to directly expose model to the view. 
        return self.model.sessions_info_dev_name_dict()
            
    def all_purpose_control_thread_sess(self, endpoint_id, id, val):
        self.model.change_vol_sess(endpoint_id, id, val)
       

    def provide_icons(self):
        self.view.icons = self.model.icons
    


        


controller = Controller()

#Implementation of IMMNotificationClient and IAudioSessionEvents per the Microsoft docs. Need to make sure to unregister on close of the application or problems may arise. 
def on_device_added(signal, device):
    print('Device added:', device.name)

    
_on_device_added = ON_DEVICE_ADDED.register(on_device_added) #method from library to register event callback methods. same follows down the lines for other on some condition....event driven, reactive UI and model.


def on_device_removed(signal, name):
    print('Device removed:', name)


_on_device_removed = ON_DEVICE_REMOVED.register(on_device_removed)


def on_device_property_changed(signal, device, key, endpoint=None):
        if endpoint is not None:
            print('Property changed:', device.name + '.' + endpoint.name, key)

        else:
            print('Property changed:', device.name, key)
    
_on_device_property_changed = ON_DEVICE_PROPERTY_CHANGED.register(on_device_property_changed)

   
def on_endpoint_volume_changed(signal, device, endpoint, is_muted, master_volume,  channel_volumes):
    print('Endpoint volume changed:', device.name + '.' + endpoint.name)
    print('mute:', is_muted)
    print('volume:', master_volume)
    for i, channel in enumerate(channel_volumes):
        print('channel:', i)
        print('volume:', channel)

    
ON_ENDPOINT_VOLUME_CHANGED.register(on_endpoint_volume_changed)


def on_endpoint_default_changed(signal, device, endpoint, role, flow):
    print('Default changed:', device.name + '.' + endpoint.name, 'role:', role, 'flow:', flow)

    
ON_ENDPOINT_DEFAULT_CHANGED.register(on_endpoint_default_changed)



def on_session_created(signal, device, endpoint, session): 
    controller.model.process_paths_to_icons(session.process_id, session.name)
    controller.provide_icons()
    controller.view.on_session_create_show(session.name, endpoint.id, session.id, session.volume.level, controller.model.change_vol_sess, controller.model.mute)
    controller.view.update()

    
ON_SESSION_CREATED.register(on_session_created)


def on_session_name_changed(signal, device, endpoint, session, old_name, new_name):
    print('Session name changed:', device.name + '.' + endpoint.name + '.' + old_name, new_name)

    
ON_SESSION_NAME_CHANGED.register(on_session_name_changed)


def on_session_grouping_changed(signal, device, endpoint, session, new_grouping_param):
    print('Session grouping changed:', device.name + '.' + endpoint.name + '.' + session.name, new_grouping_param)

    
ON_SESSION_GROUPING_CHANGED.register(on_session_grouping_changed)


def on_session_icon_changed(signal, device, endpoint, session, old_icon, new_icon):
    print('Session icon changed:', device.name + '.' + endpoint.name + '.' + session.name, 'old:', old_icon, 'new:', new_icon)

ON_SESSION_ICON_CHANGED.register(on_session_icon_changed)

def on_session_disconnect(signal, device, endpoint, name, reason):
    print('Session disconnected:', device.name + '.' + endpoint.name + '.' + name, reason)

    
ON_SESSION_DISCONNECT.register(on_session_disconnect)

def on_session_volume_changed(signal, device, endpoint, session, new_volume, new_mute):
    print('Session volume changed:', device.name + '.' + endpoint.name + '.' + session.name, 'volume:', new_volume, 'mute:', new_mute)


ON_SESSION_VOLUME_CHANGED.register(on_session_volume_changed)


controller.run()



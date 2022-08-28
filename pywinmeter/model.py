from ctypes.wintypes import LONG
import pyWinCoreAudio
import os
from pyWinCoreAudio.mmdeviceapi import EDataFlow as data_flow
from pyWinCoreAudio.mmdeviceapi import DEVICE_STATE_ACTIVE as state_active
import win32gui
import psutil
import win32ui
import win32con
import win32api
import PySide6
from PIL import Image, ImageQt
from copy import deepcopy


class EndPoint(object):

    def __init__(self, name, id):
        self.name_id_list = [name, id]
        self.sessions = []
    
    def name(self, name):
        self.name = name
  

    def add_sess(self, session_name, session_id):
        self.sessions.append((session_name, session_id))


    

class DevicesModel(object):
    devices = pyWinCoreAudio.devices(False)
    sr = os.getenv('SystemRoot') + "\\System32\\AudioSrv.Dll"
    icons = {}
    endpoint_list = []
    #Create a new class for endpoint session relationship - make my life easier. Go to sleep...
    #After thinking about, dictionary is not necessary for this, and seems to cause more problems than practicalality/utility...
    def endpoint_sess_obj(self): #A method to map an endpoint name as key to for sessions belonging to the endpoint to establish relationship.
        for device in self.devices(): #Yes, I do know what itertools is...make your case for why you think it would be more readable and I will change it. I don't think it will provide any performance gains in this case because people usually don't have a crazy amount of audio devices, endpoints, and sessions open..
                for endpoint in device:
                    if endpoint.data_flow == data_flow().eRender and endpoint.state == state_active:
                        endpoint_wrap = EndPoint(endpoint.name, endpoint.id)
                        self.endpoint_list.append(endpoint_wrap)
                        for session in endpoint:
                                self.endpoint_list[-1].add_sess(session.name, session.id)
                                self.process_paths_to_icons(session.process_id, session.name)
                            
        
        return self.endpoint_list


    def change_vol_end(self, endpoint_id, vol):
        for device in self.devices():
            for endpoint in device:
                if endpoint.id == endpoint_id:
                    endpoint.volume.level = vol 
                    break
    
    def change_vol_sess(self, session_id, vol): 
        for device in self.devices():
            for endpoint in device:
                if endpoint.data_flow == data_flow().eRender and endpoint.state == state_active:
                    for session in endpoint:
                        if session.id == session_id:
                            session.volume.level = vol 
                            break
    
    def change_bass_end(self, endpoint_id, level): 
        for device in self.devices():
            for endpoint in device:
                if endpoint.id == endpoint_id:
                    endpoint.bass = level
                    break
    
    def change_mid_end(self, endpoint_id, level): 
        for device in self.devices():
            for endpoint in device:
                if endpoint.id == endpoint_id:
                    endpoint.mid = level 
                    break
    
    
    def change_treble_end(self, endpoint_id, level): 
        for device in self.devices():
            for endpoint in device:
                if endpoint.id == endpoint_id:
                    endpoint.treble = level
    
                    break

        
    

    
    def process_paths_to_icons(self, pid, name):
            if pid != 0:
                path = psutil.Process(pid).exe()
            else:
                path = self.sr
           
            ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
            large, small = win32gui.ExtractIconEx(path,0)
            if small:
                win32gui.DestroyIcon(small[0])

            if large:
                hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_y )
                hdc = hdc.CreateCompatibleDC()
                hdc.SelectObject(hbmp)
                bmpinfo = hbmp.GetInfo()
                win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, large[0], ico_x, ico_y, 0, None, 0x0003)
                bmpstr = hbmp.GetBitmapBits(True)
                img = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'RGBA', 0, 1)
                ico = ImageQt.ImageQt(img)
                self.icons[name] = ico
            else:
                return 'No icon found'
#
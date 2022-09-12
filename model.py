from ctypes.wintypes import LONG
import pyWinCoreAudio
import os
from pyWinCoreAudio.mmdeviceapi import EDataFlow as data_flow
from pyWinCoreAudio.mmdeviceapi import DEVICE_STATE_ACTIVE as state_active
import win32con
import win32ui
import win32gui
import psutil
from PIL import Image, ImageQt




class EndPoint(object):

    def __init__(self, endpoint):
        self.endpoint_ref = endpoint
        self.sessions = {}
    
    def name(self, endpoint):
        self.endpoint_ref = endpoint
  

    def add_sess(self, session):
        self.sessions[session.id] = session


    

class DevicesModel(object):
    devices = pyWinCoreAudio.devices(False)
    sr = os.getenv('SystemRoot') + "\\System32\\AudioSrv.Dll"
    icons = {}
    endpoint_dict = {}
    equalizer_apo = None
    #Library says holding references to the endpoints, sessions, etc. is bad, but I think that as long as we make sure to delete them on program exit, this should be fine. Open an issue if you see memory leaks, please and thank you. 
    def endpoint_sess_obj(self): 
        for device in self.devices(): 
                for endpoint in device:
                    if endpoint.data_flow == data_flow().eRender and endpoint.state == state_active:
                        endpoint_wrap = EndPoint(endpoint)
                        self.endpoint_dict[endpoint.id] = endpoint_wrap
                        for session in endpoint:
                                list(self.endpoint_dict.values())[-1].add_sess(session)
                                self.process_paths_to_icons(session.process_id, session.name)
                            
        
        return self.endpoint_dict
    
    def change_vol_end(self, endpoint_id, vol):
        self.endpoint_dict.get(endpoint_id).endpoint_ref.volume.level = vol
    
    def change_vol_sess(self, endpoint_id, session_id, vol): 
        self.endpoint_dict.get(endpoint_id).sessions.get(session_id).volume.level = vol
    
    def mute(self, sessid, endid):
        if self.endpoint_dict.get(endid).sessions.get(sessid).volume.level != 0:
            self.endpoint_dict.get(endid).sessions.get(sessid).volume.level = 0
        else:
            self.endpoint_dict.get(endid).sessions.get(sessid).volume.level = 100
    
    def process_paths_to_icons(self, pid, name):
            if pid != 0:
                path = psutil.Process(pid).exe()
            else:
                path = self.sr
           
            ico_x = 32
            ico_y = 32
            large, small = win32gui.ExtractIconEx(path,0)
            if small:
                for icon in small:
                    win32gui.DestroyIcon(icon)

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
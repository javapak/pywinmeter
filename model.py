import pyWinCoreAudio
import os
from pyWinCoreAudio.mmdeviceapi import EDataFlow as data_flow
import win32gui
import psutil
import win32ui
import win32con
import win32api
from PIL import Image

class DevicesModel(object):
    devices = pyWinCoreAudio.devices()
    session_endpoint_id_dict = {}
    sr = os.getenv('SystemRoot') + "\\System32\\AudioSrv.Dll"
    icons = []

 
    def sessions_info_dev_name_dict(self): #A method to map an endpoint name as key to for sessions belonging to the endpoint to establish relationship.
        for device in self.devices(): #Yes, i do know what itertools is...make your case for why you think it would be more readable and I will change it. I don't think it will provide any performance gains in this case because people usually don't have a crazy amount of audio devices, endpoints, and sessions open..
            for endpoint in device:
                for session in endpoint:
                    if endpoint.data_flow == data_flow().eRender: #EDataFlow value of 0 indicates a rendering device (ex - speakers, etc.) - might as well use the library enums..
                        self.session_endpoint_id_dict[endpoint.name] = [session.name, session.id]
                        self.process_paths_to_icons(session.process_id)
                        print(session.name)
        return self.session_endpoint_id_dict

    
    def process_paths_to_icons(self, pid):
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
                hbmp.SaveBitmapFile( hdc, 'icon.bmp')  
                bmpinfo = hbmp.GetInfo()
                win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, large[0], ico_x, ico_y, 0, None, 0x0003)
                bmpstr = hbmp.GetBitmapBits(True)
                img = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'RGBA', 0, 1)
                self.icons.append(img)
            else:
                return 'No icon found'
#
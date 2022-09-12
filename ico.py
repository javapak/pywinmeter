import ctypes
from ctypes import POINTER
CHAR = ctypes.c_char
STRING = ctypes.c_char_p
WSTRING = ctypes.c_wchar_p
WCHAR = ctypes.c_wchar
INT = ctypes.c_int

LPCWSTR = POINTER(WCHAR)
LPCSTR = ctypes.c_char_p
LPWSTR = POINTER(WCHAR)
LPSTR = POINTER(CHAR)

def get_large_icons(path):
    lpsz_file = LPCSTR(path)
    large, small = ctypes.windll.shell32.ExtractIconExA(lpsz_file, 0)
    if small.contents:
        for ico in small:
            ctypes.windll.winuser.DestroyIcon(ico.value)
    
    if large.contents:
        srcdc = ctypes.windll.user32.GetWindowDC(0)
        memdc = ctypes.windll.gdi32.CreateCompatibleDC(srcdc)
        bmp = ctypes.windll.gdi32.CreateCompatibleBitmap(srcdc, 32, 32)
        ctypes.windll.gdi32.SelectObject(memdc, bmp)
        ctypes.windll.winuser.DrawIconEx()
            

        

        
    
# tools/xprintidle_win.py

import ctypes
import time

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]

def get_idle_duration_ms():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis
    return 0

if __name__ == "__main__":
    idle_ms = get_idle_duration_ms()
    print(idle_ms)  # prints how long the system has been idle in ms

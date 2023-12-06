from win32 import win32api, win32gui, win32print
from win32.lib import win32con

def get_screen_size():
    # Get the resolution after Scale
    w = win32api.GetSystemMetrics (0)
    h = win32api.GetSystemMetrics (1)
    
    print(f'The resolution after scale is {w}x{h}')
    return (w, h)

def get_real_resolution():
    """
    Get the real resolution of the screen
    """
    hDC = win32gui.GetDC(0)
    rw = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    rh = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    
    print(f'The real resolution is {rw}x{rh}')
    return (rw, rh)

def get_scale_rate():
    """
    Used to check the current scrren scale rate and they change working director to specific folder which contains the pics
    """
    Screen_size = get_screen_size()
    Real_resolution = get_real_resolution()
    Scale_rate = round(Real_resolution[0] / Screen_size[0] , 2) * 100
    
    print(f'the Scale Rate is {Scale_rate}%')
    return Scale_rate

if __name__ == '__main__':
    get_scale_rate()
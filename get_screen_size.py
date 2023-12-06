# coding: utf-8
# author: peanutfish
import ctypes
import os

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

def get_screen_size(dpi=False):
    """
    Get the resolution after scaling
    """
    if dpi:
        user32.SetProcessDPIAware()
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    print(f'The Resolution is {width}x{height}')
    return (width, height)

def get_scale_rate():
    scale_size = get_screen_size()
    real_size = get_screen_size(True)
    scale_rate = round(real_size[0] / scale_size[0], 2) * 100
    print(f'Current scale rate is {scale_rate}%')
    return str(scale_rate)

def write_config(file, mode):
    with open(file, mode) as f:
            f.write('scale_rate: '+scale_rate)
            print('scale rate is stored in config file')

if __name__ == '__main__':
    scale_rate = get_scale_rate()
    if not os.path.exists('config.ini'):
        write_config('config.ini', 'w')
    
    with open('config.ini', 'r') as f:
        line = f.readline()
        #print(line)
        recorded_scale_rate = line.split(":", 1)[1].strip()
        #print(recorded_scale_rate, scale_rate)
        if recorded_scale_rate != scale_rate:
            write_config('config.ini', 'w')
        else:
            print('Good:), continue...')


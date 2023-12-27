# coding: utf-8
# author: peanutfish
import ctypes
import os

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

config_dict = {}

def get_screen_size(dpi=False):
    """
    Get the resolution after scaling
    """
    # check if dpi flag is set, if so then will get real resolution
    if dpi:
        user32.SetProcessDPIAware()
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    print(f'The Resolution is {width}x{height}')
    
    return (width, height)

def get_scale_rate():
    """
    Calculate the scale rate by using just the width
    """
    scale_size = get_screen_size()
    real_size = get_screen_size(True)
    scale_rate = int((real_size[0] / scale_size[0]) * 100)
    print(f'Current scale rate is {scale_rate}%')
    
    return str(scale_rate)

def write_config(filename, mode, description, value):
    with open(filename, mode) as f:    
        f.write(description + ':' + value)
        f.write('\n')
        print(f'New {description} is stored in config file')

def read_config(filename):
    """
    Read all lins in the config file and change format to dict
    """
    with open(filename, 'r') as f:
        for each_line in f:
            desc, value = each_line.split(':', 1)
            config_dict[desc.strip()] = value.strip()
    print(config_dict)
    return config_dict

def compare_config(dict, description, value):
    if dict[description] == value:
        print(f'{description} is loaded :), continue...')
        return True
    else:
        return False
        

if __name__ == '__main__':
    scale_rate = get_scale_rate()
    if not os.path.exists('config.ini'):
        write_config('config.ini', 'w', 'Scale_Rate', scale_rate)
    
    config_dict = read_config('config.ini')
    
    if not compare_config(config_dict, 'Scale_Rate', scale_rate):
        write_config('config.ini', 'r+', 'Scale_Rate', scale_rate)
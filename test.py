import pyautogui as pg
import time
import os


NT_PASSWD = 'Ballball17'
RSA_PASSWD = '10538185'

def click_center(png, x_offset=0, y_offset=0, showed=True):
    """
    Used to click the center of a picture and also provide following function:
    1. Use x_offset,y_offset to click somewhere around center position,
    2. Use "showed" flag to mark if need to wait for the ICON/PROMPT showup before click it.
    3. Return the center position(x,y).
    """
    try:
        # Use to records how long we are waiting for prompt/icon showup
        number = 0
        # first check if need to wait ICON/PROMPT showup
        # if ICON/PROMPT is there then get its position
        if showed:
            x1, y1 = pg.locateCenterOnScreen(png)
        else:
            # if ICON/PROMPT is not there then waiting it showup
            while (not showed):
                showed = pg.locateCenterOnScreen(png)
                number += 1
                print(f'Waiting {png} for {number} times')
                # in case we wait too much time
                if number > 50:
                    print('Loging process could be hung, clearing unknown status...')
                    clear_status()
            x1, y1 = showed[0], showed[1]
 
        # click the center position or somewhere around it
        pg.click(x1+x_offset, y1+y_offset, button='left')
        # return back center position
        print(f'{png} position({x1},{y1})')
        return (x1, y1)
    except Exception as e:
        print(f'Cannot find {png} in your Screen.')


def get_rsa(token):
    """
    Get RSA Credential
    """
    # Click RSA icon to show RSA main window
    click_center('RSA_icon1.png')
    click_center('RSA_icon2.png')
    pg.moveRel(0,-200)    
    
    # Check if the RSA passcode is already being inputed, if not then get a new one
    if not click_center('RSA_copy.png'):
        click_center('RSA_main.png', 0, 0, showed=False)
        pg.typewrite(token)
        pg.press('enter')
        time.sleep(1)
        # click copy button
        click_center('RSA_copy.png')

    # Change focus to browser window in case RSA window cover it
    pg.hotkey('alt', 'tab')

def choose_GP():
    # check if no-split is connected
    click_center('GP_blue.png', 0, 0, showed=False)
    if (not pg.locateOnScreen('GP_nosplit.png')):
        print('changing gateway')
        # click the "Change Gateway"
        click_center('GW_change.png', showed=False)
        if pg.locateOnScreen('GP_choose.png'):
            pg.press('tab')
        pg.typewrite('no')
        pg.press('tab')
        pg.press('enter')

        
os.chdir(os.path.join(os.getcwd(),'150'))
#print(pg.locateCenterOnScreen('RSA_main.png'))

get_rsa(RSA_PASSWD)
#choose_GP()

# import ctypes
# user32 = ctypes.windll.user32
# user32.GetDC(0)
# height = user32.GetSystemMetrics(0)
# width = user32.GetSystemMetrics(1)

# print("DPI:", height, 'x', width)

# from win32 import win32api, win32gui, win32print
# from win32.lib import win32con

# # 获得真实分辨率
# w = win32api.GetSystemMetrics(0)
# h = win32api.GetSystemMetrics(1)
# #print(f'当前分辨率为 {w}x{h}')

# # 获取缩放后的分辨率
# hDC = win32gui.GetDC(0)
# w1 = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
# h1 = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
# #print(f'缩放后的分辨率为 {w1}x{h1}')

# # 缩放比例
# scale_rate = round(w / w1, 2) * 100
# #print(f'缩放率为{scale_rate}')
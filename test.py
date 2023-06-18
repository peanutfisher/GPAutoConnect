import pyautogui as pg
import time
import os

a = pg.locateCenterOnScreen('./GP_disconnect.png')
print(a)

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
                if number > 100:
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
    pg.doubleClick(220,1060)
    #click_center('.\RSA_icon.png', 0, 0, showed=True)
    click_center('.\RSA_main.png', 0, 0, showed=False)
    pg.typewrite(token)
    pg.press('enter')
    # move to copy button
    click_center('.\RSA_copy.png', 0, 0, showed=True)    

get_rsa()
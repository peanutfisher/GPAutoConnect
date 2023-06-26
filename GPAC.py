# 这是一个分支项目
# pyautogui实现自动连接GP(global protect)

import pyautogui as pg
import time
import os

# Main steps:
# 1. find GP icon->left click-> if already connected -> check if no-split -> if yes -> exit, if not -> func(choose no-split).
# 2. if not connected/connect failed status --> go to func(connect)
# 3. wait for prompt of NT login window
# 4. func(sign in pwd) - click pic center - typewrite(pwd) - moveRel - click sign on
# 5. get RSA credential from func(rsa) - rsa copy(mvoeRel(0,75)) - ctrl+V
# 6. func(sign in rsa window) - check if cert_confirm - click ok
# 7. wait for GP connected status --> check if gp no-split

NT_PASSWD = 'Ballball15'
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
                if number > 120:
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



def signin(temp=None):
    # mvoe mouse to input login passwd info
    x1, y1 = click_center('./GP_login_signon.png', 0, -50, showed=False)
    # check if it is NT login or RSA login
    if temp:
        pg.typewrite(temp)
    else:
        pg.hotkey('ctrl', 'v')
    # click "sign on" button
    pg.click(x1, y1, button='left', duration=0.5)
    time.sleep(3)
    # click the certification confirm dialog
    # As the Certification confirm prompt sometimes not showup
    for i in range(2):
        click_center('./cert_confirm.png', 0, 0, showed=True)


def get_rsa(token):
    """
    Get RSA Credential
    """
    #click_center('./RSA_icon.png', 0, 0, showed=True)
    # Just click location of the RSA icon(different PC different position)
    pg.click(220, 1060)
    # Check if the RSA is already being inputed, if so then click copy
    if not pg.locateOnScreen('./RSA_on.png'):
        click_center('./RSA_main.png', 0, 0, showed=False)
        pg.typewrite(token)
        pg.press('enter')
        time.sleep(1)
    # Click RSA copy button
    click_center('./RSA_copy.png', 0, 0, showed=False) 


def connect_GP(x, y):
    """
    Connect GP
    """
    # find and click "connect"
    pg.click(1870, 1010)
    pg.moveRel(0,-200)
    time.sleep(15)
    # check if GP is reconnected or connecting
    reconnect = False
    connecting = False
    count = 0
    while (not (reconnect or connecting)):
        # keep querying if reconnected
        reconnect = pg.locateOnScreen('./GP_reconnect.png')
        connecting = pg.locateOnScreen('./GP_login_signon.png')
        print(f'reconnect: {reconnect}, connecting: {connecting}')
        count += 1
        # if stuck then do cleaning
        if count > 50:
            print('Something Stuck and cannot move...')
            clear_status()
            
    # If it is connected after click "connect" goto choose_GP func
    if reconnect:
        choose_GP(x, y)
        os._exit(0)
    else:
        signin(NT_PASSWD)
        get_rsa(RSA_PASSWD)
        # GP login with RSA
        signin()

def choose_GP(x, y):
    # check if no-split is connected
    if (not pg.locateOnScreen('./GP_nosplit.png')):
        print('changing gateway')
        # click the "Change Gateway"
        pg.click(x+100, y-95, button='left', duration=0.3)
        # go to the search box
        pg.click(x+100, y-320, button='left', duration=0.3)
        pg.typewrite('no')
        # click the "no split"
        pg.click(x+100, y-292, button='left', duration=0.3)

    print('GP is connected! Enjoy it!')

def clear_status():
    """
    Clear the hung status of GP login and then retry.
    Call the CMD taskkill to kill it and then mouse move pass the icon to clear cache 
    """
    os.system('taskkill /IM PanGPA.exe /F')
    pg.moveTo(1300, 1056)
    pg.moveRel(500, 0, duration=0.5)
    print('Cleared unknown status, please retry')
    # waiting seconds and retry GPAC
    time.sleep(5)
    main()

def refresh_web():
    """
    This method is to open a rcm schedule page and turn on self view after it has been loaded.
    Desgined for LP.
    """
    os.system('start <rcm_schedule_web>')
    time.sleep(5)
    # waiting for webpage loading complete
    click_center('./RCM_page.png', 0, 0, showed=False)
    # check if self filter on, click the position if filter disabled
    click_center('./self_filter_off.png', 0, 0, showed=True)
    print('Web page loading ok with filter ON.')

def dontsleep():
    """
    This is use to start the dontsleep tools.
    """
    print('Starting Dontsleep...')
    # get the dontsleep disable icon
    pos = pg.locateCenterOnScreen('./dontsleep.png')
    if pos:
        # enable the icon if we disabled
        pg.rightClick(pos[0], pos[1])
        pg.click(pos[0]-10, pos[1]-10)
        pg.moveRel(0, -30)
    else:
        print('Dontsleep is ON.')


def main():
    # Enable the dontsleep tool
    dontsleep()
    print('Starting GP...')
    # check if GP icon is gray(notconnected or connectfailed)
    gray_gp = click_center('./gray_GP1.png', 0, 0, showed=True) or click_center('./gray_GP2.png', 0, 0, showed=True)
    blue_gp = click_center('./GP_blue.png', 0, 0, showed=True)
    # if not connected then do connection flow
    if (gray_gp):
        gp_x, gp_y = gray_gp[0], gray_gp[1]
        connect_GP(gp_x, gp_y)
        time.sleep(10)
        click_center('./GP_blue.png', 0, 0, showed=False)
        choose_GP(gp_x, gp_y)
    # if connected then check if no-split is choosen
    elif (blue_gp):
        # get GP icon position using blue icon
        gp_x, gp_y = blue_gp[0], blue_gp[1]
        choose_GP(gp_x, gp_y)
    else:
        clear_status()
        
if __name__ == '__main__':
    main()
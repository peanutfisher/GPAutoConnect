# 这是一个分支项目
# pyautogui实现自动连接GP(global protect)

import pyautogui as pg
import time
import os
# import cv2

# Main steps:
# 1. find GP icon->left click-> if already connected -> check if no-split -> if yes -> exit, if not -> func(choose no-split).
# 2. if not connected/connect failed status --> go to func(connect)
# 3. wait for prompt of NT login window
# 4. func(sign in pwd) - click pic center - typewrite(pwd) - moveRel - click sign on
# 5. get RSA credential from func(rsa) - rsa copy(mvoeRel(0,75)) - ctrl+V
# 6. func(sign in rsa window) - check if cert_confirm - click ok
# 7. wait for GP connected status --> check if gp no-split

# Update Nov.28 2023
# It is only for display resolution 1920x1080
# add support for different Scale Rate(100%, 125%, 150%)
# add verification in the last step
# RSA will change away after copied

# Account/Password depneds on you
NT_PASSWD = 'Ballball17'
RSA_PASSWD = '10538185'

# The pictures are inside different folders based on resolution size
Cur_dir = os.getcwd()
PIC_PATH = '150'
os.chdir(os.path.join(Cur_dir, PIC_PATH))

def get_scale_rate():
    """
    Used to check the current scrren scale rate and they change working director to specific folder which contains the pics
    """
    # change Working directory
    os.chdir(os.path.join(os.getcwd(), PIC_PATH))
    pass

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
            x1, y1 = pg.locateCenterOnScreen(png, confidence=0.95)
        else:
            # if ICON/PROMPT is not there then waiting it showup
            while (not showed):
                showed = pg.locateCenterOnScreen(png, confidence=0.95)
                number += 1
                print(f'Waiting {png} for {number} times')
                # in case we wait too much time
                if number > 80:
                    print('Loging process could be hung, clearing unknown status...')
                    number = 0
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
    # move mouse to input login passwd info
    x1, y1 = click_center('GP_login_signon.png', 0, -85, showed=False)
    # check if it is NT login or RSA login
    if temp:
        pg.typewrite(temp)
    else:
        pg.hotkey('ctrl', 'v')
    # click "sign on" button
    pg.doubleClick(x1, y1, button='left', duration=0.3)
    #time.sleep(2)


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


def connect_GP():
    """
    Connect GP
    """
    # find and click "connect"
    if not click_center('GP_connect.png'):
        click_center('GP_connect1.png')
    time.sleep(5)
    # Press hotkey "WIN+UP" in case browser not maximum
    pg.hotkey('win', 'up')
    # check if GP is reconnected or connecting
    reconnect = False
    connecting = False
    count = 0
    while (not (reconnect or connecting)):
        # keep querying if reconnected
        reconnect = pg.locateOnScreen('GW_change.png', confidence=0.95)
        connecting = pg.locateOnScreen('GP_login_signon.png', confidence=0.95)
        print(f'reconnect: {reconnect}, connecting: {connecting}, check: {count}times')
        count += 1
        # if stuck then do cleaning
        if count > 100:
            print('Something Stuck and cannot move...')
            count = 0
            clear_status()
            
    # If it is connected after click "connect" goto choose_GP func
    if reconnect:
        choose_GP()
        os._exit(0)
    else:
        signin(NT_PASSWD)
        get_rsa(RSA_PASSWD)
        # GP login with RSA
        signin()

def choose_GP():
    # check if no-split is connected
    if (not pg.locateOnScreen('GP_nosplit.png', confidence=0.95)):
        print('changing gateway')
        # click the "Change Gateway", 2 type 
        click_center('GW_change.png')
        click_center('GW_change1.png')
        if pg.locateOnScreen('GP_choose.png', confidence=0.95):
            # Use "Tab" key to redirect focus on the input area
            pg.press('tab')
        # Search No split channel and connecting
        pg.typewrite('no')
        pg.press('tab')
        pg.press('enter')
        # Waiting for few seconds until connected
        time.sleep(10)
        click_center('GP_nosplit.png', showed=False)
    
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
    time.sleep(8)
    main()

def refresh_web():
    """
    This method is to open a rcm schedule page and turn on self view after it has been loaded.
    Desgined for LP.
    """
    os.system('start <rcm_schedule_web>')
    time.sleep(5)
    # waiting for webpage loading complete
    click_center('RCM_page.png', 0, 0, showed=False)
    # check if self filter on, click the position if filter disabled
    click_center('self_filter_off.png', 0, 0, showed=True)
    print('Web page loading ok with filter ON.')

def dontsleep():
    """
    This is use to start the dontsleep tools.
    """
    print('Starting Dontsleep...')
    # get the dontsleep disable icon
    pos = pg.locateCenterOnScreen('dontsleep.png', confidence=0.95)
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
    gray_gp = click_center('gray_GP1.png') or click_center('gray_GP2.png')
    blue_gp = click_center('GP_blue.png')
    # if not connected then do connection flow
    # adding situation that GP icon if blinking for connecting
    if (gray_gp) or ((pg.locateOnScreen('GP_login_signon.png', confidence=0.95))):
        connect_GP()
        time.sleep(10)
        click_center('GP_blue.png', 0, 0, showed=False)
        choose_GP()
    # if connected then check if no-split is choosen
    elif (blue_gp):
        choose_GP()
    # If the blink gp showed
    else:
        clear_status()
        
if __name__ == '__main__':
    main()
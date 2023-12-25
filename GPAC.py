# coding: utf-8
# author: peanutfish

# 这是一个分支项目
# pyautogui实现自动连接GP(global protect)

from get_screen_size import *
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

# Update Nov.28 2023
# It is only for display resolution 1920x1080
# add support for different Scale Rate(100%, 125%, 150%)
# add verification in the last step
# RSA will change away after copied

# Account/Password depneds on you
NT_PASSWD = ''
RSA_PASSWD = ''
SCALE_RATE = ''


def check_config(filename):
    """
    Check the config file and get parms
    """
    config_dict = read_config(filename)
    if 'NT_PASSWORD' not in config_dict:
        nt_passwd = pg.password(text='NT_PASSWORD:', title='Please input your NT password', default='')
        write_config(filename, 'a', 'NT_PASSWORD', nt_passwd)

    if 'RSA_CODE' not in config_dict:
        rsa_code = pg.password(text='RSA_CODE:', title='Please input your RSA passcode', default='')
        write_config(filename, 'a', 'RSA_CODE', rsa_code)
    
    # reload the config file in case we had new update
    config_dict = read_config(filename)
        
    SCALE_RATE = config_dict['Scale_Rate']
    NT_PASSWD = config_dict['NT_PASSWORD']
    RSA_PASSWD = config_dict['RSA_CODE']
    
    return [SCALE_RATE, NT_PASSWD, RSA_PASSWD]


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
            x1, y1 = pg.locateCenterOnScreen(png, confidence=0.96)
        else:
            # if ICON/PROMPT is not there then waiting it showup
            while (not showed):
                showed = pg.locateCenterOnScreen(png, confidence=0.96)
                number += 1
                time.sleep(1)
                print(f'Waiting {png} for {number} times')
                # in case we wait too much time
                if number > 60:
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
        pg.write(temp)
    else:
        pg.hotkey('ctrl', 'v')
    # click "sign on" button
    pg.doubleClick(x1, y1, button='left', duration=0.3)
    time.sleep(2)


def get_rsa(token):
    """
    Get RSA Credential
    """
    # Click RSA icon to show RSA main window
    if not click_center('RSA_icon1.png'):
        click_center('RSA_icon2.png')
    pg.moveTo(0,500)
    time.sleep(3)    
    # Check if the RSA passcode is already being inputed, if not then get a new one
    if not click_center('RSA_copy.png'):
        if not click_center('RSA_main.png'):
            click_center('RSA_main1.png')
        pg.typewrite(token)
        pg.press('enter')
        time.sleep(1)
        # click copy button
        click_center('RSA_copy.png')

    # Change focus to browser window in case RSA window cover it
    pg.hotkey('alt', 'tab')


def connect_GP(passwd1, passwd2):
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
        
        # record retry times
        count += 1
        print(f'reconnect: {reconnect}, connecting: {connecting}, check: {count}times')
        
        time.sleep(1)
        # if stuck then do cleaning
        if count > 60:
            print('Something Stuck and cannot move...')
            count = 0
            clear_status()
            
    # If it is connected after click "connect" goto choose_GP func
    if reconnect:
        choose_GP()
        os._exit(0)
    else:
        signin(passwd1)
        get_rsa(passwd2)
        # GP login with RSA
        signin()

def choose_GP():
    # check if no-split is connected
    if (not pg.locateOnScreen('GP_nosplit.png', confidence=0.95)):
        print('changing gateway')
        # click the "Change Gateway", 2 types(lose focus and with focus)
        if not click_center('GW_change.png'):
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
    # refresh_web()

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
    time.sleep(30)
    # Make the GP window lose focus
    pg.hotkey('win', 'd')
    # restore the working directory before retrying
    os.chdir(os.pardir)
    
    main()

def refresh_web():
    print('Loading RCM webpage...')
    os.system('start https://rcmappprd001.corp.emc.com/rcm/RCM_Schedule/schedule.php')
    time.sleep(5)
    # waiting for webpage loading complete and click home button
    click_center('RCM_page.png', 1000, 70, showed=False)
    print('RCM page loading ok!')

def dontsleep():
    """
    This is use to start the dontsleep tools.
    """
    print('Starting Dontsleep...')
    # get the dontsleep icon
    pos = pg.locateCenterOnScreen('dontsleep.png', confidence = 0.90)
    pg.rightClick(pos[0], pos[1])
    # enable the icon if we disabled
    if click_center('dontsleep_off.png'):    
        print('Enable the Dontsleep.')
    else:
        print('Dontsleep is ON.')
    pg.moveRel(0, -200)    


def main():
    secret = check_config('config.ini')
    SCALE_RATE = secret[0]
    NT_PASSWD = secret[1]
    RSA_PASSWD = secret[2]
    print([SCALE_RATE, NT_PASSWD, RSA_PASSWD])
    # The pictures are inside different folders based on resolution size
    os.chdir(os.path.join(os.getcwd(), SCALE_RATE))
    print(os.getcwd())
    
    # Enable the dontsleep tool
    dontsleep()
    
    print('Starting GP...')
    
    connect_flag = (pg.locateOnScreen('GP_login_signon.png', confidence=0.95)) or (pg.locateOnScreen('GP_connect1.png', confidence=0.95))
    if not connect_flag:
        # check if GP icon is gray(notconnected or connectfailed)
        gray_gp = click_center('gray_GP1.png', showed=True) or click_center('gray_GP2.png', showed=True)
    blue_gp = click_center('GP_blue.png')
    # if not connected then do connection flow
    # adding situation that GP icon if blinking for connecting
    if connect_flag or gray_gp :
        connect_GP(NT_PASSWD, RSA_PASSWD)
        time.sleep(15)
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
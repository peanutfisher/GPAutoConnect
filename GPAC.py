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

# Update Dec.27 2023
# big change to click_center function, it can recognize the picture with different confidence
# according change to other parts

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

def click_center(image, click=True, wait_time=1, num=0.96, repeated=True):
    """
    Used to click the center of a picture and also provide following function:
    1. check if the image is there and return location(x,y)
    2. waiting a moment to see if the image show up
    3. in case image not found, decrease the confidence to get better recognition
    
    """
    try:
        location = None
        counter = 0
        
        while (not location):
            location = pg.locateCenterOnScreen(image, minSearchTime=wait_time, confidence=num, grayscale=True)
            
            # reduce confidence to get better recogniztion
            num -= 0.01
            counter += 1
            print(f'Waiting {image} for {counter} times')
            
            if (not repeated) and counter == 3:
                return False
            # in case we can not find the image then retry the process
            if num < 0.80:
                counter = 0
                raise
        
        # click the center position
        if click:
            pg.click(location[0], location[1])
        
        # return back center position
        print(f'{image} position({location[0]},{location[1]})')
        return (location[0], location[1])
    
    except Exception as e:
        print(f'Cannot find {image} in your Screen.')
        clear_status()

def signin(NT_PW, TOKEN):
    # Get the RSA code firstly
    get_rsa(TOKEN)
    
    # NT sign in
    if click_center('GP_nt_input.png', repeated=False):
        pg.write(NT_PW)
        click_center('GP_login_signon.png', click=True)
        print('NT password inputed')
        time.sleep(5)
    
    # RSA sign in
    if click_center('GP_rsa_input.png', repeated=False):   
        pg.hotkey('ctrl', 'v')
        click_center('GP_login_signon.png', click=True)
        print('RSA code inputed')

    else:
        # It may need to input username manually
        pass
        print('Signin failure, check login page')

def get_rsa(TOKEN):
    """
    Get RSA Credential
    """
    # Click RSA icon to show RSA main window
    if click_center('RSA_icon.png'):
        pg.moveTo(0,500)
        time.sleep(2)    
    
    # Check if the RSA passcode is already being inputed, if not then get a new one
    if click_center('RSA_main.png', repeated=False):
        pg.write(TOKEN)
        pg.press('enter')
        time.sleep(1)
    
    click_center('RSA_copy.png')

    # Change focus to browser window in case RSA window covered it
    pg.click(540, 960)

def connect_GP(NT_PW, TOKEN):
    """
    Connect GP
    """
    # find and click "connect"
    if click_center('GP_connect.png', repeated=False):
        time.sleep(8)
        # Press hotkey "WIN+UP" in case browser not maximum
        pg.hotkey('win', 'up')

        # check if GP is reconnected or connecting
        reconnect = False
        connecting = False
        count = 0
        while (not (reconnect or connecting)):
            # keep querying if reconnected
            reconnect = click_center('GW_change.png', click=False, repeated=False)
            connecting = click_center('GP_login_signon.png', click=False, repeated=False)
            
            # record retry times
            count += 1
            print(f'reconnect: {reconnect}, connecting: {connecting}, check: {count}times')
            
            if count > 10:
                print('Something Stuck and cannot move...')
                count = 0
                clear_status()
            
        # If it is connected after click "connect" goto choose_GP func
        if reconnect:
            choose_GP()
            
        else:
            signin(NT_PW, TOKEN)

    # connecting or reconnect
    else:
        choose_GP()  
        
def choose_GP():
    # check if no-split is connected
    if (not click_center('GP_nosplit.png', repeated=False)):
        print('changing gateway')
        # click the "Change Gateway"
        click_center('GW_change.png')
        time.sleep(1)
        
        click_center('GP_choose.png', repeated=False)
        # Search No split channel and connecting
        pg.typewrite('no')
        pg.press('tab')
        pg.press('enter')
        # Waiting for few seconds until connected
        time.sleep(10)
        click_center('GP_nosplit.png')
    
    print('GP is connected! Enjoy it!')
    # refresh_web()
    os._exit(0)

def clear_status():
    """
    Clear the hung status of GP login and then retry.
    Call the CMD taskkill to kill it and then mouse move pass the icon to clear cache 
    """
    os.system('taskkill /IM PanGPA.exe /F')
    pg.moveTo(1300, 1056)
    pg.moveRel(500, 0, duration=1)
    print('Cleared unknown status, retrying')
    # waiting seconds and retry GPAC
    time.sleep(30)

    # restore the working directory before retrying
    os.chdir(os.pardir)
    
    main()

def refresh_web():
    print('Loading RCM webpage...')
    os.system('start https://rcmappprd001.corp.emc.com/rcm/RCM_Schedule/schedule.php')
    time.sleep(5)
    # waiting for webpage loading complete and click home button
    click_center('RCM_page.png', repeated=False)
    print('RCM page loading ok!')

def dontsleep():
    """
    This is use to start the dontsleep tools.
    """
    print('Starting Dontsleep...')
    # get the dontsleep icon
    pos = click_center('dontsleep.png', click=False)
    pg.rightClick(pos[0], pos[1])
    # enable the icon if we disabled
    if click_center('dontsleep_off.png',repeated=False):    
        print('Enable the Dontsleep.')
    else:
        print('Dontsleep is ON.')
    pg.click(540, 960)   


def main():
    # Make the GP window lose focus
    #pg.hotkey('win', 'd')
    
    secret = check_config('config.ini')
    SCALE_RATE = secret[0]
    NT_PASSWD = secret[1]
    RSA_PASSWD = secret[2]
    #print([SCALE_RATE, NT_PASSWD, RSA_PASSWD])
    
    # The pictures are inside different folders based on resolution size
    os.chdir(os.path.join(os.getcwd(), SCALE_RATE))
    print(os.getcwd())
    
    # Enable the dontsleep tool
    dontsleep()
    
    print('Starting GP...')
    
    # scenario 1: If GP is connected
    if click_center('GP_blue.png', repeated=False):
        choose_GP()
    
    # Scenario 2: click gray GP icon for 1st connection or there is a GP window there for connection
    elif click_center('gray_GP1.png', repeated=False) or click_center('gray_GP2.png', repeated=False) or click_center('GP_connect.png', click=False, repeated=False):
        connect_GP(NT_PASSWD, RSA_PASSWD)
        time.sleep(15)
        if not click_center('GW_change.png', repeated=False):
            click_center('GP_blue.png')
        choose_GP()
    
    # Scenario 3: If the blink gp showed(connecting)
    elif click_center('GP_login_signon.png', click=False, repeated=False):
        signin(NT_PASSWD, RSA_PASSWD)
        time.sleep(15)
        if not click_center('GW_change.png', repeated=False):
            click_center('GP_blue.png')
        choose_GP()
    
    # The worst scenario - cannot connect
    else:
        clear_status()
        #print('Main process failure')
    
        
if __name__ == '__main__':
    main()
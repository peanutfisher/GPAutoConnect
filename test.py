import pyautogui as pg
import time
import os
from get_screen_size import *


NT_PASSWD = 'Ballball17'
RSA_PASSWD = '10538185'

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
        # clear_status()

def signin(NT_PW, TOKEN):
    # Get the RSA code firstly
    get_rsa(TOKEN)
    
    # NT sign in
    if click_center('GP_nt_input.png', repeated=False):
        pg.write(NT_PW)
        click_center('GP_login_signon.png', click=True)
        print('NT password inputed')
        time.sleep(8)
    
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

    # Change focus to browser window in case RSA window cover it
    pg.click(540, 960)

def connect_GP(NT_PW, TOKEN):
    """
    Connect GP
    """
    # find and click "connect"
    if click_center('GP_connect.png'):
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
                #clear_status()
            
        # If it is connected after click "connect" goto choose_GP func
        if reconnect:
            choose_GP()
            os._exit(0)
        else:
            signin(NT_PW, TOKEN)

    else:
        pass
        print('Connet_GP failure')  
        
def choose_GP():
    # check if no-split is connected
    if (not click_center('GP_nosplit.png', repeated=False)):
        print('changing gateway')
        # click the "Change Gateway"
        click_center('GW_change.png')
        time.sleep(1)
        
        if click_center('GP_choose.png', repeated=False):
            # Search No split channel and connecting
            pg.typewrite('no')
            pg.press('tab')
            pg.press('enter')
        # Waiting for few seconds until connected
        time.sleep(10)
        click_center('GP_nosplit.png')
    
    print('GP is connected! Enjoy it!')
    # refresh_web()

os.chdir(os.path.join(os.getcwd(),'125'))
#gray_gp = click_center('gray_GP1.png', showed=True) or click_center('gray_GP2.png', showed=True)
#print(pg.locateCenterOnScreen('GP_connect.png'))

#loc = click_center('GP_login_input.png', click=False)
#print(loc)

signin(NT_PASSWD, RSA_PASSWD)
#get_rsa(RSA_PASSWD)
#choose_GP()
#dontsleep()

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pytz
from db import *
import sys


driver = webdriver.Chrome('C:\Webdriver\chromedriver')
driver.maximize_window()

driver.get('https://web.whatsapp.com/')


def naming(nameofchat):
    try:
        element = driver.find_element(By.XPATH, "//p[@class='selectable-text copyable-text iq0m558w']")
        element.click()
        element.send_keys(nameofchat)
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        driver.find_element(By.XPATH, "//button[@aria-label='Cancel search']").click()
        return 1
    except:
        return 0


def online_offline_status():
    status = 0
    try:
        driver.find_element(By.XPATH, "//span[@title='typing…' or @title='online' and @class='ggj6brxn gfz4du6o r7fjleex lhj4utae le5p0ye3 _11JPr selectable-text copyable-text']")
        status=1    
        return status
    
    except:
        return status
    
def get_current_indian_time():
    # set the timezone to India
    tz = pytz.timezone('Asia/Kolkata')

    # get the current time in India
    current_time = datetime.datetime.now(tz)

    # format the time as a string
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return time_str


def main_comp():
    username  = sys.argv[1]
    scan = 0
    while scan==0:
        time.sleep(3)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='qrcode']")))
            element.screenshot('qr.png')
        except:
            scan = naming(username)
    current = 0
    while 1:
        if online_offline_status()==1:
            current = 1
            current_timestamp = []
            current_timestamp.append(get_current_indian_time())
            while current==1:
                stat = online_offline_status()
                if stat==0:
                    current=0
                    current_timestamp.append(get_current_indian_time())
            try:
                tuples = ((f"{username}",)+ tuple(current_timestamp))
                print(tuples)
                insertion_table('info',tuples)
            except:
                print("Not Online")

main_comp()

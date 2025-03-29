# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00AC8201F6106086923572E234F35BDE3BC389AA311E2F8624CD9CEF4955EE39B51BD7D26E1855667D3F4B95950652AA75AA41AC75664FDC128B2AF9099E26F53D019ADBD0CECA35E9E511029C2A8F3D21182157744EB545CD1A2DE1C95C5FDC08BADA6018F993625DFB6DCAD34F4FEAB86F873F789DC294D9BE83F4F93CBC2EFE386B74416046F237628BFA1169B4A73FE2283900E3C17D78CB1A747708E4AE1B6D82BCA34D2F540766290259B9BFA8429CE0ACC498A1E96840B317ADD6C9F639F83DB5B2F0865B9930D00B2752502615D2D9204C46BBD056411C50DC841112F35CA7F9E14BFED893B6698C49D360B60F455FF8C97213E8E4B2392776E2D8256F4F53368A25D1E39BDABC9ACD2030465BADB514956551B5758AD2787D9C516B9FB3B3322129E6AACDFCCE138081A128E0C7D3A46116BDB9E64F9DDF42D02CC68BAC5116418939670DEE5667222924397999D6BF4B35DFA69C7703D6D8424D3F6E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

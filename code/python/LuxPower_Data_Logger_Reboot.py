#!/usr/bin/python3

###################################################################
# This script reboots the LuxPower Data Logger via the UI
# Requirements\ Dependencies
# 	- apt-get install firefox-esr
# 	- python3 -m pip install -U selenium
#	- mkdir webdrivers
#	- cd webdrivers
# 	- wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
# 	- tar -xvf geckodriver-v0.29.0-linux64.tar.gz
###################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from time import sleep
from datetime import date, datetime, timedelta

#Read in config file variables
config = configparser.ConfigParser()
config.read('config.ini')
LOG_FILE_LOCATION = config['GENERAL']['LogDir']
ipAdr = config['LUX']['DataModuleIP']
userName = config['LUX']['DataModuleUser']
userPwd = config['LUX']['DataModulePwd']
gekoDriver = config['LUX']['GekoDriver']

# File directories
LOG_FILE_NAME = 'LuxPower_Logger_Reboot.log'
GEKO_LOG_FILENAME = 'Geko_Driver.log'
LOG_FILE = LOG_FILE_LOCATION + LOG_FILE_NAME
GEKO_LOG_FILE = LOG_FILE_LOCATION + GEKO_LOG_FILENAME

# Open log file
executionTimeStamp = datetime.now()
thisLogFile=open(LOG_FILE, "a+")
thisLogFile.write('\n')
thisLogFile.write('###################################################################################' + '\n')
thisLogFile.write('Start of Processing @: ' + executionTimeStamp.strftime('%Y-%m-%d %H:%M:%S') + '\n')

# Set Driver Options to run Headless
options = webdriver.FirefoxOptions()
options.headless = True
options.add_argument("--window-size=768,773")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver=webdriver.Firefox(executable_path=str(gekoDriver),service_log_path=GEKO_LOG_FILE,options=options)

try:
	# Need to call the website twice in order to login
	driver.get("http:///" + str(userName) + ":" + str(userPwd) + "@" + str(ipAdr) + "/model_en.html")
	driver.get("http:///" + str(userName) + ":" + str(userPwd) + "@" + str(ipAdr) + "/model_en.html")

	# Test by saving a screen shot
	#driver.get_screenshot_as_file("LuxPower_Screenshot.png")

	# Click the reset button on the page
	driver.find_element(By.CSS_SELECTOR, "form:nth-child(9) .btn").click()
	thisLogFile.write('# Data Logger Reboot request made. \n')

	# Wait 10 seconds for the logger to reboot
	sleep(10)

	# Load up the front page in english
	driver.get("http:///" + str(userName) + ":" + str(userPwd) + "@" + str(ipAdr) + "/index_en.html")

	# Test to see if the page has loaded and the title is "setting"
	try:
		WebDriverWait(driver, 10).until(EC.title_contains("setting"))
	except:
		thisLogFile.write('     ***ERROR: Unable to re-load webpage after reboot. \n')

	driver.quit()
except:
    thisLogFile.write('     ***ERROR: Unable to load Data Logger Webpage. \n')

# Close the log file
executionTimeStamp = datetime.now()
thisLogFile.write('# Data Logger Rebooted. \n')
thisLogFile.write('End of Processing for Time Period: ' + executionTimeStamp.strftime('%Y-%m-%d %H:%M:%S') + '\n')
thisLogFile.write('###################################################################################' + '\n')
thisLogFile.write('\n')

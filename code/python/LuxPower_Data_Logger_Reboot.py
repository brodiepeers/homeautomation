#!/usr/bin/python3

###################################################################
# This script reboots the LuxPower Data Logger via the UI
# Requirements\ Dependancies
# 	- apt-get install firefox-esr
#	- mkdir /root/webdrivers/geckodriver
#	- cd /root/webdrivers/geckodriver (note, if this directory is changed then ensure that it is reflected in the config.ini file)
# 	- wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
# 	- tar -xvf geckodriver-v0.30.0-linux64.tar.gz
# 	- python3 -m pip install -U selenium
###################################################################
###################################################################
# Version
# 11/02/21 - First baselined version
# 18/02/21 - Removed ENV from config.ini file
# 06/01/22 - Update Selenium command to use Service Object. Know issue that the output to the Gekolog file is now not used.
##################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
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

# Update command to use Service Object due to depricaiton
s = Service(str(gekoDriver))
driver=webdriver.Firefox(service=s,options=options)

try:
	# Need to call the website twice in order to login
	driver.get("http:///" + str(userName) + ":" + str(userPwd) + "@" + str(ipAdr) + "/model_en.html")
	driver.get("http:///" + str(userName) + ":" + str(userPwd) + "@" + str(ipAdr) + "/model_en.html")

	# Test by saving a screen shot
	#driver.get_screenshot_as_file("LuxPower_Screenshot.png")

	# Click the reset button on the page
	driver.find_element(By.CSS_SELECTOR, "form:nth-child(9) .btn").click()
	thisLogFile.write('# Data Logger Reboot reqeust made. \n')

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

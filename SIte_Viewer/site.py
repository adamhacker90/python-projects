# Necessary webdrivers ned to be imported
from selenium import webdriver
import os
import sys
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests

path = (os.path.join(sys.path[0], 'chromedriver.exe'))
# This is for Firefox. Similarly if 
# chrome is needed , then it has to be specified
webBrowser = webdriver.Chrome(path)
  
# first tab. Open google.com in the first tab
webBrowser.get('https://google.com')
  
# second tab
# execute_script->Executes JavaScript snippet. 
# Here the snippet is window.open that means, it 
# opens in a new browser tab
webBrowser.execute_script("window.open('about:blank', 'secondtab');")
  
# It is switching to second tab now
webBrowser.switch_to.window("secondtab")
  
# In the second tab, it opens geeksforgeeks
webBrowser.get('https://www.geeksforgeeks.org/')
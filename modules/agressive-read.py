#!/usr/bin/env python3
import sys
import unittest, time, re
from selenium import webdriver

# Select motor
driver = webdriver.Firefox(executable_path='./modules/geckodriver/geckodriver')
driver.get(sys.argv[1]) # Arg: url
# Show all texts
print(driver.find_element_by_tag_name('body').text)
# Close
driver.close()

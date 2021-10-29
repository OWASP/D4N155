#!/usr/bin/env python3

from sys import argv
from re import sub

target = sub('(^\w+:|^)\/\/', '', argv[1])
def aggressive_read(url):
    from selenium import webdriver
    driver = webdriver.Firefox(executable_path='./modules/geckodriver/geckodriver')
    driver.get(f'http://{url}')
    value = driver.find_element_by_tag_name('body').text
    driver.close()
    return value

def static_read(url):
    from objetive import text
    return text(f'http://{url}')

if argv[2] == '0':
    print(static_read(target))
else:
    print(aggressive_read(target))

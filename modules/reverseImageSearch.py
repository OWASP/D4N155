from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
#Based on this: https://stackoverflow.com/questions/18557275/how-to-locate-and-insert-a-value-in-a-text-box-input-using-python-selenium
#This is for images.google.com as of December 2021.
def reverseImageSearch(image_url, driver):
    driver.get(f'https://images.google.com/')
    #Need to click button to make URL option visible.
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[2]').click()
    #This was the id of the URL paste portion of Google Image search based on inspecting the page.
    searchedURL = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/form/div[1]/table/tbody/tr/td[1]/input')
    searchedURL.send_keys(image_url)
    submitButton = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/form/div[1]/table/tbody/tr/td[2]/input').click()
    #Get the list of urls after the submit to scrub.
    links = driver.find_elements_by_xpath('//*/text()[.="Pages that include matching images"]/following::div[@class="yuRUbf"]')
    value = []
    for link in links:
        value.append(link.find_element_by_css_selector('a').get_attribute('href'))
    return value

#Load Firefox profile and binary path here to keep cookies for social media websites because some sites
#block information if you are not logged in.
#Get the profile path by going to about:profiles in Firefox.
#Get the binary path by running which firefox
def getCookies(profilePath, binaryPath, withProfile):
    options = Options()
    options.headless = True
    if withProfile:
        ffprofile = webdriver.FirefoxProfile(profilePath)
        ffbinary = FirefoxBinary(binaryPath)
        driver = webdriver.Firefox(options=options, firefox_binary=ffbinary,firefox_profile=ffprofile)
    else:
        driver = webdriver.Firefox(options=options)
    return driver

#Scrub images from page and pass the reverse image search results back.
#If there are too many images on the page, this can get tedious.
#NameTry is an attempt to attach a picture of a person to their name to associate
#a list with a person.
#If nameTry is an empty string, no name will be preferred.
def getURLsForImages(url, imageLimit, nameTry, driver):
    driver.get(str(url))
    imageElements = driver.find_elements_by_css_selector('img')
    URLReturns = []
    imageCount = 0
    for image in imageElements:
        #Look for a person's name in the source of the image to try and associate.
        for i in nameTry:
            if str(i.lower().replace(" ", "")) in str(image.get_attribute('src')).lower().replace(" ", ""):
                time.sleep(2)
                #Do a reverse image search for all images and concatenate the results together.
                #Use set to remove duplicates.
                URLReturns = list(set(URLReturns + reverseImageSearch(str(image.get_attribute('src')), driver)))
                #imageCount = imageCount + 1
                if imageCount > imageLimit:
                    break
    return URLReturns

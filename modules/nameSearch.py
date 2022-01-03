#!/usr/bin/env python3

#These functions will be used to generate personalized wordlists.

import spacy
import os
from googlesearch import search
import sys
import requests
import reverseImageSearch
import time
#Only load this once for multiuse of parseLanguage function.
nlp = spacy.load('en_core_web_sm')
#Get names, organizations people are affiliated with, and dates from About Us or Contact Us pages to generate personalized word lists.
#Aggressive means that this will perform a reverse image search on any images found on the page (in case there are pictures of people that they reuse).
def personalizedList(isAggressive, url, nameLimit=2, keepCookies=0, profilePath="", binaryPath=""):
	from selenium import webdriver
	from selenium.webdriver.firefox.options import Options
	options = Options()
	options.headless = True                                                                                        
	driver = webdriver.Firefox(options=options, executable_path='./modules/geckodriver/geckodriver')                                        
	driver.get(url)                                                                                             
	textInput = driver.find_element_by_tag_name('body').text
	driver.quit()
	parsedLanguage = nlp(textInput)
	humanNames = []
	affiliations = []
	dates = []
	#Iterate through the extracted words and filter out the human names.
	for word in parsedLanguage.ents:
		if nameLimit == 0:
			break
		if word.label_ == 'PERSON':
			humanNames.append(str(word))
			nameLimit = nameLimit - 1
		#Find affiliated organizations and locations for searching.
		if word.label_ == 'ORG' or word.label_ == 'LOC':
			affiliations.append(str(word))
		if word.label_ == 'DATE':
			dates.append(str(word))
	#Consider usernames to be "human names".
	humanNames = humanNames + findUsernames(textInput)
	driver = reverseImageSearch.getCookies(profilePath, binaryPath, keepCookies)
	generateWordlists(humanNames, affiliations, 2, "names", isAggressive, driver)


#Get a list of names and affiliations to generate personalized word lists based on URLs found with that name.
#Pass in usernames instead of IRL names to do a username search.
def generateWordlists(names, affiliations, requestDelay, parentDirectory, isAggressive, driver):
	#Make a dictionary of names with values as URLs of websites associated
	#with the names.
	for name in names:
		#Search for a name and a list of affiliations to filter down the search.
		query =  str(name) + " " + ' '.join(affiliations)
		#Pause to avoid IP block from Google. Take the first set of results.
		#Stop after a few results to not search for results forever. These are probably
		#the most relevant results. Wanted to speed up the program for testing, so reduced results.
		result = search(query, num=2,stop=2, pause=requestDelay)
		#Aggressive personalized lists will attempt to use reverse image search to find more URLs.
		intermediateResult = []
		if isAggressive:
			for url in result:
				#Slow down requests.
				time.sleep(5)
				try:
					intermediateResult = intermediateResult + reverseImageSearch.getURLsForImages(url,2, name.split(), driver)
				except:
					response = requests.request("GET", url, headers=headers)
					time.sleep(int(response.headers["Retry-After"]))
					intermediateResult = intermediateResult + reverseImageSearch.getURLsForImages(url,2,name.split(),driver)
		result = list(result) + intermediateResult
		for url in result:
			#Use the D4NN15 file reading function because the URL wordlist function
			#sometimes throws an error with the generated URLs.
			#One URL at a time because the wordlists have a word limit.
			f = open("temporaryURLText.txt", "w+")
			f.write(str(url) + "\n")
			f.close()
			# Remove potentially dangerous characters from the URL name when giving the wordlist name.
			finalWordList = os.path.join(parentDirectory, str(name).replace(" ", "_") + "_wordlist.txt")
			command = "bash ./main -t temporaryURLText.txt"
			os.system(command)
			if os.path.exists("./reports/wordlist/wordlist.txt"):
				returnFile = open("./reports/wordlist/wordlist.txt", "r+")
				returnText = returnFile.read()
				returnFile.close()
				#The command stores the output in the same place by default. Append all the outputs together.
				if not os.path.exists(parentDirectory):
					os.mkdir(parentDirectory)
				writeFile = open(finalWordList, "a+")
				writeFile.write(returnText)
				writeFile.close()
			time.sleep(1)
	return names


#Find potential usernames from the input text. This is based on the assumption that users like to put an "@" in front of usernames on different websites, so it does not need to
#be set for a particular website. Also included is an attmept to catch twitch usernames.
def findUsernames(textInput):
	usernames = []
	for text in textInput.split():
		if text.startswith("@"):
			#Remove the @ in the list.
			usernames.append(text[1:] + "\n")
		#Get Twitch usernames
		if text.startswith("twitch.tv/"):
			usernames.append(text.replace("twitch.tv/","") + "\n")
	return usernames

personalizedList(int(sys.argv[1]), str(sys.argv[2]))

# -*- coding: utf-8 -*-
import mechanicalsoup # needed
import os
import sys

#define man
heelp =  """
    0BJ3T1V3: This software is a mini-crawler that aims to grab some text
        parts from some website or ip that responds http*.

    Objetive: python objetive.py [url] [option]
        
    URL:
        Is the host web, example: https://jul10l1r4.github.io
    
    OPTION:
        Can pass specific option.
        -t, --title     For get all titles, tags in "h1".
        -txt, --text    For get all text in paragraphs.
        -a, --anchol    For get all urls in tag "a"
"""
args = 0
# Connect to target
browser = mechanicalsoup.StatefulBrowser()
try:
    browser.open(sys.argv[1])
except:
    print(heelp)
    exit(1)

# All functions for get values
def text():
    for p in browser.get_current_page().select('p'):
        try:
                print(p.text)
        except:
                print("Houve um erro nesse url");

def title():
    for h1 in browser.get_current_page().select('h1'):
        try:
                print(h1.text)
        except:
                print("Houve um erro ao pegar esse titulo")

def links():
    for link in browser.get_current_page().select('a'):
        try:
                print(link.text)
        except:
                print("Houve um erro ao pegar esse link")

# For all arguments get in all numbers
while args <= (len(sys.argv) - 1):
    if sys.argv[args] == '--text' or '-txt' == sys.argv[args]:
        text()
    elif sys.argv[args] == '--title' or '-t' == sys.argv[args]:
        title()
    elif sys.argv[args] == '--anchol' or '-a' == sys.argv[args]:
        links()
    elif sys.argv[args] == '-h' or '--help' == sys.argv[args]:
        print(heelp)
        exit(0)
    args+=1

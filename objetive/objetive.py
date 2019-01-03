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
    exit(3)
# All functions for get values
def text():
    for p in browser.get_current_page().select('p'):
        try:
                print(p.text)
        except:
                print("Houve um erro nesse url");
    for span in browser.get_current_page().select('span'):
        try:
                print(span.text)
        except:
                print("Houve um erro ao pegar esse texto")
    for strong in browser.get_current_page().select('strong'):
        try:
                print(strong.text)
        except:
                print("Houve um erro ao pegar esse texto")
    for italic in browser.get_current_page().select('i'):
        try:
                print(i.text)
        except:
                print("Houve um erro ao pegar esse texto")

def title():
    for h1 in browser.get_current_page().select('h1'):
        try:
                print(h1.text)
        except:
                print("Houve um erro ao pegar esse titulo")

    for h2 in browser.get_current_page().select('h2'):
        try:
                print(h2.text)
        except:
                print("Houve um erro ao pegar esse titulo")
    for h3 in browser.get_current_page().select('h3'):
        try:
                print(h3.text)
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

#!/usr/bin/env python3
import sys

# It code are a test

def hackableMenuscula (x):
    blob = x.lower()

    # Replace vog.
    blob = blob.replace('a','4')
    blob = blob.replace('e','3')
    blob = blob.replace('i','1')
    blob = blob.replace('o','0')
    
    # Replace con.
    blob = blob.replace('t','7')
    return blob

out = list(map(hackableMenuscula,sys.argv[1]))
print(out)

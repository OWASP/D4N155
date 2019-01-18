#!/usr/bin/env python3
import sys

# check if are lowcase or no
def hackableMenuscula (x):
    blob = x.replace('a','4')
    blob = blob.replace('e','3')
    blob = blob.replace('i','1')
    blob = blob.replace('o','0')
    return blob

out = list(map(hackableMenuscula,sys.argv[1]))
print(out)

#!/usr/bin/env python3
import re

# Replace things, → lowercase or uppercase no problems
def highlevelrplc (ex,val,var):
    return re.sub(ex, val, var, flags=re.IGNORECASE)

# Texts to numbers 
def textnumber (x):
    # Replace vog.
    blob = highlevelrplc('a','4',x)
    blob = highlevelrplc('e','3',blob)
    blob = highlevelrplc('i','1',blob)
    blob = highlevelrplc('o','0',blob)
  
    # Replace con.
    blob = highlevelrplc('b','8',blob)
    blob = highlevelrplc('t','7',blob)
    return blob

# make the numbers
def counting3 (x):
    return x+"123"
def counting4 (x):
    return x+"1234"
def counting8 (x):
    return x+"12345678"
def counting1 (x):
    return x+"87654321"
# Weaks year
def year9 (x):
    return x+"2019"
def year8 (x):
    return x+"2018"
def year7 (x):
    return x+"2017"
def year6 (x):
    return x+"2016"

# Variant, all uppercase or lowercase
# Up, Low, and upper lower lower up
# and inverter
def uppall (x):
    return x.upper()
def lowera (x):
    return x.lower()
def ullual (x):
    i=0
    value = ""
    for letter in x:
        if i % 2 == 0:
            value += letter.upper()
        else:
            value += letter.lower()
        i=i+1
    return value
def luulal (x):
    return ullual(x).swapcase()
def inverter (x):
    return x.swapcase()

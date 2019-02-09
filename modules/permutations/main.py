#!/usr/bin/env python3

# Texts to numbers 
def textnumber (x):
    blob = x.translate(str.maketrans('aeioAEIOBTbt','431043108787'))
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

# Combinatories analysis
# comb -> mess & ssem -> parsing
# returning all parsing strings
def comb(allist):
    def parsing (x):
        final=[]
        for i in x:
            final = final + i
        return final

    # Normal
    def mess (x):
        lists = []
        for i in allist:
            lists.append(x+i)

        return lists
    
    # Mergeds values
    new = parsing(list(map(mess, allist)))
    fund = new
    return fund



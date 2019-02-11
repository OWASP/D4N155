#!/usr/bin/env python3
# Elimine the max. number
# of variables
global_list = []
# Texts to numbers 
def textnumber (x):
    return x.translate(str.maketrans('aeioAEIOBTbt','431043108787'))

# make the number
def counting1 (x):
    return x+"1"
def counting2 (x):
    return x+"12"
def counting3 (x):
    return x+"123"
def counting4 (x):
    return x+"1234"
def counting8 (x):
    return x+"12345678"
def counting81 (x):
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
    # k = key
    # k[0] -> position
    # k[1] -> value
    return ''.join(
        list(
            map(
                lambda k: k[1].upper() if k[0] % 2 == 0 else k[1].lower(),
                enumerate(x)
                )
            )
        )

def luulal (x):
    return ullual(x).swapcase()
def inverter (x):
    return x.swapcase()

# Combinatories analysis
# comb -> mess & ssem -> parsing
# returning all parsing strings
def comb(allist):

    # Get value [[1,2,3],[3,2,1]] to
    # parse [1,2,3,3,2,1] 
    def parsing (x):
        global global_list
        for i in x:
            global_list = global_list + i
        return global_list

    # Mergeds values
    return parsing(list(map(lambda x: [x+i for i in allist], allist)))

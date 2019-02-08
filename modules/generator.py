# It module make the word list
import sys
import string
from anagrams.main import *  # All modules for anagrams
from multiprocessing.dummy import Pool as ThreadPool
details = False

# Root text
texts = sys.argv[1].split()
new = []
# Alternations
texts = texts+list(map(inverter,texts))
pool = ThreadPool(2)

# f → function
# v → value
def run(f,v):
    # Thread will be parameter type flag
    return list(pool.map(f,v))

# Main
def make():
    #   EX
    # counting 3: → x+"123"
    blob = run(counting1,texts)
    blob = blob+run(counting3,texts)
    blob = blob + run(counting4,texts)
    blob = blob + run(counting8,texts)
    #   EX
    # year9 : → x+"2019"
    blob = blob + run(year9,texts)
    blob = blob + run(year8,texts)
    blob = blob + run(year7,texts)
    blob = blob + run(year6,texts)
    # EX
    # YEAR : → "Y34R"
    blob = blob + run(textnumber,texts)
    # EX 
    # year : → "YeAr"
    blob = blob + run(ullual,texts)
    blob = blob + run(luulal,texts)
    blob = blob + run(inverter,texts)
    blob = blob + run(uppall,texts)
    blob = blob + run(lowera,texts)
    # EX
    # New Yeah : → "YeahNew"
    new = comb(texts)


    # Are finals test details
    if details == True:
        blob = blob + pool.comb(blob)

    return blob

# Reduce all output for best precision
print('\n'.join(set(texts+make()+new)))

# It module make the word list
import sys
import string
from anagrams.main import *  # All modules for anagrams

# Root text
texts = [texts.translate(str.maketrans('','', ',')) for texts in sys.argv[1].split()]

# Main
def make():
    #   EX
    # counting 3: → x+"123"
    blob = list(map(counting3,texts))
    blob = blob+list(map(counting4,texts))
    blob = blob+list(map(counting8,texts))
    #   EX
    # year9 : → x+"2019"
    blob = blob+list(map(year9,texts))
    blob = blob+list(map(year8,texts))
    blob = blob+list(map(year7,texts))
    blob = blob+list(map(year6,texts))
    # EX
    # YEAR : → "Y34R"
    blob = blob+list(map(textnumber,texts))
    
    blob = '\n'.join(set(blob))
    return blob

print(make())
print('\n'.join(set(texts)))

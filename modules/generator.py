# It module make the word list
import sys
import string

# Functions useds in the make
# weaks
def counting3 (x):
    return x+"123"
def counting4 (x):
    return x+"1234"
def counting8 (x):
    return x+"12345678"
# Weaks year
def year9 (x):
    return x+"2019"
def year8 (x):
    return x+"2018"
def year7 (x):
    return x+"2017"
def year6 (x):
    return x+"2016"

# Root text
texts = [texts.translate(str.maketrans('','', string.punctuation)) for texts in sys.argv[1].split()]

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

    blob = '\n'.join(set(blob))
    return blob

print(make())
print('\n'.join(set(texts)))

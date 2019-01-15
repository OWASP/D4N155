# It module make the word list
import sys
import string

# Function
def counting (x):
    return x+"123"

texts = [texts.translate(str.maketrans('','', string.punctuation)) for texts in sys.argv[1].split()]
text123 = map(counting,texts)
print(text123)
#print('\n'.join(set(texts)))


import sys
import string

texts = [texts.translate(str.maketrans('','', string.punctuation)) for texts in sys.argv[1].split()]
print('\n'.join(set(texts)))


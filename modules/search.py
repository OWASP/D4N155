from sys import argv
from getrails import search
print("\n".join(search(argv[1])))

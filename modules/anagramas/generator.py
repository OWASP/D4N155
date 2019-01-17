#!/bin/python3
import sys
import itertools as itert
resultado=" "
for palavra in sys.argv:
    chl=str(palavra)
wl=[resultado.join(ent) for ent in itert.permutations(chl)]
print ("/n",wl,"/n")


# It module make the word list
from sys import argv
from multiprocessing.dummy import Pool as ThreadPool
from permutations.main import *  # All modules for permutations
details = False

def main(texts):
    # Root text
    texts = texts.split()
    # Alternations
    texts = texts+list(map(inverter, texts))
    pool = ThreadPool(2)
    def run(fuction,value):
        # Thread will be parameter type flag
        # --------------------| All word > 3 and < 30
        return list(filter(lambda x: True if (len(x) > 3 and len(x) < 30) else False, list(pool.map(fuction, value))))

    # Main
    def make():
        #   EX
        # counting 3: → x+"123"
        blob = run(counting1, texts)
        blob = blob + run(counting2, texts)
        blob = blob + run(counting3, texts)
        blob = blob + run(counting4, texts)
        blob = blob + run(counting8, texts)
        blob = blob + run(counting81, texts)
        #   EX
        # year9 : → x+"2019"
        blob = blob + run(year9, texts)
        blob = blob + run(year8, texts)
        blob = blob + run(year7, texts)
        blob = blob + run(year6, texts)
        # EX
        # YEAR : → "Y34R"
        blob = blob + run(textnumber, texts)
        # EX 
        # year : → "YeAr"
        blob = blob + run(ullual, texts)
        blob = blob + run(luulal, texts)
        blob = blob + run(inverter, texts)
        blob = blob + run(uppall, texts)
        blob = blob + run(lowera, texts)
        # EX
        # New Yeah : → "YeahNew"
        blob = blob + comb(texts)
        
        # Are finals test details
        if details == True:
            blob = blob + pool.comb(blob)

        return blob

    # Reduce all output for best precision
    return '\n'.join(set(texts+make()))

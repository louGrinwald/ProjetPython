'''
Created on 27 janv. 2020

@author: gresset6u
'''
from timeit import Timer
from Fibo import *

#parametres implicites
t = Timer("fibo(10)","from __main__ import fibo")

#parametres explites
trec = Timer(stmt="fiborec(10)",setup="from __main__ import fiborec")

print ("10000 iterations iteratif : ", t.timeit(number=10000))
print ("10000 iterations recursif : ", trec.timeit(number=10000))

# sont declarees precedemment les fonctions fibo(n) et fiborec(n)
if __name__ == "__main__":
    import cProfile
    print ("analyse iteratif : ")
    cProfile.run("fibo(30)")
    print ("analyse recursif : ")
    cProfile.run("fiborec(30)")

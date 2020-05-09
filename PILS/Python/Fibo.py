'''
Created on 11 janv. 2020

@author: gresset6u
'''

def fibo(n):
    """ Rend une liste contenant les n premieres valeurs de fibonacci
    """
    a,b = 1,0
    tab = []
    for i in range(n):
        tab.append(a)
        a,b = a+b,a
    return tab

def fiborec(n):
    if(n < 2):
        return 1
    else:
        return fiborec(n-1) + fiborec(n-2)
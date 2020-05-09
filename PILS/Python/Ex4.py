'''
Created on 11 janv. 2020

@author: gresset6u
'''

def factoriel(n):
    facto = 1
    for i in range(1,n):
        facto *= i
    return facto

def Cnp(n,p):
    return factoriel(n) / (factoriel(n-p) * factoriel(p))
def Anp(n,p):
    return factoriel(n) / factoriel(n-p)

def Fibonnacci(n):
    f = [1,1]
    for i in range(2,n+1):
        f.append(f[i-1] + f[i-2])
    return f

def FiboRec(n):
    if(n <= 1):
        return 1
    else:
        return FiboRec(n-1)+ FiboRec(n-2)

def Degres(n):
    iterations = int(n/20) +1
    tableau = [[0] * iterations for _ in range(2)]
    for i in range(0,iterations):
        tableau[0][i] = i*20
        tableau[1][i] = int(((i*20)-32) * (5/9))
    return tableau

print(factoriel(10))
print(Cnp(3,10))
print(Anp(3,10))
print(Fibonnacci(7))
print (FiboRec(7))
print(Degres(300))
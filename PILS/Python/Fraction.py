'''
Created on 11 janv. 2020

@author: gresset6u
'''
class Fraction:
    def __init__(self,numerateur,denominateur):
        self.num = numerateur
        if(denominateur < 0):
            raise ValueError("Le denominateur doit etre positif")
        self.denom = denominateur
    
    def __add__(self,f):
        fAdd = Fraction(self.num*f.denom + f.num*self.denom,f.denom*self.denom)
        return fAdd
    
    def __repr__(self):
        return "%d/%d" % (self.num,self.denom)
    
try:
    f1 = Fraction(-5,5)
    f2 = Fraction(2,3)
    print (f1)
    print (f2)
    print(f1+f2)
except ValueError as Ve:
    print(Ve)


    
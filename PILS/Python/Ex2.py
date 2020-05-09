'''
Created on 11 janv. 2020

@author: gresset6u
'''
from random import randint

def SommeNEntiers(n):
    """Calcule la somme des n premiers entiers"""
    somme = 0
    for i in range(0,n):
        somme += i
    return somme

print(SommeNEntiers(100))

liste = "Python " * 10
print (liste)

listeAlea = []
for i in range(100):
    listeAlea.append(randint(0,100))
print (listeAlea)

listeAlea.sort()
print (listeAlea)

listeAlea.reverse()
print (listeAlea)

remplace = int(input("Valeur a remplacer"))
remplacement = int(input("Valeur remplacante"))
listeAlea = [remplacement if x==remplace else x for x in listeAlea]
print(listeAlea)

print(sum(listeAlea))

listeAlea = [x for x in listeAlea if x%2==0 ]
print (listeAlea)

annuaire = {}
nom = input("Nom")
tel = input("Numero de tel")
annuaire[nom] = tel
print (annuaire)
print(annuaire[nom])
annuaire[nom] = "0304040404"
print (annuaire)
annuaire.pop(nom)
print (annuaire)
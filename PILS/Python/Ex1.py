'''
Created on 11 janv. 2020

@author: gresset6u
'''

n = 2**64
print (n)

t = (quotient, reste) = divmod(32500,12)
print (quotient)
print (reste)
print (t)

annee = int(input("L'annee en ce jour"))
anneeNaiss = int(input("Votre annee de naissance"))
age = annee - anneeNaiss
print(age)

personne = (input("Votre nom"),input("Votre prenom"))
print (personne[0].upper(),personne[1].capitalize())

for i in range(100):
    print(i, end=', ')
print("")
for i in range(0,100,2):
    print(i, end=', ')
print("")
for i in range(1,100,2):
    print(i, end=', ')
print("")
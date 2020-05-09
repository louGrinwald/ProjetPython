'''
Created on 11 janv. 2020

@author: gresset6u
'''
from nt import listdir

def reverse(s):
    return s[::-1]

def isPalindrome(s):
    if(s == reverse(s)):
        return True
    else:
        return False

def explode(s):
    s2 = []
    for i in range(0,len(s)):
        s2.append(s[i])
    return s2

def repair(s):
    s2 = ""
    for i in range(0,len(s)):
        s2 += s.pop(0)
    return s2    

chemin = r"C:\\Temp"
print (chemin)
fichiers = listdir(chemin)
fichiers.sort()
print (fichiers)
print(isPalindrome("kayak"))
print(isPalindrome("leon noel"))
print(explode("Patate"))
print(repair(explode("Patate")))
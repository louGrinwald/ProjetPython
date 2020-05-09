from random import randint

class CompteBon:
    def __init__(self):
        self.operateurs = "+*/-"
        self.nbOperateur = 4
        self.nbNombreTirage = 6
        self.tabNombre = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,25,25,50,50,75,75,100,100]
        compteur = 0
        self.choisis = [0,0,0,0,0,0]
        self.operations = []
        self.total = randint(100, 999)
        i = 0
        while i < 6:
            compteur = 0
            tranz = self.tabNombre.pop(randint(0,len(self.tabNombre) - 1))
            go = True
            self.choisis[i] = tranz
            i+=1
        
        #while(self.compte(self.nombre, self.nbNombreTirage, total, compteur) == 0 and total > 0):
            #total = total - 1
            #print("Le compte exact est impossible a trouver, la solution qui se rapproche le plus est: ", total, "\n")
            
    def calcul(self,a,b,op):
        if self.operateurs.find(op) == -1:
            print("Erreur : operateur invalide : ", op, "\n")
        elif a not in self.choisis or b not in self.choisis:
            print("Erreur : chiffre non disponible ",a," et/ou ",b," dans ",self.choisis) 
        else:   
            resu = -1
            if op =="+":
                resu = a + b
            if op =="*":
                resu = a * b
            if op =="-":
                if b > a:
                    print("Operation non valide, nombre negatif : "+str(a)+" - "+str(b))
                else:    
                    resu = a - b
            if op =="/":
                if b == 0:
                    print("Operation non valide, division par zero")
                elif a % b != 0:
                    print("Operation non valide, division non entiere ; "+str(a)+" / "+str(b))
                else:
                    resu = a / b
            
            if resu != -1:
                self.choisis.remove(a)
                self.choisis.remove(b)
                self.choisis.append(resu)
                self.operations.append(str(a)+op+str(b)+"="+str(resu))
    
    def retour(self):
        if len(self.operations) > 0:
            oper = self.operations.pop(len(self.operations)-1)
            i = 0
            a=""
            b=""
            op=""
            resu=""
            while True:
                try:
                    int(oper[i])
                except ValueError as Ve: 
                    break
                a += oper[i]
                i+=1
            op = oper[i]
            while True:
                i+=1
                try:
                    int(oper[i])
                except ValueError as Ve: 
                    break
                b += oper[i]
            i+=1
            resu = oper[i:]
            
            self.choisis.remove(int(resu))
            self.choisis.append(int(a))
            self.choisis.append(int(b))
          
    def affichage(self):
        print("Le nombre a atteindre est ",self.total)
        oper = "Historique des operations : \n"
        for j in range(0,len(self.operations)):
            oper = oper + self.operations[j] + ", "
        print(oper[:-2])    #[:-2] pour enlever le dernier espace et la derniere virugule
        nombres = "Nombres disponibles : \n"
        for j in range(0,len(self.choisis)):
            nombres = nombres + str(self.choisis[j]) + ", "
        print(nombres[:-2])
        print("")
        

#des outils pour la fonction de solution        
APPLY = {'+': lambda a,b: a+b,
     '-': lambda a,b: a-b,
     '*': lambda a,b: a*b,
     '/': lambda a,b: a/b}
INVERSE = {'+': '-', '-': '+', '*': '/', '/': '*'}
 
#retourne toutes les solutions pour trouver le nombre target avec les nombres du tableau numbers
#----------------------------------ATTENTION, ELLE FAIT DES DIVISIONS PAS ENTIERES-----------------
def solve(target, numbers):
    if len(numbers) == 1:
        return [int(target)] if target == numbers[0] else []
    else:
        result = []
        for num in numbers:
            for op in '+-*/':
                try:
                    new_target = APPLY[INVERSE[op]](target, num)
                    for sol in solve(new_target,[n for n in numbers if n != num]):
                        result.append((op, sol, int(num)))
                except ZeroDivisionError:
                    pass
        return result

def format(expr):
    if isinstance(expr, int):
        return str(expr)
 
    op, a, b = expr
    if isinstance(a, int):
        return "%d %s %d" % (a, op, b)
    else:
        return "(%s) %s %d" % (format(a), op, b)
     

#Exemple
#c = CompteBon()
#c.affichage()
#c.calcul(c.choisis[2], c.choisis[0], "*")
#c.affichage()
#c.calcul(c.choisis[4], c.choisis[0], "-")
#c.affichage()
#c.retour()
#c.affichage()
#c.calcul(c.choisis[1], c.choisis[0], "/")
#c.affichage()

#for sol in solve(5, [5]):
#    print("5 =", format(sol))
#Une boucle qui donne toutes les solutions 
#for sol in solve(5, [3, 2]):
#    print ("5 =", format(sol))
#for sol in solve(21, [3, 2, 5]):
#    print ("21 =", format(sol))
#Cette fonction est incapable de combiner des nombres
#for sol in solve(32, [1, 1, 4, 4]):
#    print ("32 =", format(sol)) 
#Ou alors on donne la premiere solution trouvee
#print("72 =",format(solve(72, [3, 6, 2, 4])[0]))


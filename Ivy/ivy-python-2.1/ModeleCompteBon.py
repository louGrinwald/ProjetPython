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
        
    def compte(self,tabInt, nombre, total, compteur):
        compteur += 1
        for i in range(0, nombre -1):
            for j in range(i+1, nombre):
                for k in range(1, self.nbOperateur + 1):
                    t = tabInt
                    if k == 1:
                        t[i] += t[j]
                        if t[i] == total and nombre == 2:
                            print("Le compte est bon en ", compteur)
                            print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                            if nombre > 0:
                                t[j] = t[nombre - 1]
                            if(self.compte(t, nombre - 1, total, compteur)):
                                print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                            return 1
                    
                    if k == 2:
                        t[i] *= t[j]
                        if t[i] == total and nombre == 2:
                            print("Le compte est bon en ", compteur)
                            print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                            if nombre > 0:
                                t[j] = t[nombre - 1]
                            if(self.compte(t, nombre - 1, total, compteur)):
                                print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                            return 1 
                        
                    if k == 3:
                        go = True
                        if ((t[i] > t[j] and t[i] > 0 and t[j] > 0 and ((t[i] % t[j]) == 0))): 
                            t[i] = t[i] / t[j]
                        else:
                            go = False
                        if go:
                            if t[i] == total and nombre == 2:
                                print("Le compte est bon en ", compteur)
                                print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                                if nombre > 0:
                                    t[j] = t[nombre - 1]
                                if(self.compte(t, nombre - 1, total, compteur)):
                                    print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                                return 1
                            
                    if k == 4:
                        go = True
                        if (t[i] < t[j]):
                            t[i] = t[j] - t[i]
                        else:
                            t[i] -= t[j]
                        if t[i] == total and nombre == 2:
                            print("Le compte est bon en ", compteur)
                            print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                            if nombre > 0:
                                t[j] = t[nombre - 1]
                            if(self.compte(t, nombre - 1, total, compteur)):
                                print(tabInt[i], self.operateurs[k-1], tabInt[j], t[i])
                                return 1                                  
        
        return 0

#Exemple
c = CompteBon()
c.affichage()
c.calcul(c.choisis[2], c.choisis[0], "*")
c.affichage()
c.calcul(c.choisis[4], c.choisis[0], "-")
c.affichage()
c.retour()
c.affichage()
c.calcul(c.choisis[1], c.choisis[0], "/")
c.affichage()
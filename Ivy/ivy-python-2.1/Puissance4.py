
class grillePuissance4:
    def __init__(self):
        # 0 = vide, 1 = jaune, 2 = rouge
        self.tableau = [[0] * 7 for _ in range(7)]
        for i in range(0,7):
             for j in range(0,7):
                self.tableau[i][j] = 0
                self.tableau[1][j] = 0
        self.isJaune = 1
    
    def checkWin(self,ligne,colonne):
        couleur = self.tableau[ligne][colonne]
        gagne = 0
        
        chaine = 0
        for i in range(ligne-3,ligne+3):
            if(i >= 0 and i < 7):
                if(self.tableau[i][colonne] == couleur):
                    chaine = chaine +1
                    if(chaine == 4):
                        gagne = 1
                else:
                    chaine = 0
        if(gagne == 1):
            return True
        
        chaine = 0
        for i in range(colonne-3,colonne+3):
            if(i >= 0 and i < 7):
                #print("x,y = " + str(ligne) + "," + str(i))
                if(self.tableau[ligne][i] == couleur):
                    chaine = chaine +1
                    if(chaine == 4):
                        gagne = 1
                else:
                    chaine = 0
        if(gagne == 1):
            return True
        
        chaine = 0
        for i in range(-3,3):
            x = ligne + i
            y = colonne + i
            if(x >= 0 and x < 7 and y >= 0 and y < 7):
                if(self.tableau[x][y] == couleur):
                    chaine = chaine +1
                    if(chaine == 4):
                        gagne = 1
                else:
                    chaine = 0
        if(gagne == 1):
            return True
        
        chaine = 0
        for i in range(-3,3):
            x = ligne + i
            y = colonne - i
            if(x >= 0 and x < 7 and y >= 0 and y < 7):
                if(self.tableau[x][y] == couleur):
                    chaine = chaine +1
                    if(chaine == 4):
                        gagne = 1
                else:
                    chaine = 0
        if(gagne == 1):
            return True
        
        return False
    
    def Deposer(self,colonne):
        gagne = False
        for i in range(0,colonne):
            if(self.tableau[i][colonne] == 0):
                self.tableau[i][colonne] = self.isJaune
                gagne = self.checkWin(i,colonne)
                self.isjaune = self.isJaune + 1
                if(self.isJaune == 3):
                    self.isJaune == 2
                break
        return gagne

'''
f (x,y)



o.m (x,y)

O 
{
    def m (x,y):
        ...
}

m(o,x,y)

O
{
    def m (this,x,y):
        ...
}
'''
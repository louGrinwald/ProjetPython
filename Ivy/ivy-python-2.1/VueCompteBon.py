from tkinter import *
import queue
from functools import partial
plus = 0
moins = 1
fois = 2
diviser = 4

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # Create the queue
        self.queue = queue.Queue()
        # Set up the GUI part
        self.pack()
        self.createWidgets()
        self.running = 1
        # Start the periodic call in the GUI 
        self.periodicCall()


    def cleanLabel(self):
        self.labelA['text'] = "A"
        self.labelB['text'] = "B"
        self.labelOp['text'] = "op"  
        
    def addChiffre(self, i):
        if(self.labelA['text'] == 'A'):
            self.labelA['text'] = self.boutonsChiffres[i]['text']
            self.boutonsChiffres[i].config(state=DISABLED)
            return
        if(self.labelB['text'] == 'B'):             
            self.labelB['text'] = self.boutonsChiffres[i]['text']
            self.boutonsChiffres[i].config(state=DISABLED)

        
    def addOp(self, i):
        self.labelOp['text'] = self.boutonsOperateurs[i]['text']
        
    def annuler(self):
        #une seule operation
        if(self.historique.__len__() > 0):
            self.label_historique[self.historique.__len__() - 1]['text'] = ""
            self.historique.pop(self.historique.__len__() - 1)
            self.resultatHistorique.pop(self.resultatHistorique.__len__() - 1)
            if(self.boutonsHistorique.__len__() == 2):
                for i in range(6):
                    self.boutonsChiffres[i].config(state = NORMAL)
                    self.boutonsHistorique.clear()
                    self.cleanLabel()
            else:
                for i in range(6):
                    if(self.boutonsHistorique[self.boutonsHistorique.__len__() - 1] == self.boutonsChiffres[i]['text']):
                        self.boutonsChiffres[i].config(state = NORMAL)
                self.labelA['text'] = self.resultatHistorique[self.resultatHistorique.__len__() - 1]
                self.boutonsHistorique.pop(self.boutonsHistorique.__len__() - 1)
                self.labelOp['text'] = "op"
                self.labelB['text'] = "B"
                        
    def calculer(self):
        if(self.labelA['text'] == 'A' or self.labelB['text'] == 'B' or self.labelOp['text'] == 'op'):
            return
        a = int(self.labelA['text'])
        b = int(self.labelB['text'])
        op = self.labelOp['text']
        
        res = 0
        if(op == "+"):
            res = a + b
        if(op == "-"):
            res = a - b
            if(res < 0):
                return 
        if(op == "*"):
            res = a * b
        if(op == '/'):
            if(b >0):
                res = a / b
            else:
                return
         
        self.historique.append(str(a) + ' ' + str(op) + ' ' + str(b) + ' = ' + str(res))
        self.label_historique[int(self.historique.__len__() - 1)]['text'] = self.historique[int(self.historique.__len__() - 1)]
        self.resultatHistorique.append(res)

        #si on annule l'operation alors qu'il y en a qu'une seule dans l'historique
        #il faudra reinitialiser deux boutons et non un seul
        if(self.boutonsHistorique.__len__() == 0):
            self.boutonsHistorique.append(self.labelA['text'])
            self.boutonsHistorique.append(self.labelB['text'])            
        else:
            self.boutonsHistorique.append(self.labelB['text'])
        self.labelA['text'] = str(res)
        self.labelOp['text'] = 'op'
        self.labelB['text'] = 'B'
        
      
    def effacer(self):
        for i in range(6):
            if(self.labelA['text'] == self.boutonsChiffres[i]['text'] or self.labelB['text'] == self.boutonsChiffres[i]['text']):
                self.boutonsChiffres[i].config(state= NORMAL)
        self.labelOp['text'] = "op"
        self.labelB['text'] = 'B'
        if(self.resultatHistorique.__len__() == 0):
            self.labelA['text'] = 'A'

        
    def reset(self):
        a = 0
    def valider(self):
        if(self.labelN['text'] == self.labelA['text']):
            print("vous avez trouver")

    
    def createWidgets(self):
        self.boutonsChiffres = [0,0,0,0,0,0]
        for i in range(6):
            self.boutonsChiffres[i] = Button(self, text="10"+str(i),command=partial(self.addChiffre,i))
            self.boutonsChiffres[i].grid(row = 5,column = i+2)
            
        self.boutonsOperateurs = [0,0,0,0,0,0]   
        self.boutonsOperateurs[0] = Button(self, text="+",command= partial(self.addOp,0))
        self.boutonsOperateurs[0].grid(row = 4,column = 9, sticky = E+W)
        self.boutonsOperateurs[1] = Button(self, text="-",command= partial(self.addOp,1))
        self.boutonsOperateurs[1].grid(row = 4,column = 10, sticky = E+W)
        self.boutonsOperateurs[2] = Button(self, text="*",command=partial(self.addOp,2))
        self.boutonsOperateurs[2].grid(row = 4,column = 11, sticky = E+W)
        self.boutonsOperateurs[3] = Button(self, text="/",command=partial(self.addOp,3))
        self.boutonsOperateurs[3].grid(row = 4,column = 12, sticky = E+W)
        self.boutonsOperateurs[4] = Button(self, text="=",command=self.calculer)
        self.boutonsOperateurs[4].grid(row = 5,column = 9,columnspan = 2, sticky = E+W)
        self.boutonsOperateurs[5] = Button(self, text="C",command=self.effacer)
        self.boutonsOperateurs[5].grid(row = 5,column = 11,columnspan = 2, sticky = E+W)
        
        self.boutonAbandonner = Button(self, text="Abandonner",command=self.reset)
        self.boutonAbandonner.grid(row = 2,column = 9,columnspan = 4, sticky = E+W)
        self.boutonValider = Button(self, text="Valider",command=self.valider)
        self.boutonValider.grid(row = 3,column = 9,columnspan = 4, sticky = E+W)
        
        self.historique = []
        self.resultatHistorique = []
        self.boutonsHistorique = []
        self.label_historique = [0,0,0,0,0,0]
        for i in range(6):
            self.label_historique[i] = Label(self,text="")
            self.label_historique[i].grid(row = i,column = 0,columnspan = 2)
        self.boutonRetour = Button(self, text="Annuler la derniere operation",command=self.annuler)
        self.boutonRetour.grid(row = 5,column = 0, columnspan = 2)
        
        self.labelN = Label(self,text="100")
        self.labelN.grid(row = 0,column = 2,columnspan = 6, sticky = E+W)
        
        self.labelA = Label(self,text="A")
        self.labelA.grid(row = 2,column = 2,columnspan = 2, sticky = E+W)
        
        self.labelB = Label(self,text="B")
        self.labelB.grid(row = 2,column = 6,columnspan = 2, sticky = E+W)
        
        self.labelOp = Label(self,text="op")
        self.labelOp.grid(row = 2,column = 4,columnspan = 2, sticky = E+W)
        
        self.labelMode = Label(self,text="Mode de jeu :")
        self.labelMode.grid(row = 0,column = 9,columnspan = 2, sticky = E+W)
        self.labelModeActu = Label(self,text="Entrainement")
        self.labelModeActu.grid(row = 0,column = 11,columnspan = 2, sticky = E+W)
        self.labelTimer = Label(self,text="Timer : ")
        self.labelTimer.grid(row = 1,column = 9,columnspan = 2, sticky = E+W)
        self.labelTimerActu = Label(self,text="0.00")
        self.labelTimerActu.grid(row = 1,column = 11,columnspan = 2, sticky = E+W)
          
        
    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        while self.queue.qsize() != 0:
            action = self.queue.get(false, None)
            
        
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def endApplication(self):
        self.running = 0


root = Tk()
app = Application(root)
root.mainloop()

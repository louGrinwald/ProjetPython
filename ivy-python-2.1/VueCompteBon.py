from tkinter import *
from ModeleCompteBon import *
import queue
from functools import partial

class Vue(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        self.modele = CompteBon()
        
        # Create the queue
        self.queue = queue.Queue()
        # Set up the GUI part
        self.pack()
        self.createWidgets()
        self.running = 1
        # Start the periodic call in the GUI 
        self.periodicCall()
    
    def addChiffre(self, i):
        self.boutonsChiffres[i].config(state=DISABLED)
        a = 0
    def addOp(self):
        a = 0
    def annuler(self):
        a = 0
    def calculer(self):
        self.modele.affichage()
        self.modele.calcul(3,5,'+')
        self.modele.affichage()
    def effacer(self):
        a = 0
    def reset(self):
        a = 0
    def valider(self):
        a = 0
    
    def createWidgets(self):
        self.boutonsChiffres = [0,0,0,0,0,0]
        for i in range(6):
            self.boutonsChiffres[i] = Button(self, text="Chiffre "+str(i),command=partial(self.addChiffre,i))
            self.boutonsChiffres[i].grid(row = 5,column = i+2)
            
        self.boutonsOperateurs = [0,0,0,0,0,0]   
        self.boutonsOperateurs[0] = Button(self, text="+",command=self.addOp())
        self.boutonsOperateurs[0].grid(row = 4,column = 9, sticky = E+W)
        self.boutonsOperateurs[1] = Button(self, text="-",command=self.addOp())
        self.boutonsOperateurs[1].grid(row = 4,column = 10, sticky = E+W)
        self.boutonsOperateurs[2] = Button(self, text="*",command=self.addOp())
        self.boutonsOperateurs[2].grid(row = 4,column = 11, sticky = E+W)
        self.boutonsOperateurs[3] = Button(self, text="/",command=self.addOp())
        self.boutonsOperateurs[3].grid(row = 4,column = 12, sticky = E+W)
        self.boutonsOperateurs[4] = Button(self, text="=",command=self.calculer())
        self.boutonsOperateurs[4].grid(row = 5,column = 9,columnspan = 2, sticky = E+W)
        self.boutonsOperateurs[5] = Button(self, text="C",command=self.effacer())
        self.boutonsOperateurs[5].grid(row = 5,column = 11,columnspan = 2, sticky = E+W)
        
        self.boutonAbandonner = Button(self, text="Abandonner",command=self.reset())
        self.boutonAbandonner.grid(row = 2,column = 9,columnspan = 4, sticky = E+W)
        self.boutonValider = Button(self, text="Valider",command=self.valider())
        self.boutonValider.grid(row = 3,column = 9,columnspan = 4, sticky = E+W)
        
        self.historique = [0,0,0,0,0]
        for i in range(5):
            self.historique[i] = Label(self,text="Calcul")
            self.historique[i].grid(row = i,column = 0,columnspan = 2)
        self.boutonRetour = Button(self, text="Annuler la derniere operation",command=self.annuler())
        self.boutonRetour.grid(row = 5,column = 0, columnspan = 2)
        
        self.labelA = Label(self,text="N a trouver")
        self.labelA.grid(row = 0,column = 2,columnspan = 6, sticky = E+W)
        self.labelB = Label(self,text="A").grid(row = 2,column = 2,columnspan = 2, sticky = E+W)
        self.labelOp = Label(self,text="op").grid(row = 2,column = 4,columnspan = 2, sticky = E+W)
        self.labelN = Label(self,text="B").grid(row = 2,column = 6,columnspan = 2, sticky = E+W)
        self.labelMode = Label(self,text="Mode de jeu :").grid(row = 0,column = 9,columnspan = 2, sticky = E+W)
        self.labelModeActu = Label(self,text="Entrainement").grid(row = 0,column = 11,columnspan = 2, sticky = E+W)
        self.labelTimer = Label(self,text="Timer : ").grid(row = 1,column = 9,columnspan = 2, sticky = E+W)
        self.labelTimerActu = Label(self,text="0.00").grid(row = 1,column = 11,columnspan = 2, sticky = E+W)
        
        
    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        if self.queue.qsize() != 0:
            self.action = self.queue.get()
            print(self.action)
        
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def endApplication(self):
        self.running = 0


root = Tk()
app = Vue(root)
root.mainloop()

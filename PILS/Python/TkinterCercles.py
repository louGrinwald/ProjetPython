'''
Created on 27 janv. 2020

@author: gresset6u
'''

from tkinter import *
from tkinter import colorchooser
from random import *
from _overlapped import NULL

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        largeur = 600
        hauteur = 400
        self.canv = Canvas (self, width=largeur, height=hauteur)
        self.canv.bind('<Button-1>', self.PremierPlan)
        self.canv.pack()
        self.canv.boutonCreer = Button(self, text="Creer un cercle aleatoire",command=self.CreerCercle)
        self.canv.boutonCreer.pack(side = BOTTOM)
        self.canv.boutonCouleur = Button(self, text="Changer la couleur du cercle au premier plan",command=self.ChangerCouleur)
        self.canv.boutonCouleur.pack(side = BOTTOM)
        self.canv.boutonDeplacer= Button(self, text="Deplacer le cercle au premier plan",command=self.DemanderCoords)
        self.canv.boutonDeplacer.pack(side = BOTTOM)
    def CreerCercle(self):
        rnd = randrange(0,400)
        de=("%02x"%randrange(0,255))
        re=("%02x"%randrange(0,255))
        we=("%02x"%randrange(0,255))
        ge="#"
        color=ge+de+re+we
        '''2,2 est le x,y de depart, pas egal a 0 pour pas que ca colle la fenetre
           extent est l'angle du cercle
           style = ARC sinon le rayon est affiche
        '''
        self.canv.create_arc(2, 2, rnd, rnd, extent=359.9, style = ARC, outline = color, tags ="toplevel")
    def PremierPlan(self, event):
        print ("clicked at", event.x, event.y)
        obj = self.canv.find_withtag(CURRENT)
        if(len(obj) > 0):
            self.canv.tag_raise(CURRENT,"toplevel")
            self.canv.dtag(ALL,"toplevel")
            self.canv.itemconfig(CURRENT, tags="toplevel")
    def ChangerCouleur(self):
        obj = self.canv.find_withtag("toplevel")
        if(len(obj) > 0):
            (rgb,hx) = colorchooser.askcolor()
            if((rgb,hx) != None):
                self.canv.itemconfig(self.canv.find_withtag("toplevel"),outline = hx)
    def DemanderCoords(self):
        obj = self.canv.find_withtag("toplevel")
        if(len(obj) > 0):
            self.nouvX = Entry(self, width=20)
            self.nouvX.pack(side = BOTTOM)
            self.nouvY = Entry(self, width=20)
            self.nouvY.pack(side = BOTTOM)
            self.texte = Label(self,text="Entrer la nouvelle position du cercle")
            self.texte.pack(side = BOTTOM)
            self.OK = Button(self,"Valider",command=self.Deplacer(self,self.nouvX.get(),self.nouvY.get()))
            self.OK.pack(side = BOTTOM)
    def Deplacer(self,x,y,event):
        if(x.isdigit() & y.isdigit()):
            self.canv.move(self.canv.find_withtag("toplevel"),x,y)

root = Tk()
app = Application(master=root)
app.mainloop()








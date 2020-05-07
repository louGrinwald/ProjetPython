from tkinter import *
import re
import queue
from functools import partial
from ModeleCompteBon import *
import datetime
from ivy.std_api import *


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # Create the queue
        self.queue = queue.Queue()
        # Set up the GUI part
        self.pack()
        self.createWidgets()
        self.modele = CompteBon()
        self.recupModele(self.modele.choisis, self.modele.total)
        self.timerOn = True
        self.timerBase = datetime.timedelta(seconds=15)
        self.startTime = datetime.datetime.now() + self.timerBase
        self.running = 1
        # Start the periodic call in the GUI
        self.periodicCall()
        

    def recupModele(self,nombres,N):
        self.labelN["text"] = N
        for i in range(6):
            self.boutonsChiffres[i]['text'] = nombres[i]

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
        #ne fais rien si il n'y a pas d'operations
        if(self.historique.__len__() > 0):
            self.label_historique[self.historique.__len__() - 1]['text'] = ""
            self.historique.pop()
            self.resultatHistorique.pop()
            
            #-----------------------doubles detections ?------------------------
            for i in range(self.nextFreeButton):
                if(self.boutonsHistorique[self.boutonsHistorique.__len__() - 1] == self.boutonsChiffres[i]['text']):
                    self.boutonsChiffres[i].config(state=NORMAL)
                if(self.boutonsHistorique[self.boutonsHistorique.__len__() - 2] == self.boutonsChiffres[i]['text']):
                    self.boutonsChiffres[i].config(state=NORMAL)
            
            self.boutonsHistorique.pop()
            self.boutonsHistorique.pop()
                        
            self.nextFreeButton -= 1
            self.boutonsChiffres[self.nextFreeButton]['text'] = ""
            self.boutonsChiffres[self.nextFreeButton].config(state=DISABLED)
            self.cleanLabel()
                        
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
                if(not float(res).is_integer()):
                    return
                else:
                    res = int(res)
            else:
                return
         
        self.historique.append(str(a) + ' ' + str(op) + ' ' + str(b) + ' = ' + str(res))
        self.label_historique[int(self.historique.__len__() - 1)]['text'] = self.historique[int(self.historique.__len__() - 1)]
        self.resultatHistorique.append(res)
        self.boutonsHistorique.append(self.labelA['text'])
        self.boutonsHistorique.append(self.labelB['text'])
        self.cleanLabel() 
        
        self.boutonsChiffres[self.nextFreeButton]['text'] = res
        self.boutonsChiffres[self.nextFreeButton].config(state=NORMAL)
        self.nextFreeButton += 1
                   
      
    def effacer(self):
        for i in range(self.nextFreeButton):
            #-----------------------doubles detections ?------------------------
            if(self.labelA['text'] == self.boutonsChiffres[i]['text'] or self.labelB['text'] == self.boutonsChiffres[i]['text']):
                self.boutonsChiffres[i].config(state= NORMAL)
        self.cleanLabel()
    
    def showSolution(self, fInfos):
        choisis = [0,0,0,0,0,0]
        for i in range(6):
             choisis[i] = self.boutonsChiffres[i]['text']
             
        if(solve(self.labelN['text'],choisis)):
            print("Solution : ",self.labelN['text']," = ",format(solve(self.labelN['text'],choisis)[0]))
        self.trueReset(fInfos)
    
    def reset(self):
        for i in range(6*2):
            if(i < 6):
                self.boutonsChiffres[i].config(state=NORMAL)
                self.boutonsOperateurs[i].config(state=NORMAL) 
            else:
                self.boutonsChiffres[i]['text'] = ""
                self.boutonsChiffres[i].config(state=DISABLED)
        self.historique.clear()
        for i in range(5):
            self.label_historique[i]['text'] = ""
        self.resultatHistorique.clear()
        self.boutonsHistorique.clear()
        self.nextFreeButton = 6
        self.cleanLabel()
        self.startTime = datetime.datetime.now() + self.timerBase
        self.timerOn = True
    
    def generate(self):
        self.modele = CompteBon()
        self.recupModele(self.modele.choisis, self.modele.total)
    
    def trueReset(self, fInfos):
        fInfos.destroy()
        self.reset()
        self.generate()
    
    def abandon(self):
        #On cree un popup
        fInfos = Toplevel()          # Popup -> Toplevel()
        fInfos.title('Popup')
        label = Label(fInfos, text="Voulez-vous voir la solution ?")
        label.grid(row = 0,column = 0, columnspan = 2)
        oui = Button(fInfos, text='Oui', command=partial(self.showSolution,fInfos))
        oui.grid(row = 1,column = 0)
        non = Button(fInfos, text='Non', command=partial(self.trueReset,fInfos))
        non.grid(row = 1,column = 1)
        fInfos.transient(self)       # Reduction popup impossible 
        fInfos.grab_set()          # Interaction avec fenetre jeu impossible
        self.wait_window(fInfos)   # Arret script principal
            
    def valider(self):
        for i in range(self.nextFreeButton):
            if(self.labelN['text'] == self.boutonsChiffres[i]['text']):
                print("GAGNE")
                self.timerOn = False
                return
    '''     
    def duel(self):
        #Oncree un popup
        fInfos = Toplevel()          # Popup -> Toplevel()
        fInfos.title('Popup')
        Label(fInfos, text="Une invitation a ete envoyee a votre adversaire").pack(padx=10, pady=10)
        Button(fInfos, text='Quitter', command=fInfos.destroy).pack(padx=10, pady=10)
        fInfos.transient(self)       # Reduction popup impossible 
        fInfos.grab_set()          # Interaction avec fenetre jeu impossible
        self.wait_window(fInfos)   # Arret script principal
    '''
    
    def createWidgets(self):
        #Les boutons pour les chiffres initiaux et ceux qui seront crees au fur et a mesue
        self.boutonsChiffres = [0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(6*2):
            if(i < 6):
                self.boutonsChiffres[i] = Button(self, text="10"+str(i),command=partial(self.addChiffre,i))
                self.boutonsChiffres[i].grid(row = 5,column = i+2, sticky = E+W)
            else:
                self.boutonsChiffres[i] = Button(self, text="",command=partial(self.addChiffre,i))
                self.boutonsChiffres[i].grid(row = 4,column = i-6+2, sticky = E+W)
                self.boutonsChiffres[i].config(state=DISABLED)
        #On stocke l'index du prochain bouton pour les prochains chiffres a generer
        self.nextFreeButton = 6
            
        #Les boutons des operateurs
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
        #Les boutons d'action
        self.boutonAbandonner = Button(self, text="Abandonner",command=self.abandon)
        self.boutonAbandonner.grid(row = 2,column = 9,columnspan = 4, sticky = E+W)
        self.boutonValider = Button(self, text="Valider",command=self.valider)
        self.boutonValider.grid(row = 3,column = 9,columnspan = 4, sticky = E+W)
        #Les labels de l'historique des operations et le bouton pour evenir en arriere
        self.historique = []
        self.resultatHistorique = []
        self.boutonsHistorique = []
        self.label_historique = [0,0,0,0,0,0]
        for i in range(6):
            self.label_historique[i] = Label(self,text="")
            self.label_historique[i].grid(row = i,column = 0,columnspan = 2)
        self.boutonRetour = Button(self, text="Annuler la derniere operation",command=self.annuler)
        self.boutonRetour.grid(row = 5,column = 0, columnspan = 2)
        #Les labels  du chiffre a trouver et de l'operation en cours
        self.labelN = Label(self,text="100")
        self.labelN.grid(row = 0,column = 2,columnspan = 6, sticky = E+W)
        self.labelA = Label(self,text="A")
        self.labelA.grid(row = 2,column = 2,columnspan = 2, sticky = E+W)
        self.labelB = Label(self,text="B")
        self.labelB.grid(row = 2,column = 6,columnspan = 2, sticky = E+W)
        self.labelOp = Label(self,text="op")
        self.labelOp.grid(row = 2,column = 4,columnspan = 2, sticky = E+W)
        #Les labels du mode et du timer
        self.labelMode = Label(self,text="Mode de jeu :")
        self.labelMode.grid(row = 0,column = 9,columnspan = 2, sticky = E+W)
        self.labelModeActu = Label(self,text="Entrainement")
        self.labelModeActu.grid(row = 0,column = 11,columnspan = 2, sticky = E+W)
        self.labelTimer = Label(self,text="Timer : ")
        self.labelTimer.grid(row = 1,column = 9,columnspan = 2, sticky = E+W)
        self.labelTimerActu = Label(self,text="0.00")
        self.labelTimerActu.grid(row = 1,column = 11,columnspan = 2, sticky = E+W)
        #On cree deja  un tableau pour labels du multijoueur, on l'utilisera plu stard
        self.labelScore = []
          
    def trouveMulti(self):
        self.timerOn = False
        self.boutonRetour.config(state=DISABLED)
        self.boutonAbandonner.config(state=NORMAL)
        self.boutonsOperateurs[5].config(state=DISABLED)
        self.annuler()
        self.annuler()
        self.annuler()
        self.annuler()
        self.annuler()
        self.effacer()
        for i in range(6):
            self.boutonsChiffres[i]['command'] = partial(self.addChiffreMulti,i)
            self.boutonsChiffres[i+6]['command'] = partial(self.addChiffreMulti,i+6)
        for i in range(4):
            self.boutonsOperateurs[i]['command'] = partial(self.addOpMulti,i)
        self.boutonValider['command'] = self.validerMulti
        self.boutonAbandonner['command'] = self.failProof
        self.boutonsOperateurs[4]['command'] = self.preuve
        IvySendMsg("trouve")
        
    def addChiffreMulti(self,i):
        self.addChiffre(i)
        IvySendMsg("play:"+str(i))    
    
    def addOpMulti(self,i):
        self.addOp(i)
        IvySendMsg("play:"+str(self.boutonsOperateurs[i]['text']))
        
    def validerMulti(self):
        for i in range(self.nextFreeButton):
            if(self.labelN['text'] == self.boutonsChiffres[i]['text']):
                IvySendMsg("success")
                self.addPoint(0)
        
    def quitMulti(self):
        IvySendMsg("kill")
        self.resetToSinglePlayer()
        
    def resetToSinglePlayer(self):
        self.labelModeActu['text'] = "Entrainement"
        self.boutonRetour.config(state=NORMAL)
        self.boutonValider.config(state=NORMAL)
        self.boutonAbandonner.config(state=NORMAL)
        self.boutonQuitMulti.config(state=DISABLED)
        self.boutonValider['command'] = self.valider
        self.boutonAbandonner['command'] = self.abandon
        self.reset()
        self.generate()
        self.labelScore.clear()
            
    def preuve(self):
        self.calculer()
        IvySendMsg("compute")
        
    def failProof(self):
        IvySendMsg("fail")
        self.addPoint(1)
        
    def addPoint(self,i):
        #i = 0 si point pour moi, i= 1 si point pour mon adversaire
        self.labelScore[i+3]['text'] = str(int(self.labelScore[i+3]['text']) + 1)
        
    def changeTimer(self):
        secs = self.entrySecondes.get()
        mins = self.entryMinutes.get()
        if(secs.isdigit() and mins.isdigit()):
            self.timerBase = datetime.timedelta(seconds=int(secs),minutes=int(mins))
        IvySendMsg("timer:"+secs+","+mins)
        
    def watch_mode(self):
        self.timerOn = False
        self.boutonRetour.config(state=DISABLED)
        self.boutonValider.config(state=DISABLED)
        self.annuler()
        self.annuler()
        self.annuler()
        self.annuler()
        self.annuler()
        for i in range(6):
            self.boutonsChiffres[i].config(state=DISABLED)
            self.boutonsChiffres[i+6].config(state=DISABLED)
            self.boutonsOperateurs[i].config(state=DISABLED) 
    
    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        while self.queue.qsize() != 0:
            action = self.queue.get()
            if(action[:6] == "start:"):
                self.reset()
                self.boutonValider.config(state=NORMAL)
                self.boutonRetour.config(state=NORMAL)
                nombresRaw = re.findall('\d+', action)
                N = int(nombresRaw[0])
                nombresRaw.pop(0)
                for i in range(6):
                    nombresRaw[i] = int(nombresRaw[i])
                self.recupModele(nombresRaw, N)
                self.boutonAbandonner.config(state=DISABLED)
                self.boutonValider['command'] = self.trouveMulti
                #On cree la partie multijoueur de l'interface si elle n'existe pas
                if(not self.labelScore):
                    self.labelScore = [0,0,0,0,0]
                    self.labelModeActu['text'] = "Multijoueur"
                    self.labelScore[0] = Label(self,text="Scores :")
                    self.labelScore[0].grid(row = 0,column = 13,columnspan = 4, sticky = E+W)
                    self.labelScore[1] = Label(self,text="Vous")
                    self.labelScore[1].grid(row = 1,column = 13,columnspan = 2, sticky = E+W)
                    self.labelScore[2] = Label(self,text="Votre adversaire")
                    self.labelScore[2].grid(row = 1,column = 15,columnspan = 2, sticky = E+W)
                    self.labelScore[3] = Label(self,text="0")
                    self.labelScore[3].grid(row = 2,column = 13,columnspan = 2, sticky = E+W)
                    self.labelScore[4] = Label(self,text="0")
                    self.labelScore[4].grid(row = 2,column = 15,columnspan = 2, sticky = E+W)
                    self.boutonQuitMulti = Button(self, text="Quitter le multijoueur",command=self.quitMulti)
                    self.boutonQuitMulti.grid(row = 3,column = 13,columnspan = 4, sticky = E+W)
                    self.boutonChangeTimer = Button(self, text="Changer le timer",command=self.changeTimer)
                    self.boutonChangeTimer.grid(row = 4,column = 13,rowspan = 2, sticky = W+E+'n'+S)
                    self.entrySecondes = Entry(self)
                    self.entrySecondes.grid(row = 4,column = 14,columnspan = 2, sticky = E+W)
                    self.labelSec = Label(self,text=" secondes")
                    self.labelSec.grid(row = 4,column = 16, sticky = E+W)
                    self.entryMinutes = Entry(self)
                    self.entryMinutes.grid(row = 5,column = 14,columnspan = 2, sticky = E+W)
                    self.labelMinutes = Label(self,text=" minutes")
                    self.labelMinutes.grid(row = 5,column = 16, sticky = E+W)
                    self.pack()
            elif(action[:4] == "deco"):
                self.resetToSinglePlayer()
            elif(action[:5] == "watch"):
                self.watch_mode()
            elif(action[:3] == "op:"):
                i=0
                if(action[3] == "+"):
                    i = 0
                elif(action[3] == "-"):
                    i = 1
                elif(action[3] == "*"):
                    i = 2
                elif(action[3] == "/"):
                    i = 3
                self.addOp(i)
            elif(action[:7] == "nombre:"):
                i = int(action[7:])
                self.addChiffre(i)
            elif(action == "compute"):
                self.calculer()
                for i in range(6):
                    self.boutonsChiffres[i].config(state=DISABLED)
                    self.boutonsChiffres[i+6].config(state=DISABLED)
            elif(action == "success"):
                self.addPoint(1)
            elif(action == "fail"):
                self.addPoint(0)
            elif(action[:6] == "timer:"):
                nombresRaw = re.findall('\d+', action)
                self.timerBase = datetime.timedelta(seconds=int(nombresRaw[0]),minutes=int(nombresRaw[1]))
                print("Votre adversaire a change le timer : "+nombresRaw[0]+"s, "+nombresRaw[1]+" mins")
            else:
                print(action)
            
        if(self.timerOn):
            difference = self.startTime.replace(microsecond=0) - datetime.datetime.now().replace(microsecond=0)
            if(difference >= datetime.timedelta(seconds=0)):
                self.labelTimerActu.configure(text=difference)
        
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def endApplication(self):
        self.running = 0

'''
root = Tk()
app = Application(root)
root.mainloop()
'''
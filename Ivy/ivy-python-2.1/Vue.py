from tkinter import *
import queue

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
    
    def createWidgets(self):
        largeur = 740
        hauteur = 740
        self.canv = Canvas (self, width=largeur, height=hauteur)
        self.canv.bind('<Button-1>', self.Jouer)
        self.canv.bloquage = FALSE
        self.canv.pack()
        self.CreerCercles()
        
    def setBloquage(self,bloquage):
        self.canv.bloquage = bloquage
        
    def CreerCercles(self):
        self.canv.cercles = [[0] * 7 for _ in range(7)]
        for i in range(7):
            for j in range(7):
                    x = 20 + i*100
                    y = 20 + j*100
                    self.canv.cercles[i][j] = self.canv.create_oval(x ,y, x+90 ,y+90, outline = 'black')
        '''Tests
        self.ColorierCercle(2, 3, 'yellow')
        self.ColorierCercle(5, 2, 'red')
        '''
    def CreerBoutons(self):
        self.canv.boutons = []
        for i in range(7):
            self.canv.boutons[i] = Button(self, text="Colonne "+i,command=self.Jouer(i))
            self.canv.boutonCreer.pack(side = BOTTOM)

    def ColorierCercle(self, i, j, couleur):
        self.canv.itemconfig(self.canv.cercles[i][j], fill = couleur)

    def Jouer(self,event):
        if(self.canv.bloquage == FALSE):
            #print ("clicked at", event.x, event.y)
            colonne = 0
            for i in range(7):
                 x1 = 20 + i*100
                 x2 = x1 + 90
                 if(event.x >= x1 and event.x < x2):
                    colonne = i + 1
            print("Clique sur la colonne "+str(colonne))
            if(colonne != 0):
                #prevenir l'adaptateur
                colonne = 0

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        #
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
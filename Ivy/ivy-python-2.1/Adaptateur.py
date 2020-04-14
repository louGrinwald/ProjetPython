from Puissance4 import *
from IvySniffPuissance4 import *
from Vue import *

#On cree le modele, il est dans son etat initial
modele = grillePuissance4()

#on cree le sniffer, le premier a se connecter sera le joueur 1

#On cree la vue, elle demarre elle meme son loop
root = Tk()
app = Application(root)
root.mainloop()
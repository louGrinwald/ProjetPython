from ModeleCompteBon import *
#from IvySniffPuissance4 import *
from VueCompteBon import *

#On cree le modele, il est dans son etat initial
modele = CompteBon()

#On cree la vue, elle demarre elle meme son loop
root = Tk()
app = Application(root)
root.mainloop()
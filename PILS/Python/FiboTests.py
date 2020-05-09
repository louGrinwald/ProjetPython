'''
Created on 11 janv. 2020

@author: gresset6u
'''

import unittest
from Fibo import *

class TestFiboBase(unittest.TestCase):
    """ entrees et sorties basiques
    """
    def setUp(self): #appel´e avant chaque test
        self.n = 10
    def test_longueur(self): #commence par "test"
        """ bonne taille en sortie
        """
        for i in range(1,self.n):
            self.assertEqual(i,len(fibo(i)))
        
class TestFiboValeurs(unittest.TestCase):
    """ sorties correctes
    """
    def fonctionInterne(self): # ne commence pas par test
        return [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    def test_valeurs10(self):
        self.failUnless(fibo(10) == self.fonctionInterne())
        
suite = unittest.TestSuite() #construit une batterie de test
suite.addTest(unittest.makeSuite(TestFiboBase)) #ajout `a la batterie
suite.addTest(unittest.makeSuite(TestFiboValeurs))
    
unittest.TextTestRunner(verbosity=2).run(suite)
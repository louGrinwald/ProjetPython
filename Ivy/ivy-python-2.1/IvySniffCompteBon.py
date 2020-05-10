#!/usr/bin/env python
"""An ivyprobe script for ivy-python
"""
import os, string, sys, time, getopt
#sys.path.append ("F:\ivy-python-2.1")
from ivy.std_api import *
from ModeleCompteBon import *
from VueCompteBon import *
from random import randint

#On cree la vue en global
root = Tk()
app = Application(root)

#ces valeurs determinent qui est le joueur 1 et le joueur 2
joueur = 0
rnd = randint(0,100)
#Dans le cas ou les joueurs entrent le chiffre qu'ils peuvent atteindre, ils sont stockes
best = -1
bestAdv = -1
#Un indictauer d'etat pour les egalites
#2 = egalite, les deux joueurs vont jouer, 1 = egalite, plus qu'un joueur a jouer, 0 = pas d'egalite
egalite = 0
#On stocke le N courant pour ne pas avoir a le renseigner plus tard
NCourant = -1

try:
    import readline
except ImportError:
    pass

IVYAPPNAME = 'pyivyprobe'
    
def info(fmt, *arg):
    print (fmt % arg)
    return (fmt % arg)

def usage(cmd):
    usage = '''Usage: %s [options] regexps
Options:
\t-b, --ivybus=bus  defines the Ivy bus to join defaults to 127:2010
\t-h, --help        this message
\t-n, name          changes the name of the agent, defaults to %s
\t-V, --version     prints the ivy release number
\t-v, --verbose     verbose mode (twice makes it even more verbose)

Type '.help' in ivyprobe for a list of available commands.'''
    print (usage % ( os.path.basename(cmd), IVYAPPNAME ))


'''La fonction la pour savoir qui est le joueur 1 ou 2''' 
def on_connection_change(agent, event):
    if event == IvyApplicationDisconnected :
        info('Votre adversaire s est deconnecte : %r', agent)
        app.queue.put("deco")
    else:
        IvySendMsg("choose_player:"+str(rnd))
    info('Ivy applications currently on the bus: %s',
         ','.join(IvyGetApplicationList()))
    
def on_die(agent, *arg):
    IvyStop()    

def on_msg(agent, *arg):
    info('Received from %r: %s', agent, arg and str(arg) or '<no args>')

def on_direct_msg(agent, num_id, msg):
    info('%r sent a direct message, id=%s, message=%s',
         agent, num_id, msg)
    
def on_regexp_change(agent, event, regexp_id, regexp):
    from ivy.ivy import IvyRegexpAdded
    info('%r %s regexp id=%s: %s',
            agent, event==IvyRegexpAdded and 'added' or 'removed',
            regexp_id, regexp)

def on_trouve(agent, *arg):
    comm = str(arg[0])
    if(len(comm) > 6):
        app.queue.put("best_number:"+comm[7:])
    app.queue.put("watch")
        
def on_play(agent, *arg):
    op = str(arg[0])[5]
    
    if(op in "-*/+"):
        app.queue.put("op:"+op)
    else:
        app.queue.put("nombre:"+str(arg[0])[5:])
    
def on_compute(agent, *arg):
    app.queue.put("compute")
    
def on_erase(agent, *arg):
    app.queue.put("erase")
    
def on_kill(agent, *arg):
    IvySendMsg("die")
    
def on_fail(agent, *arg):
    global egalite
    global best
    if(egalite == 2):
        egalite = 1
        app.queue.put("best_number:"+str(best))
        app.queue.put("proof")
        IvySendMsg("trouve:"+str(best))
    elif(egalite == 1):
        egalite = 0
        IvySendMsg("new_game")
    else:
        app.queue.put("pointMe")
        IvySendMsg("pointHim")
        IvySendMsg("new_game")

def on_success(agent, *arg):
    global egalite
    global best
    app.queue.put("pointHim")
    IvySendMsg("pointMe")
    if(egalite == 2):
        egalite = 1
        app.queue.put("best_number:"+str(best))
        app.queue.put("proof")
        IvySendMsg("trouve:"+str(best))
    else:
        IvySendMsg("new_game")
        
def on_pointMe(agent, *arg):
    app.queue.put("pointMe")
    
def on_pointHim(agent, *arg):
    app.queue.put("pointHim")
    
def on_timer_end(agent, *arg):
    info("Vous avez gagne")
    info('Sent to %s peers'%IvySendMsg('Vous avez perdu'))
    
def on_start(agent, *arg):
    global NCourant
    nombresRaw = re.findall('\d+', str(arg[0]))
    NCourant = int(nombresRaw[0])
    app.queue.put(str(arg[0]))
    info("Que la partie commence !")
    IvySendMsg('Que la partie commence !')
    
def on_choose_player(agent, *larg):
    nombre = int(str(larg[0])[14:])
    global rnd
    global joueur
    if(rnd > nombre):
        joueur = 1
    elif(rnd == nombre):
        rnd = randint(0,100)
        IvySendMsg("choose_player:"+str(rnd))
    else:
        joueur = 2
        IvySendMsg("new_game")
    print("Je suis le joueur "+str(joueur))
    
def on_new_game(agent, *larg):
    global joueur
    if(joueur == 1):
        modele = CompteBon()
        nombres = modele.choisis
        N = modele.total
        global NCourant
        NCourant = N
        global bestAdv
        bestAdv = -1
        global best
        best = -1
        #On prepare la chaine de caracteres
        commande = "start:"+str(N)+","
        for i in range(6):
            commande += str(nombres[i])+","
        commande = commande[:-1]
        #On transmet a la vue et a notre adversaire
        app.queue.put(commande)
        IvySendMsg(commande)
    elif(joueur == 2):
        IvySendMsg("new_game")
    else:
        print("Je suis le joueur "+joueur+" ,ceci pose donc un petit probleme")
        
def on_timer(agent, *arg):
    app.queue.put(str(arg[0]))
    
def on_bestAdv(agent, *arg):
    global bestAdv
    bestAdv = int(str(arg[0])[8:])
    IvySendMsg("best:"+str(bestAdv))
    
def on_best(agent, *arg):
    global bestAdv
    global best
    global NCourant
    global egalite
    
    best = int(str(arg[0])[5:])
    if(bestAdv != -1):
        diffBest = abs(best - NCourant)
        diffBestAdv = abs(bestAdv - NCourant)
        print("diffBest : "+str(diffBest)+", diffBestAdv : "+str(diffBestAdv))
        if(diffBestAdv > diffBest):
            app.queue.put("best_number:"+str(best))
            app.queue.put("proof")
            IvySendMsg("trouve:"+str(best))
        elif(diffBestAdv == diffBest):
            egalite = 2
            on_trouve(agent,"trouve:"+str(bestAdv))
            IvySendMsg("proof:"+str(bestAdv))
        elif(diffBestAdv < diffBest):
            on_trouve(agent,"trouve:"+str(bestAdv))
            IvySendMsg("proof:"+str(bestAdv))
        else:
            print(str(diffBestAdv)+","+str(diffBest))
    else:
        app.queue.put("watch")

def on_proof(agent, *arg):
    app.queue.put("best_number:"+str(arg[0])[6:])
    app.queue.put("proof")

def on_any(agent, *larg):
    info( "%s ", larg[0])
    
#la boucle du sniffer
def task():
    
    '''
    try:
        msg = input('')
    except (EOFError, KeyboardInterrupt):
        msg = '.quit'

    if msg == '.help':
        info("""Available commands:
    .bind 'regexp'              - add a msg to receive. The displayed index
                                                 can be supplied to .remove
    .die appname                - send die msg to appname
    .dieall-yes-i-am-sure       - send die msg to all applications
    .direct appname id arg      - send direct msg to appname
    .help                       - print this message
    .error appname id err_msg   - send an error msg to an appname
    .quit                       - terminate this application
    .remove idx                 - remove a binding (see .bind, .regexps)
    .regexps                    - show current bindings
    .regexps appname            - show all bindings registered for appname
    .showbind                   - show/hide bindings (toggle)
.   .where appname              - print the host for appname
    .who                        - display the names of all applications on
                                                                   the bus

Everything that is not a command is interpreted as a message and sent to the
appropriate applications on the bus.
""")
              
    elif msg[:5] == '.bind':
        regexp = msg[6:]
        if not regexp:
            print ('Error: missing argument')
        info('Bound regexp, id: %d', IvyBindMsg(on_msg, regexp))
        
    elif msg == '.die-all-yes-i-am-sure':
        app_names = IvyGetApplicationList()
        if not app_names:
            info('No application on the bus')
        
        for app_name in IvyGetApplicationList():
            app = IvyGetApplication(app_name)
            if not app:
                info('No application %s'%app_name)
            else:
                IvySendDieMsg(app)
    
    elif msg[:4] == '.die':
        app_name = msg[5:]
        app = IvyGetApplication(app_name)
        if app is None:
            info('No application named %s', app_name)
        IvySendDieMsg(app)
        
    elif msg[:7] == '.direct':
        try:
            app_name, num = msg[8:].split()[:2]
            arg = ' '.join(msg[8:].split()[2:])
            if not arg:
                raise ValueError
        except ValueError:
            print ('Error: wrong number of parameters')

        app = IvyGetApplication(app_name)
        if app is None:
            info('No application named %s', app_name)

        IvySendDirectMsg(app, num, arg)

    elif msg[:6] == '.error':
        try:
            app_name, num = msg[7:].split()[:2]
            err_msg = ' '.join(msg[7:].split()[2:])
            if not err_msg:
                raise ValueError
        except ValueError:
            print ('Error: wrong number of parameters')

        app = IvyGetApplication(app_name)
        if app is None:
            info('No application named %s', app_name)

        IvySendError(app, num, err_msg)

    elif msg[:7] == '.remove':
        try:
            regexp_id = int(msg[8:])
            info('Removed %d:%s', regexp_id, IvyUnBindMsg(regexp_id))
        except KeyError:
            info('No such binding')
        except ValueError:
            info('Error: expected an integer')
            
    elif msg[:8] == '.regexps':
        app_name = msg[9:]
        app = IvyGetApplication(app_name)
        if app is None:
            from ivy import std_api
            info('Our subscriptions: %s',
                   ', '.join(["%s:'%s'"%(id,regexp) for id,regexp in std_api._IvyServer.get_subscriptions()]))
        else:
            info('Subscriptions for %s: %s',
                   app_name, ', '.join(["%s:'%s'"%(id,regexp) for id,regexp in IvyGetApplicationMessages(app)]))
            
    elif msg[:9] == '.showbind':
        if not showbind:
            IvyBindRegexpChange(on_regexp_change)
            showbind=1
            info("Changes in applications' bindings are now shown")
        else:
            IvyBindRegexpChange(void_function)
            showbind=0
            info("Changes in applications' bindings are now hidden")
            
    elif msg == '.quit':
        IvyStop()
    
    elif msg[:6] == '.where':
        app_name = msg[7:]
        app = IvyGetApplication(app_name)
        if app is None:
            info('No application named %s', app)
        info('Application %s on %s:%s',app_name, app.ip, app.port)
        
    elif msg == '.who':
        print (IvyGetApplicationList())
        
    else:
        info('Sent to %s peers'%IvySendMsg(msg))
    '''
    root.after(2000, task)


if __name__ == '__main__':
    from ivy.ivy import ivylogger
    import logging

    ivybus = ''
    readymsg = '[%s is ready]' % IVYAPPNAME
    verbose=0
    showbind=0
    
    ivylogger.setLevel(logging.WARN)

    try:
        optlist, left_args = \
                 getopt.getopt(sys.argv[1:],
                               'hb:n:Vv',
                               ['help','ivybus=','name=','version','verbose'])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(2)
    for opt, arg in optlist:
        if opt in ('-h', '--help'):
            usage(sys.argv[0])
            sys.exit()
        elif opt in ('-b', '--ivybus'):
            ivybus = arg
        elif opt in ('-V', '--version'):
            import ivy
            info('ivyprobe supplied with ivy-python library version%s',
                   ivy.__version__)
        elif opt in ('-v', '--verbose'):
            if not verbose:
                ivylogger.setLevel(logging.INFO)
                verbose+=1
            elif verbose==1:
                ivylogger.setLevel(logging.DEBUG)
                verbose+=1
            else:
                if hasattr(logging, 'TRACE'):
                    ivylogger.setLevel(logging.TRACE)
        elif opt in ('-n', '--name'):
            IVYAPPNAME=arg

    info('Broadcasting on %s',
         ivybus or os.environ.get('IVYBUS') or 'ivydefault')

    # initialising the bus 
    IvyInit(IVYAPPNAME,            # application name for Ivy
            readymsg ,             # ready message
            0,                     # parameter ignored
            on_connection_change,  # handler called on connection/deconnection
            on_die                 # handler called when a die msg is received 
            )

    # starting the bus
    IvyStart(ivybus)

    # bind the supplied regexps
    for regexp in left_args:
        IvyBindMsg(on_msg, regexp)
        
    '''
    Les messages valides sont :
    trouve(:452)               quand un joueur pense avoir trouve la solution, le nombre est seulement precise si le timer s'est ecoule
    play:3 / play:+            lors du mode attente -> affichage d'un chiffre ou operateur
    compute                    declencher le calcul lors ud mode attente
    erase                      declencher le bouton C lors ud mode attente
    start:N,C1,C2,C3,C4,C5,C6  au debut pour donner le modele
    timer_end                  lorsque le timer tombe a 0
    fail                        le joueur adverse n'a pas reussi a prouver son nombre
    success                     Le joueur adverse a reussi a prouver son nombre
    choose_player               determine qui est le joueur 1
    new_game                    genere un modele pour une nouvelle partie multijoueur
    kill                        pour tuer l'autre apllication
    timer:25,2                  Si on change le timer (secs,mins)
    bestAdv:452                 Indique le meilleur chiffre que votre adversaire peut atteindre
    best:452                    Indique le meilleur chiffre que vous pouvez atteindre
    proof:452                   Vous devez prouvez ce chiffre
    pointMe                     Indique que j'ai gagne un point
    pointHim                    Indique que mon adversaire a gagne un point
    Tout autre message sera simplement affiche dans la console
    '''
    IvyBindMsg(on_trouve, '^(trouve:?[0-9]*?)$')
    IvyBindMsg(on_play, '^(play:[0-9+\-*\/]*)$')
    IvyBindMsg(on_compute, '^compute$')
    IvyBindMsg(on_erase,'^erase$')
    IvyBindMsg(on_start, '^(start:[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*,[0-9]*)$')
    IvyBindMsg(on_timer_end, '^timer_end$')
    IvyBindMsg(on_fail, '^(fail)$')
    IvyBindMsg(on_success, '^(success)$')
    IvyBindMsg(on_choose_player, '^(choose_player:[0-9]*)$')
    IvyBindMsg(on_new_game, '^new_game$')
    IvyBindMsg(on_kill, '^kill$')
    IvyBindMsg(on_timer, '^(timer:[0-9]*,[0-9]*)$')
    IvyBindMsg(on_bestAdv, '^(bestAdv:[0-9]*)$')
    IvyBindMsg(on_best, '^(best:[0-9]*)$')
    IvyBindMsg(on_proof, '^(proof:[0-9]*)$')
    IvyBindMsg(on_pointMe, '^pointMe$')
    IvyBindMsg(on_pointHim, '^pointHim$')
    IvyBindMsg(on_die, '^die$')
    IvyBindMsg(on_any, "(.*)")

    # direct msg
    IvyBindDirectMsg(on_direct_msg)

    # Ok, time to go
    time.sleep(0.5)
    
    #On lance la boucle de la vue et celle du sniffer
    root.after(2000, task)
    root.mainloop()
    
    info('Fin')

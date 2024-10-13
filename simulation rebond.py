import pygame as py
import math
import matplotlib.pyplot as plt
import numpy as np

py.init()
py.mixer.init()
# py.display.set_caption("simulation rebond")

unite=200

g=9.81


blanc=(255,255,255)
noir=(0,0,0)

coef_restitution=0.8

class Balle:
    def __init__(self,pos,masse,rayon,couleur):
        self.masse=masse
        self.rayon=rayon
        self.couleur=couleur

        self.vitesse=[0,0]
        self.pos=pos
        self.acceleration=[0,0]

        self.dico_forces={"gravite":[0,g*unite]}

class Sol:
    def __init__(self,fonction):
        self.fonction=fonction
        self.liste_points_abscisses=[]
        self.liste_points_ordonnees=[]

        self.liste_points=[]

        self.nb_points=600


    def initialiser_proprietes(self):

        for x in self.liste_points_abscisses:
            y=self.fonction(x)
            self.liste_points_ordonnees.append(y)
            self.liste_points.append([x,y])

        # print(self.liste_points)


class Simulation:
    def __init__(self):
        self.temps=0
        self.liste_balles=[]
        self.sol=None

        self.liste_temps=[]
        self.liste_vitesses=[]

        self.dt=1/500

class Affichage:
    def __init__(self,simulation,facteur):
        self.simulation=simulation
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)
        self.fps=500

        # self.son=py.mixer.Sound("C:\\Users\\olivi\\Documents\\Audacity\\flashlight_off.mp3")

    def creer_balle(self,pos,masse,rayon,couleur):
        balle=Balle(pos,masse,rayon,couleur)
        self.simulation.liste_balles.append(balle)

    def creer_sol(self,fonction):
        self.simulation.sol=Sol(fonction)
        self.simulation.sol.liste_points_abscisses=np.linspace(0,self.dimensions[0],self.simulation.sol.nb_points)
        self.simulation.sol.initialiser_proprietes()


    def mettre_a_jour_balles(self):
        for balle in self.simulation.liste_balles:
            self.mettre_a_jour_balle(balle)

    def mettre_a_jour_balle(self,balle):

        balle.acceleration[0]=sum([balle.dico_forces[cle][0]/balle.masse for cle in balle.dico_forces])
        balle.acceleration[1]=sum([balle.dico_forces[cle][1]/balle.masse for cle in balle.dico_forces])




        balle.vitesse=[
        balle.vitesse[0]+balle.acceleration[0]*self.simulation.dt,
        balle.vitesse[1]+balle.acceleration[1]*self.simulation.dt
        ]

        balle.pos=[
        balle.pos[0]+balle.vitesse[0]*self.simulation.dt,
        balle.pos[1]+balle.vitesse[1]*self.simulation.dt
        ]

        if self.verifier_collision_sol(balle):
            norme_vitesse=math.sqrt((balle.vitesse[0]**2)+(balle.vitesse[1]**2))
            # if norme_vitesse>0.7*unite:
            #     self.son.play()


            # while self.verifier_collision_sol(balle):
            balle.pos[0]-=balle.vitesse[0]*self.simulation.dt
            balle.pos[1]-=balle.vitesse[1]*self.simulation.dt
            # balle.pos[1]-=balle.vitesse[1]*self.simulation.dt/2




            # n=[
            # self.derivee_fonction(self.simulation.sol.fonction,balle.pos[0]),
            # self.derivee_fonction(self.simulation.sol.fonction,balle.pos[0])
            # ]
            # norme=math.sqrt(n[0]**2+n[1]**2)



            angle=math.atan(self.derivee_fonction(self.simulation.sol.fonction,balle.pos[0])/(self.derivee_fonction(self.simulation.sol.fonction,balle.pos[0])+.000001))





            # balle.vitesse[0]=unite*n[0]*norme_vitesse*coef/norme

            # print(self.derivee_fonction(self.simulation.sol.fonction,balle.pos[0]))
            if self.derivee_fonction(self.simulation.sol.fonction,balle.pos[0])<0:
                balle.vitesse[0]=norme_vitesse*math.cos(angle)*coef_restitution
            else:
                balle.vitesse[0]=-norme_vitesse*math.cos(angle)*coef_restitution

            balle.vitesse[1]=-norme_vitesse*math.sin(angle)*coef_restitution

            # balle.vitesse[1]=n[1]*norme_vitesse*coef_restitution/(norme)

            # print(n[1])
            # print(norme_vitesse)
            # print(balle.vitesse[1])

    def derivee_fonction(self,fonction,x):
        h=1e-10
        return -((fonction((x+h))-fonction(x))/h)

    def verifier_collision_sol(self,balle):
        return balle.pos[1]+balle.rayon>=self.simulation.sol.fonction(balle.pos[0])

    def dessiner_balles(self):
        for balle in self.simulation.liste_balles:
            self.dessiner_balle(balle)

    def dessiner_balle(self,balle):
        py.draw.circle(self.fenetre,balle.couleur,balle.pos,balle.rayon)

    def dessiner_sol(self):
        longueur_liste=len(self.simulation.sol.liste_points)
        for i in range(longueur_liste-1):
            py.draw.line(self.fenetre,noir,self.simulation.sol.liste_points[i],self.simulation.sol.liste_points[i+1],2)

    def dessiner_echelle(self):
        py.draw.line(self.fenetre,noir,[0,0],[0,unite],10)




    def loop(self):
        horloge=py.time.Clock()


        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False
            horloge.tick(self.fps)
            py.display.set_caption(str(round(horloge.get_fps(),1)))


            self.fenetre.fill(blanc)


            self.simulation.liste_temps.append(self.simulation.temps)
            self.simulation.temps+=self.simulation.dt

            # self.simulation.liste_vitesses.append(self.simulation.liste_balles[0].vitesse)


            self.mettre_a_jour_balles()


            self.dessiner_balles()
            self.dessiner_sol()
            self.dessiner_echelle()

            py.display.flip()

        py.quit()

        # plt.close()
        # plt.plot(self.simulation.liste_temps,self.simulation.liste_vitesses)
        # plt.show()





simulation=Simulation()



facteur=0.8
affichage=Affichage(simulation,facteur)


# coef=0.9
# offset=4.33

offset=math.pi/2
coef=0.5
def f(x):
    # return(0.6*(x-5)**2)
    return (math.sin(5*x/coef-2.5)+math.cos(2*x/coef))*0.5+offset+(x-4)**2
    # return(0.2*x+3)
    # return (-math.sqrt(abs(1-(x/coef-offset)**2))+1)*coef+1.5


def f_corrigee(f):  # prend grosses abscisses et renvoie grosses abscisses
    return lambda x: (affichage.dimensions[1]-f(x/unite)*unite)

# C:\Users\olivi\Documents\Audacity


affichage.creer_balle([850,100],1,7,(0,0,255))
affichage.creer_balle([882,100],1,7,(255,0,0))
affichage.creer_balle([884,100],1,7,(0,255,0))
affichage.creer_balle([860,100],1,7,(0,100,200))
affichage.creer_balle([840,100],1,7,(150,100,0))
affichage.creer_balle([830,100],1,7,(0,100,100))
affichage.creer_sol(f_corrigee(f))

affichage.loop()
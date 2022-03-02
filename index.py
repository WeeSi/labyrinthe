from turtle import width
from numpy.random import randint
import matplotlib.pyplot as plt

## Création de la classe pile
class Pile:

    ## On initialise un tableau a vide
    def __init__(self):
        self.list = []

    ## Méthode pout tester si la liste est vide ou non
    def is_empty(self):
        return self.list == []

    ## Méthode pour ajouter un a élément a la liste
    def push(self, arg):
        self.list.append(arg)

    ## Méthode pour enlevé le dernier élément de la liste, 
    ## On va regarder si la pile est vide ou pas
    def pop(self):
        if(self.is_empty()):
            raise ValueError("Pile empty")
        return self.list.pop()

## Ici on crée une variable qui va contenir notre instanciation de la classe pile
## On va ajouter les coordonnées des cases déjà parcourures, pour chaque case entrant dans la pile son etat passe a False
## Puis direction la case voisine (son etat est encore a true)
## Si on est sur une impasse, la case est alors sortie de la pile, on recommence avec le sommet suivant
def explore(laby):
    pile = Pile()
    pile.push((0, laby.q - 1))
    laby.tab[0][laby.q - 1].etat = False
    while True:
        i, j = pile.pop()
        if i == laby.p - 1 and j == 0:
            break
        if j > 0 and laby.tab[i][j].S and laby.tab[i][j-1].etat:
            pile.push((i, j))
            pile.push((i, j-1))
            laby.tab[i][j-1].etat = False
        elif i < laby.p-1 and laby.tab[i][j].E and laby.tab[i+1][j].etat:
            pile.push((i, j))
            pile.push((i+1, j))
            laby.tab[i+1][j].etat = False
        elif j < laby.q-1 and laby.tab[i][j].N and laby.tab[i][j+1].etat:
            pile.push((i, j))
            pile.push((i, j+1))
            laby.tab[i][j+1].etat = False
        elif i > 0 and laby.tab[i][j].W and laby.tab[i-1][j].etat:
            pile.push((i, j))
            pile.push((i-1, j))
            laby.tab[i-1][j].etat = False
    return pile.list

## Création de la classe Case contenant les coordonées N,W,S,E (NORTH, WEST, SOUTH, EAST) et l'état de la case. 
## Initialisation a Faux de base
class Case:
    def __init__(self):
        self.N = False
        self.W = False
        self.S = False
        self.E = False
        self.etat = False

## Création de la classe Labyrinthe, on rappel que self est l'instance de notre objet cible
## On va attribuer des proprietés p,q,tab a self et leur donner des valeurs
class Labyrinthe:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.tab = [[Case() for j in range(q)] for i in range(p)]

    ## Cette méthode est utilisé pour tracer la grille du labyrinthe, on utilisate la librairie matplot qui va nous tracer les lignes
    ## On boucle sur l'axe des abscises (p) et l'axe des ordonées (q), nos lignes seront de la couleur verte (g)
    def show(self):
        plt.plot([0, 0, self.p, self.p, 0], [
                 0, self.q, self.q, 0, 0], 2)
        for i in range(self.p - 1):
            for j in range(self.q):
                if not self.tab[i][j].E:
                    plt.plot([i+1, i+1], [j, j+1], 'g')
        for j in range(self.q - 1):
            for i in range(self.p):
                if not self.tab[i][j].N:
                    plt.plot([i, i+1], [j+1, j+1], 'g')

        plt.axis([-1, self.p + 1, -1, self.q+1])
        plt.show()

    ## Ici on crée une méthode solution qui va appeler la méthode explore, sol est notre variable qui va contenir notre grille et les cases
    ## on va boucler sur notre grille et ajouter nos coordonée i a la variable X et j a la variable Y
    ## Une fois notre boucle fini on va créer une premiere même dimmesion a X et Y puis tracer la ligne (k => couleur noir) avec plt.plot puis afficher le labyrinthe
    def solution(self):
        sol = explore(self)
        X, Y = [], []
        for (i, j) in sol:
            X.append(i+.5)
            Y.append(j+.5)
        X.append(self.p-.5)
        Y.append(.5)
        plt.plot(X, Y, 'k', 2)
        self.show()

## Dans cette fonction on créer une liste v, contenant la liste des voisiins non réunins au labyrinthe
## La direction (c) est tiré au hasard parmi la liste v, le labyrinthe sera donc générer 'aléatoirement'
def creation(p, q):
    laby = Labyrinthe(p, q)
    pile = Pile()
    i, j = randint(p), randint(q) 
    pile.push((i, j)) 
    laby.tab[i][j].etat = True 
    while not pile.is_empty():
        i, j = pile.pop()
        v = []
        if j < q-1 and not laby.tab[i][j+1].etat:
            v.append('N')
        if i > 0 and not laby.tab[i-1][j].etat:
            v.append('W')
        if j > 0 and not laby.tab[i][j-1].etat:
            v.append('S')
        if i < p-1 and not laby.tab[i+1][j].etat:
            v.append('E') 
        if len(v) > 1:
            pile.push((i, j)) 
        if len(v) > 0:
            c = v[randint(len(v))] 
            if c == 'N':
                laby.tab[i][j].N = True
                laby.tab[i][j+1].S = True
                laby.tab[i][j+1].etat = True 
                pile.push((i, j+1))
            elif c == 'W':
                laby.tab[i][j].W = True 
                laby.tab[i-1][j].E = True 
                laby.tab[i-1][j].etat = True 
                pile.push((i-1, j))
            elif c == 'S':
                laby.tab[i][j].S = True 
                laby.tab[i][j-1].N = True 
                laby.tab[i][j-1].etat = True 
                pile.push((i, j-1))
            else:
                laby.tab[i][j].E = True 
                laby.tab[i+1][j].W = True 
                laby.tab[i+1][j].etat = True 
                pile.push((i+1, j))
    return laby


laby = creation(60,50)
laby.solution()
#!/usr/bin/env python3

###############################################################
#                                                             #
# MATH202: Mathématiques pour le numérique II                #
#                                                             #
# Mini bibliothèque pour manipuler des images au format PPM.  #
#                                                             #
# Auteur: Xavier Provençal, Pierre Hyvernat                  #
#                                                             #
###############################################################


from collections import deque


class Image:

    pixels = None
    height = 0
    width = 0

    def __init__(self, *args):
        if len(args) == 0:
            raise ValueError("Nécessite un nom de fichier ou des dimensions")
        if isinstance(args[0], str):
            self._init_from_file(args[0])
        else:
            self._init_from_size(*args)

    def _init_from_file(self, filename):
        # Validation du fichier
        f = open(filename, 'r')
        firstLine = f.readline()
        if firstLine != "P3\n":
            raise ValueError("[IMAGE] Initialisation depuis un fichier incompatible")
        # Lecture des données
        d = deque()
        for l in f.readlines():
            if l[0] != '#':
                d.extend(map(int, l.split()))
        self.width = d.popleft()
        self.height = d.popleft()
        d.popleft()     # on ignore la valeur max, on prend 255
        self.pixels = list(d)

    def _init_from_size(self, *args):
        if len(args) >= 2 and isinstance(args[0], int) and isinstance(args[1], int):
            self.width = args[0]
            self.height = args[1]
        else:
            raise ValueError("Nécessite un nom de fichier ou des dimensions")
        if len(args) >= 3 and len(args[2]) == 3:
            c = list(args[2])     # tuple or list of size 3
        else:
            c = [255, 255, 255]  # default value
        self.pixels = self.width*self.height*c

    def __str__(self):
        return "Image de dimensions {} x {}".format(self.width, self.height)

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        l = [self.width, self.height] + self.pixels
        return ' '.join(map(str, l))

    @classmethod
    def from_string(cls, s):
        l = list(map(int, s.split()))
        im = Image(l[0], l[1])
        im.pixels = l[2:]
        return im

    def save(self, filename):
        assert(filename[-4:] == ".ppm")
        f = open(filename, 'w')
        f.write("P3\n")
        f.write("{} {}\n255\n".format(self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                c = self.getPixel(x, y)
                f.write("{} {} {} ".format(c[0], c[1], c[2]))
            f.write("\n")
        f.close()

    def getPixel(self, x, y):
        if not (0 <= x < self.width):
            print("[ERREUR] Numéro de colonne (x={}) invalide.".format(x))
            assert(False)
        if not (0 <= y < self.height):
            print("[ERREUR] Numéro de ligne (y={}) invalide.".format(y))
            assert(False)
        k = 3*x + 3*self.width*y
        return self.pixels[k:k+3]

    def setPixel(self, x, y, couleur):
        if not (0 <= x < self.width):
            raise ValueError("[ERREUR] Numéro de colonne (x={}) invalide.".format(x))
        if not (0 <= y < self.height):
            raise ValueError("[ERREUR] Numéro de ligne (y={}) invalide.".format(y))
        k = 3*x + 3*self.width*y
        self.pixels[k:k+3] = couleur

    def __getitem__(self, ij):
        return self.getPixel(*ij)

    def __setitem__(self, ij, c):
        self.setPixel(*ij, c)

    def rvalues(self):
        return self.pixels[::3]

    def gvalues(self):
        return self.pixels[1::3]

    def bvalues(self):
        return self.pixels[2::3]

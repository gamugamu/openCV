import numpy as np

class node():
    # weigth list
    w_ = None #[np.float32]
    # incrementateur de la longueur de la node
    w_i = 0

    # depart de la node
    s_position = [0, 0]
    # fin de la node
    e_position = [0, 0]

    def __init__(self, start_position = [0, 0], end_position = [0, 0], lenght = 0):
        self.w_ = np.zeros(lenght, np.float32)
        self.s_position = start_position
        self.e_position = end_position

    # rajoute une masse à la node.
    def densify(self, mass):
        self.w_[self.w_i] = round(mass, 2)
        self.w_i = self.w_i + 1

    # retourne la forme orthogonal de la node. La direction est de gauche a droite.
    def normalised_vector(self):
        return np.array((self.s_position + self.e_position) / (self.s_position + self.e_position))

    # retourne la valeur maximal de la node
    def lenght(self):
        point = self.e_position - self.s_position
        return point[0] if point[0] else point[1]

    # retourne la valeur absolue la plus elevee dans la node.
    def condensed_point(self):
        return np.amax(np.absolute(self.w_[0:self.w_i]))

    # retourne l'index de la valeur absolue la plus elevee.
    def idx_condensed_point(self):
        # pour rappel, les nodes ont un decalage de 1 point vers la gauche, puisqu'ils
        # decrivent la relation entre deux pixels. Comme la lecture se fait de gauche a droite.
        # pour retrouver le bon pixel il faut faire un decalage vers la droite (+1)
        return (np.absolute(self.w_[0:self.w_i]) == self.condensed_point()).nonzero()[0][0] + 1

    # retourne la position de la valeur la plus elevee dans la node.
    def absolute_point_of_condensed_point(self):
        return self.s_position + self.normalised_vector() * self.idx_condensed_point()

    # retourne la taille actuelle de la node
    def size(self):
        return self.w_i

    # ferme la node
    def close(self, end_position):
        self.e_position = end_position

    def __str__(self):
        return "<" + str(self.__class__) + "[" + str(self.w_[0:self.w_i]) + "]> - [" + str(self.s_position) + str(self.e_position) + "]" + "\n"

    def __repr__(self):
        return str(self)

    @staticmethod
    def appendNode(n, new_position, n_list, lenght):
        if n is not None:
            n.close(new_position)

        n = node(new_position, lenght=lenght)
        n_list.append(n)

        return n

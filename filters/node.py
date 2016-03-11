import numpy as np

class node():
    # weigth list
    w_ = None #[np.float32]
    w_i = 0

    s_position = [0, 0]
    e_position = [0, 0]

    def __init__(self, start_position = [0, 0], end_position = [0, 0], lenght = 0):
        self.w_ = np.zeros(lenght, np.float32)
        self.s_position = start_position
        self.e_position = end_position

    def densify(self, mass):
        self.w_[self.w_i] = round(mass, 2)
        self.w_i = self.w_i + 1

    def normalised_vector(self):
        return np.array((self.s_position + self.e_position) / (self.s_position + self.e_position))

    def lenght(self):
        point = self.e_position - self.s_position
        return point[0] if point[0] else point[1]

    def condensed_point(self):
        return np.amax(np.absolute(self.w_[0:self.w_i]))

    def idx_condensed_point(self):
        # pour rappel, les nodes ont un decalage de 1 point vers la gauche, puisqu'ils
        # decrivent la relation entre deux pixels. Comme la lecture se fait de gauche a droite.
        # pour retrouver le bon pixel il faut faire un decalage vers la droite (+1)
        return (np.absolute(self.w_[0:self.w_i]) == self.condensed_point()).nonzero()[0][0] + 1

    def absolute_point_of_condensed_point(self):
        return self.s_position + self.normalised_vector() * self.idx_condensed_point()

    def size(self):
        return self.w_i

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

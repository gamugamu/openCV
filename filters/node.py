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

    def densify(self, mass):
        self.w_[self.w_i] = round(mass, 2)
        self.w_i = self.w_i + 1

    def lenght(self):
        point = e_position - s_position
        return point[0] if point[0] else point[1]

    def size(self):
        return self.w_i

    def close(self, end_position):
        self.e_position = end_position
        print self

    def __str__(self):
        return "<node [" + str(self.w_[0:self.w_i]) + "]> - [" + str(self.s_position) + str(self.e_position) + "]"

    def __repr__(self):
        return str(self)

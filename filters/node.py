import numpy as np

class node():
    # weigth list
    w_ = np.zeros(0, np.int32)
    w_i = 0
    s_position = [0, 0]
    e_position = [0, 0]

    def __init__(self, start_position = [0, 0], lenght = 0):
        print "--- new node ---"
        self.w_ = np.zeros(lenght, np.int32)
        self.s_position = start_position

    def densify(self, mass):
        self.w_[self.w_i] = mass
        self.w_i = self.w_i + 1

    def close(self, end_position):
        self.e_position = end_position

#    def orientation(self):
#        return

    def __str__(self):
        return "<node [" + str(self.w_[0:self.w_i]) + "]> - [" + str(self.s_position) + str(self.e_position) + "]"

    def __repr__(self):
        return str(self)

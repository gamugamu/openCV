import numpy as np
from node import node

class Node_segment(node):

    def __init__(self, start_position = [0, 0], end_position = [0, 0], dimension=3, dtype_=np.int32):
        point = end_position - start_position
        segment_lenght = point[0] if point[0] else point[1]

        self.w_ = np.zeros(shape=(segment_lenght, dimension), dtype=dtype_)
        self.s_position = start_position
        self.e_position = end_position

    def densify(self, mass):
        self.w_[self.w_i] = mass
        self.w_i = self.w_i + 1

    def __str__(self):
        return "<node [" + str(self.w_[0:self.w_i]) + "]> - [" + str(self.s_position) + str(self.e_position) + "]"

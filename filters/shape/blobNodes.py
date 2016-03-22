# coding: utf8
from node import node
import numpy as np

# Un blobNodes représente une matrice 9*9 de nodes conjointes ainsi que son orientation. Les blobNodes
# peuvent s'attacher entre elles afin d'exprimer des relations.

class blob_nodes(node):
    def develop(self, lhslimage):
        # selection des pixels voisin (8 au total + le pixel central).
        # m_neighboor : matrix of node neighboor.
        m_neighboor = self.matrice_neighboor()

        # détection des voisins similaires:
        for x in range(0, 3):
            for y in range(0, 3):
                if x == 1 and y == 1:
                    print "pass " + str(m_neighboor[x][y])
                else:
                    #neighboor
                    pnt = m_neighboor[x][y]
                    nb = node(pnt, px_value = lhslimage[pnt[0], pnt[1]], depth_resolution_plan = 0)
                    print "blod develop:", nb

    def matrice_neighboor(self):
        m_neighboor = np.array([ [[-1, -1], [0, -1], [1,-1]], [[-1, 0], [0,0], [1, 0]], [[-1,1], [0,1], [1,1]] ])
        return m_neighboor + self.pnt

    # print
    def __str__(self):
        return "<#" +  str(id(self)) + " blob_nodes>" + " [pnt:" + str(self.pnt) + " - resolution: " + str(self.depth_resolution_plan) + " - px_value: " + str(self.px_value) + "]\n"

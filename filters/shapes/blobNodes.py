# coding: utf8
from node import node
import numpy as np

# Un blobNodes représente une matrice 9*9 de nodes conjointes ainsi que son orientation. Les blobNodes
# peuvent s'attacher entre elles afin d'exprimer des relations.

class blob_nodes(node):
    n_list = None

    # constitue la liste des pixels qui lui sont similaire en luminosité.
    def develop(self, lhslimage, threshold=10):
        self.n_list = []

        # selection des pixels voisin (8 au total + le pixel central).
        # m_neighboor : matrix of node neighboor.
        m_neighboor = self.matrice_neighboor()
        blob_pixel_lum = lhslimage[self.pnt[0], self.pnt[1]][1]

        # détection des voisins similaires:
        for x in range(0, 3):
            for y in range(0, 3):
                # on cherche un voisin ayant aproximativement la meme intensité lumineuse.
                pnt = m_neighboor[x][y]
                # coordonné inversé?
                px_value = lhslimage[pnt[1], pnt[0]]

                if abs(int(blob_pixel_lum) - int(px_value[1])) < threshold:
                    nb = node(pnt, px_value = px_value, depth_resolution_plan = 0)
                    self.n_list.append(nb)

        print self.n_list

    # retourne une matrice 9*9 relatif a la position du blobNode
    def matrice_neighboor(self):
        m_neighboor = np.array([ [[-1, -1], [0, -1], [1,-1]], [[-1, 0], [0,0], [1, 0]], [[-1,1], [0,1], [1,1]] ])
        return m_neighboor + self.pnt

    # GUI
    def debug_view(self, scale_factor, cv_image, color):
        for node in self.n_list:
            node.debug_view(scale_factor, cv_image, color)
            #for y in range(0, 3):
            #    cv2.circle(cv_image, tuple( (transform[x][y] * scale_factor).astype(int)), 2, (100, 50, 255), thickness=3)

    # print
    def __str__(self):
        return "<#" +  str(id(self)) + " blob_nodes>" + " [pnt:" + str(self.pnt) + " - resolution: " + str(self.depth_resolution_plan) + " - px_value: " + str(self.px_value) + "]\n"

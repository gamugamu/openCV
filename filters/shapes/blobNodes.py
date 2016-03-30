# coding: utf8
from node import node
import numpy as np
import cv2

# Un blobNodes représente une matrice 9*9 de nodes conjointes ainsi que son orientation. Les blobNodes
# peuvent s'attacher entre elles afin d'exprimer des relations.

class blob_orientation:
    NONE    = 0
    LEFT    = 1
    RIGHT   = 2
    UP      = 4
    DOWN    = 8

    @staticmethod
    def orientation_from_pnt(pnt):
        orientation = blob_orientation.NONE
        orientation |= blob_orientation.LEFT    if pnt[0] == 1  else blob_orientation.NONE
        orientation |= blob_orientation.RIGHT   if pnt[0] == -1 else blob_orientation.NONE
        orientation |= blob_orientation.UP      if pnt[1] == 1  else blob_orientation.NONE
        orientation |= blob_orientation.DOWN    if pnt[1] == -1 else blob_orientation.NONE
        return orientation

class blob_nodes(node):
    n_list      = None # [node]
    orientation = blob_orientation.NONE
    matrix_size = 0

    def __init__(self, matrix_size, pnt, px_value, depth_resolution_plan):
        self.matrix_size = matrix_size
        self.pnt = pnt
        self.depth_resolution_plan = depth_resolution_plan
        self.px_value = px_value

    # constitue la liste des pixels qui lui sont similaire en luminosité.
    def develop(self, lhslimage, threshold=10, blob_pixel_lum=None):
        self.n_list = []

        # selection des pixels voisin (8 au total + le pixel central).
        # m_neighboor : matrix of node neighboor.
        m_neighboor = self.matrice_neighboor()

        # détection des voisins similaires:
        for x in range(0, self.matrix_size[0]):
            for y in range(0, self.matrix_size[1]):
                # on cherche un voisin ayant aproximativement la meme intensité lumineuse.
                pnt = m_neighboor[x][y]
                # coordonné inversé?
                px_value = lhslimage[pnt[1], pnt[0]]

                if abs(int(blob_pixel_lum) - int(px_value[1])) < threshold:
                    nb = node(pnt, px_value = px_value, depth_resolution_plan = 0)
                    self.n_list.append(nb)
                    self.orientation |= blob_orientation.orientation_from_pnt(self.pnt - pnt)

        #print filter(lambda x: np.array_equal(x.pnt, self.pnt), self.n_list)
        #print "orientation" + str(self.orientation)

        if self.orientation & blob_orientation.DOWN == blob_orientation.DOWN:
            # déplacement vers le bas, de la taille de la hauteur de la matrice.
            m = blob_nodes.matrice_size_for_image_bounds(self.pnt + [0, self.matrix_size[1]], lhslimage)

            return (m , self.pnt + [0, m[1]])
        else:
            return None

    # retourne une matrice 9*9 relatif a la position du blobNode
    def matrice_neighboor(self):
        m_neighboor = np.array([ [[-1, -1], [0, -1], [1,-1]], [[-1, 0], [0,0], [1, 0]], [[-1,1], [0,1], [1,1]] ])
        return m_neighboor + self.pnt

    # retourne la taille de la matrice possible pour la taille de l'image; afin de ne pas
    # dépasser les index de la matrice des pixels de l'image.
    @staticmethod
    def matrice_size_for_image_bounds(pntBorder, image_size):
        # par default la matrice est de 3*3. Si ce n'est pas possible, on redescend
        # vers une taille plus petite.
        matrice_size    = [3, 0]
        height, width   = image_size.shape[:2]
        #if pntBorder[0] - 1 <= 0:
        #    matrice_size[0] = matrice_size[0] - 1

        #if width - pntBorder[0] <= 0:
        #    matrice_size[0] = matrice_size[0] - 1
        print "pntBorder -> " + str(pntBorder) + "height :" + str(height)

        matrice_size[1] = height - pntBorder[1]

        if matrice_size[1] >= 3:
            matrice_size[1] = 3
        else:
            matrice_size[1] = matrice_size[1] + 1

        #print "S_Size -> " + str(matrice_size) + ":" + str(width)

        return matrice_size

    # GUI
    def debug_view(self, scale_factor, cv_image, color):
        for node in self.n_list:
            node.debug_view(scale_factor, cv_image, color)

        x1 = tuple( ((self.pnt - [1, 1]) * scale_factor).astype(int))
        # ! le point est décentré de 0.5 d'ou le rapport -1 / +2 sur une matrice 9*9
        x2 = tuple( ((self.pnt + [2, 2]) * scale_factor).astype(int))

        cv2.rectangle(cv_image, x1, x2, color, 2)

    # print
    def __str__(self):
        return "<#" +  str(id(self)) + " blob_nodes>" + " [pnt:" + str(self.pnt) + " - resolution: " + str(self.depth_resolution_plan) + " - px_value: " + str(self.px_value) + "]\n"

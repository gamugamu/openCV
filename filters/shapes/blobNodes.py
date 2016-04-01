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
    def orientation_from_blob(pnt, matrix, list_nodes):
        orientation = blob_orientation.NONE
        orientation |= blob_orientation.LEFT    if pnt[0] == 1  else blob_orientation.NONE
        orientation |= blob_orientation.RIGHT   if pnt[0] == -1 else blob_orientation.NONE
        orientation |= blob_orientation.UP      if pnt[1] == 1  else blob_orientation.NONE
        orientation |= blob_orientation.DOWN    if pnt[1] == -1 else blob_orientation.NONE
        return orientation

class blob_nodes(node):
    #static
    defaut_Matrice_Size_3x3 = [3,3]

    n_list      = None # [node]
    orientation = blob_orientation.NONE # pas de direction, par default
    matrix_size = [0, 0] # plan 2 dimensions

    def __init__(self, matrix_size, pnt, px_value, depth_resolution_plan):
        self.matrix_size            = matrix_size
        self.pnt                    = pnt
        self.depth_resolution_plan  = depth_resolution_plan
        self.px_value = px_value

    # constitue la liste des pixels qui lui sont similaire en luminosité.
    def develop(self, lhslimage, threshold=10, blob_pixel_lum=None):
        self.n_list = []

        # selection des pixels voisin (8 au total + le pixel central).
        # m_neighboor : matrix of node neighboor.
        print "---------------------------"
        linked_pnt = self.pnt

        # détection des voisins similaires:
        for x in range(0, self.matrix_size[0]):
            for y in range(0, self.matrix_size[1]):
                # on cherche un voisin ayant aproximativement la meme intensité lumineuse.
                pnt = self.pnt + [x, y]
                # Note: les coordonnées de lhslimage semblent inversées.
                px_value = lhslimage[pnt[1], pnt[0]]
                if abs(int(blob_pixel_lum) - int(px_value[1])) < threshold:
                    # on verifie si la node est voisine de la chaine en cours. Si elle
                    # est complétement détachée des autres (une node est voisine de l'autre
                    # si elle est a côté sur l'axe x ou y), alors on ne la place pas dans la chaine.
                    # a voir ce qu'il faudra en faire. Mais sera détachée du blob en cours.
                    print "start -----------------------"
                    for l_pnt in linked_pnt:
                        print "loop---"
                        if np.where((pnt - l_pnt) == 0)[0].size != 0:
                            nb = node(pnt, px_value = px_value, depth_resolution_plan = 0)
                            self.n_list.append(nb)
                            linked_pnt = np.append(linked_pnt, pnt)
                            # print presque.... le total de distance de x est y doit etre inférieur ou égale à 1)
                            print "linked --- neighboorhood " + str(linked_pnt) + "--\n == " + str( np.where((pnt - l_pnt) == 0)[0].size )
                            print "continue ---"
                            break
                        else:
                            print "not linked -------"

        #self.orientation = blob_orientation.orientation_from_blob(self.pnt, self.matrix_size, self.list_nodes)
        self.orientation = blob_orientation.DOWN

        # en fonction des orientations données, vérifie si la direction a déjà été visitée.
        # Si la direction n'a pas été visitée, vérifie si elle est accessible (pas en dehors
        # du champs de la matrice d'image).
        pnt_orientation = None
        if self.orientation & blob_orientation.DOWN == blob_orientation.DOWN:
            # déplacement vers le bas, de la taille de la hauteur de la matrice.
            pnt_orientation = self.pnt + [0, self.matrix_size[1]]
        else:
            return None

        # calcul de la matrice, depuis le point de direction.
        m = blob_nodes.matrice_size_for_image_bounds(pnt_orientation, lhslimage)

        if not m is None:
            return (m , self.pnt + [0, self.matrix_size[1]])
        else:
            return None

    # retourne la taille de la matrice possible pour la taille de l'image; afin de ne pas
    # dépasser les index de la matrice des pixels de l'image.
    @staticmethod
    def matrice_size_for_image_bounds(pntBorder, image_size):

        # par default la matrice est de 3*3. Si ce n'est pas possible, on redescend
        # vers une taille plus petite.
        height, width = image_size.shape[:2]
        if pntBorder[0] >= width or pntBorder[1] >= height:
            return None

        matrice_size = [3, 0]

        #if pntBorder[0] - 1 <= 0:
        #    matrice_size[0] = matrice_size[0] - 1

        #if width - pntBorder[0] <= 0:
        #    matrice_size[0] = matrice_size[0] - 1

        matrice_size[1] = height - pntBorder[1]
        # si la distance est trop grande, on remet par default la taille
        # standard de la matrice. Dans le cas contraire, la matrice ne peut
        # pas être négative ni égale à 0.
        if matrice_size[1] >= blob_nodes.defaut_Matrice_Size_3x3[1]:
            matrice_size[1] = blob_nodes.defaut_Matrice_Size_3x3[1]

        #print "S_Size -> " + str(matrice_size) + ":" + str(width)

        return matrice_size

    # GUI
    def debug_view(self, scale_factor, cv_image, color):
        for node in self.n_list:
            node.debug_view(scale_factor, cv_image, color)

        x1 = tuple( ((self.pnt) * scale_factor).astype(int))
        # ! le point est décentré de 0.5 d'ou le rapport -1 / +2 sur une matrice 9*9
        x2 = tuple( ((self.pnt + self.matrix_size) * scale_factor).astype(int))

        cv2.rectangle(cv_image, x1, x2, color, 2)

    # print
    def __str__(self):
        return "<#" +  str(id(self)) + " blob_nodes>" + " [pnt:" + str(self.pnt) + " - resolution: " + str(self.depth_resolution_plan) + " - px_value: " + str(self.px_value) + "]\n"

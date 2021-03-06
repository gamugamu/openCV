# coding: utf8
from shape import shape
import cv2

# Une node représente un groupement de valeurs de pixel ou un l'état d'un pixel. Les nodes
# peuvent s'attacher entre elles, s'inserer l'une dans l'autre afnin d'exprimer des relations.

class node(shape):
    pnt = None
    px_value = None # [hls]
    depth_resolution_plan = 0
    neighboorg = [] # les nodes voisines qui sont similaires

    # permer d'instancier une node en fonction de sa position dans l'image.
    # depth_resolution_plan permet de connaitre le degrès de définition d'une node.
    # 2 nodes avec un depth_resolution_plan différent ne sont pas sur le même plan.
    def __init__(self, pnt, px_value, depth_resolution_plan):
        self.pnt = pnt
        self.depth_resolution_plan = depth_resolution_plan
        self.px_value = px_value

    def append(self, node_neighboorg):
        self.neighboorg.append(node_neighboorg)

    # GUI
    def debug_view(self, scale_factor, cv_image, color):
        cv2.circle(cv_image, tuple( ((self.pnt + [0.5, 0.5]) * scale_factor).astype(int)), 2, color, thickness=3)

    # print
    def __str__(self):
        return "<#" +  str(id(self)) + " node>" + " [pnt:" + str(self.pnt) + " - resolution: " + str(self.depth_resolution_plan) + " - px_value: " + str(self.px_value) + "]\n"

    def __repr__(self):
        return str(self)


from Step_segment import *
import threading
import time
import cv2
from math import sqrt
import numpy as np

class massD_(Step_segment):

    #tache en background
    def bkg_analysis(self):
        #todo: creer les nodes de segment:
        # normalise
        l_image = self.destructed_view.low_res_image
        segment_cross_line = np.zeros(Destructed_view.d_resolution - 1, np.int32)
        lhsl_image = cv2.cvtColor(l_image, cv2.COLOR_BGR2HSV)

        for x in range(0, Destructed_view.d_resolution - 1):
            a = np.int32(lhsl_image[x,x][2])
            b = np.int32(lhsl_image[x + 1, x + 1][2])
            segment_cross_line[x] = a - b

        mass_weight = np.int32(0)
        w_line = np.zeros(Destructed_view.d_resolution - 1, np.int32)

        n_v = 0

        for x in range(0, segment_cross_line.size - 1):
            if segment_cross_line[x] == 0:
                print "0"

            elif segment_cross_line[x] > 0:
                if n_v != -1:
                    print "--- new node ---"
                    print "==== [", x, "]", mass_weight

                mass_weight = mass_weight - 1
                n_v = -1
                print "-1"
            else:
                if n_v != 1:
                    print "--- new node ---"
                    print "==== [", x, "]", mass_weight
                n_v = 1
                mass_weight = mass_weight + 1
                print "+1"

            w_line[x] = mass_weight

        print "==== [", segment_cross_line.size, "]", mass_weight

        print segment_cross_line
        print w_line
        print "--------------"
        self.call_back(self)

    #override
    def perform_analysis(self, destructed_view = None, call_back = None):
        self.destructed_view = destructed_view
        self.call_back  = call_back
        # l'analyse se fait en bkg. Un rapport est rendu lorsque massD_
        # a deconstruit un segment de l'image.
        d = threading.Thread(name='mass_segment', target=self.bkg_analysis)
        d.setDaemon(True)
        d.start()

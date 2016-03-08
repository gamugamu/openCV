
from Step_segment import *
import threading
import cv2
import node
import numpy as np
from node import node

class massD_(Step_segment):

    n_list = None

    #tache en background
    def bkg_analysis(self):
        segment_cross_line = self.make_segment_cross_line()
        self.n_list = []
        self.node_by_mass(self.n_list, segment_cross_line)

        print "segment_cross_line", segment_cross_line
        self.call_back(self)

    def make_segment_cross_line(self):

        #todo: creer les nodes de segment:
        # normalise
        l_image = self.destructed_view.low_res_image

        segment_cross_line = np.zeros(shape=(Destructed_view.d_resolution - 1, 3), dtype=np.int32)
        lhsl_image = cv2.cvtColor(l_image, cv2.COLOR_BGR2HLS)

        for x in range(0, Destructed_view.d_resolution):
            print lhsl_image[x,x]

        #determine la masse de chaque pixel contigue
        for x in range(0, Destructed_view.d_resolution - 1):
            a = lhsl_image[x,x]
            b = lhsl_image[x + 1, x + 1]
            segment_cross_line[x] = a.astype(int) - b.astype(int)

        return segment_cross_line

    #n_list, segment_cross_line, inout
    def node_by_mass(self, n_list, segment_cross_line):
        mass_weight = np.int32(0)
        n_v = 0
        n = node([0, 0], Destructed_view.d_resolution)
        n_list.append(n)

        # permet de creer les nodes entres les masses.
        for x in range(0, segment_cross_line.shape[0]):
            if segment_cross_line[x][1] == 0:
                pass

            elif segment_cross_line[x][1] > 0:
                if n_v != -1:
                    n = self.appendNode(n, [x, x], n_list)
                mass_weight = mass_weight - 1
                n_v = -1

            else:
                if n_v != 1:
                    n = self.appendNode(n, [x, x], n_list)
                n_v = 1
                mass_weight = mass_weight + 1

            n.densify(mass_weight)

        n.close([x, x])

    def appendNode(self, n, new_position, n_list):
        n.close(new_position)
        n = node(new_position, Destructed_view.d_resolution)
        n_list.append(n)
        return n

    #override
    def perform_analysis(self, destructed_view = None, call_back = None):
        self.destructed_view = destructed_view
        self.call_back  = call_back

    def start_analysis(self):
        # l'analyse se fait en bkg. Un rapport est rendu lorsque massD_
        # a deconstruit un segment de l'image.
        d = threading.Thread(name='mass_segment', target=self.bkg_analysis)
        d.setDaemon(True)
        d.start()
        pass

    def debug_view(self, opencvImage):
        scale_d_factor = self.destructed_view.scaleFactor_d_resolution()
        colors = [(255, 0, 0), (0, 255, 0)]

        for x in range(0, len(self.n_list)):
            node = self.n_list[x]
            x_scaled = (node.s_position[0] + 1 ) * scale_d_factor[0], (node.s_position[1] + 1 ) * scale_d_factor[1]
            y_scaled = (node.e_position[0] + 1 ) * scale_d_factor[0], (node.e_position[1] + 1 ) * scale_d_factor[1]

            cv2.line(opencvImage, x_scaled, y_scaled, colors[ x % 2 ], 5)

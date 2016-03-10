
from Step_segment import *
import threading
import cv2
import node
import numpy as np
from node import node
from nodeSegment import Node_segment

class massD_(Step_segment):

    n_list = None
    n_listColor = None

    #tache en background
    def bkg_analysis(self):
        segment_cross_line = self.make_segment_cross_line(np.array([0, 0]), np.array([Destructed_view.d_resolution - 1, Destructed_view.d_resolution - 1]))
        self.n_list = []
        self.n_listColor = []

        self.node_by_mass(self.n_list, segment_cross_line, range_tolerance=(-1, 1), hls_index=1)
        self.node_by_mass(self.n_listColor, segment_cross_line, range_tolerance=(-5, 5), hls_index=0)

        #print "segment_cross_line", segment_cross_line
        self.call_back(self)

    def make_segment_cross_line(self, s_point, e_point):
        #todo: creer les nodes de segment:
        # normalise
        l_image = self.destructed_view.low_res_image
        point = e_point - s_point
        segment_lenght = point[0] if point[0] else point[1]

        segment_cross_line = Node_segment(start_position=s_point, end_position=e_point, dimension=3)

        # seulement les teintes et la luminosite des pixels nous interesse. Le format HLS est
        # donc le plus approprie.
        lhsl_image = cv2.cvtColor(l_image, cv2.COLOR_BGR2HLS)

        #for x in range(0, Destructed_view.d_resolution):
        #    print lhsl_image[x,x]

        # axe normalise. Permet d'iterer le long de la ligne.
        n_point = np.array((s_point + e_point) / (s_point + e_point))

        # determine la masse de chaque pixel contigue, en iterant le long
        # de la ligne.
        for x in range(0, segment_lenght):
            a_point = n_point * x
            a = lhsl_image[a_point[0], a_point[1]]

            b_point = n_point * (x + 1)
            b = lhsl_image[b_point[0], b_point[1]]
            # calcule la difference entre un point et le suivant.
            segment_cross_line.densify(a.astype(int) - b.astype(int))

        return segment_cross_line

    # n_list, segment_cross_line, inout
    # retourne une liste de node liee par leur differences d'intensite lumineuse.
    def node_by_mass(self, n_list, segment_cross_line, range_tolerance, hls_index):
        mass_weight = np.int32(0)

        n_v = 0
        n = self.appendNode(n=None, new_position=[0, 0], n_list=n_list)

        # permet de creer les nodes entres les masses.
        for x in range(0, segment_cross_line.w_.shape[0]):
            mass_weight = segment_cross_line.w_[x][hls_index] / 255.0
            if segment_cross_line.w_[x][hls_index] in range(range_tolerance[0], range_tolerance[1]):
                # ici on definit les petites differences d'inclinaison dans la node.
                #print "segment_cross_line", segment_cross_line[x][hls_index]
                #print "segment_cross_line255", segment_cross_line[x][hls_index] / 255.0
                pass

            # si superieur a 0, alors superieur au range max.
            elif segment_cross_line.w_[x][hls_index] > 0:
                if n_v != -1:
                    n = self.appendNode(n, [x, x], n_list)
                # mass_weight est juste une indication scalaire qui informe l'
                # inclinaison de la masse. De paire avec segment_cross_line, on
                # determine dans cette inclinaison les differences entre les pixels voisins.
                # La ou commence une nouvelle node, il y a forcement une grande difference d'inclinaison avec sa
                # voisine. Et si a l'interieur d'une node, les inclinaisons sont changeantes, on peut en
                # determiner une granularite dans la masse. En fonction de cette 'granularite', on peut en deduire
                # si il s'agit d'une texture homogenene ou en degrade, une texture, ou meme du bruit. De meme qu'en liant
                # les nodes, on peut determiner si il y a un rythme, ou une direction apparante dans l'image.
                n_v = -1

            # si inferieur a 0, alors inferieur au range min.
            else:
                if n_v != 1:
                    n = self.appendNode(n, [x, x], n_list)

                n_v = 1

            n.densify(mass_weight)

        n.close([x, x])

    # lie les nodes les une aux autres.
    def appendNode(self, n, new_position, n_list):
        if n is not None:
            n.close(new_position)

        n = node(new_position, lenght=Destructed_view.d_resolution)
        n_list.append(n)
        return n

    # override
    def perform_analysis(self, destructed_view = None, call_back = None):
        self.destructed_view = destructed_view
        self.call_back = call_back

    def start_analysis(self):
        # l'analyse se fait en bkg. Un rapport est rendu lorsque massD_
        # a deconstruit un segment de l'image.
        d = threading.Thread(name='mass_segment', target=self.bkg_analysis)
        d.setDaemon(True)
        d.start()
        pass

    def debug_view(self, opencvImage):
        # affiche visuellement le resultat des nodes.
        scale_d_factor = self.destructed_view.scaleFactor_d_resolution()
        colors = [(255, 0, 0), (0, 255, 0)]
        colors2 = [(0, 0, 255), (0, 0, 0)]

        self.debug_view_perform_drawing(self.n_list, scale_d_factor, opencvImage, [(255, 0, 0), (0, 255, 0)], 2)
        self.debug_view_perform_drawing(self.n_listColor, scale_d_factor, opencvImage, [(0, 0, 255), (0, 0, 0)], 2, [0, 10])

    def debug_view_perform_drawing(self, nodelist, scale_factor, cv_image, bi_color, line_thickness, overlay=[0,0]):
        for x in range(0, len(nodelist)):
            node = nodelist[x]

            s_scaled = (node.s_position[0] + 1 ) * scale_factor[0] + overlay[0], (node.s_position[1] + 1 ) * scale_factor[1] + overlay[1]
            e_scaled = (node.e_position[0] + 1 ) * scale_factor[0] + overlay[0], (node.e_position[1] + 1 ) * scale_factor[1] + overlay[1]

            (node.s_position[0] + 1 ) * scale_factor[0]
            cv2.line(cv_image, s_scaled, e_scaled, bi_color[ x % 2 ], line_thickness)
            cv2.circle(cv_image, s_scaled, 1, bi_color[ x % 2 ], thickness=3)
            cv2.circle(cv_image, e_scaled, 1, bi_color[ x % 2 ], thickness=3)

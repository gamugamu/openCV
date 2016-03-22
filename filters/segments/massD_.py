# coding: utf8
from Step_segment import *
import threading
import cv2
import numpy as np
from filters.shape.filar import filar
from filters.shape.filarSegment import filar_segment
from filters.shape.blobNodes import blob_nodes
from massD_segmenter import massD_segmenter

# gère la logique d'appeler massD_segmenter pour decouper l'image en masse. Décide de continer de segmenter ou pas.
# (Step_segment)
class massD_(Step_segment):

    f_list = None
    hls_index = 1
    massD_s = massD_segmenter()

    #tache en background
    def bkg_analysis(self):
        #todo: creer les nodes de segment:
        # normalise
        self.f_list = []
        self.massD_s.image_for_segmentation(self.destructed_view.low_res_image)
        diagon   = Destructed_view.d_resolution - 1
        segment  = self.massD_s.make_segment([0, 0], [diagon, diagon])

        # c_lum : la colonne contenant la luminosite des pixels.
        # l_med : la moyenne des valeurs de c_lum
        c_lum = segment.w_[:,self.hls_index]
        l_med = abs(np.median(c_lum).astype(int)) + 1

        self.filar_by_mass(self.f_list, segment, range_tolerance=(np.amin(c_lum) + l_med, np.amax(c_lum) - l_med), hls_index=self.hls_index)
        self.call_back(self)

    # f_list, segment_cross_line, inout
    # retourne une liste de filets liee par leur differences d'intensite lumineuse.
    def filar_by_mass(self, f_list, segment, range_tolerance, hls_index):
        mass_weight = np.int32(0)

        f_v = 0
        f = filar.appendFilar(f=None, new_position=[0, 0], f_list=f_list, lenght=Destructed_view.d_resolution)

        # permet de creer les fils entres les masses.
        for x in range(0, segment.lenght()):
            mass_weight = segment.w_[x][hls_index] / 255.0
            f.densify(mass_weight)

            if segment.w_[x][hls_index] in range(range_tolerance[0], range_tolerance[1]):
                # ici sont definit les petites differences d'inclinaison dans le fil.
                pass

            # si superieur a 0, alors superieur au range max.
            elif segment.w_[x][hls_index] > 0:
                if f_v != -1:
                    f = filar.appendFilar(f, segment.positionAtIndex(x), f_list, Destructed_view.d_resolution)
                # mass_weight est juste une indication scalaire qui informe l'
                # inclinaison du fil. De paire avec segment_cross_line, on
                # determine dans cette inclinaison les differences entre les pixels voisins.
                # La ou commence un nouveal fil, il y a forcement une grande difference d'inclinaison avec son
                # voisin. Et si a l'interieur d'un fil, les inclinaisons sont changeantes, on peut en
                # determiner une granularite dans la masse. En fonction de cette 'granularite', on peut en deduire
                # si il s'agit d'une texture homogenene ou en degrade, une texture, ou meme du bruit. De meme qu'en liant
                # les fils, on peut determiner si il y a un rythme, ou une direction apparante dans l'image.
                f_v = -1

            # si inferieur a 0, alors inferieur au range min.
            else:
                if f_v != 1:
                    f = filar.appendFilar(f, segment.positionAtIndex(x), f_list, Destructed_view.d_resolution)

                f_v = 1


        f.close(segment.positionAtIndex(x))

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
        # affiche visuellement le resultat des fils.
        scale_d_factor = self.destructed_view.scaleFactor_d_resolution()
        colors = [(255, 0, 0), (0, 255, 0)]

        self.debug_view_perform_drawing(self.f_list, scale_d_factor, opencvImage, colors, 2, [0, 0])

    def debug_view_perform_drawing(self, filar_list, scale_factor, cv_image, bi_color, line_thickness, overlay=[0,0]):
        for x in range(0, len(filar_list)):
            filar = filar_list[x]

            s_scaled = (filar.s_position[0] + 1 ) * scale_factor[0] + overlay[0], (filar.s_position[1] + 1 ) * scale_factor[1] + overlay[1]
            e_scaled = (filar.e_position[0] + 1 ) * scale_factor[0] + overlay[0], (filar.e_position[1] + 1 ) * scale_factor[1] + overlay[1]

            cv2.line(cv_image, s_scaled, e_scaled, bi_color[ x % 2 ], line_thickness)
            cv2.circle(cv_image, s_scaled, 1, bi_color[ x % 2 ], thickness=3)
            cv2.circle(cv_image, e_scaled, 1, bi_color[ x % 2 ], thickness=3)

        # recuperation du fil le plus visible:
        heaviest_filar = sorted(self.f_list, key=lambda x: x.condensed_point(), reverse=True)[0]
        pnt = (heaviest_filar.absolute_point_of_condensed_point()) * scale_factor
        print "n_list\n", self.f_list
        cv2.circle(cv_image, tuple(pnt), 10, (255, 0, 255), thickness=3)

        self.neighborhooding(scale_factor, cv_image)


    def neighborhooding(self, scale_factor, cv_image):
        #on récupère le fil qui a le contraste le plus elevé.
        heaviest_filar = sorted(self.f_list, key=lambda x: x.condensed_point(), reverse=True)[0]
        pnt = heaviest_filar.absolute_point_of_condensed_point()

        # note resolution à gerer.
        blob = blob_nodes(pnt, px_value = self.massD_s.lhsl_image[pnt[0], pnt[1]], depth_resolution_plan = 0)
        print blob

        blob.develop(lhslimage=self.massD_s.lhsl_image)
        return
        # ------- purement GUI
        transform = transform + [0.5, 0.5]

        for x in range(0, 3):
            for y in range(0, 3):
                cv2.circle(cv_image, tuple( (transform[x][y] * scale_factor).astype(int)), 2, (100, 50, 255), thickness=3)

        print "point selectionné : \n", self.massD_s.lhsl_image[pnt[0] , pnt[1]]
        print "\nvoisin : >\n", self.massD_s.lhsl_image[pnt[0]-1 : pnt[0]+2, pnt[1]-1 : pnt[1]+2]
import cv2
import numpy as np
from Step_segment import *
from filters.shapes.filar import filar
from filters.shapes.filarSegment import filar_segment

# segmente les masses visuelles. Soit en filars, soit en node (blob_nodes)
class massD_segmenter(Step_segment):
    lhsl_image  = None
    segments    = None

    def make_segment(self, s_point, e_point):
        if self.lhsl_image is not None:
            #todo: creer les nodes de segment:
            # normalise
            segment = filar_segment(start_position=np.array(s_point), end_position=np.array(e_point), dimension=3)

            # axe normalise. Permet d'iterer le long de la ligne.
            n_vector = segment.normalised_vector()

            # determine la masse de chaque pixel contigue, en iterant le long
            # de la ligne.
            for x in range(0, segment.lenght()):
                a_point = n_vector * x
                a = self.lhsl_image[a_point[0], a_point[1]]

                b_point = n_vector * (x + 1)
                b = self.lhsl_image[b_point[0], b_point[1]]
                # calcule la difference entre un point et le suivant.
                segment.densify(a.astype(int) - b.astype(int))

            self.segments.append(segment)

            return segment
        else:
            return None

    def image_for_segmentation(self, image):
        # seulement les teintes et la luminosite des pixels nous interesse. Le format HLS est
        # donc le plus approprie.
        self.lhsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        self.segments   = []

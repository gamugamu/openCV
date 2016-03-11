
from Step_segment import *
from massD_ import massD_
import cv2
import numpy as np

class mass_fragmenter(Step_segment):
    massD = massD_()

    def perform_analysis(self, destructed_view = None, call_back = None):
        self.destructed_view = destructed_view
        self.massD.perform_analysis(destructed_view, call_back)

    def start_analysis(self):
        self.massD.start_analysis()

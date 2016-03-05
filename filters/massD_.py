
from Step_segment import *

class massD_(Step_segment):
    #override
    def perform_analysis(self, destructed_view = None, call_back = None):
        call_back(self)

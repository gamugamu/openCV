from filters.Destructed_view import Destructed_view

# template
class Step_segment():
    destructed_view = None
    # tout les vues a analyser doivent etre de type DestructedView
    @staticmethod
    def cvView_as_destructed_view(opencvImage):
        return Destructed_view(opencvImage)

    def perform_analysis(self, destructed_view = None, call_back = None):
        pass

    def start_analysis(self):
        pass

    def debug_view(opencvImage):
        pass

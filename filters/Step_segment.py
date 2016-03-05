from Destructed_view import Destructed_view

class Step_segment():
    # tout les vues a analyser doivent etre de type DestructedView
    @staticmethod
    def cvView_as_destructed_view(opencvImage):
        return Destructed_view(opencvImage)

    def perform_analysis(self, destructedView):
        pass

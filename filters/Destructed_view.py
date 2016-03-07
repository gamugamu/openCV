import cv2

class Destructed_view():

    d_resolution = 12
    low_res_image = None

    def getresolution(self):
        return self._d_resolution

    def setresolution(self, value):
        self._d_resolution = value

    def delresolution(self):
        del self._d_resolution

    def __init__(self, openCVImage):
        self.cvImg = openCVImage
        self.low_res_image = cv2.resize(openCVImage, (self.d_resolution, self.d_resolution))

    def size(self):
         s = self.cvImg.shape[:2]
         return (s[1], s[0])

    def scaleFactor_d_resolution(self):
        size = self.cvImg.shape[:2]
        return (size[1] / self.d_resolution, size[0] / self.d_resolution)

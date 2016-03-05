from filters import *

def analyzeTest():
    imgCat = cv2.imread('cat.jpg', 3)
    imgCat = cv2.resize(imgCat, (500, 300))
    cv2.imshow('image',imgCat)

    masssD = massD_()

    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    analyzeTest()

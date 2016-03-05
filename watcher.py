from filters import *

def report_analysis(step_segment):
    print "done", step_segment

def analyzeTest():
    imgCat = cv2.imread('cat.jpg', 3)
    imgCat = cv2.resize(imgCat, (500, 300))
    cv2.imshow('image',imgCat)

    dImage = Step_segment.cvView_as_destructed_view(imgCat)
    masssD = massD_()
    masssD.perform_analysis(dImage, report_analysis)

    while(1):
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzeTest()

from filters import *

def report_analysis(step_segment):
    pass

def analyzeTest():
    list_img = ["n.png", "up.png" , "cat.jpg", "mir.png", "charly.jpg", "mirInv.png", "shape.jpg"]

    for x in range (0, len(list_img)):
        imgCat = cv2.imread(list_img[x], 3)
        dImage = Step_segment.cvView_as_destructed_view(imgCat)
        masssD = massD_()
        masssD.perform_analysis(dImage, report_analysis)

        height, width = imgCat.shape[:2]
        reized_lowDef = cv2.resize(masssD.destructed_view.low_res_image, (width, height), interpolation=cv2.INTER_AREA)

        cv2.imshow('image',imgCat)
        cv2.imshow('image2', reized_lowDef)
        time.sleep(10)
        #k = cv2.waitKey(1) & 0xFF
        #if k == 27:

    cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzeTest()

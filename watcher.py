from filters import *

reized_lowDef = None

def report_analysis(step_segment):
    step_segment.debug_view(reized_lowDef)

def analyzeTest():
    list_img = ["cat.jpg",  "mir.png", "n.png", "up.png", "shape.jpg", "charly.jpg", "mirInv.png"]
    global reized_lowDef

    for x in range (0, len(list_img)):
        img = cv2.imread(list_img[x], 3)
        dImage = Step_segment.cvView_as_destructed_view(img)
        massD = massD_()
        massD.perform_analysis(dImage, report_analysis)

        height, width = img.shape[:2]
        reized_lowDef = cv2.resize(massD.destructed_view.low_res_image, (width, height), interpolation=cv2.INTER_AREA)
        massD.start_analysis()

        cv2.imshow('frame', img)
        cv2.imshow('low-frame', reized_lowDef)
        cv2.waitKey(1000)

        #k = cv2.waitKey(1) & 0xFF
        #if k == 27:

    cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzeTest()

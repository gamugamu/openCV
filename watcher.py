from filters import *

reized_lowDef = None

def report_analysis(step_segment):
    step_segment.debug_view(reized_lowDef)
    print "--- result ---"
    #print step_segment.n_list

def analyzeTest():
    list_img = [ "mir.png","n.png", "up.png", "cat.jpg", "shape.jpg", "charly.jpg", "mirInv.png", "bird.png", "eagle.png", "landscape.png"]

    global reized_lowDef

    for x in range (0, 12):
        img = cv2.imread(str(x) + ".png", 3)

        dImage = Step_segment.cvView_as_destructed_view(img)
        mass_f = mass_fragmenter()
        mass_f.perform_analysis(dImage, report_analysis)

        height, width = img.shape[:2]
        reized_lowDef = cv2.resize(mass_f.destructed_view.low_res_image, (width, height), interpolation=cv2.INTER_AREA)
        mass_f.start_analysis()

        cv2.waitKey(10)
        cv2.imshow('frame', img)
        cv2.imshow('low-frame', reized_lowDef)
        k = cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzeTest()

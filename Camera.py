import numpy as np
import cv2
import os.path

listOfFilters = [\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml",\
    #"D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml",\
    #"D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt_tree.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_profileface.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_fullbody.xml",\
    #"D:/opencv/opencv/sources/data/hogcascades/hogcascade_pedestrians.xml",\
    #"D:/opencv/opencv/sources/data/lbpcascades/lbpcascade_frontalface.xml",\
    #"D:/opencv/opencv/sources/data/lbpcascades/lbpcascade_profileface.xml",\
    ]

listOfFiltersRGB = {\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml":[0,0,0],\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml":[0,0,255],\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt_tree.xml":[0,255,0],\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml":[0,255,255],\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_profileface.xml":[255,0,0],\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_fullbody.xml":[255,0,255],\
    "D:/opencv/opencv/sources/data/hogcascades/hogcascade_pedestrians.xml":[255,255,0],\
    "D:/opencv/opencv/sources/data/lbpcascades/lbpcascade_frontalface.xml":[255,255,255],\
    #"D:/opencv/opencv/sources/data/lbpcascades/lbpcascade_profileface.xml":[255,0,0],\
    }

life = 0
video_file= 'E:/Entertainment/Movies/Animation/Wall-E/WALL-e.avi'
video_file= 'In/Sample.avi'
video_file= 'In/MohmedSaad1.avi'
Video = 0

Image_File = "In/Sample1.jpg"

def detectOneFileter(img, filterObj):
   # print(" two ")
    #img = cv2.imread(path)
    cascade = cv2.CascadeClassifier(filterObj)
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    #print("I am here")
    return rects,img


allcolor = []
def detect(img):
   allrects = [] 
   for obj in  listOfFilters:
       rects, img = detectOneFileter(img, obj)
       for x in rects:
           allrects.append(x)
           allcolor.append(listOfFiltersRGB[obj])
   return allrects, img

def box(rects, img):
    global image
    index = 0
    for x1, y1, x2, y2 in rects:
        print(allcolor)
        #cv2.rectangle(img, (x1, y1), (x2, y2), (allcolor[0][index], allcolor[2][index], allcolor[1][index]), 2)
        #print(allcolor[index][0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (allcolor[index][0], allcolor[index][1], allcolor[index][2]), 2)
        index = index + 1

    del allcolor[0:len(allcolor)]
    image = img
    #cv2.imwrite('/vagrant/img/detected.jpg', img);
    
def Cam_LifeWork():
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            #print(" one ")
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #gray = frame
            # Display the resulting frame
            rects, img = detect(gray)
            box(rects, img)
            cv2.imshow('frame',image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error frame")
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
def Cam_FileWork():
    
    #print("I am here")
    if os.path.isfile(video_file):
        cap = cv2.VideoCapture(video_file)
        while(cap.isOpened()):
            #print("I am here 1")
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects, img = detect(gray)
            box(rects, frame)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def Img_FileWork():
    rects = []
    hsv_planes = [[[]]]
    if os.path.isfile(Image_File):
        BGR=cv2.imread(Image_File)
        gray = cv2.cvtColor(BGR, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(BGR,cv2.COLOR_BGR2HSV)
        #print(hsv)
        #cv2.split( hsv, hsv_planes );
       # define range of blue color in HSV
        lower_blue = np.array([110,0,0])
        upper_blue = np.array([130,255,255])
       # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
       # Bitwise-AND mask and original image
        res = cv2.bitwise_and(BGR,BGR, mask= mask)
        rects, img = detect(res)
        box(rects, BGR)
        while(1):
            cv2.imshow('frame',BGR)
            cv2.imshow('mask',mask)
            cv2.imshow('res',res)
            cv2.imshow('image', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #cap.release()
    cv2.imwrite('Out/Out.jpg', image)
    cv2.destroyAllWindows()
      
        
def main():
    if Video == 1:
        if life == 1:
            Cam_LifeWork()
        elif os.path.isfile(video_file):
            Cam_FileWork()
        else:
            print("Wrong input !!!")
    else:
        Img_FileWork()
        
    return
    
main()

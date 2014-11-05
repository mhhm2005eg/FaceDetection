import numpy as np
import cv2
import cv2.cv as cv

import os.path
import datetime  
import sys, time
#from matplotlib import pyplot as plt

listOfFilters = [\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_profileface.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_fullbody.xml",\
    #"D:/opencv/opencv/sources/data/hogcascades/hogcascade_pedestrians.xml",\
    #"D:/opencv/opencv/sources/data/lbpcascades/lbpcascade_frontalface.xml",\
    #"D:/opencv/opencv/sources/data/lbpcascades/lbpcascade_profileface.xml",\
    ]
listOfEyeFilters = [\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_eye.xml",\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"\
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
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_eye.xml":[128,128,128],\
    "D:/opencv/opencv/sources/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml":[255,128,128],\
    }

life = 0
video_file= 'E:/Entertainment/Movies/Animation/Wall-E/WALL-e.avi'
video_file= 'In/Sample.avi'
video_file= 'In/MohmedSaad1.avi'
Video = 1
IMAGE = 0

Image_File = "In/Sample1.jpg"

def detectOneFileter(img, filterObj, size):
   # print(" two ")
    #img = cv2.imread(path)
    cascade = cv2.CascadeClassifier(filterObj)
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (size,size))
    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    #print("I am here")
    return rects,img


allcolor = []
def detect(img, lst, size):
   allrects = [] 
   for obj in  lst:
       rects, img = detectOneFileter(img, obj, size)
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


#datetime tt22

def getCFT():
    img1 = cv2.imread(Image_File, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    h, w = img1.shape[:2]
    vis0 = np.zeros((h,w), np.float32)
    vis0[:h, :w] = img1
    vis1 = np.fft.fft2(img1)
    #vis1 = cv2.dct(vis0)
    #img2 = cv2.CreateMat(vis1.shape[0], vis1.shape[1], cv2.CV_32FC3)
    #cv2.CvtColor(cv2.fromarray(vis1), img2, cv2.CV_GRAY2BGR)

    #cv2.imwrite('out/output.jpg', vis1)
    cv2.imshow('frame', vis1)
def Cam_FileWork():
    
    #print("I am here")
    if os.path.isfile(video_file):
        cap = cv2.VideoCapture(video_file)
        ret, frame = cap.read()
        height, width, depth = frame.shape
        time_initial = time.time()
        index = 1
        while(cap.isOpened()):
            #print("I am here 1")
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects, img = detect(gray,listOfFilters,20)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print(st)
            box(rects, frame)
            for x1, y1, x2, y2 in rects:
                Face = gray[y1:y2, x1:x2]
                eyes, img1 = detect(Face, listOfEyeFilters,10)
                for x01, y01, x02, y02 in eyes:
                    center = int(x1 + x01 + (x02-x01)*0.5), int(y1 + y01 + (y02-y01)*0.5 )
                    radius = cv.Round( (y01 + x01)*0.25 );
                    print(center, radius, x1, x01)
                    cv2.circle( frame, (center), radius,( 200, 200, 200 ), 1 );
                     

            deff = (ts - time_initial)
            avg = deff/index
            cv2.putText(image,st+"  Avg: "+ str(avg)+" [sec/fram]", (0,height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.41, 255)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            index = index + 1
            print(deff)
            print(index)
    cap.release()
    cv2.destroyAllWindows()

def Img_FileWork():
    rects = []
    if os.path.isfile(Image_File):
        imgref=cv2.imread(Image_File)
        gray = cv2.cvtColor(imgref, cv2.COLOR_BGR2GRAY)
        rects, img = detect(gray)
        box(rects, imgref)
        while(1):
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #cap.release()
    cv2.imwrite('Out/Out.jpg', image)
    cv2.destroyAllWindows()

def test():
    getCFT()
        
def main():
    if Video == 1:
        if life == 1:
            Cam_LifeWork()
        elif os.path.isfile(video_file):
            Cam_FileWork()
        else:
            print("Wrong input !!!")
    elif IMAGE == 1:
        Img_FileWork()
    else:
        test()
        
    return
    
main()

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
video_file= 'In/car1.avi'
Video = 0
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
def OptFlow():
    cap = cv2.VideoCapture(video_file)
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Create some random colors
    color = np.random.randint(0,255,(100,3))

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    cv2.imshow('frame',old_frame)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    n=0
    while(1):
        n=n+1
        if n == 20:
            mask = np.zeros_like(old_frame)
            n=0
        ret,frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_gray == None:
            continue 
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        if  p1 == None:
            mask = np.zeros_like(old_frame)
            ret, old_frame = cap.read()
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
            p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
            print("Empty ...")
            continue
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(frame,mask)

        cv2.imshow('frame',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)

    cv2.destroyAllWindows()
    cap.release()
        
        
def OptFlowxx():
    cap = cv2.VideoCapture(video_file)

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Create some random colors
    color = np.random.randint(0,255,(100,3))

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    cv2.imshow('frame',mask)
    while(cap.isOpened()):
        ret,frame1 = cap.read()
        #cv2.imshow('frame',frame1)
        print(ret)
        frame_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame_gray)
        #if frame_gray == None:
            #break
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        print(str)
        #if p1 == None:
            #break
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
        print(good_new, good_old)
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            cv2.line(mask, (a,b),(c,d), [255,155, 77], 2)
            cv2.circle(frame1,(a,b),5,color[i].tolist(),-1)
        #mask = np.zeros_like(frame)
        #if frame != None:
        img = cv2.add(frame1,mask)
        
        #print(mask.size.width)
        cv2.imshow('frame',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)

    cv2.destroyAllWindows()
    cap.release()
def ObjDetection():
    cap = cv2.VideoCapture(video_file)
    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255

    while(1):
        ret, frame2 = cap.read()
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        cv2.imshow('frame2',rgb)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('opticalfb.png',frame2)
            cv2.imwrite('opticalhsv.png',rgb)
        prvs = next

    cap.release()
    cv2.destroyAllWindows()
def test():
    OptFlow()
        
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

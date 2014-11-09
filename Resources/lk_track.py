#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

import numpy as np
import cv2
import video
from common import anorm2, draw_str
from time import clock
from matplotlib import pyplot as plt
import math
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
height, width, depth = 0 , 0,0                 
class Vec:
    ref = np.array([1,0])
    def __init__(self, ID, points):
        self.ref = np.array([1,0])
        self.avg = 0
        self.angle = 0
        self.ID = ID
        points = np.array(points)
        self.avg=np.mean(points, axis=0)
        dx= abs(points[-1][0] - points[0][0])
        dy= abs(points[-1][1] - points[0][1])
        P =np.array([dx,dy])
        dot =np.dot(self.ref, P)
        x_modulus = np.sqrt((self.ref*self.ref).sum())
        y_modulus = np.sqrt((P*P).sum())
        cos_angle = dot / x_modulus / y_modulus # cosinus of angle between x and y
        angle = np.arccos(cos_angle)
        angle = angle * 360 / 2 / np.pi # angle in degrees
        self.angle = angle
def PointsToVectors(lines):
    n = 0
    Pvector = []
    img = vis.copy() #np.ones((height, width, 3), np.uint8)
    #img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    for line in lines:
        if len(line) < 5:
            continue
        v = Vec(n,line)
        Pvector.append( v )
        print(Pvector[n].avg , Pvector[n].angle)
        center=tuple(Pvector[n].avg)
        rad = 10
        font =1
        fact = math.pow(Pvector[n].angle, 2)%255
        cv2.circle(img, center , rad, [fact,  fact ,fact], font)
        plt.subplot(221),plt.imshow(img, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        #plt.show()
        cv2.imshow('vectors', img)
        n = n + 1


def kmean(points):
    if not points:
        return
    cluster_n = 10
    img_size = 512
    #print("input \n")
    #print(points)
    PointsToVectors(points)
    print __doc__
    points = np.array(points)
    shape = ( -1, 2 )
    
    # generating bright palette
    #print("array \n")
    #print(points)
    if not points.any:
        return
    #T = tuple(map(tuple, points))
    L =points.tolist()
    #print(L)
    m=0
    LL=[]
    TT=[]
    for l in L:
        m = m + len(l)
        for p in l:
            LL.append(p)
            TT.append(tuple(p))
        
    #height1, width1, depth1 = points.shape
    #l = len(T)
    #num = height1*width1
    #print(m)
    if m < cluster_n:
        return points
    if not (m % 2 == 0):
        #print(points[len(points)-1])
        #points.remove((points[-1,-1]))
        points = np.delete(points, [len(points)-1,0,0])
        #LL.remove(-1)
        del TT[-1]
        #print(TT)
    points = TT                                         
    #print(points)
    #else:
    #points=points.reshape( shape )
    global colors
    colors = np.zeros((1, cluster_n, 3), np.uint8)
    colors[0,:] = 255
    colors[0,:,0] = np.arange(0, 180, 180.0/cluster_n)
    colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)[0]

    while True:
        #print 'sampling distributions...'
        #points, _ = make_gaussians(cluster_n, img_size)

        term_crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 3, 1.0)
        ret, labels, centers = cv2.kmeans(np.float32(points), cluster_n, term_crit, 1, 0)
        #print(labels)
        img = frame_gray #np.zeros((height, width, 3), np.uint8)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)  
        for (x, y), label in zip(np.int32(points), labels.ravel()):
            c = map(int, colors[label])
            #print (c)
            cv2.circle(img, (x, y), 1, c, -1)
            #print center
        i = 0
        for center in(centers) :
            #print (label)
            ll = (labels.tolist())
            #print(ll)
            #print(ll.index([i]))
            c = map(int,colors[i])
            i = i+1
            #print(c)
            center=tuple(center)
            rad = 10
            font =1
            cv2.circle(img, center , rad, c, font)

        cv2.imshow('gaussian mixture', img)
        ch = 0xFF & cv2.waitKey(0)
        break
        if ch == 27:
            break
            
        return centers
class App:
    def __init__(self, video_src):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = video.create_capture(video_src)
        self.frame_idx = 0

    def run(self):
        while True:
            ret, frame = self.cam.read()
            if not ret:
                return
            global frame_gray
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            global height, width, depth
            height, width = frame_gray.shape
            #print(frame_gray.shape)
            global vis
            vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                print("#"*30+"\n")    
                print(tr) 
                print("#"*30+"\n")
                self.tracks = new_tracks
                print(kmean(new_tracks))
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])


            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv2.imshow('lk_track', vis)

            ch = 0xFF & cv2.waitKey(1)
            if ch == 27:
                break
            #print(tr)
def main():
    import sys
    try: video_src = sys.argv[1]
    except: video_src = "..\in\MohmedSaad1.avi"

    print __doc__
    App(video_src).run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

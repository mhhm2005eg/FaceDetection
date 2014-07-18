import numpy as np
import cv2
import os.path
from matplotlib import pyplot as plt

Image_File = "In/Sample1.jpg"

def HighPassFilter(fftshiftImage, filterSIze):
    rows, cols = fftshiftImage.shape
    crow,ccol = rows/2 , cols/2
    fftshiftImage[crow-(filterSIze/2):crow+(filterSIze/2), ccol-(filterSIze/2):ccol+(filterSIze/2)] = 0
    return (fftshiftImage)


def filterFunc():
    rects = []
    hsv_planes = [[[]]]
    if os.path.isfile(Image_File):
        BGR=cv2.imread(Image_File)
        gray = cv2.cvtColor(BGR, cv2.COLOR_BGR2GRAY)
        img = gray
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        
        plt.subplot(221),plt.imshow(img, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        
        plt.subplot(222),plt.imshow(magnitude_spectrum, cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        
        FiltzeredFFT = HighPassFilter(fshift, 60)
        plt.subplot(223),plt.imshow(np.abs(FiltzeredFFT), cmap = 'gray')
        plt.title('Filtered'), plt.xticks([]), plt.yticks([])
        
		
        f_ishift = np.fft.ifftshift(FiltzeredFFT)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        plt.subplot(224),plt.imshow(np.abs(img_back), cmap = 'gray')
        plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
        plt.show()














def main():
	filterFunc()
  
    
main()
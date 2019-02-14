import os
import cv2
import csv
import numpy as np
import time
import argparse
from datetime import date
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy import signal
import peakutils
from PIL import Image

def scale(img, xScale, yScale):
    res = cv2.resize(img, None,fx=xScale, fy=yScale, interpolation = cv2.INTER_AREA)
    return res


def crop(infile,height,width):
    im = Image.open(infile)   
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)
            
def averagePixels(path):
    r, g, b = 0, 0, 0
    count = 0
    pic = Image.open(path)
    for x in range(pic.size[0]):
          for y in range(pic.size[1]):
              imgData = pic.load()
              tempr,tempg,tempb = imgData[x,y]
              r += tempr
              g += tempg
              b += tempb
              count += 1
      # calculate averages
    return (r/count), (g/count), (b/count), count

def keyframeDetection(source, dest,xPixel,yPixel,Thres):
    
    keyframePath = dest+'/keyFrames'
    if not os.path.exists(keyframePath):
        os.makedirs(keyframePath)

    imageGridsPath = dest+'/imageGrids'
    if not os.path.exists(imageGridsPath):
        os.makedirs(imageGridsPath)
        
    csvPath = dest+'/csvFile'
    if not os.path.exists(csvPath):
        os.makedirs(csvPath)
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(source)
  
    if (cap.isOpened()== False):
        print("Error opening video file")
    lstfrm = []
    lstdiffMag = []
    timeSpans = []
    listMeanRGB = []
    listOutput = []
    images = []
    lastFrame = None
    Start_time = time.process_time() # first time video frame is opened
    
    # Read until video is completed
    while(cap.isOpened()):
    # Capture frame-by-frame
      ret, frame = cap.read()
      if frame is not None:
          cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          gray = scale(gray, 1, 1)
          grayframe = scale(gray, 1, 1)
          gray = cv2.GaussianBlur(gray, (9,9), 0.0)
  
      frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
      lstfrm.append(frame_number)
      images.append(grayframe)
      
      if frame_number == 0:
          lastFrame = gray
  
      diff = cv2.subtract(gray, lastFrame)
      diffMag = cv2.countNonZero(diff)
      lstdiffMag.append(diffMag) 
      stop_time = time.process_time() # time the next video frame is ope
      time_Span = stop_time-Start_time
      timeSpans.append(time_Span)
      # the current video frame is assigned to the variable "lastFrame"
      lastFrame = gray
  
      if ret == True:
       # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break  # Break the loop
      else:
        break
 
    # When everything done, release the video capture object
    cap.release()
    y = np.array(lstdiffMag)
    # calculate the keyframe by looking for the peak values of the pixel differences from previous frame to current frame
    base = peakutils.baseline(y, 2) # Data baseline will be deducted from the raw data
    indices = peakutils.indexes(y-base, Thres, min_dist=1)
    
    ##plot to monitor the selected keyframe   
    plt.plot(indices, y[indices], "x")
    l = plt.plot(lstfrm, lstdiffMag, 'r-')
    plt.xlabel('frames')
    plt.ylabel('pixel difference')
    plt.title("Pixel value differences from frame to frame and the peak values")
    plt.show()
    
    cnt = 1 #counter
    for x in indices:
        # Write keyframe in the keyframePath
        cv2.imwrite(os.path.join(keyframePath , 'keyframe'+ str(cnt) +'.jpg'), images[x])
        cv2.waitKey(0)
        cnt +=1
    
    ccnt = 1 #counter
    for x in indices:
        if __name__=='__main__':
            infile = keyframePath +'/keyframe'+ str(ccnt) +'.jpg'
            im = Image.open(infile)   
            imgwidth, imgheight = im.size
            height = int(imgheight//yPixel)
            width = int(imgwidth//xPixel)
        
            start_num = 1
            listMeanRGB.clear()
            for k,piece in enumerate(crop(infile,height,width),start_num):
                img=Image.new('RGB', (width,height), 255)
                img.paste(piece)
                path=os.path.join(imageGridsPath + '/image-%s' % ccnt +'(Grid-%s).png' % k)
                img.save(path)
            
                rr, gg, bb, totalpxl = averagePixels(path)
                mean_RGB = int((rr+gg+bb)/3)
                listMeanRGB.append(mean_RGB)        
    
        listOutput.append('keyframe ' + str(ccnt) + ' happened at ' + str(timeSpans[x]) + ' sec. Median value of the pixels of all grids is ' + str(listMeanRGB))
        print('keyframe ' + str(ccnt) + ' happened at ' + str(timeSpans[x]) + ' sec. Median value of the pixels of all grids is ' + str(listMeanRGB))
        ccnt+=1
    #save csv file including the keyframes timestamp and the median value of the pixels of all grids in each keyframe   
    path2file = csvPath + '/output.csv'
    with open(path2file, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(1,ccnt):
            writer.writerows([[listOutput[i-1]]])
        csvFile.close()   
        
    # Closes all the frames
    cv2.destroyAllWindows()

parser = argparse.ArgumentParser()

parser.add_argument('-s','--source', help='source file', required=True)
parser.add_argument('-d', '--dest', help='destination folder', required=True)
parser.add_argument('-x', '--xPixel', help='number of pixel in X', default=3)
parser.add_argument('-y','--yPixel', help='number of pixel in Y', default=3)
parser.add_argument('-t','--Thres', help='Threshold of the image difference', default=0.5)

args = parser.parse_args()


# Run the extraction
keyframeDetection(args.source, args.dest, int(args.xPixel), int(args.yPixel), float(args.Thres))

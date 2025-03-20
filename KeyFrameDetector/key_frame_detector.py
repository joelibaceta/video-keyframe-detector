import os
import cv2
import csv
import numpy as np
import time
import peakutils
from KeyFrameDetector.utils import convert_frame_to_grayscale, prepare_dirs, plot_metrics

def keyframeDetection(source, dest, Thres, max_keyframes=8, plotMetrics=False, verbose=False):
    i = 0
    keyframePath = dest + '/keyFrames'
    imageGridsPath = dest + '/imageGrids'
    csvPath = dest + '/csvFile'
    path2file = csvPath + '/output.csv' 
    prepare_dirs(keyframePath, imageGridsPath, csvPath)
    
     
    cap = cv2.VideoCapture(source)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
     
     
    if not cap.isOpened():
        print("Error opening video file")
        return
     
     
    lstfrm = []
    lstdiffMag = []
    timeSpans = []
    images = []
    full_color = []
    lastFrame = None
    Start_time = time.process_time()
     
     
    for i in range(length):
        if i > 5000:
            break
        ret, frame = cap.read()
        print(f"""Processing frame {i} of {length}""")
        if not ret:
            break
         
         
        grayframe, blur_gray = convert_frame_to_grayscale(frame)
        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
        lstfrm.append(frame_number)
        images.append(grayframe)
        full_color.append(frame)
         
         
        if frame_number == 0:
            lastFrame = blur_gray

        diff = cv2.subtract(blur_gray, lastFrame)
        diffMag = cv2.countNonZero(diff)
        lstdiffMag.append(diffMag)
        stop_time = time.process_time()
         
         
        timeSpans.append(stop_time - Start_time)
        lastFrame = blur_gray

    cap.release()
    y = np.array(lstdiffMag)
    base = peakutils.baseline(y, 2)
    indices = peakutils.indexes(y - base, Thres, min_dist=1)

     
     

    if len(indices) > max_keyframes:
        ranked_indices = sorted(indices, key=lambda i: lstdiffMag[i], reverse=True)[:max_keyframes]
        indices = sorted(ranked_indices)
     
     

    if plotMetrics:
        plot_metrics(indices, lstfrm, lstdiffMag)

    cnt = 1
     
     
    for x in indices:
         
         
        cv2.imwrite(os.path.join(keyframePath, f'keyframe{cnt}.jpg'), full_color[x])
        log_message = f'keyframe {cnt} happened at {timeSpans[x]} sec.'
        if verbose:
            print(log_message)
        with open(path2file, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([log_message])
        cnt += 1
     
     
    cv2.destroyAllWindows()



if __name__  == '__main__':
    keyframeDetection('@zabi.ff8_video_7425631184450833682.mp4', 'output', 0.3, 8)
import os
import cv2
import csv
import numpy as np
import time
import peakutils
import logging
from KeyFrameDetector.utils import convert_frame_to_grayscale, prepare_dirs, plot_metrics

logging.basicConfig(
    filename='keyframe_detection.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def keyframeDetection(source, dest, Thres, max_keyframes=8, plotMetrics=False, verbose=False):
    keyframePath = os.path.join(dest, 'keyFrames')
    imageGridsPath = os.path.join(dest, 'imageGrids')
    csvPath = os.path.join(dest, 'csvFile')
    path2file = os.path.join(csvPath, 'output.csv')
    prepare_dirs(keyframePath, imageGridsPath, csvPath)

    cap = cv2.VideoCapture(source)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not cap.isOpened():
        logging.error("Error opening video file")
        cap.release()
        return

    lstfrm = []
    lstdiffMag = []
    timeSpans = []
    images = []
    full_color = []
    lastFrame = None
    Start_time = time.process_time()

    for i in range(length):
        ret, frame = cap.read()
        logging.debug(f"Processing frame {i} of {length}")
        if not ret:
            logging.warning(f"Frame {i} could not be read. Stopping early.")
            break

        grayframe, blur_gray = convert_frame_to_grayscale(frame)
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
        lstfrm.append(frame_number)
        images.append(grayframe)
        full_color.append(frame)

        if frame_number == 0:
            lastFrame = blur_gray
            lstdiffMag.append(0)
            timeSpans.append(0)
            continue

        diff = cv2.subtract(blur_gray, lastFrame)
        diffMag = cv2.countNonZero(diff)
        lstdiffMag.append(diffMag)

        stop_time = time.process_time()
        timeSpans.append(stop_time - Start_time)
        lastFrame = blur_gray

    cap.release()

    if len(lstdiffMag) < 3:
        logging.warning("Not enough frames for peak detection.")
        return

    y = np.array(lstdiffMag)
    base = peakutils.baseline(y, 2)
    indices = peakutils.indexes(y - base, Thres, min_dist=1)

    if len(indices) > max_keyframes:
        ranked_indices = sorted(indices, key=lambda i: lstdiffMag[i], reverse=True)[:max_keyframes]
        indices = sorted(ranked_indices)

    if plotMetrics:
        plot_metrics(indices, lstfrm, lstdiffMag)

    cnt = 1
    write_header = not os.path.exists(path2file)

    for x in indices:
        cv2.imwrite(os.path.join(keyframePath, f'keyframe{cnt}.jpg'), full_color[x])
        log_message = f'keyframe {cnt} happened at {timeSpans[x]} sec.'
        if verbose:
            logging.info(log_message)
        with open(path2file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if write_header:
                writer.writerow(["Keyframe Log"])
                write_header = False
            writer.writerow([log_message])
        cnt += 1

    cv2.destroyAllWindows()

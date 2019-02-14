# keyframeDetection
The script is used to detect the keyframes in a video

## Description
keyframeDetector.py is an OpenCV/Python based script for extracting keyframes from a video. It comprises script that performs the following function

### keyframeDetection: 
Outputs a set of frames and csv file that represent the timestamp of the keyframes in the video. This will generate an output folder with subfolders that contain images at various scales. The output includes the greyscale keyframes in foder “keyFrames”. The keyframe number is appended to the image names.  The grids of the keyframes is saved in folder “imageGrids”. The keyframe number and the grid number are appended to the image names.The csv file is saved as “output.csv” in folder “csvFile”. All the data are collected during the process. It should be noted that when you run the script, first a plot with peak points is shown. The x axis is the video frames and the y axis represents the the total number of nonzero pixels when two subsequet frames are subtracted. You need to close the plot in order to see the keyframes and csv file in the specified folders.    

## Status
Useful for the video with less noise and huge transition in from frame to frame. The global keyframe will be identified by setting the threshold as close to 1 as possible. 

## Setup
Requires a working python installing with the OpenCV package and modules such as numpy, argparse, pyplot from matplotlib, peakutils and Image from PIL (Python Imaging Library). The suggested python IDE to run this script is Thonny. The download link is given at https://thonny.org/

## Usage
There is one main script. keyframeDetector.py contains the keyframe ditection, keyframe plot analysis and image grids from the split keyframes.

### keyframeDetector
`python keyframeDetector.py -s "/path/to/input/mp4file/video.mp4" -d "/path/to/output/folder" -x int (grid size in width) -y int(grid size in height) –t float between 0 to 1`

-s  --source: This is a path to the source file which includes video. For example if the video is in the desktop, then the path will be `/Users\Myname\Desktop\videoname.mp4`. Note that the source should include the video name with *.mp4 and should be in double quotation marks.  
-d  --dest: The path where you want to save the outputs. It should be a folder already created by the user and the full path for the folder should be given. For example, if the folder is “DemoResults” placed in Desktop, the path will be `/Users\Myname\Desktop\DemoResults`

-x --xPixel: An optional parameter. It is a grid size of the keyframe in width. The default value is 3. 

-y --yPixel: An optional parameter. It is a grid size of the keyframe in height. The default value is 3. 

-t --Thres: An optional parameter. There is a float number between 0, 1 (Normalized threshold). It determines the keyframes based on the number of nonzero pixels calculated from the two consecutive frames subtraction. The current frame in the video is subtracted from the previous frame and the nonzero pixels are counted and saved in the list of array. In the keyframe detection, only the peaks with amplitude higher than the threshold will be detected. For example, if the threshold is 0.8, then the frames with nonzero pixels over 80% will be selected. The default value is 0.5. 

## Usage in Thonny
The syntax to run the script in Thonny is given below

`%Run path/to/folder/keyframeDetector.py -s "/path/to/input/mp4file/video.mp4" -d "/path/to/output/folder" -x int (grid size in width) -y int(grid size in height) –t float between 0 to 1)`

### Example
`%Run /Users/Myname/Desktop/keyframeDetector.py -s "/Users/Myname/Desktop/demoVideo1.mp4" -d "/Users/Myname/Desktop/Myresults" -x 4 -y 4 -t 0.5`

<center>

   ![header](images/header.png)
    
</center>

A `Key Frame` is a location on a video timeline which marks the beginning or end of a smooth transition throughout the fotograms, `Key Frame Detector` try to look for the most representative and significant frames that can describe the movement or main events in a video using peakutils peak detection functions.

<br/>
<p align="center">

   <img src="images/demo.gif"> 

</p>
<br/>

## Installation

**Requirements**

- python3
- numpy
- opencv
- peakutils
- matplotlib
- PIL

```python
pip install video-keyframe-detector
```

## Command-Line Usage
After installing the package (see Installation section), you can run the keyframe detector from the terminal:

```python
Change directory to video-keyframe-detector:
pip install -r requirements.txt
python3 cli.py -s "videos/acrobacia.mp4" -d output/ -t 0.3
```

## Python API Usage
You can also use the detector directly in your Python code:

```python
from KeyFrameDetector.key_frame_detector import keyframeDetection

source_video = "videos/acrobacia.mp4"
output_dir = "output"
threshold = 0.3

keyframeDetection(
    source=source_video,
    dest=output_dir,
    Thres=threshold,
    max_keyframes=5,      
    plotMetrics=True,     
    verbose=True         
)
```


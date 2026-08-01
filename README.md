# Kick Tracker

Kick Tracker is a computer vision project that uses MediaPipe Pose and OpenCV to extract body landmark data from a kicking motion video and save it to a CSV file for further biomechanical analysis.

The program:

* Loads a video file containing a kick.
* Detects and tracks body landmarks using MediaPipe Pose.
* Saves landmark coordinates and visibility confidence values to a CSV file.
* Displays the tracked pose skeleton on the video in real time.
* Generates a simple plot of left hip vertical movement over time.

---

## Features

* Pose estimation using MediaPipe Pose
* Landmark tracking for:

  * Nose
  * Shoulders
  * Hips
  * Knees
  * Ankles
  * Foot indices
* CSV export of raw landmark data
* Optional frame skipping for faster processing
* Real-time visualization of tracked landmarks
* Motion analysis plotting with Matplotlib

---

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Required libraries:

* OpenCV (`opencv-python`)
* MediaPipe
* Matplotlib

---

## Project Structure

```text
kickTracker/
│
├── kick_tracker.py
├── kick_slow_square.mp4
├── landmark_raw_data.csv
├── requirements.txt
└── README.md
```

---

## Configuration

At the top of the script, several settings can be modified:

```python
use_webcam = False
video_file = "kick_slow_square.mp4"
output_csv = "landmark_raw_data.csv"
frame_skip = 0
```

### Parameters

| Variable     | Description                           |
| ------------ | ------------------------------------- |
| `use_webcam` | Reserved for future webcam support    |
| `video_file` | Input video file                      |
| `output_csv` | Output CSV filename                   |
| `frame_skip` | Skip every N frames during processing |

Example:

```python
frame_skip = 2
```

Processes one frame and skips the next two.

---

## How It Works

### 1. Load Video

OpenCV loads the video file:

```python
cap = cv2.VideoCapture(video_file)
```

### 2. Detect Pose

MediaPipe detects and tracks body landmarks:

```python
results = pose.process(rgb)
```

### 3. Save Landmark Data

For each frame, the script stores:

* x coordinate
* y coordinate
* z coordinate
* visibility confidence

Example CSV columns:

```text
frame,timestamp,LEFT_HIP_x,LEFT_HIP_y,LEFT_HIP_z,LEFT_HIP_viscon,...
```

Coordinates are normalized between 0 and 1 relative to image dimensions.

---

## Running the Program

Execute:

```bash
python kick_tracker.py
```

A window will appear showing the tracked pose skeleton.

Press:

```text
1
```

to stop processing and close the application.

---

## Output

### CSV File

The script generates:

```text
landmark_raw_data.csv
```

Each row contains:

* Frame number
* Timestamp
* Landmark coordinates
* Visibility confidence

Example:

```text
frame,timestamp,LEFT_HIP_x,LEFT_HIP_y,LEFT_HIP_z,LEFT_HIP_viscon
0,0.034,0.512,0.601,-0.113,0.998
```

### Motion Plot

After processing, the script creates a graph showing:

```text
Left Hip Y Position vs Time
```

The Y-axis is inverted so upward body movement appears visually intuitive.

---

## Tracked Landmarks

The following landmarks are recorded:

* NOSE
* LEFT_SHOULDER
* RIGHT_SHOULDER
* LEFT_HIP
* RIGHT_HIP
* LEFT_KNEE
* RIGHT_KNEE
* LEFT_ANKLE
* RIGHT_ANKLE
* LEFT_FOOT_INDEX
* RIGHT_FOOT_INDEX

---

## Future Improvements

Potential enhancements:

* Webcam support
* Joint angle calculations
* Automatic kick phase detection
* Velocity and acceleration analysis
* Multiple graph outputs
* Data smoothing and filtering
* Export to Excel format
* Real-time performance metrics

---

## Applications

This project can be used for:

* Martial arts analysis
* Soccer kicking mechanics
* Biomechanics research
* Sports performance evaluation
* Motion tracking experiments
* Engineering and computer vision projects

---

## License

This project is intended for educational and research purposes.

import cv2
import mediapipe as mp
import csv
import time
import matplotlib.pyplot as plt

#general setup
use_webcam = False
video_file = "kick_slow_square.mp4"
output_csv = "landmark_raw_data.csv"
frame_skip = 0
#skip every nth frame

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
#shorten module path names

landmarks = [
    mp_pose.PoseLandmark.LEFT_HIP,
    mp_pose.PoseLandmark.RIGHT_HIP,
    mp_pose.PoseLandmark.NOSE,
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_KNEE,
    mp_pose.PoseLandmark.RIGHT_KNEE,
    mp_pose.PoseLandmark.LEFT_ANKLE,
    mp_pose.PoseLandmark.RIGHT_ANKLE,
    mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
    mp_pose.PoseLandmark.RIGHT_FOOT_INDEX
]
#saves landmarks needed for tracking

cap = cv2.VideoCapture(video_file)
#uploads video to opencv

csvfile = open(output_csv, "w", newline="")
csvwriter = csv.writer(csvfile)
header = ["frame", "timestamp"]
for lm in landmarks:
    header += [f"{lm.name}_x", f"{lm.name}_y", f"{lm.name}_z", f"{lm.name}_viscon"]
#header printing:
#xyz positions, viscon; how confident mp is that a landmark is visible

csvwriter.writerow(header)

#mp setup
with mp_pose.Pose(
    static_image_mode = False,
    #true = detect per frame; false = detect once and track
    #false better speed and consistence in csv data
    model_complexity = 2,
    #lite, normal, heavy model
    enable_segmentation = False,
    #segmentation body outline mask
    min_detection_confidence = 0.2,
    #confidence to detect pose
    min_tracking_confidence = 0.7
    #confidence to track pose
    ) as pose:

    frame_idx = 0
    start_time = time.time()

    Flag = True

    while Flag:
        ret, frame = cap.read()
        
        if not ret:
            print("Reached end of video or cannot open video file")
            break
        #end capture

    
        if frame_skip and (frame_idx % (frame_skip + 1) != 0):
            frame_idx += 1
            continue
        #frame skipping

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #bgr(opencv) to rgb(mp)

        results = pose.process(rgb)
        #run pose detection

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 2, circle_radius = 2),
                mp_drawing.DrawingSpec(color = (255, 0, 255), thickness = 2)
            )
        print_timestamp = round((time.time() - start_time), ndigits = 3)
        row = [frame_idx, print_timestamp]

        if results.pose_landmarks:
            lm_list = results.pose_landmarks.landmark
            for lm in landmarks:
                res = lm_list[lm.value]
                #value is scaled and normalized to image size from 0-1
                res.x = round(res.x, ndigits = 3)
                res.y = round(res.y, ndigits = 3)
                res.z = round(res.z, ndigits = 3)
                res.visibility = round(res.visibility, ndigits = 3)
                #round datapoints to 3 decimal places
                row += [res.x, res.y, res.z, res.visibility]
        else:
            row += [None, None, None, None] * len(landmarks)
            #skips to the next row when body/landmarks are not detected

        csvwriter.writerow(row)

        cv2.imshow("Kick Tracker (press 1 to quit)", frame)

        frame_idx += 1

        if cv2.waitKey(1) & 0xFF == ord("1"):
            Flag = False
            continue

cap.release()
cv2.destroyAllWindows()
csvfile.close()
print(f"Landmark data saved to {output_csv}")

csv_file = "landmark_raw_data.csv"
time_vals = []
left_hip_y = []

with open(csv_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            t = float(row["timestamp"])
            y = float(row["LEFT_HIP_y"])
            time_vals.append(t)
            left_hip_y.append(y)
        except (TypeError, ValueError):
            continue


plt.figure()
plt.plot(time_vals, left_hip_y)
plt.xlabel("Time (s)")
plt.ylabel("Left Hip Y Position (0 = top, 1 = bottom)")
plt.title("Left Hip Y Position vs Time")
plt.grid(True)
plt.gca().invert_yaxis()
plt.show()

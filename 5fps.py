#======================
#That code shows you how you can use yolo to detect something in a predifined area 
#======================
import cv2
from ultralytics import YOLO, solutions

model = YOLO("models/lil_big_ai.pt")
cap = cv2.VideoCapture("test_video_input/2024-07-04 22-22-47.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Define region points
region_points = [(0, 0), (w, 0), (w, h), (0, h)]

# Video writer
video_writer = cv2.VideoWriter("object_counting_output2.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init Object Counter
counter = solutions.ObjectCounter(
    view_img=True,
    reg_pts=region_points,
    classes_names=model.names,
    draw_tracks=True,
    line_thickness=2,
)

# Calculer le pas pour obtenir 10 frames par seconde
skip_frames = int(fps // 5)

frame_count = 0

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Traiter seulement une frame sur `skip_frames`
    if frame_count % skip_frames == 0:
        tracks = model.track(im0, persist=True, show=False, conf=0.1)
        im0 = counter.start_counting(im0, tracks)
        video_writer.write(im0)

    frame_count += 1

cap.release()
video_writer.release()
cv2.destroyAllWindows()

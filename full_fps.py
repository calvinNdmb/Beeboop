import cv2
from ultralytics import YOLO, solutions

model = YOLO("/content/runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture("/content/My Video.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

region_points = [(0, 0), (w, 0), (w, h), (0, h)]

video_writer = cv2.VideoWriter("object_counting_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))


counter = solutions.ObjectCounter(
    view_img=False,  
    reg_pts=region_points,
    classes_names=model.names,
    draw_tracks=True,
    line_thickness=2,
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Traiter chaque frame
    tracks = model.track(im0, persist=True, show=False, conf=0.1)
    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()
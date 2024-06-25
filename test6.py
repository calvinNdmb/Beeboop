import cv2
from ultralytics import YOLO, solutions

# Utiliser un modèle plus léger
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("My Video.mp4")
assert cap.isOpened(), "Error reading video file"

# Réduire la résolution de la vidéo
target_width, target_height = 320, 240
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("object_counting_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (target_width, target_height))

# Init Object Counter
counter = solutions.ObjectCounter(
    view_img=False,  # Désactiver l'affichage des images
    reg_pts=[(0, 0), (target_width, 0), (target_width, target_height), (0, target_height)],
    classes_names=model.names,
    draw_tracks=True,
    line_thickness=1,
)

frame_skip = 3  # Traiter seulement une frame sur trois
frame_count = 0

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Redimensionner l'image pour réduire la charge de calcul
    im0 = cv2.resize(im0, (target_width, target_height))

    # Traiter seulement une frame sur `frame_skip`
    if frame_count % frame_skip == 0:
        tracks = model.track(im0, persist=True, show=False, conf=0.349)
        im0 = counter.start_counting(im0, tracks)
        video_writer.write(im0)

    frame_count += 1

cap.release()
video_writer.release()
cv2.destroyAllWindows()

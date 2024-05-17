import numpy as np
from ultralytics import YOLO
import cv2
im1 = cv2.imread('training_database/3466294_2f5bd421f8_n.jpg')
model = YOLO('best.pt')
results = model.predict(source=[im1])
print (type(results))
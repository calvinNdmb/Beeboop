from ultralytics import YOLO
import cv2
im1 = cv2.imread('utilities/test.jpg')
model = YOLO('models/best.pt')
results = model.predict(source=[im1])
print (type(results))
import cv2
from ultralytics import YOLO
import os

ROOT_PATH = '/home/sowmyavenky/yolo_env/'
BEST_PT = os.path.join(ROOT_PATH, 'invasives.pt')

model = YOLO(BEST_PT)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame1 = cap.read()
    results = model(frame1)  # predict on an image

    # Process and display the results
    for result in results:
      # The classification model returns top 5 predicted classes and confidence scores
      print(f"Top 1 class: {result.names[result.probs.top1]}, Confidence: {result.probs.top1conf.item():.2f}")

    cv2.imshow('YOLO V11 Detection', frame1)   
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

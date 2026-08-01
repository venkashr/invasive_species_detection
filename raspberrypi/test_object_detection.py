import cv2
from ultralytics import YOLO

model = YOLO('yolo11n.pt')
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run inference
    results = model(frame)

    # Visualize results on the frame
    annotated_frame = results[0].plot()

    # --- ADJUST DISPLAY SIZE HERE ---
    # Resize to 1280x720 (or any resolution)
    resized_frame = cv2.resize(annotated_frame, (1280, 720))

    # Display the frame
    cv2.imshow("YOLOv11 Detection", resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


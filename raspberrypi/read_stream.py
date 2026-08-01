import cv2
import threading
from time import sleep
import os
import random
from ultralytics import YOLO
from pymavlink import mavutil


# Define border parameters
BORDER_SIZE = 10
BORDER_COLOR = [0, 223, 255] # BGR color for the border (Blue in this case)

ROOT_PATH = '/home/sowmyavenky/yolo_env/'
BEST_PT = os.path.join(ROOT_PATH, 'invasives.pt')
model = YOLO(BEST_PT)

# === Threaded Video Capture Class ===
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        self.lock = threading.Lock()

        actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Actual resolution set: {int(actual_width)}x{int(actual_height)}")

        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while not self.stopped:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                with self.lock:
                    self.ret, self.frame = ret, frame

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else (False, None)

    def stop(self):
        self.stopped = True
        self.cap.release()

# === Start Video Stream ===
stream = VideoStream(0)
sleep(1)  # Let the stream warm up
frame_count = 0

master = mavutil.mavlink_connection('/dev/ttyACM0', baud="115200")

# Make sure the connection is valid
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (master.target_system, master.target_component))

gps_text = ''

# === Main Loop ===
while True:
    ret, frame = stream.read()
    if not ret or frame is None:
        sleep(0.1)
        continue

    # Resize and predict
    results = model(frame)  # predict on an image

    # Process and display the results
    confidence = results[0].probs.top1conf.item()
    if confidence > 0.6:
      species_and_confidence = f"Detected {results[0].names[results[0].probs.top1]}, Confidence: {results[0].probs.top1conf.item():.2f}"
    else:
      species_and_confidence = ''

    frame_count += 1

    # 2. Get GPS data for the current frame (requires custom logic)
    msg = master.recv_match()
    if  msg:
      if msg.get_type() == 'TERRAIN_REPORT':
        gps_text = str(msg) 
      if msg.get_type() == 'ATTITUDE':
        gps_text = str(msg)


    # 3. Put text on the frame
    # Origin (0,0) is top-left corner
    cv2.putText(frame, gps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(frame, species_and_confidence, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 223, 255), 2)
    
    # Apply the border to the frame
    # Arguments: src, top, bottom, left, right, borderType, value
    bordered_frame = cv2.copyMakeBorder(
        frame,
        BORDER_SIZE,
        BORDER_SIZE,
        BORDER_SIZE,
        BORDER_SIZE,
        cv2.BORDER_CONSTANT,
        value=BORDER_COLOR
    )
    
    cv2.imshow('Drone Video Feed', bordered_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
stream.stop()
cv2.destroyAllWindows()


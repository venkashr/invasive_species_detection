import cv2
import threading
from time import sleep
import os
import random

# === RTSP stream URL ===
rtsp_url = 'rtsp://admin:Olfk$1234@192.168.40.206/12'
# Define border parameters
BORDER_SIZE = 20
BORDER_COLOR = [255, 0, 0] # BGR color for the border (Blue in this case)
detected_species = ["Chinese Privet", "Japanese Climbing Fern", "Elephant Ears", "Chinese Tallow"]

# === Threaded Video Capture Class ===
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
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
stream = VideoStream(rtsp_url)
sleep(1)  # Let the stream warm up
frame_count = 0

# === Main Loop ===
while True:
    ret, frame = stream.read()
    if not ret or frame is None:
        sleep(0.1)
        continue

    # Resize and predict
    #frame = cv2.resize(frame, (1290, 720))
    random_boolean = random.randint(0, 1) == 1
    frame_count += 1

    # 2. Get GPS data for the current frame (requires custom logic)
    # Example: Mock data for demonstration purposes
    latitude = 30.088 + (frame_count * 0.0001)
    longitude = -95.4284 + (frame_count * 0.0001)
    gps_text = f"{latitude:.6f}, {longitude:.6f}"

    if random_boolean:
        species_text = random.choice(detected_species)
    else:
        species_text = ""

    # 3. Put text on the frame
    # Origin (0,0) is top-left corner
    cv2.putText(frame, gps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
    # cv2.putText(frame, species_text, (10, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
    
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

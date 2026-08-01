import cv2
import random

import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import os
from pymavlink import mavutil

from gpiozero import DistanceSensor
from time import sleep

# Initialize the DistanceSensor using GPIO Zero library
# Trigger pin is connected to GPIO 23, Echo pin to GPIO 24
sensor = DistanceSensor(echo=24, trigger=23)


VIDEO_PATH = "/home/sowmyavenky/yolo_env/chinese_privet.mp4"

translator = {
    'chinese_privet' : 'Chinese Privet',
    'chinese_tallow' : 'Chinese Tallow',
    'japanese_climbing_fern' : 'Japanese Climbing Fern',
    'kudzu' : 'Kudzu',
    'mimosa_tree' : "Mimosa Tree",
    'chinaberry' : 'Chinaberry',
    'dodder' : 'Dodder',
    'paper_mulberry' : 'Paper Mulberry',
    'Nandina' : 'Nandina',
    'Chamberbitter':'Chamberbitter',
    'dandelion' : 'Dandelion',
    'Dollarweed' : 'Dollarweed',
    'chinese_parasol' : 'Chinese Parasol',
    'elephant_ears' : 'Elephant Ears',
    'japanese_honeysuckle' : 'Japanese Honeysuckle',
    'tree_of_heaven': 'Tree of Heaven'
}

MODEL_PATH = '/home/sowmyavenky/yolo_env/invasives.pt'
# Load the YOLOv11 model
model = YOLO(MODEL_PATH)
new_resolution = (1920, 1080)

cap = cv2.VideoCapture(VIDEO_PATH)
cap.set(3, 640)
cap.set(4, 480)
    
frame_count = 0
# master = mavutil.mavlink_connection('/dev/ttyACM0', baud="115200")

# Make sure the connection is valid
# master.wait_heartbeat()
# print("Heartbeat from system (system %u component %u)" %
#      (master.target_system, master.target_component))

gps_text = ''
                 
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()
    
while True:
    ret, frame = cap.read()
    frame_count = frame_count + 1
    if not ret:
        break   # No more frames → end of video

    # 2. Get GPS data for the current frame (requires custom logic)
    msg = None
    #msg = master.recv_match()
    print(msg)
    if  msg:
      if msg.get_type() == 'TERRAIN_REPORT':
        gps_text = str(msg)
      if msg.get_type() == 'ATTITUDE':
        gps_text = str(msg)

    dis = sensor.distance * 100  # Measure distance and convert from meters to centimeters
    results = model.predict(source=frame)
    for result in results:
        # Get the class name (top prediction)
        probs = result.probs # Class probabilities
        top_class_id = probs.top1
        top_class_name = model.names[top_class_id]
        confidence = round(probs.top1conf.item(), 2)

        latitude = 30.088 + (frame_count * 0.0001)
        longitude = -95.4284 + (frame_count * 0.0001)
        gps_text = f"{latitude:.6f}, {longitude:.6f}"

        resized_frame = cv2.resize(frame, new_resolution, interpolation=cv2.INTER_AREA)
        cv2.putText(resized_frame, translator[top_class_name] + " Confidence : " + str(confidence * 100) + "%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (6, 64, 43), 4)
        cv2.putText(resized_frame, gps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (6, 64, 43), 4)
        if dis < 100.0: 
          cv2.putText(resized_frame, 'Obstacle in: {:.2f} cm'.format(dis), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 4)
        else:
          cv2.putText(resized_frame, 'No Obstacles detected', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (6, 64, 43), 4)

    cv2.imshow('Drone Video Feed', resized_frame)

    # Press Q to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

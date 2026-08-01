import cv2
import random

import numpy as np

# Define border parameters
BORDER_SIZE = 20
BORDER_COLOR = [255, 0, 0] # BGR color for the border (Blue in this case)
detected_species = ["Chinese Privet", "Japanese Climbing Fern", "Elephant Ears", "Chinese Tallow"]

cap = cv2.VideoCapture()
# Define the desired new resolution (width, height)
new_resolution = (848, 480)

cap = cv2.VideoCapture("/home/sowmyavenky/yolo_env/chinese_privet.mp4")
    
frame_count = 0
                  
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()
    
while True:
    random_boolean = random.randint(0, 1) == 1
    ret, frame = cap.read()
    frame_count += 1

    if not ret:
        break   # No more frames → end of video

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
    cv2.putText(frame, gps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 3)
    cv2.putText(frame, species_text, (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 4)
    
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

    # Display the resulting frame
    resized_frame = cv2.resize(bordered_frame, new_resolution, interpolation=cv2.INTER_AREA)
    
    cv2.imshow('Drone Video Feed', resized_frame)

    # Press Q to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

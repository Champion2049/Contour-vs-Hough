from picamera2 import Picamera2
import cv2
import numpy as np
from gpiozero import Motor
import time

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# Motor setup
flmotor = Motor(forward=18, backward=12)
frmotor = Motor(forward=17, backward=10)
blmotor = Motor(forward=9, backward=13)
brmotor = Motor(forward=16, backward=11)

# **PID Control Parameters**
Kp = 0.6   
Ki = 0.01  
Kd = 0.25  

prev_error = 0
integral = 0
base_speed = 1.0  # Normal speed

# **Motor Control Function**
def update_motors(left_speed, right_speed):
    flmotor.forward(left_speed) if left_speed > 0 else flmotor.backward(-left_speed)
    frmotor.forward(right_speed) if right_speed > 0 else frmotor.backward(-right_speed)
    blmotor.forward(left_speed) if left_speed > 0 else blmotor.backward(-left_speed)
    brmotor.forward(right_speed) if right_speed > 0 else brmotor.backward(-right_speed)

# **Process Frame for Contour-Based Tracking**
def process_frame(frame):
    global prev_error, integral, base_speed

    # **Convert to grayscale and apply adaptive thresholding**
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # **Region of Interest (lower half)**
    height, width = thresh.shape
    roi = thresh[height//2:, :]  

    # **Find contours**
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  
        else:
            cx = width // 2  
    else:
        cx = width // 2  

    # **PID Control for Steering**
    error = cx - (width // 2)
    integral += error
    derivative = error - prev_error
    correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
    prev_error = error

    left_speed = base_speed - correction * 0.002  
    right_speed = base_speed + correction * 0.002  

    # **Dynamic Speed Adjustment**
    curve_intensity = abs(error) / (width // 2)
    if curve_intensity > 0.5:
        base_speed = 0.6  # Reduce speed on sharp turns
    else:
        base_speed = 1.0  # Normal speed is 1.0

    left_speed = max(0, min(1, left_speed))
    right_speed = max(0, min(1, right_speed))

    # **Move Motors**
    update_motors(left_speed, right_speed)

    # **Draw path center line**
    cv2.line(frame, (cx, height // 2), (cx, height), (255, 0, 0), 3)
    cv2.putText(frame, f"Error: {error}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Speed: {base_speed:.2f}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    return frame

# **Main Loop**
while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    processed_frame = process_frame(frame)

    # Display processed video feed
    cv2.imshow("Refined Contour-Based Tracking", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
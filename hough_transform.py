from picamera2 import Picamera2
import cv2
import numpy as np
from gpiozero import Motor
import time
import matplotlib.pyplot as plt

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# Motor setup
flmotor = Motor(forward=18, backward=12)
frmotor = Motor(forward=17, backward=10)
blmotor = Motor(forward=9, backward=13)
brmotor = Motor(forward=16, backward=11)

# PID Control Parameters
Kp = 1.2
Ki = 0.02
Kd = 0.5

prev_error = 0
integral = 0
base_speed = 1.0
turn_speed = 0.5

# Error tracking
error_history = []
time_stamps = []
start_time = time.time()

def update_motors(left_speed, right_speed):
    flmotor.forward(left_speed) if left_speed > 0 else flmotor.backward(-left_speed)
    frmotor.forward(right_speed) if right_speed > 0 else frmotor.backward(-right_speed)
    blmotor.forward(left_speed) if left_speed > 0 else blmotor.backward(-left_speed)
    brmotor.forward(right_speed) if right_speed > 0 else brmotor.backward(-right_speed)

def hough_transform_tracking(frame):
    global prev_error, integral, base_speed

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    height, width = edges.shape
    roi = edges[int(height * 0.7):, :]
    lines = cv2.HoughLinesP(roi, 1, np.pi/180, 50, minLineLength=50, maxLineGap=150)

    cx = width // 2
    if lines is not None:
        avg_x = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            avg_x.append((x1 + x2) // 2)

        if avg_x:
            cx = int(np.mean(avg_x))

    # PID Control
    error = cx - (width // 2)
    integral = 0.8 * integral + error
    derivative = error - prev_error
    correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
    prev_error = error

    # Log error and timestamp
    error_history.append(error)
    time_stamps.append(time.time() - start_time)

    left_speed = base_speed - correction * 0.002  
    right_speed = base_speed + correction * 0.002  

    curve_intensity = abs(error) / (width // 2)
    if curve_intensity > 0.5:
        base_speed = turn_speed
        time.sleep(0.1)
    else:
        base_speed = 1.0

    left_speed = max(0, min(1, left_speed))
    right_speed = max(0, min(1, right_speed))
    update_motors(left_speed, right_speed)

    cv2.line(frame, (cx, int(height * 0.7)), (cx, height), (0, 255, 0), 3)
    cv2.putText(frame, f"Error: {error}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return frame

# Main Loop
try:
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        processed_frame = hough_transform_tracking(frame)

        cv2.imshow("Hough Transform Path Tracking", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop motors
    flmotor.stop()
    frmotor.stop()
    blmotor.stop()
    brmotor.stop()

    # Save error graph
    plt.figure(figsize=(10, 5))
    plt.plot(time_stamps, error_history, label="PID Error", color='blue')
    plt.xlabel("Time (s)")
    plt.ylabel("Error")
    plt.title("PID Error Over Time (Hough Transform Tracking)")
    plt.legend()
    plt.grid(True)
    plt.savefig("hough_error_tracking_graph.png")
    plt.show()

    cv2.destroyAllWindows()

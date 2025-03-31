---

# 🚗 Contour Tracking vs Hough Transform: RC Car Experiment

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-red)

This repository contains Python implementations of **Contour Tracking** and **Hough Transform Tracking** algorithms, designed to control an RC car using a Raspberry Pi. The goal is to compare the performance of these two techniques in detecting and following paths or obstacles in real-time environments .


## 📌 Overview

The project focuses on implementing two popular computer vision techniques—**Contour Detection** and **Hough Transform**—to enable an RC car to detect and follow paths or lanes autonomously. The Raspberry Pi acts as the brain of the system, processing video input and controlling the car's motors accordingly.

- **Contour Detection**: Detects shapes and boundaries in the environment by identifying edges and grouping them into contours.
- **Hough Transform**: Detects straight lines in the environment, which can be used for lane detection or obstacle avoidance .

Both methods are compared in terms of accuracy, computational efficiency, and robustness in dynamic environments.

---

## ✨ Features

- Real-time object/line detection using OpenCV.
- Control of an RC car via GPIO pins on a Raspberry Pi.
- Modular codebase with separate implementations for contour tracking (`contour.py`) and Hough transform tracking (`hough_transform.py`).
- Easy-to-follow setup instructions for replicating the experiment.

---

## 🔧 Setup Instructions

### Prerequisites

1. **Hardware Requirements**:
   - Raspberry Pi (Recommended: Raspberry Pi 4 Model B).
   - RC Car (1/10 scale recommended) .
   - USB Webcam or Pi Camera Module.
   - Motor Driver (e.g., L298N).

2. **Software Requirements**:
   - Python 3.8 or higher.
   - OpenCV (`pip install opencv-python`).
   - NumPy (`pip install numpy`).

3. **Optional**:
   - Bluetooth module for smartphone control .

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Champion2049/IEE_RC.git
   cd IEE_RC
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Connect your hardware:
   - Attach the motor driver to the Raspberry Pi GPIO pins.
   - Mount the camera on the RC car.

4. Configure the GPIO pins in the code if needed.

---

## ▶️ Usage

### Running Contour Tracking
To run the contour-based tracking algorithm:
```bash
python contour.py
```

### Running Hough Transform Tracking
To run the Hough transform-based tracking algorithm:
```bash
python hough_transform.py
```

### Controls
- The RC car will start moving automatically when the script is executed.
- Use keyboard inputs (if implemented) or modify the code to customize behavior.

---

## 📂 Files

| File Name          | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `contour.py`       | Implements contour detection for path tracking.                           |
| `hough_transform.py` | Implements Hough transform for line detection and tracking.                |

---

## 📊 Results

- **Contour Tracking**: Effective for detecting irregular shapes but may struggle with noisy environments.
- **Hough Transform**: Ideal for detecting straight lines and works well in structured environments like roads .

For detailed results, refer to the `results` folder (if applicable).

---

## 🤝 Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

Steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m "Add YourFeatureName"`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---


## 📚 References

-  Obstacle detection using Raspberry Pi for driving safety based on the Hough transform.
-  Hough transform track: Topics by Science.gov.
-  An optical flow and Hough transform-based approach to lane departure warning systems.
-  Smartphone-controlled RC car using Raspberry Pi.
-  Steering angle estimation for self-driving cars using CNN models.

---

Feel free to reach out if you have any questions or need further assistance!


🎨 Color Detection & Serial Control System
This project uses a webcam to detect specific colors (Red and Blue) within a defined Region of Interest (ROI). Once a color is detected, it sends a signal via Serial communication to a microcontroller (like an Arduino Nano) to trigger physical actions.

🛠 Hardware Setup
Camera: Connect your USB webcam to the PC/Laptop.

Microcontroller: Connect the Arduino Nano via USB.

Wiring: Ensure any servos or actuators are powered correctly and connected to the Nano.

📍 Configuration Steps
1. Identify the COM Port
Open Device Manager on Windows.

Look under Ports (COM & LPT).

Find "USB Serial Port" or "Arduino Nano" and note the number (e.g., COM10).

Update Code: In the script, change ser = serial.Serial('COM10', 9600) to match your port.

2. Identify the Camera Index
If using a built-in laptop camera, it is usually index 0.

External webcams are usually index 1 or 2.

Update Code: Change cap = cv2.VideoCapture(1) if the window shows the wrong camera or fails to open.

📦 Installation & Dependencies
You must have Python installed. Open your terminal/command prompt and run the following commands to install the required libraries:

🚀 How to Run
Connect the hardware.

Update the COM port in the script.

Run the script:

Controls:

The window will show a zoomed-in view of the detection area.

Press 'q' on your keyboard to stop the program and close the serial port safely.

📝 Logic Reference
The system sends the following characters over Serial at 9600 Baud:

🔍 Troubleshooting
Serial Error: Ensure the Arduino Serial Monitor is closed in the Arduino IDE before running the Python script. Two programs cannot use the same COM port at once.

No Camera: If you see "Camera not detected," try changing the index in cv2.VideoCapture().

Detection Issues: If the colors aren't being picked up, adjust the lower and upper HSV arrays in the code to match your lighting conditions.

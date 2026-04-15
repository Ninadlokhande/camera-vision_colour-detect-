import cv2
import numpy as np
import serial
import time

# --- SERIAL SETUP ---
# Update 'COM3' to your specific port (e.g., 'COM4' or '/dev/ttyUSB0')
# connect camera as well as serial com port to laptop
try:
    ser = serial.Serial('COM10', 9600, timeout=1)      
    # IMP  :==   check com port serial in using device manager
    time.sleep(2)  # Wait for microcontroller to initialize
    print("Serial port connected.")
except Exception as e:
    print(f"Serial Error: {e}")
    ser = None

cap = cv2.VideoCapture(1)  #change to 1 if you have multiple cameras or want to use an external webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
if not cap.isOpened():
    print("Camera not detected")
    exit()

# Track the last sent signal to avoid spamming the microcontroller
last_signal = '0'

def draw_detections(frame, mask, color_name, box_color):
    """
    Finds contours in the mask and draws boxes/labels.
    Returns True if a valid object is detected.
    """
    detected = False
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1200:  # Adjust this to change sensitivity to object size
            x, y, w, h = cv2.boundingRect(cnt)
            # Draw the rectangle and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            cv2.putText(frame, color_name, (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
            detected = True
    return detected

print("Starting detection... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    # Syntax: frame[y_start:y_end, x_start:x_end]
# Example: Capture only the middle section
    frame = frame[100:400, 200:500]
    if not ret:
        break

    # 1. Pre-processing: Blur the frame to reduce sensor noise
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    
    # 2. Convert to HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


    large_frame = cv2.resize(frame, (800, 800), interpolation=cv2.INTER_LINEAR)
    
    
    # --- COLOR DEFINITIONS ---
    
    # RED: Needs two ranges because red is at both ends of the Hue spectrum
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    # BLUE: Widened range to see darker/lighter blues more effectively
    # Hue: 90-130, Saturation: 70-255, Value: 50-255
    lower_blue = np.array([90, 70, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # --- LOGIC & SERIAL OUTPUT ---
    current_signal = '0'  # Default state (nothing detected)

    # Check for Red first (Priority 1)
    if draw_detections(frame, mask_red, "RED", (0, 0, 255)):
        current_signal = '1'
    
    # Check for Blue (Priority 2)
    # Using 'if' instead of 'elif' allows drawing both boxes, 
    # but the signal logic below will prioritize Blue if Red isn't there.
    if draw_detections(frame, mask_blue, "BLUE", (255, 0, 0)):
        if current_signal == '0': # Only set to '2' if Red wasn't found
            current_signal = '2'

    # Send signal to Microcontroller ONLY when it changes
    if ser and current_signal != last_signal:
        ser.write(current_signal.encode())
        print(f"Signal sent: {current_signal}")
        last_signal = current_signal

    # --- VISUALS ---
    #cv2.imshow("Detection System", frame)
    large_frame = cv2.resize(frame, (800, 800), interpolation=cv2.INTER_LINEAR)
    
    cv2.imshow("Detection System ", large_frame)
    # Optional: Uncomment below to see the blue mask for debugging
    # cv2.imshow("Blue Mask Debug", mask_blue)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
if ser:
    ser.close()
cap.release()
cv2.destroyAllWindows()
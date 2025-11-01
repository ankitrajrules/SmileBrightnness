"""
SmileBrightness - Automatic screen brightness control based on smile detection.

This script uses computer vision to detect faces and smiles in real-time using
the webcam. When a smile is detected, the screen maintains its original brightness.
When no smile is detected for a certain number of frames, the screen dims.

Author: Your Name
License: MIT
"""

import cv2
import screen_brightness_control as sbc
import time
from typing import Tuple, List

# Configuration constants
FACE_SCALE_FACTOR = 1.3
FACE_MIN_NEIGHBORS = 5
FACE_MIN_SIZE = (30, 30)
SMILE_SCALE_FACTOR = 1.8
SMILE_MIN_NEIGHBORS = 20
SMILE_MIN_SIZE = (25, 25)

def initialize_cascades() -> Tuple[cv2.CascadeClassifier, cv2.CascadeClassifier]:
    """Initialize and return the face and smile cascade classifiers."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    return face_cascade, smile_cascade

# Additional configuration constants
NO_SMILE_THRESHOLD = 30  # Consecutive frames without smile to trigger
LOWER_BRIGHTNESS = 30    # Brightness level when not smiling

def get_initial_brightness() -> int:
    """Get and return the initial screen brightness."""
    original_brightness = sbc.get_brightness()
    if isinstance(original_brightness, list):
        return original_brightness[0]  # Use first monitor's brightness
    return original_brightness

def detect_smile(frame: cv2.Mat, face_cascade: cv2.CascadeClassifier, 
                smile_cascade: cv2.CascadeClassifier) -> bool:
    """
    Detect smiles in the given frame.
    
    Args:
        frame: The input frame from the webcam
        face_cascade: The face detection cascade classifier
        smile_cascade: The smile detection cascade classifier
    
    Returns:
        bool: True if a smile is detected, False otherwise
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 
                                        scaleFactor=FACE_SCALE_FACTOR,
                                        minNeighbors=FACE_MIN_NEIGHBORS,
                                        minSize=FACE_MIN_SIZE)
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray,
                                              scaleFactor=SMILE_SCALE_FACTOR,
                                              minNeighbors=SMILE_MIN_NEIGHBORS,
                                              minSize=SMILE_MIN_SIZE)
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        if len(smiles) > 0:
            # Draw smile rectangle(s)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(frame, (x+sx, y+sy), 
                            (x+sx+sw, y+sy+sh), (0, 255, 0), 2)
            return True
    
    return False

def main():
    """Main function to run the smile detection and brightness control."""
    face_cascade, smile_cascade = initialize_cascades()
    original_brightness = get_initial_brightness()
    consecutive_no_smile = 0
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            smile_detected = detect_smile(frame, face_cascade, smile_cascade)
            
            # Display the frame
            cv2.imshow('SmileBrightness', frame)
            
            # Brightness control logic
            if smile_detected:
                consecutive_no_smile = 0
                sbc.set_brightness(original_brightness)
            else:
                consecutive_no_smile += 1
                if consecutive_no_smile >= NO_SMILE_THRESHOLD:
                    sbc.set_brightness(LOWER_BRIGHTNESS)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(0.2)  # Reduce CPU usage
            
    finally:
        # Cleanup resources
        cap.release()
        cv2.destroyAllWindows()
        sbc.set_brightness(original_brightness)  # Restore original brightness

if __name__ == "__main__":
    main()
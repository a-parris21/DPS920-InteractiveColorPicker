import cv2
import numpy as np
from hand_detection import HandDetector  # Replace 'your_module_name' with the actual module name

def main():
    # Create an instance of the HandDetector class
    hand_detector = HandDetector()

    # Open a connection to the default camera (0) or a video file
    cap = cv2.VideoCapture(0)  # Change to the path of your video file if needed

    while cap.isOpened():
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        # Find hand landmarks and check for pointing gesture
        frame, results = hand_detector.find_hand(frame)
        hand_position = hand_detector.find_position(frame)

        # Check if pointing gesture is detected
        if hand_detector.is_pointing(hand_position):
            # Get the position of the pointing finger
            pointing_finger_position = hand_position[8] if len(hand_position) > 8 else None
            if pointing_finger_position:
                print(f"Pointing detected at position: {pointing_finger_position[1:]}")

        # Display the frame with hand landmarks
        cv2.imshow("Hand Tracking", frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

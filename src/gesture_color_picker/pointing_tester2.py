import cv2
import numpy as np
import pyautogui
from hand_detection import HandDetector  # Replace 'your_module_name' with the actual module name

# Set the center and radius of the circle
circle_center = (320, 240)
circle_radius = 90

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

        # Get the screen dimensions dynamically
        screen_width_px, screen_height_px = pyautogui.size()

        # Calculate pixels per centimeter based on the screen width
        pixels_per_cm = screen_width_px / 20  # Assume a width of 20 centimeters for illustration

        # Check if pointing gesture is detected and hand is pointing at the circle
        if hand_detector.is_pointing(hand_position):
            # Calculate the distance to the circle in centimeters
            distance_to_circle_cm = np.sqrt((hand_position[8][1] - circle_center[0])**2 + (hand_position[8][2] - circle_center[1])**2) / pixels_per_cm

            # Print the distance for debugging
            print("Distance to Circle (cm):", distance_to_circle_cm)

            if distance_to_circle_cm <= circle_radius:
                print("Pointing detected!")

                # Draw a circle on the screen using PyAutoGUI
                pyautogui.click(circle_center)

        # Draw the circle on the frame
        cv2.circle(frame, circle_center, circle_radius, (0, 255, 0), 2)

        # Display the frame with hand landmarks and the circle
        cv2.imshow("Hand Tracking", frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

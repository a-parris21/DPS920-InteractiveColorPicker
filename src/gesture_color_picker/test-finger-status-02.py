import cv2
from hand_detection import HandDetector

# PLEASE NOTE: This is supposed to be a variation of `test-finger-status.py` that only prints the messages
# when a specific key is pressed. However, it does not operate as intended and prints a message only
# on start-up and when a new hand is detected.

def main():
    # Create an instance of HandDetector
    hand_detector = HandDetector(static_mode=True, max_hands=1)

    # Open a video capture object (0 corresponds to the default camera)
    cap = cv2.VideoCapture(0)

    finger_status_printed = False  # Flag to track whether finger status has been printed

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Find hands in the frame
        frame_with_landmarks, results = hand_detector.find_hand(frame, draw=True)

        if results.multi_hand_landmarks:
            # Find positions of landmarks
            lst_position = hand_detector.find_position(frame)

            # Check finger status
            finger_status = hand_detector.fingerUp(lst_position)

            # Check if 'S' key is pressed and print message
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s') and not finger_status_printed:  # Check for 's' instead of 'S'
                print("Finger Status:", finger_status)
                finger_status_printed = True
            elif key != ord('s'):
                finger_status_printed = False  # Reset the flag if 'S' key is not pressed

        # Display the frame with landmarks
        cv2.imshow("Hand Detection", frame_with_landmarks)

        # Break the loop if 'q' key is pressed
        if key == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

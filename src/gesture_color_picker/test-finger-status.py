import cv2
from hand_detection import HandDetector

# PLEASE NOTE: This program continuously prints the finger status every frame which is a lot of data
# and can result in lag as well as inconsistent messsage printing speed. This is purely for testing.

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

            # Print finger status only once when a hand is detected
            if not finger_status_printed:
                print("Finger Status:", finger_status)
                finger_status_printed = True
        else:
            finger_status_printed = False  # Reset the flag if no hand is detected

        # Display the frame with landmarks
        cv2.imshow("Hand Detection", frame_with_landmarks)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

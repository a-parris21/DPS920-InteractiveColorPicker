import cv2
from hand_detection import HandDetector

def main():
    # Create an instance of HandDetector
    hand_detector = HandDetector(static_mode=True, max_hands=1)

    # Open a video capture object (0 corresponds to the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Find hands in the frame
        frame_with_landmarks, results = hand_detector.find_hand(frame, draw=True)

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

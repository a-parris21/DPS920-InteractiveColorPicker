import cv2
from hand_detection import HandDetector

# Initialize the HandDetector
hand_detector = HandDetector()

# Set the initial value of the print_msg_flag
print_msg_flag = True

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Check if 'M' key is pressed to reset print_msg_flag
    key = cv2.waitKey(1)
    if key == ord('M') or key == ord('m'):
        print(f"print_msg_flag was = {print_msg_flag}")
        print_msg_flag = True
        print(f"print_msg_flag = {print_msg_flag}")

    # Find hand and landmarks
    frame, results = hand_detector.find_hand(frame)

    # Find positions of landmarks
    lst_position = hand_detector.find_position(frame)

    # Check if the hand is pointing
    is_pointing = hand_detector.is_pointing(lst_position)

    # Print coordinates if the hand is pointing and print_msg_flag is True
    if is_pointing and print_msg_flag:
        thumb_tip = lst_position[4]
        index_finger_tip = lst_position[8]

        print(f"Thumb Tip Coordinates: {thumb_tip[1]:.4f}, {thumb_tip[2]:.4f}")
        print(f"Index Finger Tip Coordinates: {index_finger_tip[1]:.4f}, {index_finger_tip[2]:.4f}")

        # Set print_msg_flag to False
        print_msg_flag = False

    cv2.imshow("Hand Detection", frame)

    # Break the loop if 'Esc' key is pressed
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

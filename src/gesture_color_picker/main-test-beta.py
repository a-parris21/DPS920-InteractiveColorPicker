import cv2 as cv
import numpy as np
import pygame
from hand_detection import HandDetector

# READ ME!
# This version of the program correctly detects when the index finger tip, landmark #8, enters or leaves
# the clear button bounding box. I haven't sorted out all the logic just yet but this detects and computes
# the coordinates correctly.

# Initialize the camera (change the camera index if needed)
cap = cv.VideoCapture(0)  # 0 corresponds to the default camera, you can adjust it based on your setup

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Initialize Pygame
pygame.init()

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Define colors for palette and <clear> button
COLORS = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]  # Red, Yellow, Green, Blue
CLEAR_BTN_COLOR = (240, 240, 240)

# Define bounding boxes (as tuples) for colour buttons and clear button.
palette_bboxes = []
for i in range(len(COLORS)):
    palette_bboxes.append((i * 100, 0, 100, 50))

clear_btn_bbox = (540, 50, 100, 100)
clear_btn_bbox_normalized = (540/DISPLAY_WIDTH , 50/DISPLAY_HEIGHT, 100/DISPLAY_WIDTH, 100/DISPLAY_HEIGHT)

# Initialize the active color
active_color = COLORS[0]
active_color_index = -1

# Font for the button text
font = pygame.font.Font(None, 24)

# Create a Pygame window
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Interactive Color Picker")

# Tracks whether the camera is rotated incorrectly.
CAM_ROTATION_FLAG = 1
CAM_FLIP_FLAG = 0  # Tracks whether the camera is mirrored.


# This function fixes any incorrect rotation & flipping of the camera.
# Accepts as parameters two flags and the camera frame object and returns the correctly oriented camera.
def fix_cam_orientation(cam_frame):
    if CAM_ROTATION_FLAG == 1:  # The camera was incorrectly rotated 90 deg clockwise
        cam_frame = cv.rotate(cam_frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    elif CAM_ROTATION_FLAG == 2:  # The camera was incorrectly rotated 180 deg
        cam_frame = cv.rotate(cam_frame, cv.ROTATE_180)
    elif CAM_ROTATION_FLAG == 3:  # The camera was incorrectly rotated 90 deg counterclockwise
        cam_frame = cv.rotate(cam_frame, cv.ROTATE_90_CLOCKWISE)

    # Original video output is always mirrored horizontally
    # so flip the camera horizontally at least once.
    # cam_frame = cv.flip(cam_frame, 0)

    if CAM_FLIP_FLAG == 1:  # The camera was not initially mirrored horizontally, revert it.
        cam_frame = cv.flip(cam_frame, 0)
    elif CAM_FLIP_FLAG == 2:  # The camera was mirrored vertically .
        cam_frame = cv.flip(cam_frame, 1)
    elif CAM_FLIP_FLAG == 3:  # The camera was mirrored horizontally & vertically.
        cam_frame = cv.flip(cam_frame, -1)

    return cam_frame


# Apply coordinate fixes based on camera transformations.
# Actually this may not work
def fix_coordinates(orig_x, orig_y, normalize_flag):
    new_x, new_y = 0, 0
    max_width = 1.00
    max_height = 1.00
    if normalize_flag:
        max_width = 1.00
        max_height = 1.00
    else:
        max_width = DISPLAY_WIDTH
        max_height = DISPLAY_HEIGHT

    if CAM_ROTATION_FLAG == 1:  # Correction was applied: rotated 90 deg counterclockwise
        new_x = max_height - orig_y
        new_y = orig_x
    elif CAM_ROTATION_FLAG == 2:  # Correction was applied: rotated 180 deg
        new_x = max_height - orig_y
        new_y = max_width - orig_x
    elif CAM_ROTATION_FLAG == 3:  # Correction was applied: 90 deg clockwise
        new_x, new_y = orig_y, (max_width - orig_x)
        new_x = orig_y
        new_y = max_width - orig_x

    if CAM_FLIP_FLAG == 1:  # Correction was applied: flipped horizontally
        new_x = max_width - orig_x
        new_y = orig_y
    elif CAM_FLIP_FLAG == 2:  # Correction was applied: flipped vertically
        new_x = orig_x
        new_y = max_height - orig_y
    elif CAM_FLIP_FLAG == 3:  # Correction was applied: flipped horizontally & vertically
        new_x = max_width - orig_x
        new_y = max_height - orig_y

    new_x, new_y = orig_y, orig_x

    return new_x, new_y


def is_landmark_in_range(rectangle, landmark_index, lst_position):
    ret_val = False

    if len(lst_position) >= 21 and 0 <= landmark_index < 21:
        # Get the coordinates of the specified landmark
        orig_x = lst_position[landmark_index][1]
        orig_y = lst_position[landmark_index][2]

        # Unpack the tuple to get x_min, y_min, width, and height
        x_min_rect, y_min_rect, rect_width, rect_height = rectangle

        # Check if the landmark is within the specified rectangular range
        ret_val = (
            x_min_rect <= orig_x <= x_min_rect + rect_width and
            y_min_rect <= orig_y <= y_min_rect + rect_height
        )
    return ret_val


# should internally detect the hand position, compute which  colour region the hand is in, and return the index of that colour
def detect_hand():
    return 0


# accept as parameter the index of the new active color and change the active color
def update_active_color(new_color):
    global active_color

    if (new_color >= 0) and (new_color <= 3):
        active_color = COLORS[new_color]
    else:
        active_color = None
    return 0


def generate_feedback():
    return 0


def gimme_string(bbox):
    x1, y1, w, h = bbox
    x2 = x1 + w
    y2 = y1 + h
    stringggg = f"{x1},{y1} | {x2},{y2}"
    return stringggg

# Initialize HandDetector
hand_detector = HandDetector()

run_while_loop = True
while run_while_loop:
    # Capture the video frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = fix_cam_orientation(frame)

    # Convert the OpenCV frame to Pygame surface
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    pygame_frame = pygame.surfarray.make_surface(frame)

    # Draw the camera frame onto the Pygame surface
    screen.blit(pygame_frame, (0, 0))

    # Draw the color palette
    for i, color in enumerate(COLORS):
        pygame.draw.rect(screen, color, palette_bboxes[i])

    # Draw the CLEAR button
    clear_button_rect = pygame.draw.rect(screen, CLEAR_BTN_COLOR, clear_btn_bbox)
    clear_button_text = font.render("CLEAR", True, (0, 0, 0))
    text_rect = clear_button_text.get_rect()
    text_rect.center = clear_button_rect.center
    screen.blit(clear_button_text, text_rect.topleft)

    if active_color is not None:
        # Draw the active color indicator
        pygame.draw.rect(screen, active_color, (0, 300, 50, 50))

    # HAND DETECTION HERE
    # Define code inside 'detect_hand()' function unless otherwise needed.
    hand_index = detect_hand()  # Adjust this based on your actual gesture detection logic

    if hand_index is not None:
        # active_color_index = hand_index
        # update_active_color(active_color_index)
        zz = 0

    # Hand detection
    _, hand_results = hand_detector.find_hand(frame, draw=False)

    # Get hand positions
    hand_positions = hand_detector.find_position(frame)

    message_printed_flag = False

    # Check if hand positions are available
    if hand_positions:
        # Assuming screen_resolution is a tuple (screen_width, screen_height)
        scaling_factor_x = DISPLAY_WIDTH
        scaling_factor_y = DISPLAY_HEIGHT

        scaled_hand_positions = []
        fixed_hand_positions = []
        # Scale the hand positions
        for id, x, y in hand_positions:
            fx, fy = fix_coordinates(x, y, True)
            scaled_x = fx * scaling_factor_x
            scaled_y = fy * scaling_factor_y
            scaled_hand_positions.append([id, scaled_x, scaled_y])
            fixed_hand_positions.append([id, fx, fy])

        formatted_elements = [f"ID: {id}, X: {x:.4f}, Y: {y:.4f}" for id, x, y in hand_positions]
        result_string = " | ".join(formatted_elements)

        # Check if any landmark overlaps with the clear button bounding box
        for id, x, y in hand_positions:
            #if is_landmark_in_range(clear_btn_bbox, id, scaled_hand_positions):
            if not message_printed_flag:
                message_printed_flag = True
                print(f"CLEAR Button Bounding Box: {gimme_string(clear_btn_bbox)}")
                print(f"CLEAR Button Normalized: {gimme_string(clear_btn_bbox_normalized)}")
                print(f"Index 8 - {hand_positions[8]}")
                print(f"Index 8 Fix - {fixed_hand_positions[8]}")
                print(f"Hand Landmarks - {result_string}")
                if is_landmark_in_range(clear_btn_bbox_normalized, 8, fixed_hand_positions):
                    print(f"Found! Landmark 8 is in the box")
                if is_landmark_in_range(clear_btn_bbox, 8, scaled_hand_positions):
                    print(f"Found! Unnormalized Landmark 8 is in the box")

    # FEEDBACK HERE
    # Your code for gesture recognition and actions
    # Check the position of the hand and perform actions accordingly

    # Update the display
    pygame.display.flip()

    # Break the loop if a key is pressed (for example, 'q' for quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_while_loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run_while_loop = False
            elif event.key == pygame.K_m:
                message_printed_flag = False
# can add handler code for another key to let the user return to main menu, and use ESC to fully quit

# Release the camera and close all windows
cap.release()
cv.destroyAllWindows()

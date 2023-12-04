import cv2
import numpy as np
import pygame

# Initialize the camera (change the camera index if needed)
cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can adjust it based on your setup

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Initialize Pygame
pygame.init()

CLEAR_BTN_COLOR = (240, 240, 240)

# Define colors in your palette
colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]  # Red, Yellow, Green, Blue

# Initialize the active color
active_color = None
active_color_index = -1

# Font for the button text
font = pygame.font.Font(None, 24)

# Create a Pygame window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Interactive Color Picker")


CAM_ROTATION_FLAG = 1  # Tracks whether the camera is rotated incorrectly.
CAM_FLIP_FLAG = 0  # Tracks whether the camera is flipped incorrectly.


# This function fixes any incorrect rotation & flipping of the camera.
# Accepts as parameters two flags and the camera frame object and returns the correctly oriented camera.
def fix_cam_orientation(cam_frame, rotate_flag, flip_flag):
    # The camera is incorrectly rotated 90 deg clockwise
    if rotate_flag == 1:
        cam_frame = cv2.rotate(cam_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # The camera is incorrectly rotated 90 deg counterclockwise
    elif rotate_flag == 2:
        cam_frame = cv2.rotate(cam_frame, cv2.ROTATE_90_CLOCKWISE)
    # The camera is incorrectly rotated 180 deg
    elif rotate_flag == 3:
        cam_frame = cv2.rotate(cam_frame, cv2.ROTATE_180)

    # The camera is incorrectly horizontally flipped
    if flip_flag == 1:
        cam_frame = cv2.flip(cam_frame, 0)
    # The camera is incorrectly vertically flipped.
    elif flip_flag == 2:
        cam_frame = cv2.flip(cam_frame, 1)
    # The camera is incorrectly horizontally & vertically flipped.
    elif flip_flag == 3:
        cam_frame = cv2.flip(cam_frame, -1)

    return cam_frame


# should internally detect the hand position, compute which  colour region the hand is in, and return the index of that colour
def detect_hand():
    return 0


# accept as parameter the index of the new active color and change the active color
def update_active_color(new_color):
    global active_color

    if (new_color >= 0) and (new_color <= 3):
        active_color = colors[new_color]
    else:
        active_color = None
    return 0


def generate_feedback():
    return 0


run_while_loop = True
while run_while_loop:
    # Capture the video frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = fix_cam_orientation(frame, CAM_ROTATION_FLAG, CAM_FLIP_FLAG)

    # Convert the OpenCV frame to Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pygame_frame = pygame.surfarray.make_surface(frame)

    # Draw the camera frame onto the Pygame surface
    screen.blit(pygame_frame, (0, 0))

    # Draw the color palette
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (i * 100, 0, 100, 50))

    # Draw the CLEAR button
    clear_button_rect = pygame.draw.rect(screen, CLEAR_BTN_COLOR, (550, 50, 80, 40))
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
        active_color_index = hand_index
        update_active_color(active_color_index)

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
# can add handler code for another key to let the user return to main menu, and use ESC to fully quit

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

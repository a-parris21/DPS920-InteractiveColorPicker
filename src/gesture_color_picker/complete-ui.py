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
active_color = (255, 0, 0)  # Start with red

# Font for the button text
font = pygame.font.Font(None, 24)

# Create a Pygame window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Interactive Color Picker")

run_while_loop = True
while run_while_loop:
    # Capture the video frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the captured frame
    #cv2.imshow("Video Feed", frame)

    # Get the dimensions of the video
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #print(f"Video dimensions: {width} x {height}")

    # Rotate the camera (FLIPPED ON MY SYSTEM)
    # Rotate the frame 90 degrees anticlockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Convert the OpenCV frame to Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pygame_frame = pygame.surfarray.make_surface(frame)

    # Draw the camera frame onto the Pygame surface
    screen.blit(pygame_frame, (0, 0))

# HAND DETECTION HERE
    # Your code for hand detection

    # Draw the color palette
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (i * 100, 0, 100, 50))

    clear_button_rect = pygame.draw.rect(screen, CLEAR_BTN_COLOR, (550, 50, 80, 40))
    clear_button_text = font.render("CLEAR", True, (0, 0, 0))
    text_rect = clear_button_text.get_rect()
    text_rect.center = clear_button_rect.center
    screen.blit(clear_button_text, text_rect.topleft)

    # Draw the active color indicator
    pygame.draw.rect(screen, active_color, (0, 300, 50, 50))

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

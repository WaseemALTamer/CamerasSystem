from TickSystem import FpsController
import pygame
import sys
import numpy as np
from PIL import Image


# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Display Image')



# Load the JPEG image using Pillow
image_path = 'Image.jpg'  # Replace with the path to your JPEG image
pil_image = Image.open(image_path)
image_array = np.array(pil_image)


# Create a dummy image (1080p resolution, 1 frame)
width, height = 1920, 1080
frame_data = np.zeros((height, width, 3), dtype=np.uint8)
frame_data[:, :, 0] = 255  # Red channel to max (red frame)





# Load image
image_path = 'Image.jpg'  # Replace with the path to your image
image = pygame.image.load(image_path)


# Main loop
FrameRateControll = FpsController()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            # Update the display surface to the new size
            width, height = event.size

        

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    dummy_image = pygame.surfarray.make_surface(image_array)

    Resizedimage = pygame.transform.scale(dummy_image, (width, height))  # Scale image to fit screen (optional)
    screen.blit(Resizedimage, (0, 0))

    # Update the display
    pygame.display.update()
    FrameRateControll.ShowFps()
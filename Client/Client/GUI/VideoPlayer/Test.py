import pygame

# Initialize Pygame
pygame.init()

# Surface dimensions
width, height = 400, 300

# Create a surface with alpha transparency
surface = pygame.Surface((width, height), pygame.SRCALPHA)

# Define colors
color1 = (255, 0, 0, 255)  # Red with full opacity
color2 = (0, 0, 255, 255)  # Blue with full opacity

# Fill the left half of the surface with color1
pygame.draw.rect(surface, color1, pygame.Rect(0, 0, width // 2, height))

# Fill the right half of the surface with color2
pygame.draw.rect(surface, color2, pygame.Rect(width // 2, 0, width // 2, height))

# Display the surface on a screen (for demonstration)
screen = pygame.display.set_mode((width, height))
screen.blit(surface, (0, 0))
pygame.display.flip()

# Event loop to keep window open (for demonstration)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
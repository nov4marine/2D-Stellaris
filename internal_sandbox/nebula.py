import pygame
import noise
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Generate noise-based nebula
width, height = 800, 600
nebula = pygame.Surface((width, height))

for x in range(width):
    for y in range(height):
        value = noise.pnoise2(x * 0.005, y * 0.005, octaves=6)  # Smooth noise
        brightness = int((value + 1) * 127)  # Normalize to 0-255
        nebula.set_at((x, y), (brightness, brightness//2, 255))  # Blue-tinted nebula

running = True
while running:
    screen.fill((0, 0, 0))  # Black background
    screen.blit(nebula, (0, 0))  # Render nebula texture
    pygame.display.flip()  # Refresh screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


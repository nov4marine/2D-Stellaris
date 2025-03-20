# This is also a copilot template for the main game loop. only partially functional and was rewritten as mygame.py

import pygame
import sys
import pygame_gui.elements.ui_label
import config
import pygame_gui
from src.camera import Camera
from src.galaxy import Galaxy
from src.solar_system import SolarSystem
from src.gui import GUIManager

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 2000
MAP_HEIGHT = 2000
PAN_SPEED = 5
EDGE_THRESHOLD = 50

def main():
    """main game loop for now"""

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stellaris-Inspired Game")
    clock = pygame.time.Clock()

    #initialize Pygame GUI
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    gui_manager = GUIManager(SCREEN_WIDTH, SCREEN_HEIGHT, manager)

    galaxy = Galaxy()  # Initialize the galaxy
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)  # Initialize the camera

    current_view = "galaxy" #track which view is the current view
    solar_system = None #placeholder for solar system

    running = True
    while running:
        #behold the clock
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # one left click
                if current_view == "galaxy":
                    #check if star is clicked
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_star = galaxy.get_hovered_star(mouse_x, mouse_y, camera.x, camera.y, camera.zoom)
                    if clicked_star:
                        print(f"switching to solar system view for {clicked_star['name']}")
                        solar_system = SolarSystem(star_name=clicked_star["name"])
                        current_view = "solar system"
                        gui_manager.initialize_solar_system_gui(solar_system.star_name)

            #process input while in solar system view
            if current_view == "solar system" and event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == gui_manager.return_button:
                    gui_manager.clear_gui()
                    current_view = "galaxy"

            manager.process_events(event)

        #handle stuff in galaxy view
        if current_view == "galaxy":
            # Handle zooming input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_EQUALS]:  # Zoom in
                camera.apply_zoom(0.1, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif keys[pygame.K_MINUS]:  # Zoom out
                camera.apply_zoom(-0.1, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Update the camera (handles panning logic)
            camera.update(PAN_SPEED, EDGE_THRESHOLD, SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT)

            # Get hovered star for tooltips or interactivity
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hovered_star = galaxy.get_hovered_star(mouse_x, mouse_y, camera.x, camera.y, camera.zoom)

            # Render the galaxy using the camera's position and zoom
            screen.fill((0, 0, 0))
            galaxy.draw(screen, camera.x, camera.y, camera.zoom, hovered_star)
            gui_manager.initialize_galaxy_gui()


            #update tooltip
            if hovered_star:
                gui_manager.tooltip.set_text(f"{hovered_star['name']} ({hovered_star['type']})")
                gui_manager.tooltip.set_relative_position((mouse_x + 10, mouse_y + 10)) #offsets tooltip slightly
                gui_manager.tooltip.show()
            else:
                gui_manager.tooltip.hide()

        #handle stuff in solar system view
        elif current_view == "solar system":
            solar_system.update(time_delta)
            gui_manager.tooltip.hide()
            #render solar system view
            screen.fill((0, 0, 0))
            solar_system.draw(screen)
            
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

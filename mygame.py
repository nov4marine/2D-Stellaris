import sys 
import pygame
import pygame_gui

from src.camera import Camera
from src.galaxy import Galaxy
from src.solar_system import SolarSystem
from src.gui import GUIManager
from src.input import StellarisInputManager

screen_width = 1920
screen_height = 1080

class Stellaris_2D:
    """yes, game is a class, just roll with it for better organization?"""

    def __init__(self): 
        """"initialize game?"""
        pygame.init()

        #pretend the "selfs" aren't there; it'll be easier to grasp
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("2D Stellaris")
        self.manager = pygame_gui.UIManager((screen_width, screen_height))

        #instance classes for in-game objects here?
        self.galaxy = Galaxy()
        self.camera = Camera(screen_width, screen_height)
        self.input_manager = StellarisInputManager()
        self.gui_manager = GUIManager(screen_width, screen_height, self.manager)

        self.game_state = {
            "view_mode": "galaxy",  # or "solar_system"
            "selected_star": None,  # The star selected in the galaxy view
            "current_solar_system": None,  # The solar system currently being viewed
        }

    def run_game(self): 
        """this is the game loop for now"""
        while True:
            self.time_delta = self.clock.tick(60) / 1000
            self._input()
            self._update()
            self._render()
            self._render_gui()

    def _input(self):
        """handle and apply input"""
        self.input_manager.process_input(self.camera, self.galaxy, self.manager, self.game_state)
        self.input_manager.handle_camera_panning(self.camera)
        
    def _update(self): 
        """update state of the game/simulation with new input and time that has passed"""
        self.galaxy.update_solar_systems(self.time_delta) # ONLY updates orbits of planets
        self.manager.update(self.time_delta) # Update the GUI manager
        self.camera.update_zoom() # Smoothly update the camera zoom

    def _render(self):
        """MY render to screen new stuf function method"""
        self.screen.fill((0, 0, 20))
        if self.game_state["view_mode"] == "galaxy":
            self.galaxy.render_galaxy(self.screen, self.camera)
        elif self.game_state["view_mode"] == "solar_system":
            solar_system = self.game_state["current_solar_system"]
            if solar_system: #ensure solar systme exists
                solar_system.render_solarsystem(self.screen, self.camera, self.game_state["selected_star"])

    def _render_gui(self):
        """render GUI elements"""
        if self.game_state["view_mode"] == "galaxy":
            self.gui_manager.clear_gui()
            self.gui_manager.initialize_galaxy_gui()
        elif self.game_state["view_mode"] == "solar_system":
            self.gui_manager.clear_gui()
            solar_system_name = self.game_state["selected_star"]["name"]
            self.gui_manager.initialize_solar_system_gui(solar_system_name)

        #draw the gui elements
        self.manager.draw_ui(self.screen)
        
        # Draw the whole game screen
        pygame.display.flip()
        

Stellaris_2D().run_game()

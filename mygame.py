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
        self.gui_manager = GUIManager

        self.view_mode = "galaxy"


    def run_game(self): 
        """this is the game loop for now"""
        while True:
            self.time_delta = self.clock.tick(60) / 1000
            self._input()
            self._update()
            self._render()

    def _input(self):
        """handle and apply input"""
        self.input_manager.process_input(self.galaxy, self.camera)
        self.input_manager.handle_camera_panning(self.camera)

    def _update(self): 
        """update state of the game/simulation with new input and time that has passed"""
        self.galaxy.update_solar_systems(self.time_delta)

    def _render(self):
        """MY render to screen new stuf function method"""
        self.screen.fill((0, 0, 20))
        if self.view_mode == "galaxy":
            self.galaxy.render_galaxy(self.screen, self.camera)
        elif self.view_mode == "solar_system":
            self.solar_system.render_solarsystem(self.screen, self.camera)
        
        pygame.display.flip()
        

Stellaris_2D().run_game()
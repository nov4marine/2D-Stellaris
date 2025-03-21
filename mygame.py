import sys 
import pygame
import pygame_gui

from src.camera import Camera
from src.galaxy import Galaxy
from src.solar_system import SolarSystem
from src.gui import GUIManager
from src.input import StellarisInputManager
import src.globalVars

screen_width = 800
screen_height = 600

class Stellaris_2D:
    """yes, game is a class, just roll with it for better organization?"""

    def __init__(self): 
        """"initialize game?"""
        pygame.init()

        #pretend the "selfs" aren't there; it'll be easier to grasp
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("2D Stellaris")
        self.manager = pygame_gui.UIManager((screen_width, screen_height), './2D-Stellaris/src/theme.json')

        #instance classes for in-game objects here?
        self.galaxy = Galaxy()
        self.camera = Camera(screen_width, screen_height, self.screen)
        self.input_manager = StellarisInputManager()
        self.gui_manager = GUIManager(screen_width=screen_width, screen_height=screen_height, manager=self.manager)
        self.manager.set_visual_debug_mode(True)
        

        src.globalVars.init()

        src.globalVars.curr_solar_system = None
        src.globalVars.view_mode = "galaxy"
        src.globalVars.view_switched = False

        self.background = pygame.Surface((screen_width, screen_height))
        self.background.fill((0, 0 ,20))


    def run_game(self): 
        """this is the game loop for now"""
        while True:
            self.time_delta = self.clock.tick(60) / 1000
            self._input()
            self._update()
            self.screen.blit(self.background, (0, 0))

            self._render()

            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)

    def _input(self):
        """handle and apply input"""
        self.input_manager.process_input(self.galaxy, self.camera)
        self.input_manager.handle_camera_panning(self.camera)
        self.camera.update_zoom()

    def _update(self): 
        """update state of the game/simulation with new input and time that has passed"""
        self.galaxy.update_solar_systems(self.time_delta)

    def _render(self):
        """MY render to screen new stuf function method"""
        if src.globalVars.view_mode == "galaxy":
            self.galaxy.render_galaxy(self.screen, self.camera)
            if src.globalVars.view_switched == True:
                self.gui_manager.initialize_galaxy_gui()
        elif src.globalVars.view_mode == "solar_system":
            if src.globalVars.view_switched == True:
                self.gui_manager.initialize_solar_system_gui(src.globalVars.curr_solar_system.star_name)
                self.manager.root_container.recalculate_container_layer_thickness()
            src.globalVars.curr_solar_system.render_solarsystem(self.screen, self.camera)
            
        
        pygame.display.flip()
        

Stellaris_2D().run_game()

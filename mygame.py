import sys 
import pygame
import pygame_gui

from src.gui import SolarSystemGUI, GUIManager, GalaxyGUI
from src.camera import Camera
from src.input import MenuInputManager
from src.game_state import game_state
from src.player_manager import PlayerManager, HumanPlayer, AIPlayer

from src.main_menu import MainMenuUI, NewGameUI

from src.nation import Nation

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

        #this is the lower level GUI manager from pygame_gui module. not my GUI manager. This manager IS REQUIRED to be passed to my GUI manager for ALL UI elements to work.
        self.pygui_manager = pygame_gui.UIManager((screen_width, screen_height)) 

        #instance classes for in-game objects here?
        self.camera = Camera(screen_width, screen_height)
        self.menu_input_manager = MenuInputManager()

        #render background images
        self.galaxy_background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/galaxy_background.png").convert()
        self.solar_system_background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/solar_system_background.png").convert()
        self.solar_system_background = pygame.transform.scale(self.solar_system_background, (screen_width, screen_height))
        self.galaxy_background = pygame.transform.scale(self.galaxy_background, (screen_width, screen_height))

        self.game_state = game_state
        self.galaxy = None

    def run_game(self): 
        """this is the game loop for now"""
        while True:
            self.time_delta = self.clock.tick(60) / 1000
            fps = self.clock.get_fps()
            #print(f"FPS: {fps}")

            if self.game_state["current_state"] == "main_menu":
                if not hasattr(self, "menu_ui") or not isinstance(self.menu_ui, MainMenuUI):
                    self.menu_ui = MainMenuUI(self.screen, self.game_state, self.pygui_manager)
                self.menu_input_manager.process_input(self.game_state, self.pygui_manager, self.menu_ui)
                self.menu_ui.draw_background()
                self.pygui_manager.update(self.time_delta)
                self.pygui_manager.draw_ui(self.screen)
                
            elif self.game_state["current_state"] == "new_game":
                if not hasattr(self, "menu_ui") or not isinstance(self.menu_ui, NewGameUI):
                    self.menu_ui = NewGameUI(self.screen, self.game_state, self.pygui_manager)
                self.menu_input_manager.process_input(self.game_state, self.pygui_manager, self.menu_ui)
                self.menu_ui.draw_background()
                self.pygui_manager.update(self.time_delta)
                self.pygui_manager.draw_ui(self.screen)

            elif self.game_state["current_state"] == "settings":
                #menu_ui = SettingsUI(self.screen, self.game_state, self.pygui_manager)  # Display the settings menu
                #self.menu_input_manager.process_input(self.game_state, self.pygui_manager, menu_ui)
                pass  # Placeholder for settings menu logic

            # Expand into other menus as needed using the above patterns

            elif self.game_state["current_state"] == "gameplay":
                if self.game_state["gameplay_initialized"] == False:
                    self.game_state["gameplay_initialized"] = True
                    self.galaxy = self.game_state["galaxy"]
                    self.pygui_manager.clear_and_reset()  # Clear the GUI manager for gameplay
                
                # eventually each player will run a separate instance of the game loop I think?
                self._input()
                self._update()
                self._render()
                #self._render_gui()
                #draw the gui elements
                self.pygui_manager.update(self.time_delta)  # Update the GUI manager
                self.pygui_manager.draw_ui(self.screen)  # Draw the GUI elements
            
            pygame.display.flip()  # Update the display

            
    def _input(self):
        """handle and apply input"""
        for player in self.game_state["player_manager"].players:
            if isinstance(player, HumanPlayer):
                player.input_manager.process_input(self.camera, self.galaxy, self.pygui_manager, self.game_state)
            elif isinstance(player, AIPlayer):
                # AI input handling logic here
                pass

        
    def _update(self): 
        """update state of the game/simulation with new input and time that has passed"""
        self.galaxy.update_solar_systems(self.time_delta) # ONLY updates orbits of planets
        self.pygui_manager.update(self.time_delta) # Update the GUI manager
        self.camera.update_zoom() # Smoothly update the camera zoom

    def _render(self):
        """MY render to screen new stuf function method"""
        self.screen.fill((0, 0, 50))
        if self.game_state["view_mode"] == "galaxy":
            self.screen.blit(self.galaxy_background, (0, 0))  # Draw the galaxy background
            self.galaxy.render_galaxy(self.screen, self.camera)
        elif self.game_state["view_mode"] == "solar_system":
            self.screen.blit(self.solar_system_background, (0, 0))
            solar_system = self.game_state["current_solar_system"]
            if solar_system: #ensure solar systme exists
                solar_system.render_solarsystem(self.screen, self.camera, self.game_state["selected_star"])

    def _render_gui(self):
        """render GUI elements"""

        # Update the core HUD elements with game state information
        if self.game_state["view_mode"] == "galaxy":
            self.galaxy_ui.draw()  # Draw the galaxy UI
        elif self.game_state["view_mode"] == "solar_system":
            if self.solar_system_gui is None:
                self.solar_system_gui = SolarSystemGUI(self.pygui_manager, self.game_state["current_solar_system"], self.nation)
                self.solar_system_gui.draw()  # Draw the solar system UI
            else:
                # Update the solar system UI with the current solar system information
                self.solar_system_gui.star = self.game_state["current_solar_system"]
                self.solar_system_gui.draw()  # Draw the solar system UI

        

Stellaris_2D().run_game()

import sys 
import pygame
import pygame_gui

from src.input import MenuInputManager, GlobalInputManager
from src.game_state import game_state
from src.player_manager import PlayerManager, HumanPlayer, AIPlayer

from src.main_menu import MainMenuUI, NewGameUI

from src.nation import Nation


class Stellaris_2D:
    """yes, game is a class, just roll with it for better organization?"""

    def __init__(self): 
        """"initialize game?"""
        pygame.init()

        #pretend the "selfs" aren't there; it'll be easier to grasp
        self.screen_width = game_state["screen_width"]
        self.screen_height = game_state["screen_height"]
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("2D Stellaris")

        #this is the lower level GUI manager from pygame_gui module. not my GUI manager. This manager IS REQUIRED to be passed to my GUI manager for ALL UI elements to work.
        game_state["pygui_manager"] = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.pygui_manager = game_state["pygui_manager"]

        #instance classes for in-game objects here?
        self.menu_input_manager = MenuInputManager()

        self.game_state = game_state
        self.galaxy = None

        self.game_state["global_ui_manager"] = self.pygui_manager

        self.local_player = None  # Add this line

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
                    # Set the local player
                    self.local_player = next(
                        (p for p in self.game_state["player_manager"].players
                         if isinstance(p, HumanPlayer) and getattr(p, "is_local", True)),
                        None
                    )
                self._input()
                self._update()
                self._render()
                self._render_gui()
                self.pygui_manager.update(self.time_delta)
                self.pygui_manager.draw_ui(self.screen)
            pygame.display.flip()  # Update the display

            
    def _input(self):
        """Handle and apply input for the local player."""
        if self.local_player:
            self.local_player.global_input_manager.process_input()

    def _update(self): 
        """Update the global state of the game/simulation time that has passed"""
        self.galaxy.update_solar_systems(self.time_delta) # ONLY updates orbits of planets
        self.local_player.global_gui_manager.update_all_modules()

    def _render(self):
        """Render to screen."""
        self.screen.fill((0, 0, 50))
        self.local_player.camera.update_zoom()
        view_mode = self.local_player.states.get("view_mode", "galaxy")
        if view_mode == "galaxy":
            self.galaxy.render_galaxy(self.screen, self.local_player.camera)
        elif view_mode == "solar_system":
            solar_system = self.local_player.states["current_solar_system"].solar_system
            solar_system.render(self.screen, self.local_player.camera)

    def _render_gui(self):
        """Render GUI elements for the local human player only."""
        pass  # Placeholder for GUI rendering logic

        

Stellaris_2D().run_game()

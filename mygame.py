import sys 
import pygame
import pygame_gui

from src.gui import SolarSystemGUI, GUIManager, GalaxyGUI
from src.camera import Camera
from src.galaxy import Galaxy
from src.solar_system import SolarSystem
from src.input import StellarisInputManager

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
        self.manager = pygame_gui.UIManager((screen_width, screen_height))

        #instance classes for in-game objects here?
        self.galaxy = Galaxy()
        self.camera = Camera(screen_width, screen_height)
        self.input_manager = StellarisInputManager()
        self.nation = Nation("rome", 10, "rome") #change to a list of nations later
        self.gui_manager = GUIManager(screen_width, screen_height, self.manager, self.nation)
        self.galaxy_ui = GalaxyGUI(self.manager, self.nation) #initialize the galaxy gui
        self.solar_system_gui = None

        #render background images
        self.galaxy_background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/galaxy_background.png").convert()
        self.solar_system_background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/solar_system_background.png").convert()
        self.solar_system_background = pygame.transform.scale(self.solar_system_background, (screen_width, screen_height))
        self.galaxy_background = pygame.transform.scale(self.galaxy_background, (screen_width, screen_height))

        self.game_state = {
            "current_state": "main_menu",  # or "gameplay"

            "view_mode": "galaxy",  # or "solar_system"
            "selected_star": None,  # The star selected in the galaxy view
            "current_solar_system": None,  # The solar system currently being viewed
        }

    def run_game(self): 
        """this is the game loop for now"""
        while True:
            self.time_delta = self.clock.tick(60) / 1000
            fps = self.clock.get_fps()
            print(f"FPS: {fps}")

            if self.game_state["current_state"] == "main_menu":
                self.main_menu()
            elif self.game_state["current_state"] == "gameplay":
                self._input()
                self._update()
                self._render()
                self._render_gui()

    def main_menu(self):
        # Load a background image (make sure you have the file in your directory)
        background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/menu_background.jpg")
        self.screen.blit(background, (0, 0))  # Draw the background image

        # Draw a semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        self.screen.blit(overlay, (0, 0))
        
        # Title text
        menu_font = pygame.font.Font(None, 50)  # Use a cool font if available
        title = menu_font.render("Stellaris 2D", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        # Animated buttons (hover effects)
        mouse_pos = pygame.mouse.get_pos()
        button_font = pygame.font.Font(None, 36)

        # Start Button
        start_rect = pygame.Rect(300, 250, 200, 50)
        start_color = (255, 255, 255) if start_rect.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(self.screen, start_color, start_rect, border_radius=10)
        start_text = button_font.render("Start New Game", True, (0, 0, 0))
        self.screen.blit(start_text, (start_rect.x + 50, start_rect.y + 10))

        # Exit Button
        exit_rect = pygame.Rect(300, 350, 200, 50)
        exit_color = (255, 255, 255) if exit_rect.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(self.screen, exit_color, exit_rect, border_radius=10)
        exit_text = button_font.render("Exit", True, (0, 0, 0))
        self.screen.blit(exit_text, (exit_rect.x + 75, exit_rect.y + 10))

        # Update display
        pygame.display.flip()

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state["current_state"] = "EXIT"
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos):
                    self.game_state["current_state"] = "gameplay"
                elif exit_rect.collidepoint(mouse_pos):
                    self.game_state["current_state"] = "EXIT"
                    sys.exit()
            self.input_manager.main_menu(self.game_state)  # Process input events in the main menu

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
            self.screen.blit(self.galaxy_background, (0, 0))  # Draw the galaxy background
            self.galaxy.render_galaxy(self.screen, self.camera)
        elif self.game_state["view_mode"] == "solar_system":
            self.screen.blit(self.solar_system_background, (0, 0))
            solar_system = self.game_state["current_solar_system"]
            if solar_system: #ensure solar systme exists
                solar_system.render_solarsystem(self.screen, self.camera, self.game_state["selected_star"])

    def _render_gui(self):
        """render GUI elements"""
        if self.gui_manager is None:
            self.gui_manager.initialize_core_hud(self.nation)  # Initialize core HUD elements

        # Update the core HUD elements with game state information
        if self.game_state["view_mode"] == "galaxy":
            self.galaxy_ui.draw()  # Draw the galaxy UI
        elif self.game_state["view_mode"] == "solar_system":
            if self.solar_system_gui is None:
                self.solar_system_gui = SolarSystemGUI(self.manager, self.game_state["current_solar_system"], self.nation)
                self.solar_system_gui.draw()  # Draw the solar system UI
            else:
                # Update the solar system UI with the current solar system information
                self.solar_system_ui.star = self.game_state["current_solar_system"]
                self.solar_system_ui.draw()  # Draw the solar system UI

        #draw the gui elements
        self.manager.draw_ui(self.screen)
        
        # Draw the whole game screen
        pygame.display.flip()
        

Stellaris_2D().run_game()

import pygame
import pygame_gui
import sys
from src.game_state import game_state

###############################################################################
# Menu Input Manager
###############################################################################

class MenuInputManager:
    """Handles input events for menus and setup screens."""

    def process_input(self, game_state, gui_manager, menu_ui):
        for event in pygame.event.get():
            gui_manager.process_events(event)
            menu_ui.handle_events(event)

###############################################################################
# Global Input Manager (in gameplay)
# Handles input events for the entire game, including galaxy and solar system views.
###############################################################################

class GlobalInputManager:
    """Handles all input events for a given player and nation, with different modes for view states."""
    def __init__(self, player, nation=None):
        self.player = player
        self.nation = nation
        self.camera = player.camera
        self.pygui_manager = game_state["pygui_manager"]
        self.galaxy = game_state["galaxy"]
        self.game_ui = player.global_gui_manager

        self.key_states = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_EQUALS: False,
            pygame.K_MINUS: False
        }

    def process_input(self):
        for event in pygame.event.get():

            self.pygui_manager.process_events(event)
            self.game_ui.handle_all_gui_events(event)

            # Global input (quit, ESC, etc.)
            if event.type == pygame.QUIT:
                sys.exit()

            if self.player.states["view_mode"] == "galaxy":
                self.handle_galaxy_input(event)
            elif self.player.states["view_mode"] == "solar_system":
                solar_system = self.player.states["current_solar_system"].solar_system
                self.handle_solar_system_input(event, solar_system)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Example: always return to galaxy view
                        self.player.states["view_mode"] = "galaxy"
                        self.player.states["current_solar_system"] = None
        self.handle_camera_input()

    def handle_galaxy_input(self, event):

        # Key presses/releases
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_states:
                self.key_states[event.key] = True
        if event.type == pygame.KEYUP:
            if event.key in self.key_states:
                self.key_states[event.key] = False

        # Mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for star in self.galaxy.galaxy_stars:
                    if star.rect and star.rect.collidepoint(event.pos):
                        self.player.states["view_mode"] = "solar_system"
                        self.player.states["current_solar_system"] = star

                        self.camera.reset(0, 0, 1)
                        self.camera.center_camera_on_star()
            if event.button == 3:  # Right click
                print("Right click at", pygame.mouse.get_pos())

        if event.type == pygame.MOUSEWHEEL:
            new_zoom = self.camera.target_zoom + (event.y * 0.1)
            cursor_pos = pygame.mouse.get_pos()
            self.camera.zoom_to(new_zoom, cursor_pos)


    def handle_solar_system_input(self, event, solar_system):

        # Key presses/releases
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_states:
                self.key_states[event.key] = True
        if event.type == pygame.KEYUP:
            if event.key in self.key_states:
                self.key_states[event.key] = False

        # Mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Example: select a planet if clicked
                for body in solar_system.bodies:
                    if body.rect and body.rect.collidepoint(event.pos):
                        print(f"Selected planet: {body.name}")
            if event.button == 3:  # Right click
                print("Right click at", pygame.mouse.get_pos())

        if event.type == pygame.MOUSEWHEEL:
            new_zoom = self.camera.target_zoom + (event.y * 0.1)
            cursor_pos = pygame.mouse.get_pos()
            self.camera.zoom_to(new_zoom, cursor_pos)

    def handle_camera_input(self):
        if self.key_states[pygame.K_w]:
            self.camera.move(0, -50)
        if self.key_states[pygame.K_s]:
            self.camera.move(0, 50)
        if self.key_states[pygame.K_a]:
            self.camera.move(-50, 0)
        if self.key_states[pygame.K_d]:
            self.camera.move(50, 0)
        if self.key_states[pygame.K_EQUALS]:
            self.camera.set_zoom(self.camera.target_zoom * 1.05)
        if self.key_states[pygame.K_MINUS]:
            self.camera.set_zoom(self.camera.target_zoom * 0.95)



# In your main loop, instantiate and use the appropriate input manager:
# menu_input_manager = MenuInputManager()
# gameplay_input_manager = GameplayInputManager()
# ...
# if game_state["current_state"] == "main_menu":
#     menu_input_manager.process_input(game_state, gui_manager, menu_ui)
# elif game_state["current_state"] == "gameplay":
#     gameplay_input_manager.process_input(camera, galaxy, gui_manager, game_state)
    
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #   mouse_x, mouse_y = pygame.mouse.get_pos()
         #   selected_star = galaxy.get_star_at_position(mouse_x, mouse_y, camera)  # Function to find clicked star
         #   if selected_star is not None:
         #       selected_solar_system = galaxy.solar_systems[selected_star["name"]]  # Fetch solar system
         #       view_mode = "solar_system"

    

    

    #cheat sheet:
    # pygame.event.get() translates to: pygame, fetch all user inputs since the last time 
    #that this function was called (which is usually the previous clock tick)
    #pygame event types: 
        #Keyboard events: KEYDOWN, KEYUP
        #mouse events: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
            #in this context event.pos gives the x,y coordinates of mouse when action occurred
        #window events: QUIT, VIDEORESIZE (which just means window was resized)
        #custom user events can be created using pygame.USEREVENT

    # "fetch" is a bit of a misnomer, as it doesn't actually fetch anything, but rather returns a list of events that have occurred since the last time this function was called.
    # pygame.event.get() is a blocking call, meaning it will wait until an event occurs before returning.
    # .get(thing) is a method that retrieves the value associated with the key "thing" in a dictionary. In this case, it retrieves the value associated with the key "thing" in the dictionary returned by pygame.event.get().
    # .get(thing) basically is you pointing at or having pygame target that thing within whatever context.
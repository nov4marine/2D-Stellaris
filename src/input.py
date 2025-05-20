import pygame
import pygame_gui
import sys

# Only import what you need, and avoid circular imports!

###############################################################################
# Menu Input Manager
###############################################################################

class MenuInputManager:
    """Handles input events for menus and setup screens."""

    def process_input(self, game_state, gui_manager, menu_ui):
        for event in pygame.event.get():
            #print(event)
            gui_manager.process_events(event)
            menu_ui.handle_events(event)


###############################################################################
# Gameplay Input Manager
###############################################################################

class GameplayInputManager:
    """Handles input events for in-game controls."""

    def __init__(self, nation):
        self.key_states = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_EQUALS: False,
            pygame.K_MINUS: False
        }
        self.nation = nation

    def process_input(self, camera, galaxy, gui_manager, game_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            gui_manager.process_events(event)

            # Key presses/releases
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_states:
                    self.key_states[event.key] = True
                if event.key == pygame.K_ESCAPE:
                    game_state["view_mode"] = "galaxy"
                    game_state["selected_star"] = None
                    game_state["current_solar_system"] = None

            if event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False

            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click

                    for star in galaxy.stars:
                        if star["rect"].collidepoint(event.pos): # Check if the star was clicked
                            # If the star was clicked, set the selected star and update the game state
                            game_state["view_mode"] = "solar_system" 
                            game_state["selected_star"] = star
                            game_state["current_solar_system"] = galaxy.solar_systems.get(star["name"])
                            camera.reset(0, 0, 1)
                            camera.center_camera_on_star()
                            
                if event.button == 3:  # Right click
                    print("Right click at", pygame.mouse.get_pos())

            if event.type == pygame.MOUSEWHEEL:
                new_zoom = camera.target_zoom + (event.y * 0.1)
                cursor_pos = pygame.mouse.get_pos()
                camera.zoom_to(new_zoom, cursor_pos)

        self.handle_camera_panning(camera)

    def handle_camera_panning(self, camera):
        if self.key_states[pygame.K_w]:
            camera.move(0, -50)
        if self.key_states[pygame.K_s]:
            camera.move(0, 50)
        if self.key_states[pygame.K_a]:
            camera.move(-50, 0)
        if self.key_states[pygame.K_d]:
            camera.move(50, 0)
        if self.key_states[pygame.K_EQUALS]:
            camera.set_zoom(camera.target_zoom * 1.05)
        if self.key_states[pygame.K_MINUS]:
            camera.set_zoom(camera.target_zoom * 0.95)

###############################################################################
# Usage Example (in your main game loop)
###############################################################################

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
import pygame
import pygame_gui
import sys

class StellarisInputManager:
    """Handles input events and provides key states for real-time controls."""

    def __init__(self):
        # Tracks the state of keys (pressed or not)
        self.key_states = {
            pygame.K_w: False,  # Pan up
            pygame.K_s: False,  # Pan down
            pygame.K_a: False,  # Pan left
            pygame.K_d: False,  # Pan right
            pygame.K_EQUALS: False,  # Zoom in
            pygame.K_MINUS: False  # Zoom out
        }

    def process_input(self, camera, galaxy, manager, game_state):
        """Process input events and update key states."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Exit the program when quitting

            manager.process_events(event)  # Process GUI events

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_states:
                    self.key_states[event.key] = True

            # Handle key releases
            if event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to galaxy view
                    game_state["view_mode"] = "galaxy"
                    game_state["selected_star"] = None
                    game_state["current_solar_system"] = None


            # Handle mouse 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click

                    for star in galaxy.stars:
                        # Check if the mouse position is within the star's hitbox
                        if star["rect"].collidepoint(event.pos):
                            # If it is, set the selected star in the game state
                            game_state["view_mode"] = "solar_system"
                            game_state["selected_star"] = star
                            game_state["current_solar_system"] = galaxy.solar_systems.get(star["name"]) # Fetch solar system
                            camera.reset(0, 0, 1)  # Reset camera to default position and zoom 
                            camera.center_camera_on_star()  # Center camera on the selected star


                if event.button == 3:  # Right click
                    ("right_click", pygame.mouse.get_pos())
            if event.type == pygame.MOUSEWHEEL:
                new_zoom = camera.target_zoom + (event.y * 0.1)
                cursor_pos = pygame.mouse.get_pos()
                camera.zoom_to(new_zoom, cursor_pos)  # Zoom towards the mouse position

    # Handle real-time camer a movement
    def handle_camera_panning(self, camera):
        if self.key_states[pygame.K_w]:  # Pan up
            camera.move(0, -50)
        if self.key_states[pygame.K_s]:  # Pan down
            camera.move(0, 50)
        if self.key_states[pygame.K_a]:  # Pan left
            camera.move(-50, 0)
        if self.key_states[pygame.K_d]:  # Pan right
            camera.move(50, 0)
        if self.key_states[pygame.K_EQUALS]:
            camera.set_zoom(camera.target_zoom * 1.05)
        if self.key_states[pygame.K_MINUS]:
            camera.set_zoom(camera.target_zoom * 0.95)



    

    
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
import pygame
import pygame_gui
import sys
import src.camera

class StellarisInputManager:
    """Handles input events and provides key states for real-time controls."""

    def __init__(self, galaxy):
        # Tracks the state of keys (pressed or not)
        self.key_states = {
            pygame.K_w: False,  # Pan up
            pygame.K_s: False,  # Pan down
            pygame.K_a: False,  # Pan left
            pygame.K_d: False,  # Pan right
            pygame.K_PLUS: False,  # Zoom in
            pygame.K_MINUS: False  # Zoom out
        }
        self.galaxy = galaxy

    def process_input(self):
        """Process input events and update key states."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Exit the program when quitting

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_states:
                    self.key_states[event.key] = True

            # Handle key releases
            if event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                sys.stdout.write("click @ (" + str(mousePos[0]) + ", " + str(mousePos[1]) + ")\n")
                self.handle_clicks(mousePos, event, self.galaxy)

                if event.button == 1:  # Left click
                    ("left_click", pygame.mouse.get_pos())
                elif event.button == 3:  # Right click
                    ("right_click", pygame.mouse.get_pos())

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

    def handle_clicks(self, mousePos, event, galaxy):
        match event.button:
            case 1:
                #left click
                star = galaxy.get_star_from_pos(mousePos)

                sys.stdout.write(star)
            case 3:
                #right click
                pass


'''
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #   mouse_x, mouse_y = pygame.mouse.get_pos()
         #   selected_star = galaxy.get_star_at_position(mouse_x, mouse_y, camera)  # Function to find clicked star
         #   if selected_star is not None:
         #       selected_solar_system = galaxy.solar_systems[selected_star["name"]]  # Fetch solar system
         #       view_mode = "solar_system"
    #cheat sheet: pygame.event.get() translates to pygame, fetch all user inputs since the last time 
    #that this function was called (which is usually the previous clock tick)
    #pygame event types: 
        #Keyboard events: KEYDOWN, KEYUP
        #mouse events: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
            #in this context event.pos gives the x,y coordinates of mouse when action occurred
        #window events: QUIT, VIDEORESIZE (which just means window was resized)
        #custom user events can be created using pygame.USEREVENT'
'''
import pygame_gui
import pygame
import src.globalVars

class GUIManager:
    """separate class to manage all GUI in this game"""
    def __init__(self, screen_width, screen_height, manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.solar_system_label = None
        self.return_button = None
        self.tooltip = None
        self.manager = manager

    def initialize_solar_system_gui(self, solar_system_name):
        # Create the solar system label
        self.solar_system_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, self.screen_height - 50), (300, 50)),
            text=f"Solar System: {solar_system_name}",
            manager=self.manager
        )

        # Create the return button
        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 150, self.screen_height - 50), (140, 40)),
            text="Return to Galaxy",
            manager=self.manager
        )
        src.globalVars.view_switched = False

    def initialize_galaxy_gui(self):
        #create star info tooltip
        self.tooltip = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (200, 30)),
            text="",
            manager=self.manager
        )
        src.globalVars.view_switched = False

    def clear_gui(self):
        # Hide or reset GUI elements
        if self.solar_system_label:
            self.solar_system_label.kill() #kills solar system label
            self.solar_system_label = None
        if self.return_button:
            self.return_button.kill() #kills return to galaxy view button
            self.return_button = None
        if self.tooltip:
            self.tooltip.kill() #kills star info tooltip
            self.tooltip = None


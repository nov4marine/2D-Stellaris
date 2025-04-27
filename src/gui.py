import pygame_gui
import pygame

class GUIManager:
    """global GUI for a given nation"""
    def __init__(self, screen_width, screen_height, manager, nation):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.manager = manager
        self.nation = nation

        self.icons = {
            "government": pygame.image.load("2D-Stellaris/assets/icons/government.png").convert_alpha(),
            "society": pygame.image.load("2D-Stellaris/assets/icons/society.png").convert_alpha(),
            "tech": pygame.image.load("2D-Stellaris/assets/icons/tech.png").convert_alpha(),
            "population": pygame.image.load("2D-Stellaris/assets/icons/population.png").convert_alpha(),
            "planets": pygame.image.load("2D-Stellaris/assets/icons/planets.png").convert_alpha(),
            "budget": pygame.image.load("2D-Stellaris/assets/icons/budget.png").convert_alpha(),
            "expansion planner": pygame.image.load("2D-Stellaris/assets/icons/expansion.png").convert_alpha(),
            "fleet management": pygame.image.load("2D-Stellaris/assets/icons/fleet_management.png").convert_alpha(),
            "diplomacy": pygame.image.load("2D-Stellaris/assets/icons/diplomacy.png").convert_alpha(),
            "market": pygame.image.load("2D-Stellaris/assets/icons/market.png").convert_alpha(),
        }

        # Create the top bar and collapsed panel as modular elements
        self.top_bar = TopBar(0, 0, 1920, 50, manager, nation)
        self.collapsed_panel = CollapsiblePanel(0, 50, 50, 300, 300, manager)
        # Add the rest of the gloabal GUI elements for a given nation here 

    def clear_gui(self):
        # Hide / reset GUI elements that are exclusive to specific views
        pass

    def initialize_core_hud(self, nation):
        """This function initializes the core HUD elements that are always present in the game."""
        # Create the top bar and left collapsed panel as modular elements
        self.top_bar = TopBar(0, 0, 1920, 50, self.manager, nation)
        self.collapsed_panel = CollapsiblePanel(0, 50, 50, 300, 300, self.manager)


    def draw(self):
        """Draw the GUI elements on the screen."""
         # Draw the top bar
        self.collapsed_panel.handle_event(pygame.event.get())  # Handle hover events

class TopBar:
    def __init__(self, x, y, width, height, manager, nation):
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((x, y), (width, height)),
            starting_height=1,
            manager=manager
        )
        self.labels = {
            "bureaucracy": pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, 10), (200, 30)),
                text=f"Bureaucracy: {nation.bureaucracy}",
                manager=manager,
                container=self.panel
            ),

            "research": pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((60, 10), (400, 30)),
                text=f"Research: {nation.research}",
                manager=manager,
                container=self.panel
            ),

            "budget": pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((100, 10), (600, 30)),
                text=f"Budget: {nation.budget}",
                manager=manager,
                container=self.panel
            ),

            "gdp": pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((140, 10), (800, 30)),
                text=f"GDP: {nation.gdp}",
                manager=manager,
                container=self.panel
            ),

            "population": pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((180, 10), (1000, 30)),
                text=f"Population: {nation.population}",
                manager=manager,
                container=self.panel
            ),

            "gdp per capita": pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((220, 10), (1200, 30)),
                text=f"GDP per Capita: {nation.gdp_percapita}",
                manager=manager,
                container=self.panel
            ),

            "budget bar": pygame_gui.elements.UIProgressBar(
                relative_rect=pygame.Rect((1690, 10), (200, 30)),
                manager=manager,
                container=self.panel
            )

            # Add other labels here (research, budget, GDP)
        }

    def update(self, nation):
        self.labels["bureaucracy"].set_text(f"Bureaucracy: {nation.bureaucracy}")
        # Repeat for other labels

class Panel:
    def __init__(self, x, y, width, height, manager):
        # Pygame GUI element as an attribute
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((x, y), (width, height)),
            starting_height=1,
            manager=manager
        )
        self.children = []  # List of child elements within the panel

    def add_child(self, child):
        self.children.append(child)

    def draw_children(self):
        # You can loop through children to manage rendering or updates
        for child in self.children:
            if isinstance(child, Button):  # Example specific to buttons
                child.set_text("Updated!")

class Button:
    def __init__(self, x, y, width, height, text, manager, action=None):
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (width, height)),
            text=text,
            manager=manager
        )
        self.action = action  # Function to call on click

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.get_relative_rect().collidepoint(event.pos):
                if self.action:
                    self.action()

class CollapsiblePanel:
    def __init__(self, x, y, collapsed_width, expanded_width, height, manager):
        self.collapsed_rect = pygame.Rect((x, y), (collapsed_width, height))
        self.expanded_rect = pygame.Rect((x, y), (expanded_width, height))
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.collapsed_rect,
            starting_height=1,
            manager=manager
        )
        self.expanded = False

    def toggle(self, hover):
        if hover and not self.expanded:
            self.panel.set_dimensions(self.expanded_rect.size)
            self.expanded = True
        elif not hover and self.expanded:
            self.panel.set_dimensions(self.collapsed_rect.size)
            self.expanded = False

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.collapsed_rect.collidepoint(mouse_pos)
        self.toggle(hover)

class Icon:
    def __init__(self, filepath, x, y, width, height, manager, container=None):
        self.icon = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((x, y), (width, height)),
            image_surface=pygame.image.load(filepath).convert_alpha(),
            manager=manager,
            container=container
        )


class SolarSystemGUI:
    def __init__(self, manager, star, nation=None):
        """Initialize the Solar System GUI with a given solar system and nation."""
        self.manager = manager
        self.star = star  # the particular star system to be displayed
        self.nation = nation

        self.star_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((810, 1030), (300, 50)),
            text=f"Solar System: {self.star.star_name}",
            manager=self.manager
        )

        self.return_button = Button(
            x=10, y=10, width=140, height=40,
            text="Return to Galaxy",
            manager=self.manager,
            action=self.return_to_galaxy_view
        )

    def update(self, events):
        for event in events:
            # Handle solar system-specific events
            pass

    def draw(self):
        # Handle any custom drawing or updates for solar system GUI
        pass

class GalaxyGUI:
    def __init__(self, manager, nation=None):
        self.manager = manager

    def update(self, events):
        for event in events:
            # Handle galaxy-specific events
            pass

    def draw(self):
        # Handle any custom drawing or updates for galaxy GUI
        pass

# cheat sheet for quick tips/ reference: 
# partially transparent images: convert_alpha()
#opaque images: convert()

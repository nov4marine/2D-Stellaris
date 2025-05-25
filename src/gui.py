import pygame_gui
import pygame
from src.game_state import game_state

class GlobalGUIManager:
    """global GUI for a given nation that persists across all views"""
    def __init__(self, player, nation):
        self.manager = game_state["global_ui_manager"]
        self.nation = nation
        self.player = player

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

        # The GUI shall be split into a collection of organized components:
        # - Top Bar: Displays important information (e.g., budget, research, etc.)
        # - Left Collapsed Panel: Contains buttons for various actions (e.g., fleet management, diplomacy, etc.)
        # - Right Ledger, Stellaris-style: Displays information about star systems, planets, and fleets

        # Global HUD elements always visible
        self.top_bar = TopBar(0, 0, 1920, 50, self.manager, self.nation, self.icons)
        self.collapsed_panel = CollapsiblePanel(0, 50, 50, 240, 600, self.manager, self.nation, self.icons) 
        self.outliner_panel = OutlinerPanel(1680, 50, 240, 900, self.manager, self.nation)

        self.planetary_management_window = None
        self.solar_system_gui = None
        self.galaxy_gui = None

    def update_all_modules(self):
        """update all component modules of my GUI manager that handles all GUI for a given nation"""
        self.top_bar.update()
        self.outliner_panel.update()

    def handle_all_gui_events(self, event):
        """handle events for all component modules of my GUI manager that handles all GUI for a given nation"""
        self.top_bar.handle_event(event)
        self.collapsed_panel.handle_event(event)
        self.outliner_panel.process_event(event)
        # Handle other events as needed




class TopBar:
    def __init__(self, x, y, width, height, manager, nation, icons):
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(x, y, width, height),
            starting_height=1,
            manager=manager
        )
        self.manager = manager
        self.nation = nation
        self.icons = icons

        # Define the stats to display, in order
        self.stats = [
            {"name": "gold", "attr": "budget", "icon": icons["budget"], "tooltip": "Total treasury"},
            {"name": "gdp", "attr": "gdp", "icon": icons["budget"], "tooltip": "Gross Domestic Product"},
            {"name": "pops", "attr": "population", "icon": icons["population"], "tooltip": "Total population"},
            {"name": "research", "attr": "research", "icon": icons["tech"], "tooltip": "Research points"},
            {"name": "bureaucracy", "attr": "bureaucracy", "icon": icons["government"], "tooltip": "Bureaucratic capacity"},

            #gonna comment out the ones that are not implemented yet
            #{"name": "executive_authority", "attr": "executive_authority", "icon": icons["authority"], "tooltip": "Executive authority"},
            #{"name": "legitimacy", "attr": "legitimacy", "icon": icons["legitimacy"], "tooltip": "Legitimacy"},
            #diplo points/ influence? 

            # Add more as needed
        ]

        self.elements = []
        x_pos = 10
        icon_size = 32
        spacing = 20
        label_width = 120

        for stat in self.stats:
            # Icon
            icon_elem = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(x_pos, (height - icon_size)//2, icon_size, icon_size),
                image_surface=stat["icon"],
                manager=manager,
                container=self.panel
            )
            # Label
            value = getattr(nation, stat["attr"], "N/A") if nation else "N/A"
            button_elem = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(x_pos + icon_size + 5, (height - 30)//2, label_width, 30),
                text=str(value),
                manager=manager,
                container=self.panel
            )
            button_elem.set_tooltip(stat["tooltip"])

            self.elements.append((icon_elem, button_elem))
            x_pos += icon_size + label_width + spacing

    def update(self):
        # Update the label values each frame
        for (icon_elem, button_elem), stat in zip(self.elements, self.stats):
            value = getattr(self.nation, stat["attr"], "N/A") if self.nation else "N/A"
            button_elem.set_text(str(value))
    
    def handle_event(self, event):
        # Handle events for the top bar
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for icon_elem, button_elem in self.elements:
                if event.ui_element == button_elem:
                    # Handle button click (e.g., open a detailed view)
                    print(f"Clicked on {button_elem.get_text()}")

        # Handle other events as needed

class CollapsiblePanel:
    def __init__(self, x, y, collapsed_width, expanded_width, height, manager, nation, icons):
        self.collapsed_rect = pygame.Rect(x, y, collapsed_width, height)
        self.expanded_rect = pygame.Rect(x, y, expanded_width, height)
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.collapsed_rect,
            starting_height=1,
            manager=manager
        )
        self.expanded = False
        self.manager = manager
        self.nation = nation
        self.icons = icons

        self.buttons = [
            {"name": "Situation Log", "icon": "situation_log", "tooltip": "View situation log"},
            {"name": "Government", "icon": "government", "tooltip": "View government"},
            {"name": "Budget", "icon": "budget", "tooltip": "View budget"},
            {"name": "Population", "icon": "population", "tooltip": "View population"},
            {"name": "Buildings", "icon": "buildings", "tooltip": "View buildings"},
            {"name": "Society", "icon": "society", "tooltip": "View society"},
            {"name": "Technology", "icon": "tech", "tooltip": "View technology"},
            {"name": "Leaders", "icon": "leaders", "tooltip": "View leaders"},
            {"name": "Species", "icon": "species", "tooltip": "View species"},
            {"name": "Planets and Sectors", "icon": "planets", "tooltip": "View planets and sectors"},
            {"name": "Expansion Planner", "icon": "expansion", "tooltip": "View expansion planner"},
            {"name": "Fleet Management", "icon": "fleet_management", "tooltip": "Manage fleets"},
            {"name": "Diplomacy", "icon": "diplomacy", "tooltip": "View diplomacy"},
            {"name": "Market", "icon": "market", "tooltip": "View market"},
            {"name": "Claims", "icon": "claims", "tooltip": "View claims"},
            {"name": "Discoveries", "icon": "discoveries", "tooltip": "View discoveries"},
        ]

        self.elements = []
        x_pos = 10
        y_pos = 10
        icon_size = 32
        spacing = 10
        label_width = expanded_width - (icon_size + 30)

        for button in self.buttons:
            # Use placeholder if icon is missing
            icon_surface = self.icons.get(button["icon"], self.icons["government"])
            icon_elem = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(x_pos, y_pos, icon_size, icon_size),
                image_surface=icon_surface,
                manager=manager,
                container=self.panel
            )
            button_elem = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(x_pos + icon_size + 8, y_pos, label_width, icon_size),
                text=button["name"],
                manager=manager,
                container=self.panel
            )
            button_elem.set_tooltip(button["tooltip"])
            self.elements.append((icon_elem, button_elem))
            y_pos += icon_size + spacing

    def toggle(self, hover):
        if hover and not self.expanded:
            self.panel.set_dimensions(self.expanded_rect.size)
            for icon_elem, button_elem in self.elements:
                button_elem.show()
            self.expanded = True
        elif not hover and self.expanded:
            self.panel.set_dimensions(self.collapsed_rect.size)
            for icon_elem, button_elem in self.elements:
                button_elem.hide()
            self.expanded = False

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        hover = True if self.collapsed_rect.collidepoint(mouse_pos) or self.expanded_rect.collidepoint(mouse_pos) else False
        self.toggle(hover)

class SolarSystemGUI:
    def __init__(self, nation=None):
        self.manager = game_state["global_ui_manager"]
        self.solar_system = None
        self.nation = nation

        # Static GUI elements
        self.star_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((810, 1030), (300, 50)),
            text="",
            manager=self.manager
        )

    def set_solar_system(self, solar_system):
        self.solar_system = solar_system
        self.star_label.set_text(f"Solar System: {solar_system.name}")

    def update(self, events):
        for event in events:
            # Handle solar system-specific events
            pass

    def draw(self):
        # Use self.solar_system as needed
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

#fun and extremely useful tool for pygame GUI button grids
class ButtonGrid:

    def __init__(self, gui_manager, container, rows, cols, button_size, spacing, start_pos, button_texts=None, button_images=None):
        """
        Create a grid of buttons.

        Args:
            gui_manager: The pygame_gui.UIManager instance.
            container: The container for the buttons (e.g., a UIPanel).
            rows: Number of rows in the grid.
            cols: Number of columns in the grid.
            button_size: Tuple (width, height) for each button.
            spacing: Tuple (horizontal_spacing, vertical_spacing) between buttons.
            start_pos: Tuple (x, y) for the top-left position of the grid.
            button_texts: List of texts for the buttons (optional).
            button_images: List of images for the buttons (optional).

        Returns:
            A list of dictionaries containing button objects and their metadata.
        """
        self.gui_manager = gui_manager
        self.container = container
        self.rows = rows
        self.cols = cols
        self.button_size = button_size
        self.spacing = spacing
        self.start_pos = start_pos
        self.button_texts = button_texts
        self.button_images = button_images

        self.buttons = []
        self.button_width, button_height = button_size
        self.horizontal_spacing, vertical_spacing = spacing
        self.start_x, self.start_y = start_pos

        for row in range(rows):
            for col in range(cols):
                # Calculate button position
                x = self.start_x + col * (self.button_width + self.horizontal_spacing)
                y = self.start_y + row * (button_height + vertical_spacing)

                # Determine button text or image
                text = button_texts[row * cols + col] if button_texts else ""
                image = button_images[row * cols + col] if button_images else None

                # Create the button
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(x, y, self.button_width, button_height),
                    text=text,
                    manager=gui_manager,
                    container=container
                )

                # Set the button image if provided
                if image:
                    button.set_image(pygame.image.load(image).convert_alpha())

                # Store the button and its metadata
                self.buttons.append({
                    "button": button,
                    "row": row,
                    "col": col,
                    "text": text,
                    "image": image,
                    "selected": False
                })

        return self.buttons

class OutlinerPanel:
    def __init__(self, x, y, width, height, manager, nation):
        self.manager = manager
        self.nation = nation

        # Main scrollable container
        self.scroll_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(x, y, width, height),
            manager=manager
        )

        # Background panel for headers/buttons
        self.background_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, width, height),
            starting_height=0,
            manager=manager,
            container=self.scroll_container
        )

        self.sections = {
            "Planets": [],
            "Military Fleets": [],
            "Civilian Fleets": [],
            "Starbases": [],
            "Projects": [],
        }
        self.section_states = {key: True for key in self.sections}  # True = expanded

        self.section_headers = {}
        self.section_buttons = {}

        section_y = 10
        section_spacing = 10
        header_height = 28
        item_height = 28
        item_spacing = 2
        panel_width = width - 20

        for section in self.sections:
            # Section header button (collapsible)
            header_btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(10, section_y, panel_width, header_height),
                text=f"▼ {section}",
                manager=manager,
                container=self.background_panel
            )
            self.section_headers[section] = header_btn
            self.section_buttons[section] = []
            section_y += header_height + 2

            # Add item buttons (initially visible)
            items = getattr(nation, section.lower().replace(" ", "_"), [])
            for item in items:
                btn = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(20, section_y, panel_width - 10, item_height),
                    text=getattr(item, "name", str(item)),
                    manager=manager,
                    container=self.background_panel
                )
                self.section_buttons[section].append(btn)
                section_y += item_height + item_spacing

            section_y += section_spacing

        self._reflow()

    def _reflow(self):
        """Update positions and visibility of all elements based on collapsed state."""
        section_y = 10
        header_height = 28
        item_height = 28
        item_spacing = 2
        panel_width = self.background_panel.get_relative_rect().width - 20

        for section, header_btn in self.section_headers.items():
            # Move header
            header_btn.set_relative_position((10, section_y))
            # Update arrow
            expanded = self.section_states[section]
            header_btn.set_text(("▼ " if expanded else "► ") + section)
            section_y += header_height + 2

            # Move/hide item buttons
            for btn in self.section_buttons[section]:
                if expanded:
                    btn.show()
                    btn.set_relative_position((20, section_y))
                    section_y += item_height + item_spacing
                else:
                    btn.hide()
            section_y += 10  # section spacing

    def process_event(self, event):
        # Handle section header clicks for collapsing/expanding
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for section, header_btn in self.section_headers.items():
                if event.ui_element == header_btn:
                    self.section_states[section] = not self.section_states[section]
                    self._reflow()
                    return True
                # ...handle item button clicks...
        return False

    def update(self):
        # Remove old buttons from the UI
        for section in self.section_buttons:
            for btn in self.section_buttons[section]:
                btn.kill()
        self.section_buttons = {key: [] for key in self.sections}

        section_y = 10
        header_height = 28
        item_height = 28
        item_spacing = 2
        section_spacing = 10
        panel_width = self.background_panel.get_relative_rect().width - 20

        for section in self.sections:
            section_y += header_height + 2
            items = getattr(self.nation, section.lower().replace(" ", "_"), [])
            for item in items:
                btn = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(20, section_y, panel_width - 10, item_height),
                    text=getattr(item, "name", str(item)),
                    manager=self.manager,
                    container=self.background_panel
                )
                self.section_buttons[section].append(btn)
                section_y += item_height + item_spacing
            section_y += section_spacing

        self._reflow()


class PlanetaryManagementWindow:
    """Big window for managing a colony"""
    def __init__(self, manager, colony):
        self.manager = manager
        self.colony = colony
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((400, 100), (900, 800)),
            manager=manager,
            window_display_title=f"Planetary Management: {colony.name}",
            object_id="#planetary_management_window"
        )

        # Tabs (Overview, Pops, Buildings, Construction)
        self.tabs = pygame_gui.elements.UITabBar(
            relative_rect=pygame.Rect((0, 0), (900, 40)),
            manager=manager,
            container=self.window
        )
        self.tab_panels = {}
        for tab_name in ["Overview", "Pops", "Buildings", "Construction"]:
            panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((0, 40), (900, 760)),
                starting_height=1,
                manager=manager,
                container=self.window,
                visible=(tab_name == "Overview")
            )
            self.tab_panels[tab_name] = panel

        # --- Overview Tab ---
        overview_panel = self.tab_panels["Overview"]
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 20), (400, 30)),
            text=f"Planet: {colony.name} ({colony.type})",
            manager=manager,
            container=overview_panel
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 60), (400, 30)),
            text=f"Habitability: {colony.habitability}%",
            manager=manager,
            container=overview_panel
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 100), (400, 30)),
            text=f"Owner: {colony.owner}",
            manager=manager,
            container=overview_panel
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 140), (400, 30)),
            text=f"GDP: {colony.gdp}",
            manager=manager,
            container=overview_panel
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 180), (400, 30)),
            text=f"Unrest: {colony.unrest}",
            manager=manager,
            container=overview_panel
        )
        # Add more stats as needed

        # --- Pops Tab ---
        pops_panel = self.tab_panels["Pops"]
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (200, 30)),
            text="Population (Pops):",
            manager=manager,
            container=pops_panel
        )
        y = 50
        for pop in colony.colony_pops:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, y), (800, 28)),
                text=f"{pop.pop_type} | Size: {pop.size} | Profession: {getattr(pop.profession, 'profession', 'Unemployed')} | Income: {pop.income} | Happiness: {pop.happiness}",
                manager=manager,
                container=pops_panel
            )
            y += 32

        # --- Buildings Tab ---
        buildings_panel = self.tab_panels["Buildings"]
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (200, 30)),
            text="Buildings:",
            manager=manager,
            container=buildings_panel
        )
        y = 50
        for building in colony.colony_buildings:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, y), (800, 28)),
                text=f"{building.name} (Lvl {building.levels}) | Jobs: {', '.join([job.profession for job in building.jobs])} | Input: {building.input_goods} | Output: {building.output_goods}",
                manager=manager,
                container=buildings_panel
            )
            y += 32

        # --- Construction Tab ---
        construction_panel = self.tab_panels["Construction"]
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 10), (200, 30)),
            text="Construction Queue:",
            manager=manager,
            container=construction_panel
        )
        y = 50
        for item in colony.construction_queue:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, y), (800, 28)),
                text=f"{item['building'].name} | Remaining Cost: {item['remaining_cost']} | Time: {item['remaining_time']}",
                manager=manager,
                container=construction_panel
            )
            y += 32

        # --- Tab Switching Logic ---
        self.tabs.select_tab("Overview")
        self.tabs.set_tabs(["Overview", "Pops", "Buildings", "Construction"])
        self.tabs.set_active_tab("Overview")
        self.tabs.set_tab_visibility("Overview", True)
        self.tabs.set_tab_visibility("Pops", True)
        self.tabs.set_tab_visibility("Buildings", True)
        self.tabs.set_tab_visibility("Construction", True)

        # You may need to implement tab switching logic using handle_event

    def handle_event(self, event):
        # Implement tab switching and close logic here
        pass

    def update(self):
        # Refresh data if colony changes
        pass
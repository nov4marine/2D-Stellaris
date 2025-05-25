import pygame
import pygame_gui

pygame.init()
pygame.display.set_caption("Planetary Management Window Demo")
window_surface = pygame.display.set_mode((1280, 900))
manager = pygame_gui.UIManager((1280, 900))

# --- Dummy Data Classes ---
class DummyPop:
    def __init__(self, pop_type, size, profession, income, happiness):
        self.pop_type = pop_type
        self.size = size
        self.profession = profession
        self.income = income
        self.happiness = happiness

class DummyBuilding:
    def __init__(self, name, levels, jobs, input_goods, output_goods):
        self.name = name
        self.levels = levels
        self.jobs = jobs
        self.input_goods = input_goods
        self.output_goods = output_goods

class DummyColony:
    def __init__(self):
        self.name = "New London"
        self.type = "Continental"
        self.habitability = 85
        self.owner = "United Earth"
        self.sector = "Sector 1"
        self.governor = "John Doe"
        self.gdp = 12345
        self.unrest = 2.5
        self.colony_designation = "Mining World"
        self.colony_pops = [
            DummyPop("Human", 1000, "Farmer", 2.5, 80),
            DummyPop("Robot", 200, "Laborer", 1.2, 100)
        ]
        self.colony_buildings = [
            DummyBuilding("Farm", 2, [DummyPop("Human", 100, "Farmer", 2.5, 80)], "Grain", "Food"),
            DummyBuilding("Factory", 1, [DummyPop("Robot", 50, "Laborer", 1.2, 100)], "Ore", "Goods")
        ]
        self.construction_queue = [
            {"building": DummyBuilding("Power Plant", 1, [], "Minerals", "Energy"), "remaining_cost": 500, "remaining_time": "90 days"}
        ]

colony = DummyColony()

# --- Planetary Management Window with Tab Buttons ---
class PlanetaryManagementWindow:
    def __init__(self, manager, colony):
        self.manager = manager
        self.colony = colony
        self.window_width = 800
        self.window_height = 800
        self.tab_height = 30
        self.tab_margin = 30

        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((100, 50), (self.window_width, self.window_height)),
            manager=manager,
            window_display_title=f"Planetary Management: {colony.name}",
            object_id="#planetary_management_window"
        )

        # Tab buttons at the bottom
        tab_names = ["Overview", "Economy", "Population", "Buildings", "Armies", "Holdings"]
        self.tabs = {}
        self.active_tab = "Overview"
        for i, tab_name in enumerate(tab_names):
            btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    10 + i * 120,
                    self.window_height - self.tab_height - self.tab_margin,
                    110,
                    self.tab_height 
                ),
                text=tab_name,
                manager=manager,
                container=self.window
            )
            self.tabs[tab_name] = btn

        # Panels for each tab (leave space at bottom for tabs)
        self.tab_panels = {}
        for tab_name in tab_names:
            panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(
                    0, 0,
                    self.window_width,
                    self.window_height - self.tab_height - self.tab_margin 
                ),
                starting_height=1,
                manager=manager,
                container=self.window,
                visible=(tab_name == self.active_tab)
            )
            self.tab_panels[tab_name] = panel

        # grid config for each tab

        #grid config for Overview tab
        overview_grid = [ #columspan is width, rowspan is height
            {"panel_id": "vista", "row": 0, "col": 0, "rowspan": 1, "colspan": 2},
            {"panel_id": "districts", "row": 1, "col": 0, "rowspan": 1, "colspan": 2},
            {"panel_id": "buildings", "row": 2, "col": 0, "rowspan": 1, "colspan": 2},
            {"panel_id": "sidebar", "row": 1, "col": 2, "rowspan": 2, "colspan": 1},
            {"panel_id": "planet stats", "row": 0, "col": 2, "rowspan": 1, "colspan": 1},
        ]
        self.overview_panels = self.create_grid_panels(self.tab_panels["Overview"], overview_grid)

        #sub menu panels
        self._building_buttons()
        self._district_buttons()
        self._vista_buttons()
        self._stats()
        self._construction_queue()
        self._construction_menu()

    def _vista_buttons(self):
        # Add a label to the "vista" panel
        self.flag = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            image_surface=pygame.Surface((100, 50)),  # Placeholder for flag image
            manager=self.manager,
            container=self.overview_panels["vista"]
        )

        # Colony designation information
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(100, 0, 200, 50),
            text=f"({self.colony.colony_designation})",
            manager=self.manager,
            container=self.overview_panels["vista"],
        )

        # Colony type information
        climate_rect = pygame.Rect(0, 0, 200, 50)
        climate_rect.topright = (0, 0)
        pygame_gui.elements.UILabel(
            relative_rect=climate_rect,
            text=f"{self.colony.type}",
            manager=self.manager,
            container=self.overview_panels["vista"],
            anchors={"right": "right", "top": "top"}
        )

        # Governor information
        governor_rect = pygame.Rect(0, 0, 150, 100)
        governor_rect.bottomleft = (5, -5)
        pygame_gui.elements.UIButton(
            relative_rect=governor_rect,
            text=f"{self.colony.governor}",
            manager=self.manager,
            container=self.overview_panels["vista"],
            anchors={"bottom": "bottom", "left": "left"}
        ) #expand later when leaders are implemented

        #Colony modifiers
        modifer_rect = pygame.Rect(0, 0, 50, 50)
        modifer_rect.bottomright = (-5, -5)
        pygame_gui.elements.UIImage(
            relative_rect=modifer_rect,
            image_surface=pygame.Surface((150, 100)),  # Placeholder for modifier image
            manager=self.manager,
            container=self.overview_panels["vista"],
            anchors={"bottom": "bottom", "right": "right"}
        ) #expand later when modifiers are implemented

    def _district_buttons(self):
        # Add a label to the district panel
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (-1, 20)),
            text="Resource Districts",
            manager=self.manager,
            container=self.overview_panels["districts"]
        )

        construct_rect = pygame.Rect(0, 0, 200, 30)
        construct_rect.topright = (-5, 5)
        pygame_gui.elements.UIButton(
            relative_rect=construct_rect,
            text="Construct",
            manager=self.manager,
            container=self.overview_panels["districts"],
            anchors={"top": "top", "right": "right"}
        )

        # Dynamically create a grid of building buttons
        button_width = 80
        button_height = 80
        button_margin_x = 10
        button_margin_y = 10
        buttons_per_row = 6  # You can adjust this for your UI

        for idx, building in enumerate(self.colony.colony_buildings): #change to resource districts
            row = idx // buttons_per_row
            col = idx % buttons_per_row
            x = 10 + col * (button_width + button_margin_x)
            y = 40 + row * (button_height + button_margin_y)
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(x, y, button_width, button_height),
                text=building.name,
                manager=self.manager,
                container=self.overview_panels["districts"]
            )

    def _building_buttons(self):
        # Add a label to the "buildings" panel
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (-1, 20)),
            text="Buildings",
            manager=self.manager,
            container=self.overview_panels["buildings"]
        )

        construct_rect = pygame.Rect(0, 0, 200, 30)
        construct_rect.topright = (-5, 5)
        pygame_gui.elements.UIButton(
            relative_rect=construct_rect,
            text="Construct",
            manager=self.manager,
            container=self.overview_panels["buildings"],
            anchors={"top": "top", "right": "right"}
        )

        # Dynamically create a grid of building buttons
        button_width = 80
        button_height = 80
        button_margin_x = 10
        button_margin_y = 10
        buttons_per_row = 6  # You can adjust this for your UI

        for idx, building in enumerate(self.colony.colony_buildings):
            row = idx // buttons_per_row
            col = idx % buttons_per_row
            x = 10 + col * (button_width + button_margin_x)
            y = 40 + row * (button_height + button_margin_y)
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(x, y, button_width, button_height),
                text=building.name,
                manager=self.manager,
                container=self.overview_panels["buildings"]
            )

    def _construction_queue(self):
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 5, -1, 20),
            text=f"{self.colony.name}: {self.colony.sector}",
            manager=self.manager,
            container=self.overview_panels["sidebar"]
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 80, -1, 20),
            text=f"Construction Queue",
            manager=self.manager,
            container=self.overview_panels["sidebar"]
        )

        y = 110
        panel_height = 50
        panel_width = 220
        for idx, item in enumerate(self.colony.construction_queue):
            # Panel for each queue item
            item_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(10, y, panel_width, panel_height),
                starting_height=1,
                manager=self.manager,
                container=self.overview_panels["sidebar"]
            )
            # Building name
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(5, 5, -1, 15),
                text=item['building'].name,
                manager=self.manager,
                container=item_panel
            )
            # Countdown timer
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(panel_width - 100, 5, -1, 15),
                text=f"{item['remaining_time']}",
                manager=self.manager,
                container=item_panel
            )
            # Progress bar 
            progress_bar = pygame_gui.elements.UIProgressBar(
                relative_rect=pygame.Rect(5, 25, panel_width - 15, 20),
                manager=self.manager,
                container=item_panel,

            )
            progress_bar.set_current_progress((1 - item['remaining_cost'] / item['building'].levels))
            


            # Remove button
            remove_btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(panel_width - 35, 0, 25, 25),
                text="X",
                manager=self.manager,
                container=item_panel,
                object_id=f"#remove_queue_{idx}"
            )
            y += panel_height + 10


        # --- Construction Menu as a side window ---
    def _construction_menu(self):
        self.construction_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(
                self.window_width,  # right of main window
                50,
                300,
                600
            ),
            manager=self.manager,
            window_display_title="Construct Building",
            object_id="#construction_queue_window"
        )

        # Example: list of available buildings (replace with your real data)
        available_buildings = [
            DummyBuilding("Farm", 2, [], "Minerals", "Food"),
            DummyBuilding("Factory", 1, [], "Ore", "Goods"),
            DummyBuilding("Power Plant", 1, [], "Minerals", "Energy"),
        ]

        scroll_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(0, 0, 300, 600),  # match your window size
            manager=self.manager,
            container=self.construction_window
        )

        panel_y = 10
        panel_height = 80
        panel_width = 260
        icon_size = 48

        self.build_buttons = []  # Store for event handling

        for idx, building in enumerate(available_buildings):
            # Panel for each building
            build_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(10, panel_y, panel_width, panel_height),
                starting_height=1,
                manager=self.manager,
                container=scroll_container
            )

            # Icon (placeholder, replace with real image)
            pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(5, 16, icon_size, icon_size),
                image_surface=pygame.Surface((icon_size, icon_size)),
                manager=self.manager,
                container=build_panel
            )

            # Name
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(60, 5, 140, 24),
                text=building.name,
                manager=self.manager,
                container=build_panel
            )

            # Cost
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(60, 30, 90, 20),
                text=f"Cost: {building.input_goods}",
                manager=self.manager,
                container=build_panel
            )

            # Upkeep
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(150, 30, 90, 20),
                text=f"Upkeep: ...",  # Replace with real upkeep
                manager=self.manager,
                container=build_panel
            )

            # Build time
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(60, 50, 90, 20),
                text=f"Time: ...",  # Replace with real build time
                manager=self.manager,
                container=build_panel
            )

            # Add to queue button (or make the whole panel clickable)
            add_btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(panel_width - 50, 20, 40, 40),
                text="+",
                manager=self.manager,
                container=build_panel,
                object_id=f"#add_building_{idx}"
            )
            self.build_buttons.append(add_btn)

            panel_y += panel_height + 10

    def _stats(self): #modify later to show real stats
        # Example stats to display (label, value)
        stats = [
            ("GDP", self.colony.gdp),
            ("Unrest", self.colony.unrest),
            ("Habitability", f"{self.colony.habitability}%"),
            ("Pops", len(self.colony.colony_pops)),
            ("Buildings", len(self.colony.colony_buildings)),
            ("Owner", self.colony.owner),
            # Add more stats as needed, up to 18 for a 3x6 grid
        ]

        cols = 1
        rows = 6
        label_width = 90
        value_width = 100
        cell_width = label_width + value_width + 10
        cell_height = 20
        margin_x = 5
        margin_y = 5

        for idx, (label, value) in enumerate(stats):
            col = idx % cols
            row = idx // cols
            x = margin_x + col * (cell_width + margin_x)
            y = margin_y + row * (cell_height + margin_y)
            # Label (text or icon)
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(x, y, label_width, cell_height),
                text=str(label),
                manager=self.manager,
                container=self.overview_panels["planet stats"]
            )
            # Value
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(x + label_width + 5, y, value_width, cell_height),
                text=str(value),
                manager=self.manager,
                container=self.overview_panels["planet stats"]
            )

    def handle_event(self, event):
        # Tab switching logic
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for tab_name, btn in self.tabs.items():
                if event.ui_element == btn:
                    self.set_active_tab(tab_name)

    def set_active_tab(self, tab_name):
        for name, panel in self.tab_panels.items():
            panel.hide()
        self.tab_panels[tab_name].show()
        self.active_tab = tab_name

    # Add this method to your PlanetaryManagementWindow class
    def update_construction_window_position(self):
        # Get the current position of the main window
        main_rect = self.window.get_relative_rect()
        # Calculate the new position for the construction window
        new_x = main_rect.x + main_rect.width - 25
        new_y = main_rect.y
        # Move the construction window
        self.construction_window.set_position((new_x, new_y))

    def create_grid_panels(self, parent_panel, grid_config, grid_rows=3, grid_cols=3, margin=10):
        """
        Creates a grid of UIPanels on the given parent_panel according to grid_config.
        grid_config: list of dicts with keys:
            - panel_id: str #panel name
            - row: int
            - col: int
            - rowspan: int # height of the panel
            - colspan: int # width of the panel
        Returns a dict mapping panel_id to UIPanel.
        """
        panel_width = (self.window_width - (grid_cols + 1) * margin) // grid_cols
        panel_height = (self.window_height - self.tab_height - self.tab_margin - (grid_rows + 1) * margin) // grid_rows
        panels = {}
        for cfg in grid_config:
            x = margin + cfg["col"] * (panel_width + margin)
            y = margin + cfg["row"] * (panel_height + margin)
            width = panel_width * cfg.get("colspan", 1) + margin * (cfg.get("colspan", 1) - 1)
            height = panel_height * cfg.get("rowspan", 1) + margin * (cfg.get("rowspan", 1) - 1)
            panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(x, y, width, height),
                starting_height=1,
                manager=self.manager,
                container=parent_panel
            )
            panels[cfg["panel_id"]] = panel
        return panels

# --- Main loop for demo ---
clock = pygame.time.Clock()
planet_window = PlanetaryManagementWindow(manager, colony)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)
        planet_window.handle_event(event)
        planet_window.update_construction_window_position()

    manager.update(time_delta)
    window_surface.fill((30, 30, 40))
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
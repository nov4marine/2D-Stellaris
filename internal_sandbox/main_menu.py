import pygame
import sys 
import pygame_gui
from src.nation_storage import NationStorage
from src.nation import Nation
from src.game_state import game_state

class BaseMenuUI:
    def __init__(self, screen, game_state, gui_manager):
        self.screen = screen
        self.game_state = game_state
        self.gui_manager = gui_manager

    def draw_background(self):
        raise NotImplementedError

    def handle_events(self, event):
        raise NotImplementedError

    def get_conditions(self):
        raise NotImplementedError

    # Add any other methods/properties you want all menu UIs to have

def main_menu(screen, game_state, input_manager, gui_manager):
    """Main menu function to display the main menu and handle user input."""

    gui_manager.clear_and_reset()  # Clear the GUI manager for the main menu

    # Load a background image (make sure you have the file in your directory)
    background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/menu_background.jpg")
    screen.blit(background, (0, 0))  # Draw the background image

    # Draw a semi-transparent overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
    screen.blit(overlay, (0, 0))
    
    # Title text
    menu_font = pygame.font.Font(None, 50)  # Use a cool font if available
    title = menu_font.render("Stellaris 2D", True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

    # Animated buttons (hover effects)
    mouse_pos = pygame.mouse.get_pos()
    button_font = pygame.font.Font(None, 36)

    # Start Button
    start_rect = pygame.Rect(300, 250, 200, 50)
    start_color = (255, 255, 255) if start_rect.collidepoint(mouse_pos) else (200, 200, 200)
    pygame.draw.rect(screen, start_color, start_rect, border_radius=10)
    start_text = button_font.render("Start New Game", True, (0, 0, 0))
    screen.blit(start_text, (start_rect.x + 50, start_rect.y + 10))

    # Exit Button
    exit_rect = pygame.Rect(300, 350, 200, 50)
    exit_color = (255, 255, 255) if exit_rect.collidepoint(mouse_pos) else (200, 200, 200)
    pygame.draw.rect(screen, exit_color, exit_rect, border_radius=10)
    exit_text = button_font.render("Exit", True, (0, 0, 0))
    screen.blit(exit_text, (exit_rect.x + 75, exit_rect.y + 10))



    # Handle input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state["current_state"] = "EXIT"
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(mouse_pos):
                game_state["current_state"] = "new_game"
            elif exit_rect.collidepoint(mouse_pos):
                game_state["current_state"] = "EXIT"
                sys.exit()




class NewGameUI: 
    def __init__(self, screen, game_state, gui_manager):
        self.screen = screen
        self.game_state = game_state
        self.gui_manager = gui_manager

        # Nation selection panel
        self.nation_selection_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 250, 1080),
            manager=gui_manager
        )

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 0, 220, 40),
            text="Select Your Nation",
            manager=gui_manager,
            container=self.nation_selection_panel
        )

        self.nation_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(10, 50, 220, 900),
            item_list=self.load_nation_names(),
            container=self.nation_selection_panel,
            manager=gui_manager
        )

        self.delete_nation_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(120, 960, 100, 40),
            text="Delete",
            manager=gui_manager,
            container=self.nation_selection_panel
        )

        self.nation_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(450, 240, 1200, 600),
            starting_height=2,
            manager=gui_manager
        )

        self.nation_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 220, 40),
            text="Empire Name",
            manager=gui_manager,
            container=self.nation_panel,
            anchors={'centerx': 'centerx'}
        )



        ###############################

        self.return_to_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 1010, 220, 50),
            text="Return to Main Menu",
            manager=gui_manager,
            starting_height=4
        )


        #####################################

        self.setup_phase_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(450, 160, 1200, 70),
            starting_height=2,
            manager=gui_manager
        )

        self.nation_summary = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 10, 220, 45),
            text="Nation Summary",
            manager=gui_manager,
            container=self.setup_phase_panel
        )

        self.edit_nation = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(240, 10, 220, 45),
            text="Edit Nation",
            manager=gui_manager,
            container=self.setup_phase_panel
        )

        self.galaxy_setup = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(470, 10, 220, 45),
            text="Setup Galaxy",
            manager=gui_manager,
            container=self.setup_phase_panel
        )

        ########################################

        self.nation_edit_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(450, 240, 1200, 600),
            manager=gui_manager,
            visible=False  # Initially hidden
        )

###############################################################
        # Level 1 of sub menu panels

        self.edit_nation_phase_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 250, 1080),
            starting_height=2,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        self.edit_nation_phases = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(10, 50, 220, 900),
            item_list=["Empire Name", "Species", "Homeworld", "Origin", "Government and Ethos", "Laws", "Ship Appearance", "Ruler"],
            container=self.edit_nation_phase_panel,
            manager=gui_manager
        )

################################################################
        # Level 2 of sub menu panels beneath the edit_nation_panel. 
        #all of this is used to create or edit the empire.

        # Empire Name, color, and flag Panel

        self.edit_empire_name_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            starting_height=2,
            manager=gui_manager,
            container=self.nation_edit_panel
        )

        self.save_nation_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(990, 540, 200, 50),
            starting_height=2,
            text="Save Nation",
            manager=gui_manager,
            container=self.nation_edit_panel
        )

        self.nation_name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(0, 0, 600, 50),
            manager=gui_manager,
            container=self.edit_empire_name_panel,
            anchors={'centerx': 'centerx'}
        )
        self.nation_name_entry.set_text("Enter Nation Name")

        #self.nation_flag_selector = pygame_gui.elements.
        #add nation flag selector here
        #self.nation_flag_selector = pygame_gui.elements.UIImageButton(

        # Species Panel
        # This panel is for selecting the species of the empire.
        self.edit_species_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        self.species_name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(0, 0, 600, 50),
            manager=gui_manager,
            container=self.edit_species_panel
        )
        self.species_name.set_text("Enter Species Name")

        self.species_traits = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(300, 70, 600, 400),
            item_list=[
                "Intelligent",
                "Strong",
                "Quick Learners",
                "Resilient",
                "Natural Engineers",
                "Natural Physicists",
                "Natural Sociologists",
                "Talented",
                "Industrious",
                "Thrifty",
                "Agrarian",
                "Adaptive",
                "Conformists",
                "Communal",
                "Decadent",
                "Fleeting",
                "Nonadaptive",
                "Slow Learners",
                "Weak",
                "Unruly",
                "Unfit",
                "Repugnant",
                "Deviants",
                ],
            allow_multi_select=True,
            container=self.edit_species_panel,
            manager=gui_manager
        )

        #self.species_appearance = pygame_gui.elements.UISelectionList(

        # Edit Homeworld Panel
        # This panel is for selecting the homeworld of the empire.
        self.edit_homeworld_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        self.homeworld_name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(20, 20, 550, 50),
            manager=gui_manager,
            container=self.edit_homeworld_panel,
        )
        self.homeworld_name_entry.set_text("Enter Homeworld Name")

        self.homeworld_star_name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(20, 80, 550, 50),
            manager=gui_manager,
            container=self.edit_homeworld_panel,
        )
        self.homeworld_star_name_entry.set_text("Enter Home Star Name")

        self.homeworld_climate = pygame_gui.elements.UIDropDownMenu(
            options_list=["Savanna", "Arid", "Desert", "Ocean", "Continental", "Tropical",  "Tundra", "Alpine", "Artic",],
            starting_option="Tropical",
            relative_rect=pygame.Rect(600, 20, 550, 200),
            manager=gui_manager,
            container=self.edit_homeworld_panel
        )
        self.homeworld_selected = ""

        # Edit Origin Panel
        # This panel is for selecting the origin of the empire.
        self.edit_origin_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        self.origin_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(50, 50, 750, 300),
            item_list=[
                "Prosperous Unification",
                "Mechanist",
                "Syncretic Evolution",
                "Post-Apocalyptic",
                "Life-Seeded",
                "Remnants",
                "Voidborne",
                "Lost Colony",
                "Ocean Paradise",
                "Shattered Ring",
                "Void Dwellers",
                "Scavenger World",
                "Machine World",
                "Hollow World",
                "Galactic Doorstep",
                ],
            manager=gui_manager,
            container=self.edit_origin_panel,
        )

        self.origin_description = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(800, 50, 350, 200),
            html_text="Select an origin to see its description.",
            manager=gui_manager,
            container=self.edit_origin_panel,
        )

        # Edit Government and Ethos Panel
        # This panel is for selecting the government and ethos of the empire.
        self.edit_government_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        # Ethos Spectrum selection
        self.ethos_buttons = []
        self.selected_ethos = {}

        # Define ethos pairs (opposites)
        ethics_spectrum = [
            {"pair": ["Materialist", "Spiritualist"], "images": ["Materialist.png", "Spiritualist.png"]},
            {"pair": ["Xenophile", "Xenophobe"], "images": ["Xenophile.png", "Xenophobe.png"]},
            {"pair": ["Militarist", "Pacifist"], "images": ["Militarist.png", "Pacifist.png"]},
            {"pair": ["Authoritarian", "Egalitarian"], "images": ["Authoritarian.png", "Egalitarian.png"]},
        ]

        # Dynamically create buttons for each ethos pair
        for i, ethos_pair in enumerate(ethics_spectrum):
            for j, ethos_name in enumerate(ethos_pair["pair"]):
                x = 75 + j * 150  # Horizontal spacing (left and right buttons in a row)
                y = 100 + i * 100  # Vertical spacing (each pair in a new row)

                # Create the ethos button
                ethos_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(x, y, 50, 50),
                    text=ethos_name,
                    manager=gui_manager,
                    container=self.edit_government_panel
                )


                # Store the button and its selection state
                self.ethos_buttons.append({
                    "button": ethos_button,
                    "name": ethos_name,
                    "pair": ethos_pair["pair"],
                    "selected": False,
                })


        self.government_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Democracy", "Monarchy", "Dictatorship", "theocracy", "Communism", "Anarchy"],
            starting_option="Democracy",
            relative_rect=pygame.Rect(383, 100, 333, 400),
            manager=gui_manager,
            container=self.edit_government_panel
        )

        self.civics_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(716, 100, 333, 400),
            item_list=[
                "Agrarian Idyll",
                "Beacon of Liberty",
                "Citizen Service",
                "Corporate Dominion",
                "Cutthroat Politics",
                "Distinguished Admiralty",
                "Divine Mandate",
                "Free Haven",
                "Imperial Cult",
                "Indoctrination",
                "Interstellar Dominion",
                "Merchant Guilds",
                "Nationalistic Zeal",
                "Philosopher King",
                "Police State",
                "Shadow Council",
                "Technocracy",
                ],
            allow_multi_select=True,
            container=self.edit_government_panel,
            manager=gui_manager
        )


        # Edit Laws Panel
        # This panel is for selecting the starting laws of the empire.
        self.edit_laws_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        #don't know yet if starting laws should be fixed to ethos and/or government or if they should be free to choose.
        #might be easier to just have a handful of default sets based on ethos and government.
        
        # Edit Ship Appearance Panel
        # This panel is for selecting the ship appearance of the empire.
        self.edit_ship_appearance_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        self.ship_appearance_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(50, 50, 333, 400),
            item_list=[
                "Corvette",
                "Destroyer",
                "Cruiser",
                "Battleship",
                "Titan",
                "Colossus",
                ],
            container=self.edit_ship_appearance_panel,
            manager=gui_manager
        )

        # Edit Ruler Panel
        # This panel is for selecting the ruler of the empire.
        self.edit_ruler_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1200, 600),
            container=self.nation_edit_panel,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        # This will be for customizing the starting ruler of the empire within reasonable limits.
        # Adding a system of leaders with traits and skills that can be leveled up over time.
        # This will be a more complex system that will be added later.

        ####################################################################

        # Galaxy Setup Panel
        # This panel is for selecting the galaxy setup options like in Stellaris.
        self.galaxy_setup_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(450, 240, 1200, 600),
            starting_height=2,
            manager=gui_manager,
            visible=False  # Initially hidden
        )

        self.galaxy_size_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(200, 50, 200, 50),
            text="Galaxy Size:",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )
        
        # Galaxy Size Dropdown. Small is 800 stars, Medium is 1000 stars, Large is 1200 stars.
        # number of star systems might become more customizable later.
        # For now, we will just have a few preset sizes to choose from.
        self.galaxy_size_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Small", "Medium", "Large"],
            starting_option="Medium",
            relative_rect=pygame.Rect(800, 50, 300, 50),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        # Galaxy Shape Dropdown. Spiral + number of arms, Elliptical, Irregular, Ring, and more to come.
        self.galaxy_shape_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["2 Arm Spiral", "4 Arm Spiral", "Elliptical", "Irregular", "Ring"],
            starting_option="4 Arm Spiral",
            relative_rect=pygame.Rect(800, 100, 300, 50),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.galaxy_shape_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(200, 100, 200, 50),
            text="Galaxy Shape:",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        # Galaxy Age Dropdown? Young, Old, Ancient, and more to come. Might add flavor to the game.

        #hyperlane density slider. 0x to 5x density. 0x is no hyperlanes, 1x is normal, 2x is double, and so on.
        # No idea how to implement this yet, but it will be a slider that goes from 0 to 5 lol.
        self.hyperlane_density_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(800, 150, 300, 50),
            start_value=1,
            value_range=(0.5, 5),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.hyperlane_density_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(200, 150, 200, 50),
            text=f"Hyperlane Density: {self.hyperlane_density_slider.get_current_value()}",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.number_of_nations_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(800, 200, 300, 50),
            start_value=1,
            value_range=(1, 40),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.number_of_nations_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(200, 200, 200, 50),
            text=f"Number of Nations: {self.number_of_nations_slider.get_current_value()}",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.advanced_ai_starts_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(800, 250, 300, 50),
            start_value=1,
            value_range=(0, 10),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.advanced_ai_starts_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(200, 250, 200, 50),
            text=f"Advanced AI Starts: {self.advanced_ai_starts_slider.get_current_value()}",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.fallen_empires_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(800, 300, 300, 50),
            start_value=2,
            value_range=(0, 5),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.fallen_empires_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(200, 300, 200, 50),
            text=f"Fallen Empires: {self.fallen_empires_slider.get_current_value()}",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        # Difficulty Dropdown. Easy, Normal, Hard. 
        # Time to learn how to implement difficulty settings and reinforcement learning.
        # OHHHH BOY THIS IS GONNA BE FUN.
        self.difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Easy", "Normal", "Hard"],
            starting_option="Normal",
            relative_rect=pygame.Rect(800, 350, 300, 50),
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )

        self.start_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(990, 540, 200, 50),
            text="Start Game",
            manager=gui_manager,
            container=self.galaxy_setup_panel
        )


    def draw_background(self):
        # Load a background image (make sure you have the file in your directory)
        self.background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/menu_background.jpg")
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))  # Scale to fit the screen
        self.screen.blit(self.background, (0, 0))  # Draw the background image

        # Draw a semi-transparent overlay
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        self.screen.blit(self.overlay, (0, 0))

    ###########################################

    def get_conditions(self):
        """Get the conditions for the game setup."""
        return {
            "galaxy_parameters": {
                "size": self.galaxy_size_dropdown.selected_option,
                "shape": self.galaxy_shape_dropdown.selected_option,
                "hyperlane_density": self.hyperlane_density_slider.get_current_value(),
                "number_of_nations": int(self.number_of_nations_slider.get_current_value()),
                "advanced_ai_starts": int(self.advanced_ai_starts_slider.get_current_value()),
                "fallen_empires": int(self.fallen_empires_slider.get_current_value()),
                "difficulty": self.difficulty_dropdown.selected_option
            },
            "nation_parameters": {
                "name": self.nation_name_entry.get_text(),
                "species": self.species_name.get_text(),
                "population": 100000000, # initial value without modifiers is 100 million
                "homeworld": {
                    "planet": self.homeworld_name_entry.get_text(),
                    "star": self.homeworld_star_name_entry.get_text(),
                    "climate": self.homeworld_climate.selected_option
                },
                "ethos": [b["name"] for b in self.ethos_buttons if b["selected"]],
                "origin": self.origin_list.get_single_selection(),
                "civics": self.civics_list.get_multi_selection(),
                "government": self.government_dropdown.selected_option,
            }
        }

###########################################

    def load_nation_names(self):
        """Load nation names from storage."""
        nations = NationStorage.load_nations()
        return [nation["name"] for nation in nations]
    
    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_nation_button:
                self.save_nation()
            elif event.ui_element == self.delete_nation_button:
                self.delete_selected_nation()

    def save_nation(self):
        """Save the currently edited nation."""
        nation = Nation(
            name=self.nation_name_entry.get_text(),
            population=10000000,
            species = [self.species_name.get_text()],
            #species_traits=self.species_traits.get_single_selection(),
            homeworld = {
                "planet": self.homeworld_name_entry.get_text(),
                "star": self.homeworld_star_name_entry.get_text(),
                "climate": self.homeworld_selected
            },
            ethos= [b["name"] for b in self.ethos_buttons if b["selected"]],
            origin=self.origin_list.get_single_selection(),
            civics= self.civics_list.get_multi_selection(),
            government= self.government_dropdown.selected_option,
            ship_appearance="Default",
            first_ruler="Ruler Name",
        )
        NationStorage.save_nation(nation)
        self.nation_list.set_item_list(self.load_nation_names())

    def delete_selected_nation(self):
        """Delete the selected nation."""
        selected_nation = self.nation_list.get_single_selection()
        if selected_nation:
            NationStorage.delete_nation(selected_nation)
            self.nation_list.set_item_list(self.load_nation_names())

    def load_nation_details(self, nation_name):
        """Load the details of a selected nation into the editor."""
        nations = NationStorage.load_nations()
        for nation_data in nations:
            if nation_data["name"] == nation_name:
                nation = Nation.from_dict(nation_data)
                # Set UI fields to match loaded nation
                self.nation_name_entry.set_text(nation.name)
                self.species_name.set_text(nation.species[0] if nation.species else "")
                # self.species_traits.select_items(nation.species_traits)  # If you implement traits
                self.homeworld_name_entry.set_text(nation.homeworld.get("planet", ""))
                self.homeworld_star_name_entry.set_text(nation.homeworld.get("star", ""))
                self.homeworld_climate.selected_option = nation.homeworld.get("climate", "")
                # Set ethos button selection
                for b in self.ethos_buttons:
                    b["selected"] = b["name"] in nation.ethos
                    # Optionally update button appearance here
                # Set origin
                #self.origin_list.select_item(nation.origin)
                # Set civics
                #self.civics_list.select_items(nation.civics)
                # Set government
                self.government_dropdown.selected_option = nation.government
                # Set ship appearance
                #self.ship_appearance_list.select_item(nation.ship_appearance)
                # Set first ruler (if you have a field for it)
                # self.ruler_name_entry.set_text(nation.first_ruler)
                break

    def handle_events(self, event):
        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.nation_list:
                self.load_nation_details(event.text)
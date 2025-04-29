import pygame
import sys 
import pygame_gui

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

        # Load a background image (make sure you have the file in your directory)
        self.background = pygame.image.load("C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/menu_background.jpg")
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))  # Scale to fit the screen
        screen.blit(self.background, (0, 0))  # Draw the background image

        # Draw a semi-transparent overlay
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        self.screen.blit(self.overlay, (0, 0))

        self.nation_selection_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 250, 1080),
            starting_height=2,
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
            item_list=["Random", "Create New", "United Nations", "United States", "China", "Russia", "India"],
            container=self.nation_selection_panel,
            manager=gui_manager
        )


        self.nation_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(450, 240, 1200, 600),
            starting_height=2,
            manager=gui_manager
        )

        self.nation_name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(300, 10, 600, 50),
            manager=gui_manager,
            container=self.nation_panel
        )
        self.nation_name_entry.set_text("Enter Nation Name")

        self.government_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["Democracy", "Monarchy", "Dictatorship", "theocracy", "Communism", "Anarchy"],
            starting_option="Democracy",
            relative_rect=pygame.Rect(300, 70, 600, 50),
            manager=gui_manager,
            container=self.nation_panel
        )

        self.ethos_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(300, 130, 600, 400),
            item_list=["Materialist", "Spiritualist", "Militarist", "Pacifist", "Xenophile", "Xenophobe", "Authoritarian", "Egalitarian"],
            container=self.nation_panel,
            manager=gui_manager
        )

        ###############################

        self.return_to_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 1010, 220, 50),
            text="Return to Main Menu",
            manager=gui_manager,
            container=self.nation_selection_panel
        )
        self.start_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(990, 540, 200, 50),
            text="Start Game",
            manager=gui_manager,
            container=self.nation_panel,
        )



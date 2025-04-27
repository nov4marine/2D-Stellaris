import pygame
import pygame_gui
import json

class UIEditor:
    def __init__(self, screen_size):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("UI Editor")
        self.clock = pygame.time.Clock()
        self.ui_manager = pygame_gui.UIManager(screen_size)
        self.elements = []  # Store all draggable UI elements
        self.dragging_element = None

    def add_element(self, element_type, rect, text=""):
        """Add a new UI element to the editor."""
        if element_type == "UIButton":
            element = pygame_gui.elements.UIButton(
                relative_rect=rect,
                text=text,
                manager=self.ui_manager
            )
            self.elements.append(element)

    def add_window(self, rect, title="New Window"):
        window = pygame_gui.elements.UIPanel(
            relative_rect=rect,
            starting_layer_height=1,
            manager=self.ui_manager
        )
        self.elements.append({"type": "Window", "element": window, "children": []})

    def add_child_to_window(self, parent_window, child_element):
        parent_window["children"].append(child_element)

    def save_layout(self, filename="layout.json"):
        """Save the current layout to a JSON file."""
        layout = []
        for element in self.elements:
            rect = element.get_relative_rect()
            layout.append({
                "type": "UIButton",
                "x": rect.x,
                "y": rect.y,
                "width": rect.width,
                "height": rect.height,
                "text": element.text
            })
        with open(filename, "w") as f:
            json.dump(layout, f)
        print(f"Layout saved to {filename}!")

    def load_layout(self, filename="layout.json"):
        """Load a layout from a JSON file."""
        with open(filename, "r") as f:
            layout = json.load(f)
        for item in layout:
            rect = pygame.Rect((item["x"], item["y"]), (item["width"], item["height"]))
            self.add_element(item["type"], rect, item["text"])

    def run(self):
        """Main loop for the editor."""
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for element in self.elements:
                        if element.get_relative_rect().collidepoint(event.pos):
                            self.dragging_element = element
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging_element = None
                elif event.type == pygame.MOUSEMOTION and self.dragging_element:
                    new_pos = (event.pos[0] - self.dragging_element.get_relative_rect().width // 2,
                               event.pos[1] - self.dragging_element.get_relative_rect().height // 2)
                    self.dragging_element.set_relative_position(new_pos)

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.screen.fill((30, 30, 30))  # Background color for the editor
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()

class TabManager:
    def __init__(self):
        self.tabs = {}
        self.active_tab = None

    def add_tab(self, tab_button, tab_panel):
        self.tabs[tab_button] = tab_panel
        if self.active_tab is None:
            self.active_tab = tab_panel  # Default to the first tab

    def switch_tab(self, clicked_tab):
        for button, panel in self.tabs.items():
            panel.hide() if button != clicked_tab else panel.show()
            self.active_tab = panel

# Run the editor
if __name__ == "__main__":
    editor = UIEditor((1920, 1080))
    editor.add_element("UIButton", pygame.Rect((100, 100), (150, 50)), "Sample Button")
    editor.run()
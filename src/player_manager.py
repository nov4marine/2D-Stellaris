# This file will host the PlayerManager class and the Player classes for both local human, multiplayer/networked human, and AI players.
# Will also end up hosting all initial development for the AI player, and may need to be split into multiple files later.


from src.gui import *
from src.nation import Nation
from src.game_state import game_state
from src.input import GlobalInputManager
from src.camera import Camera

class Player:
    def __init__(self, name, nation=None, gui_manager=None, input_manager=None):
        self.name = name
        self.nation = nation
        self.gui_manager = gui_manager
        self.input_manager = input_manager

    def issue_command(self, action, parameters=None):
        raise NotImplementedError("this method MUST be overriden by subclasses or else you will have PROBLEMS.")

class HumanPlayer(Player):
    def __init__(self, name, nation=None, is_local=False):
        super().__init__(name, nation)
        self.is_local = is_local
        self.states = {
            "view_mode": "galaxy",
            "current_solar_system": None,
        }
        self.camera = Camera(game_state["screen_width"], game_state["screen_height"])
        self.global_gui_manager = None
        self.global_input_manager = None
        self.gui_managers = {}

    def get_active_gui_manager(self):
        return self.gui_managers[self.view_state["view_mode"]]

    def issue_command(self, action, parameters=None):
        action.execute()

class AIPlayer(Player):
    def __init__(self, name, nation=None, ai_controller=None):
        super().__init__(name, nation)
        self.ai_controller = ai_controller
        
    def issue_command(self, action, parameters=None):
        #AI logic here? 
        action.execute()

class NetworkedPlayer(Player):
    def __init__(self, name, nation=None, network_manager=None):
        super().__init__(name, nation)
        self.network_manager = network_manager

    def issue_command(self, action, parameters=None):
        #communicate action to and from the server?
        pass

class PlayerManager:
    def __init__(self):
        self.players = []  # Stores human & AI players
        self.nation_assignments = {}  # Maps players to nations

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
            self.nation_assignments.pop(player, None)
            print(f"{player.name} has been removed")

    def assign_nation(self, player, nation):
        self.nation_assignments[player] = nation
        player.nation = nation
        player.global_gui_manager = GlobalGUIManager(player, nation)
        player.global_input_manager = GlobalInputManager(player, nation)
        player.gui_managers = {
            "galaxy": GalaxyGUI(nation),
            "solar_system": SolarSystemGUI(nation),
        }

        print(f"{player.name} has been assigned to {nation.name}!")

    def update_ai_players(self, time_delta):
        for player in self.players:
            if isinstance(player, AIPlayer):
                player.ai_controller.update(time_delta)

class AIController:
    def __init__(self, nation):
        self.nation = nation

    def decide_action(self, game_state):
        """Placeholder for RL agent decision logic"""
        pass

    def update(self, game_state, action_manager):
        """execute action decided above"""
        action = self.decide_action(game_state)
        action_manager.execute_action(action)

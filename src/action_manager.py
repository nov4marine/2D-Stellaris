from src.nation import Nation
from src.colony import *
from src.galaxy import Galaxy
from src.solar_system import SolarSystem
from src.gui import GUIManager, GalaxyGUI, SolarSystemGUI
from src.player_manager import PlayerManager, HumanPlayer, AIPlayer

from src.game_state import game_state

class Action:
    def __init__(self, executor=None):
        """Base class for actions taken by a given executor. Executor can be player or AI."""
        self.executor = executor

    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")

class ManageEconomyAction(Action):
    def __init__(self, nation):
        super().__init__(executor=nation)

    def execute(self):
        self.executor['gdp'] += 1000
        print(f"{self.executor['name']}'s GDP is now {self.executor['gdp']}")

class ActionManager:
    def __init__(self):
        self.action_log = [] #log of all executed actions for obvious(?) reasons like debugging. action is logged immediately before execution in case of failure.

    def execute_action(self, action):
        self.action_log.append(action)
        action.execute()

################################################

class GenericAction(Action):
    def __init__(self, executor, action_type, parameters=None):
        super().__init__(executor)
        self.action_type = action_type
        self.parameters = parameters

    def execute(self):
        if self.action_type == "manage_economy":
            self.executor.gdp += self.parameters.get("amount", 1000)
            print(f"{self.executor.name}'s GDP increased to {self.executor.gdp}")
        elif self.action_type == "build_ship":
            print(f"{self.executor.name} is building {self.parameters['ship_type']}!")

######################################################
# Action classes for specific actions
# These classes inherit from the base Action class and implement specific actions.

class StartNewGameAction(Action):
    """Behold, the holiest of all actions: starting a new game."""
    def __init__(self, game_state, manager, setup_dict):
        super().__init__(None) # No executor needed for this action
        self.game_state = game_state
        self.manager = manager
        self.setup_dict = setup_dict
        self.capital_system = None

    def execute(self):
        # Logic to start a new game
        print("Starting a new game...")
        #pull parameters from setup_dict from the setup menu
        galaxy_paremeters = self.setup_dict["galaxy_parameters"]
        nation_parameters = self.setup_dict["nation_parameters"]

        size_map = {"small": 800, "medium": 1000, "large": 1200}
        galaxy_size = size_map.get(galaxy_paremeters["size"], 1000)
        num_stars = galaxy_size
        
        # Create a new galaxy based on the parameters
        self.game_state["galaxy"] = Galaxy(
            galaxy_size=10000,
            num_stars=num_stars
        )

        self.game_state["player_manager"] = PlayerManager() #create the player manager
        #create AI players equal to the number of nations selected in setup, create a random nation and assign to each.
        for i in range(galaxy_paremeters["number_of_nations"]): 
            #self.game_state["player_manager"].add_player(AIPlayer(name=f"AI Player {nation}")) #uncomment this to allow adding AI players. 
            #randomly select a nation from the list of nations, create it, and assign it to the player
            #self.game_state["player_manager"].assign_nation(player, nation)
            #create a gui, input, and ai controller for each AI player (but the AI probably won't need a GUI, and the input manager will be different I think)
            #self.game_state["player_manager"].players[i].gui_manager = GUIManager(self.game_state["galaxy"], self.game_state["player_manager"].players[i])
            #self.game_state["player_manager"].players[i].input_manager = InputManager(self.game_state["player_manager"].players[i])
            pass #for now, just pass
        
        #add the human player (in this case THE player in single player)
        self.game_state["player_manager"].add_player(HumanPlayer(name="Player 1")) #add the human player
        #create custom nation for the human player based on the setup menu
        capital_system = SolarSystem.assign_capital_system(self.game_state["galaxy"], nation_parameters)
        print(f"Capital system assigned: {capital_system}")
        nation1 = Nation(
            name=nation_parameters["name"],
            species=nation_parameters["species"],
            population=nation_parameters["population"],
            homeworld=capital_system, # earth, sol
            ethos=nation_parameters["ethos"],
            origin=nation_parameters["origin"],
            civics=nation_parameters["civics"],
            government=nation_parameters["government"],
        )
        #assign that nation to the human player
        self.game_state["player_manager"].assign_nation(self.game_state["player_manager"].players[-1], nation1, self.manager)

        for nation in self.game_state["player_manager"].nation_assignments.values():
            nation.initialize_nation()  # Initialize each nation

        #later implement a function to create a new nation for each player or AI
        #for now, just create a new nation for the player

        #create function that initializes all neccessary GUI for each player/nation, specific to that player/nation

        self.game_state["current_state"] = "gameplay"


##########################################################

class ExploreGalaxyAction(Action):
    def __init__(self, executor, galaxy):
        super().__init__(executor)
        self.galaxy = galaxy

    def execute(self):
        # Logic to explore the galaxy
        print(f"{self.executor.name} is exploring the galaxy.")

class BuildBuildingAction(Action):
    def __init__(self, executor, building_type, parameters=None):
        super().__init__(executor)
        self.building_type = building_type
        self.parameters = parameters if parameters else {}

    def execute(self):
        # Logic to build the building
        print(f"{self.executor.name} is building a {self.building_type} with parameters: {self.parameters}")

class ResearchTechnologyAction(Action):
    def __init__(self, executor, technology):
        super().__init__(executor)
        self.technology = technology

    def execute(self):
        # Logic to research the technology
        print(f"{self.executor.name} is researching {self.technology.name}.")

class MoveFleetAction(Action):
    def __init__(self, executor, fleet, destination):
        super().__init__(executor)
        self.fleet = fleet
        self.destination = destination

    def execute(self):
        # Logic to move the fleet to the destination
        print(f"{self.executor.name} is moving {self.fleet.name} to {self.destination.name}.")

class ColonizePlanetAction(Action):
    def __init__(self, executor, planet, colony_name):
        super().__init__(executor)
        self.planet = planet
        self.colony_name = colony_name

    def execute(self):
        # Logic to colonize the planet
        print(f"{self.executor.name} is colonizing {self.planet.name} as {self.colony_name}.")

class BuildShipAction(Action):
    def __init__(self, executor, ship_type, parameters=None):
        super().__init__(executor)
        self.ship_type = ship_type
        self.parameters = parameters if parameters else {}

    def execute(self):
        # Logic to build the ship
        print(f"{self.executor.name} is building a {self.ship_type} with parameters: {self.parameters}")
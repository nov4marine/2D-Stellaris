# This file will house all things directly related to the military model. Unless it gets too long.

class Military:
    def __init__(self, owner, doctrine=None):
        """Initialize the military with an owner and empty lists for fleets, ships, and armies. Most of what's here will be registry and tracking, not actual actions."""
        self.owner = owner
        self.doctrine = doctrine  # Military doctrine 
        self.military_xp = 0 # will be used similarly to hoi4 army/air/navy xp
        self.modifiers = {}
        self.fleets = [] # List of fleets which will be a class containing ships
        self.starbases = [] # List of starbases 
        self.ships = [] # List of ships which will be a class containing ship properties
        self.armies = []
        self.expenses = {} # Dictionary to track military expenses by category {"naval wages": 0, "ship maintenance": 0, "army wages": 0, "army maintenance": 0, etc.}

    def add_fleet(self, fleet):
        # Add a new fleet to the military
        self.fleets.append(fleet)

    def remove_fleet(self, fleet):
        # Remove a fleet from the military
        if fleet in self.fleets:
            self.fleets.remove(fleet)

    def add_ship(self, ship):
        # Add a new ship to the military
        self.ships.append(ship)

    def remove_ship(self, ship):
        # Remove a ship from the military
        if ship in self.ships:
            self.ships.remove(ship)

    def add_army(self, army):
        # Add a new army to the military
        self.armies.append(army)

    def remove_army(self, army):
        # Remove an army from the military
        if army in self.armies:
            self.armies.remove(army)

    def calculate_expenses(self):
        # Calculate military expenses by category based on fleets, ships, armies, etc.
        for fleet in self.fleets:
            self.expenses["naval wages"] = fleet.calculate_wages()
            self.expenses["ship maintenance"] = fleet.calculate_maintenance()

        for army in self.armies:
            self.expenses["army wages"] = army.calculate_wages()
            self.expenses["army maintenance"] = army.calculate_maintenance()
        # Add more expense categories as needed

class Ship:
    """super class for all ships, both military and civilian. This will be used to track ship properties, components, and stats."""
    def __init__(self, name, ship_type, ship_class, component_slots, components=None):
        self.name = name
        self.ship_type = ship_type
        self.ship_class = ship_class
        # Dictionary of components. ship designer will handle comptability restrictions and component stats. {"category": number of slots}
        self.components = components if components is not None else [] # List of components on ship, which will be class objects
        self.component_slots = component_slots # Dictionary of component slots. {"category": number of slots}
        self.crew = {} # Dictionary of crew attributes such as quantity, morale?, experience, training, etc.
        self.upkeep = {} # Dictionary of upkeep attributes such as fuel, ammo, etc.
        self.base_stats = {} # Dictionary of ship stats such as speed, firepower, armor, etc. primarily based on components
        self.real_stats = {} # Dictionary of ship stats after modifiers such as from components, crew, and fleet modifiers, or damage
        self.status = "active"  # Status of the ship (active, mothballed, etc.)

    def calculate_stats(self):
        # Calculate ship stats based on components and crew
        self.base_stats["speed"] = sum(component.speed for component in self.components)
        self.base_stats["firepower"] = sum(component.firepower for component in self.components)
        self.base_stats["armor"] = sum(component.armor for component in self.components)
        # Add more stats as needed
        
    def calculate_maintenance(self):
        # Calculate maintenance cost based on ship type and size
        return self.size * 10  # Placeholder formula

    def calculate_wages(self):
        # Calculate wages for crew based on ship type and size
        return self.size * 5  # Placeholder formula

    def change_component(self, component_name, new_component):
        # Change a component of the ship
        if component_name in self.component_slots:
            # Check if the new component is compatible with the ship
            self.component_slots[component_name] = new_component
        else:
            print(f"Component {component_name} not found in ship {self.name}.")

    def reinforce_crew(self, crew_member):
        # Reinforce the crew of the ship
        if crew_member not in self.crew:
            self.crew[crew_member] = 1

    def mothball(self):
        # Mothball the ship (put it in reserve)
        self.status = "mothballed"
        # Add logic to reduce maintenance costs or remove from active fleet

    def reactivate(self):
        # Reactivate the ship (bring it back into service)
        self.status = "active"
        # Add logic to restore maintenance costs or add to active fleet

    def decommission(self):
        # Decommission the ship (remove it from service)
        self.status = "decommissioned"
        # Add logic to remove from fleet and scrap the ship

    def die(self):
        # Handle the death of the ship (e.g., destroyed in combat)
        self.status = "destroyed"
        # Add logic to remove from fleet and handle salvage or loss and play explosion effects

class Component:
    """Super class for all types of components. This will be used to track component properties, stats, and compatibility.
        There will be subclasses for each type of component, such as weapons, engines, etc.
    """
    def __init__(self, name, component_type, component_class, stats):
        self.name = name
        self.component_type = component_type  # Type of component (e.g., weapon, engine, etc.)
        self.component_class = component_class  # Class of component (e.g., small, medium, large)

class MilitaryShip(Ship):
    def __init__(self, name, fleet, position, ship_type, ship_class, component_slots, role, components=None):
        super().__init__(name, ship_type, ship_class, component_slots, components)
        self.name = name
        self.fleet = fleet  # Fleet to which the ship belongs
        self.position = position  # Position where the ship is located (where initially spawned) (x, y coordinates)
        self.ship_type = "military"
        self.ship_class = ship_class
        self.component_slots = component_slots
        self.components = components if components is not None else []
        self.crew = {}
        self.upkeep = {}
        self.stats = {}
        self.status = "active"
        self.role = role  # Role of the ship (e.g., swarmer, tank, support, etc.)
        self.targeting_priorities = {}  # Dictionary to store target priorities based on ship logic,

    def acquire_targets(self, enemies):
        """select targets from the list of enemies based on ship logic, and assign priorities to them"""
        for enemy in enemies:
            # Logic to determine target priority based on ship role and enemy attributes
            if self.role == "swarmer":
                # randomly target the closest 5% of the enemy fleet, with priority based on distance
                distance = self.calculate_distance(enemy)
                self.targeting_priorities[enemy] = distance

    def calculate_distance(self, enemy):
        """calculate the distance to the enemy ship"""
        # Placeholder logic for distance calculation
        return ((self.position[0] - enemy.position[0]) ** 2 + (self.position[1] - enemy.position[1]) ** 2) ** 0.5
    
    def engage_target(self, target):
        """engage the target ship"""
        # Logic to engage the target ship based on ship role and target attributes
        if self.role == "swarmer":
            # Logic for swarmer role engagement
            pass
        elif self.role == "tank":
            # Logic for tank role engagement
            pass
        elif self.role == "support":
            # Logic for support role engagement
            pass
        else:
            print(f"Unknown ship role: {self.role}")

    def disengage_target(self, target):
        """disengage the target ship"""
        # Logic to disengage from the target ship
        if target in self.targeting_priorities:
            del self.targeting_priorities[target]
        else:
            print(f"Target {target} not found in targeting priorities.")
        # Add logic to handle disengagement mechanics, such as retreating or regrouping
    
    def take_damage(self, damage):
        """take damage from enemy fire"""
        # Logic to handle damage taken by the ship
        self.stats["armor"] -= damage
        if self.stats["armor"] <= 0:
            self.decommission()

class Fleet:
    def __init__(self, name, fleet_type, ships=None):
        self.name = name
        self.fleet_type = fleet_type  # Type of fleet (e.g., naval, transport, etc.)
        self.ships = ships if ships is not None else []  # List of ships in the fleet
        self.status = "active"  # Status of the fleet (active, mothballed, docked, etc.)
        self.commander = None # Commander of the fleet when I add leaders
        self.modifiers = {} # Dictionary to store fleet modifiers, mostly from the commander
        self.mission = None # Mission assigned to the fleet (e.g., exploration, combat, etc.) will be a class
        self.in_combat = False # Flag to indicate if the fleet is in combat
        self.formation = None # Formation of the fleet (e.g., line, wedge, etc.) should be a class?
        self.speed = 0 # Speed of the fleet, which will be the speed of the slowest ship in the fleet
        self.position = (0, 0) # Position of the fleet in the galaxy
        self.destination = None # Destination of the fleet
        self.morale = 100 # Morale of the fleet, which will be an average of the morale of all ships in the fleet
        self.upkeep = {} # Dictionary to track upkeep costs for the fleet
        self.supply = 0 # Supply of the fleet, which will be a total quantity of supplies available to the fleet
        
    def assign_commander(self, commander):
        # Assign a commander to the fleet
        self.commander = commander
        # Add logic to assign skills and bonuses based on the commander's attributes

    def recall_commander(self):
        # Recall the commander from the fleet
        self.commander = None
        # Add logic to remove skills and bonuses based on the commander's attributes

    def add_ship(self, ship):
        # Add a ship to the fleet
        self.ships.append(ship)

    def remove_ship(self, ship):
        # Remove a ship from the fleet
        if ship in self.ships:
            self.ships.remove(ship)

    def set_formation(self, formation):
        # Set the formation of the fleet
        self.formation = formation
        # Add logic to arrange ships in the specified formation

    def set_mission(self, mission):
        # Set the mission of the fleet
        self.mission = mission
        # Add logic to assign tasks based on the mission

    def calculate_speed(self):
        # Calculate the speed of the fleet based on the slowest ship
        if self.ships:
            self.speed = min(ship.stats["speed"] for ship in self.ships)
        else:
            self.speed = 0

    def calculate_morale(self):
        # Calculate the morale of the fleet based on the average morale of all ships
        if self.ships:
            self.morale = sum(ship.stats["morale"] for ship in self.ships) / len(self.ships)
        else:
            self.morale = 100

    def set_destination(self, destination):
        # Set the destination of the fleet
        self.destination = destination
        # Add logic to navigate to the destination

    def engage_combat(self, enemy_fleet):
        # Engage in combat with an enemy fleet
        self.in_combat = True
        # Add logic to handle combat mechanics, targeting, and damage calculations

    def disengage_combat(self):
        # Disengage from combat
        self.in_combat = False
        # Add logic to handle retreat or regrouping

    def dock(self, dock):
        # Dock the fleet at a space station or planet
        self.status = "docked"
        # Add logic to handle docking procedures and repairs

    def undock(self):
        # Undock the fleet from a space station or planet
        self.status = "active"
        # Add logic to handle undocking procedures and rejoining the fleet

    def exercise(self):
        # Conduct exercises to improve fleet experience and accrue experience points
        for ship in self.ships:
            ship.stats["experience"] += 1

    def calculate_upkeep(self):
        # Calculate the upkeep cost for the fleet based on the ships in it
        self.upkeep = sum(ship.calculate_maintenance() for ship in self.ships) + sum(ship.calculate_wages() for ship in self.ships)
        return self.upkeep
    

class CivilianShip(Ship):
    def __init__(self, name, ship_type, ship_class, component_slots, components=None):
        super().__init__(name, ship_type, ship_class, component_slots, components)
        self.name = name
        self.ship_type = "civilian"
        self.ship_class = ship_class
        self.component_slots = component_slots
        self.components = components if components is not None else []
        self.crew = {}
        self.upkeep = {}
        self.stats = {}
        self.status = "active"

class Starbase:
    def __init__(self, name, position, size, status="active"):
        self.name = name
        self.position = position  # Position of the starbase in the galaxy
        self.size = size  # Size of the starbase (e.g., small, medium, large)
        self.status = status  # Status of the starbase (active, under construction, etc.)
        self.modules = []  # List of modules installed on the starbase
        self.upkeep = {}  # Dictionary to track upkeep costs for the starbase
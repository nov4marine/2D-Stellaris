from src.interest_group import InterestGroup
from src.colony import *
from src.economy import *
from src.military import *
from src.government import *

class Nation:
    def __init__(self, name, population, species, homeworld, ethos, origin, civics, government, ship_appearance=None, first_ruler=None):
        self.name = name
        self.flag = None #flag of the nation
        self.color = (200, 0, 0) #used for soverignity and other things, like the color of the nation in the galaxy map
        self.gdp = 0 #the big one that determines everything else
        self.population = population #starting population (instance of pop? or total number?)
        self.species = species # a list of all species in the nation. initially just the starting species
        self.gdp_percapita = 0
        self.homeworld = homeworld #starting capital planet and system
        self.capital = None #capital planet (instance of planet)
        self.capital_system = None #capital system (instance of solar system)
        self.ethos = ethos #list of ethics
        self.origin = origin
        self.civics = civics
        self.government = government
        self.colonies = [] #list of colonies in the nation
        self.bank = None #investment manager
        self.ship_appearance = ship_appearance
        self.first_ruler = first_ruler
        self.research = None #research manager
        self.research_rate = 0 #research rate, probably a percentage of the total research points available
        self.modifiers = [] #list of modifiers that affect the nation. this will be a list of dictionaries, each with a name and value
        self.planets = [] #list of colonized planets in the nation. 

        self.bureaucracy = 0
        self.budget = 0
        
        # above this line is the basic information about the nation. below are components of the nation that will be used in the game
        #self.tax_department = IRS() # the tax department for the nation.
        self.market = Market(self) # the market for the nation.
        self.military = Military(self) 
        self.interest_groups = [] #list of interest groups in the nation
        self.diplomatic_relations = {} #dictionary of relations with other nations (might later be expanded to types of relations)
        self.state_religion = None #state religion, if any. None if secular, state atheism is a religion in this model lol
        
        self.intel = {} #dictionary of intel level on each other empire (might later be expanded to types of intel)
        self.council_positions = {} # Will be a dictionary of Council positions and the person filling them, based on Stellaris.
        
        
        #laws that the nation has (dict of laws)

        self.possible_laws = {
            #Power Laws
            "Power Structure": ["Republic", "Monarchy", "Theocracy", "Council Republic"],
            "Distribution of Power": ["Universal Suffrage", "Census Suffrage", "Wealth voting", "Oligarchy", "Technocracy", "Autocracy", "Single Party State", "Anarchy"],
            "Citizenship": ["Ethnostate", "Alien Residents", "Alien Enslavement", "Universal Citizenship", "Undesirables"],
            "Religion": ["Secular", "State Religion", "State Preference", "State Atheism"],
            "Bureaucracy": ["Centralized", "Decentralized", "Federal"],
            "Army Doctrine": ["Professional", "Militia", "Conscription", "Volunteer"],
            "Navy Doctrine": ["Professional", "Militia", "Conscription", "Volunteer"],
            "War Doctrine": ["Total War", "Limited War", "Conventional Warfare", "Guerrilla Warfare"],
            "Internal Security": ["National Guard", "Internal Security Forces", "Secret Police"],
            # Economy Laws
            "Economic System": ["Interventionism", "Laissez-Faire", "Command Economy", "Cooperative Ownership"],
            "Trade Policy": ["Free Trade", "Protectionism", "Autarky"],
            "Taxation": ["Progressive Taxation", "Flat Tax", "Per-capita Tax"],
            "Policing" : ["Community Policing", "Militarized Policing", "Private Policing"],
            "Education" : ["Public Education", "Private Education", "Religious Education"],
            "Healthcare" : ["Universal Healthcare", "Private Healthcare"],
            "Unions" : ["All Allowed", "Banned", "State Unions", "Suppressed Unions"],
            "Environmental Protection" : ["Strong Protections", "Weak Protections", "No Protections"],
            # Human Rights Laws
            "Speech and Assembly": ["Both Protected", "Free Speech", "Free Assembly", "Censorship"],
            "Labor Rights": ["Strong Protections", "Weak Protections", "No Protections"],
            "Gender and Sexuality": ["Full Equality", "Partial Equality", "No Guarantees"],
            "Welfare" : ["Universal Basic Income", "Social Safety Net", "No Welfare"],
            "Housing" : ["No Housing Program", "Public Housing", "Private Housing Regulation"],
            "Immigration and Refugees" : ["Open Borders", "Primary Species Only", "Closed Borders"],
            "Slavery" : ["Prohibited", "Aliens Only", "Allowed"],
            #Stellaris Laws that will be categorized later
            "Genetic Modification" : ["Regulated", "Prohibited", "Allowed"],
            "Artificial Intelligence" : ["Servitude", "Prohibited", "Citizen Rights"],
            "Robotics" : ["Allowed", "Prohibited"], 
            "Diplomatic Stance" : ["Expansionist", "Cooperative", "Isolationist", "Belligerent", "Supremacist"],
            "War Philosophy" : ["Just Cause", "Liberation", "Imperialist", "Defensive"],
            "Rules of War" : ["Selective", "Indiscriminate", "Armageddon"],
            "Resettlement" : ["Prohibited", "Allowed"],
            "Initial Border Status" : ["Open", "Closed"],
            "Population Controls" : ["Prohibited", "Allowed"],
            "Purge" : ["Prohibited", "Displacement Only", "Allowed"]
        }

        self.current_laws = {
            #Power Laws
            "Power Structure": "Republic",
            "Distribution of Power": "Universal Suffrage",
            "Citizenship": "Alien Residents", #might correspond to which species the player can give rights to
            "Religion": "Secular", # no idea how I'm going to implement separate religions, but I think it would be a good fit for Stellaris
            "Bureaucracy": "Centralized", # honestly not sure what this means in the context of Stellaris, but it seems like a good idea to have it
            "Army Doctrine": "Professional", # might use some combination of Victoria and hoi4 army doctrines
            "Navy Doctrine": "Professional", # might use some combination of Stellaris and hoi4 navy doctrines
            "Internal Security": "National Guard", # Not sure what other options should be here, but this will definitely be relavant for planetary events, emergent or random
            # Economy Laws
            "Economic System": "Interventionism",
            "Trade Policy": "Free Trade",
            "Taxation": "Progressive Taxation",
            "Policing" : "Community Policing",
            "Education" : "Public Education",
            "Healthcare" : "Universal Healthcare",
            "Unions" : "All Allowed",
            "Environmental Protection" : "Strong Protections",
            # Human Rights Laws
            "Speech and Assembly": "Both Protected",
            "Labor Rights": "Strong Protections",
            "Gender and Sexuality": "Full Equality",
            "Welfare" : "Universal Basic Income",
            "Housing" : "No Housing Program",
            "Immigration and Refugees" : "Open Borders",
            "Slavery" : "Prohibited",
            #Stellaris Laws that will be categorized later
            "Genetic Modification" : "Regulated",
            "Artificial Intelligence" : "Servitude",
            "Robotics" : "Allowed",
            "Diplomatic Stance" : "Expansionist",
            "War Philosophy" : "Just Cause",
            "Rules of War" : "Conventional Warfare",
            "Resettlement" : "Prohibited",
            "Initial Border Status" : "Open",
            "Population Controls" : "Prohibited",
            "Purge" : "Prohibited", 

        }



    def initialize_nation(self):
        """Initialize the nation."""
        self.initialize_interest_groups()
        self.initialize_capital()

    def initialize_capital(self):
        """Initialize the capital system and planet."""
        self.capital = self.homeworld[0]         # Planet object
        self.capital_system = self.homeworld[1]
        #self.capital_system.owner = self  # SolarSystem object

        # Attach a Colony to the planet
        self.capital.colony = Colony(
            planet=self.capital,
            type=getattr(self.capital, "climate", None),
            habitability=100,
            land_area=getattr(self.capital, "size", None),
            owner=self,
            name=getattr(self.capital, "name", None),
            market=self.market,
            initial_homeworld=True,
            initial_population=self.population,
        )
        self.colonies.append(self.capital.colony)
        self.planets.append(self.capital)
        

    def initialize_interest_groups(self):
        """Initialize the interest groups for the nation."""
        # This will be a rough draft of the base interest groups that all nations start with.
        # starting with a base of at least 1 for each ethos 
        self.interest_groups = [
            InterestGroup("Spiritualists", "Description of spiritualists", self),
            InterestGroup("Industrialists", "both individual capitalists, and institutional mega corps", self),
            InterestGroup("Armed Forces", "people who love and support the military", self),
            InterestGroup("Technocrats", "Liberals, intelligentsia, tech bros, finance bros, and the highly educated", self),
            InterestGroup("Petit Bourgeoisie", "Urban conservatives, small business owners, etc. the racists", self),
            InterestGroup("Proletariat", "The working class, the laborers, the people who do all the work", self),
            InterestGroup("Ruralists", "The farmers, the people who grow the food. Prefer decentralization. often but not always conservative", self),
            InterestGroup("Environmentalists", "The people who care about the environment. Often but not always leftist", self),
            InterestGroup("Libertarians", "The people who care about freedom. Often but not always rightist", self),

        ]

    ################# #bottom 2 here are for saving and loading nations from json files

    def to_dict(self):
        """Convert the nation to a dictionary for saving."""
        return {
            "name": self.name,
            "population": self.population,
            "species": self.species,
            "homeworld": self.homeworld,
            "ethos": self.ethos,
            "origin": self.origin,
            "civics": self.civics,
            "government": self.government,
            "ship_appearance": self.ship_appearance,
            "first_ruler": self.first_ruler
        }

    @staticmethod
    def from_dict(data):
        """Create a Nation object from a dictionary."""
        return Nation(
            name=data["name"],
            population=data["population"],
            species=data["species"],
            homeworld=data["homeworld"],
            ethos=data["ethos"],
            origin=data["origin"],
            civics=data["civics"],
            government=data["government"],
            ship_appearance=data["ship_appearance"],
            first_ruler=data["first_ruler"],
        )
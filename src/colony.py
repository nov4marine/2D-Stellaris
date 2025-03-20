class Colony:
    """mega class to represent an inhabited world"""
    def __init__(self, planet, type, habitability, owner, name):
        self.planet = planet
        self.type = type
        self.habitability = habitability
        self.owner = owner 
        self.name = name

        self.population = 1000000
        self.unrest = 0
        self.gdp = 0
        self.buildings = {}
        self.construction = 0
        self.deficits = 0
        self.output = 0
        self.unemployed = 0

        self.colony_setup = self._colony_setup()

    def _colony_setup():
        """method to generate initial buildings upon colonization"""

    def construction():
        """method to model construction and upgrading of infrastructure"""

    def population_growth():
        """method to model population growth"""
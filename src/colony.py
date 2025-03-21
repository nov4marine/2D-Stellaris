class Colony:
    """mega class to represent an inhabited world"""
    def __init__(self, planet, type, habitability, owner, name, market):
        self.planet = planet
        self.type = type
        self.habitability = habitability
        self.owner = owner 
        self.name = name
        self.market = market

        self.pops = []
        self.unrest = 0
        self.gdp = 0
        self.buildings = []
        self.construction_points = 0
        self.deficits = 0
        self.output = 0
        self.unemployed = 0

        self.colony_setup = self._colony_setup()

    def _colony_setup(self):
        """method to generate initial buildings upon colonization"""

    def construction(self):
        """method to model construction and upgrading of infrastructure"""

    def population_growth(self):
        """method to model population growth"""

    def consume_needs(self):
        for pop in self.pops:
            pop.consume_goods(self.market)

    def produce_goods(self):
        for building in self.buildings:
            building.operate(self.market)

class Pop:
    def __init__(self, pop_type, size, job, needs):
        self.type = pop_type
        self.size = size
        self.job = job
        self.needs = needs  # Example: {"food": 5, "consumer_goods": 2}
        self.happiness = 100

    def consume_goods(self, market):
        for good, quantity in self.needs.items():
            if market.buy_good(self, good, quantity):
                continue
            else:
                self.happiness -= 10  # Penalize unmet needs

class Building:
    def __init__(self, name, building_type, land_area, input_goods, output_goods, jobs, efficiency=1.0, levels=1):
        self.name = name
        self.type = building_type
        self.land_area = land_area
        self.input_goods = input_goods  # Example: {"minerals": 20}
        self.output_goods = output_goods  # Example: {"steel": 10}
        self.jobs = jobs #dictionary. Example {"technicians": 1000}
        self.efficiency = efficiency
        self.levels = levels
        self.revenue = 0
        self.expenses = 0

    def operate(self, market):
        #reset for the tick
        self.expenses = 0
        self.revenue = 0

        # Buy inputs
        for good, quantity in self.input_goods.items():
            total_inputs = quantity * self.efficiency * self.levels
            self.expenses += market.buy_good(good, total_inputs)

        # Sell outputs
        for good, quantity in self.output_goods.items():
            total_outputs = quantity * self.efficiency * self.levels
            self.revenue += market.sell_good(good, total_outputs)
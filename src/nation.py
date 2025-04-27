class Nation:
    def __init__(self, name, population, capital):
        self.name = name
        self.gdp = 0
        self.population = population
        self.gdp_percapita = 0
        self.capital = capital
        self.colonies = []
        self.bank = 0

        self.bureaucracy = 0
        self.budget = 0
        self.research = 0
        
        #self.setup = initialize_nation()

    #def initialize_nation(self):
        #capital = Capital()
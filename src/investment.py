#Investment logic, including the private investment queue, and gov auto-investor logic.
from nation import Nation
from colony import Colony, Building

class InvestmentBank:
    """investment manager for construction"""
    def __init__(self, owner, banks):
        self.owner = owner
        self.banks = banks
        self.investment_pool = 0

    def calculate_average_profitability(self):
        colony_profitability = {}
        for bank in self.banks:
            profitability_data = bank.evaluate_profitability()
            #calculate the average for this planet
            average_profitability = sum(profitability_data.values()) / len(profitability_data)
            colony_profitability[bank.parent_colony.name] = (average_profitability, bank)
        return colony_profitability

    def distribute_investments(self):
        """Distribute the investment pool based on average profitability."""
        # Step 1: Get average profitability for each planet
        colony_profitability = self.calculate_average_profitability()

        # Step 2: Calculate the total profitability across all planets
        total_profitability = sum(colony_profitability.values())

        # Step 3: Allocate funds based on weighted profitability
        for planet, (avg_profitability, bank) in colony_profitability.items():
            # Calculate the share of the investment pool for this planet
            share = (avg_profitability / total_profitability) * self.investment_pool
            bank.reinvestment_pool += share


class LocalBank:
    """local private investment manager, similar to victoria financial districts."""
    def __init__(self, parent_colony):
        self.parent_colony = parent_colony
        self.levels = 1 #add 1 level per owned building level on the planet, similar to victoria
        self.jobs = [] #list of job instances, which are only owner-class
        self.reinvestment_pool = 0

    def evaluate_profitability(self):
        opportunity_catalogue = {}
        for building in self.parent_colony.buildings:
            #calculates profit per level per construction cost
            profitability = (building.profit / building.levels) /building.construction_cost
            opportunity_catalogue[building.name] = profitability #appends to dictionary "building name": profitability
        return opportunity_catalogue

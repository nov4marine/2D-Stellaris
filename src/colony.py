class Colony:
    """mega class to represent an inhabited world"""
    def __init__(self, planet, type, habitability, land_area, owner, name, market):
        self.planet = planet
        self.type = type
        self.habitability = habitability
        self.land_area = land_area
        self.owner = owner 
        self.name = name
        self.market = market
        self.planet_modifiers = {} #dictionary for planet-wide modifiers e.g. {"industrial edict": 1.2}

        #these are central registries to track the economic units of the colony
        self.colony_pops = [] #list of all pops in on this world
        self.colony_buildings = [] #list of all buildings on this world
        self.colony_jobs = [] #list of all jobs on this world

        self.unrest = 0
        self.gdp = 0
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

    def process_job_market(self):
        """let every pop evaluate the the job market for offers"""
        for pop in self.pops:
            pop.evaluate_jobs()
        if pop.best_offer:
            pop.accept_newjob()

    def consolidate_pops(self):
        """method to consolidate pops of identical properties and jobs"""


class Building:
    def __init__(self, name, colony, building_type, land_size, input_goods, output_goods, efficiency=1.0, levels=1):
        self.name = name
        self.colony = colony
        self.type = building_type
        self.land_size = land_size
        self.input_goods = input_goods  # Example: {"minerals": 20}
        self.output_goods = output_goods  # Example: {"steel": 10}
        self.jobs = [] #list of job instances, 1 for each profession the building hires
        self.efficiency = efficiency
        self.levels = levels
        self.revenue = 0
        self.expenses = 0
        self.cash_reserves = 0

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

    def calculate_payouts(self):
        """Distribute revenue proportionally based on the wage and pop size working in each job."""
        payouts = {}
        # For a simple demonstration, we weight each pop's share by (job wage * pop size).
        total_weight = sum(job.wage * job.current_employment() for job in self.jobs)
        
        # Avoid division by zero if there are no assigned pops.
        if total_weight == 0:
            return payouts

        for job in self.jobs:
            for pop in job.assigned_pops:
                # Each pop's proportional share of the building's revenue:
                share = (job.wage * pop.size / total_weight) * self.revenue
                payouts[pop.name] = payouts.get(pop.name, 0) + share
        return payouts


class Job: 
    """jobs on a colony, referencing their parent building"""
    def __init__(self, profession, wage, max_positions, building=None):
        self.profession = profession #profession for this job
        self.wage = wage #wage is the pay of this job
        self.building = building
        self.max_positions = max_positions #total number of employees for this job
        self.assigned_pops = [] #list of pops employed in this job 

    def current_employment(self):
        """returns the current number of individuals assigned to this job"""
        return sum(pop.size for pop in self.assigned_pops)
    
    def job_openings(self):
        """returns how many more individuals can be assigned to this job"""
        return self.max_positions - self.current_employment()
    
    def consolidate_pops(self):
        """
        Automatically merge pops with identical properties.
        The key for merging is a combination of the pop's name and traits.
        This reduces fragmentation and keeps assigned_pops list tidy.
        """
        consolidated = {}
        for pop in self.assigned_pops:
            # Use (name, frozenset of trait items) as the key
            key = (pop.name, frozenset(pop.traits.items()))
            if key in consolidated:
                consolidated[key].size += pop.size
            else:
                # Create a new Pop instance as the basis of consolidation.
                consolidated[key] = Pop(pop.name, pop.size, current_job=self, traits=pop.traits)
        # Replace the assigned pops list with the consolidated pops.
        self.assigned_pops = list(consolidated.values())
    
class Pop:
    def __init__(self, name, colony, pop_type, size, profession, needs, income, current_job=None):
        self.name = name
        self.colony = colony
        self.pop_type = pop_type
        self.size = size
        self.profession = profession
        self.needs = needs  # Example: {"food": 5, "consumer_goods": 2}
        self.happiness = 100
        self.income = income
        self.current_job = current_job #reference to the job this pop is assigned to

    def consume_goods(self, market):
        for good, quantity in self.needs.items():
            market.buy_good(self, good, quantity)

    def split(self, amount):
        """
        Splits 'amount' individuals from this pop and returns a new Pop instance.
        The current pop's size is reduced by 'amount'.
        """
        if amount > self.size:
            raise ValueError("Not enough individuals to split!")
        self.size -= amount
        # Optionally, you can modify the name or add an identifier to the split pop.
        return Pop(self.colony, self.pop_type, amount, self.profession, self.needs, self.income, current_job=None)

    def evaluate_job_market(self, available_jobs, threshold=0.1):
        """
        Look for jobs with a wage that is significantly higher than the current job's wage.
        Only switch if the potential increase is at least 'threshold' (e.g., 0.1 for a 10% increase).
        If the new job lacks capacity for the entire pop, the pop is split and only available portion migrates.
        """
        # Use 0 as baseline if not employed.
        current_wage = self.current_job.wage if self.current_job else 0
        best_job = None
        best_wage = current_wage

        # Evaluate each job to see if it offers a meaningful improvement.
        for job in available_jobs:
            cap = job.job_openings()
            if cap <= 0:
                continue  # Skip jobs with no room

            if self.current_job:
                # Only consider switching if the wage increase meets the threshold.
                if job.wage > best_wage and ((job.wage - current_wage) / current_wage) >= threshold:
                    best_job = job
                    best_wage = job.wage
            else:
                # If unemployed, select based solely on the wage.
                if job.wage > best_wage:
                    best_job = job
                    best_wage = job.wage

        # If a suitable job is found, determine how many individuals can migrate:
        if best_job:
            cap = best_job.job_openings()
            migrating_size = min(self.size, cap)
            if migrating_size <= 0:
                print("No capacity available in the new job.")
                return self

            # If only part of the pop can migrate:
            if migrating_size < self.size:
                migrated_pop = self.split(migrating_size)
                migrated_pop.current_job = best_job
                best_job.assigned_pops.append(migrated_pop)
                print(f"{migrated_pop.size} individuals from pop '{self.name}' migrated to job '{best_job.title}' with wage {best_job.wage}")
                return migrated_pop
            else:
                # Entire pop migrates:
                if self.current_job:
                    if self in self.current_job.assigned_pops:
                        self.current_job.assigned_pops.remove(self)
                self.current_job = best_job
                best_job.assigned_pops.append(self)
                print(f"The entire pop '{self.name}' migrated to job '{best_job.title}' with wage {best_job.wage}")
                return self
        else:
            print(f"Pop '{self.name}' did not find a better job offer.")
        return self
    


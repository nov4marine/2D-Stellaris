class Colony:
    """mega class to represent an inhabited world"""
    def __init__(self, planet, type, habitability, land_area, owner, name, market, initial_population, initial_homeworld=False):
        self.planet = planet
        self.type = type
        self.habitability = habitability
        self.land_area = land_area
        self.owner = owner 
        self.name = name
        self.market = market
        self.colony_designation = None #Stellaris specialization
        self.initial_homeworld = initial_homeworld #is this the homeworld of the owner?
        self.initial_population = initial_population #initial pops to be generated upon colonization
        self.planet_modifiers = {} #dictionary for planet-wide modifiers e.g. {"industrial edict": 1.2}

        #these are central registries to track the economic units of the colony
        self.colony_pops = [] #list of all pops in on this world
        self.colony_buildings = [] #list of all buildings on this world
        self.colony_jobs = [] #list of all jobs on this world
        # labor_market_pressure = jobseekers / job openings #This might be implemented on a per planet or per job basis. dont forget to add the function to calculate it 

        self.construction_queue = [] #List of buildings under construction

        self.unrest = 0
        self.gdp = 0
        self.construction_points = 0
        self.deficits = 0
        self.output = 0
        self.unemployed = 0
        self.local_bank = None

        self.colony_setup = self._colony_setup()

    def _colony_setup(self):
        """method to generate initial buildings and pops upon colonization. Will later be customized to use species and building types"""
        if self.initial_homeworld:
            # Generate initial buildings
            self.colony_buildings.append(MiningBuilding(self, levels=3))
            self.colony_buildings.append(EnergyBuilding(self, levels=3))
            self.colony_buildings.append(FarmBuilding(self, levels=3))
            self.colony_buildings.append(CityDistrict(self, levels=3))
            self.colony_buildings.append(ResearchLab(self))
            self.colony_buildings.append(ConsumerGoodsFactory(self))
            self.colony_buildings.append(AlloyFoundry(self))
            self.colony_buildings.append(AdministrativeBuilding(self))
            self.colony_buildings.append(HoloTheater(self))

            # Generate initial pops
            pop = Pop(
                colony=self,
                pop_type="Human",
                size=self.initial_population,
                profession=None,  # No profession assigned at the start
                needs={"Food": 2, "Consumer Goods": 1},  # Example needs
                income=0,  # Initial income is zero
            )
            self.colony_pops.append(pop)
        
        else:
            # Generate initial buildings
            self.colony_buildings.append(MiningBuilding(self))
            self.colony_buildings.append(EnergyBuilding(self))
            self.colony_buildings.append(FarmBuilding(self))
            self.colony_buildings.append(CityDistrict(self))

            # Generate initial pops
            pop = Pop(
                colony=self,
                pop_type="Human",
                size=self.initial_population,
                profession=None,  # No profession assigned at the start
                needs={"Food": 2, "Consumer Goods": 1},  # Example needs
                income=0,  # Initial income is zero
            )
            self.colony_pops.append(pop)

    def progess_construction(self):
        """method to iterate through the construction queue"""
        completed_buildings = []
        for item in self.construction_queue:
            if self.construction_points > 0 and item["remaining_cost"] > 0:
                #deduct construction points from remaining cost, and time from time remaining
                construction_used = min(self.construction_points, item["remaining_cost"])
                item["remaining_cost"] -= construction_used
                self.construction_points -= construction_used
                item["remaining_time"] -= 30
            if item["remaining_time"] <= 0 and item["remaining_cost"] <= 0:
                completed_buildings.append(item)
        
        for item in completed_buildings:
            self.construction_queue.remove(item)
            building = item["building"]
            funder = item["funder"]

            existing_building = next((b for b in self.colony_buildings if b.name == building.name), None)
            if existing_building:
                # Add a level to the existing building
                existing_building.add_level(funder)
                print(f"Added a level to {existing_building.name} on {self.name}, funded by {funder}.")
            else:
                # Create a new instance of the building and add it to the colony
                self.colony_buildings.append(building)
                building.add_level(funder)  # First level is added here
                print(f"Constructed a new {building.name} on {self.name}, funded by {funder}.")       

    def queue_construction(self, building, funder):
        self.construction_queue.append({
            "building": building,
            "remaining_time": building.construction_time,
            "remaining_cost": building.construction_cost,
            "funder": funder
        })

    def replace_building(self, old_building_name, new_building):
        """Replace an existing building with a new one."""
        old_building = next((b for b in self.colony_buildings if b.name == old_building_name), None)
        if old_building:
            self.colony_buildings.remove(old_building)
            self.colony_buildings.append(new_building)
            print(f"Replaced {old_building_name} with {new_building.name} on {self.name}.")
        else:
            print(f"No building named {old_building_name} found on {self.name}.")

    def delevel_building(self, building, levels):
        """Destroys levels of a building, either by demolition or war."""
        for b in self.colony_buildings:
            if b.name == building.name:
                # Reduce levels, but ensure they don't go below 0
                b.levels = max(0, b.levels - levels)
                return  # Exit the loop once the building is found and modified
        print(f"No building named {building.name} found on {self.name}.")

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


class Building:
    def __init__(self, name, building_type, construction_cost, construction_time, upkeep, input_goods, output_goods, jobs, efficiency=1.0, levels=0, land_size=None, colony=None):
        self.name = name
        self.colony = colony
        self.type = building_type
        self.construction_cost = construction_cost
        self.construction_time = construction_time
        self.upkeep = upkeep
        self.land_size = land_size
        self.input_goods = input_goods  # Example: {"minerals": 20}
        self.output_goods = output_goods  # Example: {"steel": 10}
        self.jobs = jobs #the profession that the building hires. Might change to be more than 1 later. 
        self.efficiency = efficiency
        self.levels = levels
        self.revenue = 0
        self.expenses = 0
        self.profit = 0
        self.cash_reserves = 0
        self.dividends = 0
        self.ownership = {"total": 0, "private": 0, "government": 0, "workers": 0}

    def add_level(self, funder):
        """Add an additional level of the building, owned by the funder"""
        self.levels += 1
        self.ownership[funder] += 1
        self.ownership["total"] += 1

    def operate(self, market):
        #reset for the tick
        self.expenses = 0
        self.revenue = 0
        self.profit = 0
        self.dividends = 0

        # Buy inputs and add cost of all inputs to expenses
        for good, quantity in self.input_goods.items():
            total_inputs = quantity * self.efficiency * self.levels
            self.expenses += market.buy_good(good, total_inputs)

        # Sell outputs and add cost of all outputs to revenue
        for good, quantity in self.output_goods.items():
            total_outputs = quantity * self.efficiency * self.levels
            self.revenue += market.sell_good(good, total_outputs)

    def calculate_profit(self):
        """calculate profit from revenue and expenses. dip into or subtract from cash reserves as needed"""
        self.profit = self.revenue - self.expenses
        if self.profit <= 0:
            self.cash_reserves += self.profit #if profit is negative, subtract from cash reserves
        if self.profit > 0:
            if self.cash_reserves < 1000:
                self.cash_reserves += (self.profit / 2)
                self.dividends += (self.profit / 2)
            if self.cash_reserves >= 1000:
                self.dividends += self.profit
                
    def pay_dividends(self):
            #determine relative share of dividends for each owner using "levels owned/total levels"
            if self.ownership["total"] == 0:
                raise ValueError("Total ownership cannot be zero")
            investor_share = self.dividends * (self.ownership["private"] / self.ownership["total"])
            government_share = self.dividends * (self.ownership["government"] / self.ownership["total"])
            worker_share = self.dividends * (self.ownership["workers"] / self.ownership["total"])

            #publish the above info for higher classes to fetch
            return {"investors": investor_share, "government": government_share, "workers":worker_share}
            
    def calculate_payouts(self):
        """
        Pay workers based on wages, using cash reserves if revenue is insufficient.
        """
        payouts = {}
        total_wages = 0

        # Step 1: Calculate total wages owed.
        for job in self.jobs:
            for pop in job.assigned_pops:
                total_wages += job.wage * pop.size

        # Step 2: Pay wages from revenue and reserves.
        if self.revenue + self.cash_reserves >= total_wages:
            # Full payment scenario: Pay each worker their full wage.
            for job in self.jobs:
                for pop in job.assigned_pops:
                    payout = job.wage * pop.size
                    payouts[pop.profession] = payouts.get(pop.profession, 0) + payout
                    pop.income += payout  # Update pop's income attribute directly
            # Update cash reserves after payment.
            self.expenses +=  total_wages
        else:
            # Insufficient funds scenario: Pay proportionally to available funds.
            available_funds = self.revenue + self.cash_reserves
            proportion = available_funds / total_wages  # Fraction of wages that can be paid.
            for job in self.jobs:
                for pop in job.assigned_pops:
                    payout = (job.wage * pop.size) * proportion
                    payouts[pop.name] = payouts.get(pop.name, 0) + payout
                    pop.income += payout  # Update pop's income attribute directly
            # Deplete cash reserves entirely.
            self.cash_reserves = 0

        # Return the payouts dictionary (optional tracking or logging).
        return payouts

    def share_profit(self):
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
    """jobs on a colony, referencing their parent building. This class represents a job title defined by the employer."""
    def __init__(self, profession, wage, max_positions, building=None):
        self.profession = profession #profession for this job
        self.wage = wage #wage is the pay of this job
        self.building = building
        self.max_positions = max_positions #total number of employees for this job
        self.assigned_pops = [] #list of pops employed in this job 
        self.qualifications = {}

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
            key = (pop.profession, pop.pop_type)
            if key in consolidated:
                consolidated[key].size += pop.size
            else:
                # Create a new Pop instance as the basis of consolidation.
                consolidated[key] = Pop(pop.colony, pop.pop_type, pop.size, profession=self, needs=pop.needs, income=pop.income, current_job=self)
        # Replace the assigned pops list with the consolidated pops.
        self.assigned_pops = list(consolidated.values())

    def adjust_wage(self, labor_market_pressure, min_wage=1):
        """raise or cut wages of your employees based on the conditions of the labor market"""
        if labor_market_pressure > 1.1:
            self.wage *= 1.05  # Increase wage by 5%
        elif labor_market_pressure < 0.9:
            self.wage = max(self.wage * 0.95, min_wage)  # Decrease wage by 5%
    
class Pop:
    def __init__(self, colony, pop_type, size, profession, needs, income, current_job=None):
        self.colony = colony
        self.pop_type = pop_type
        self.size = size
        self.workforce_ratio = 0.5 #default workforce ratio, can be modified by traits or buildings
        self.profession = profession
        self.needs = needs  # Example: {"food": 5, "consumer_goods": 2}
        self.happiness = 100
        self.income = income
        self.current_job = current_job #reference to the job this pop is assigned to
        self.education = 1
        self.wage = self.income / self.size
        self.wealth = 0
        self.political_power = 0
        self.political_affiliation = {} # dictionary of interest groups and the percentage of the pop that belongs to them
        self.movement_affiliation = {} # dictionary of political movements and the percentage of the pop that belongs to them
        self.religion = None

    def calculate_wealth(self):
        """calculate wealth from income and size"""
        # Example: Wealth could be a function of income and size.
        self.wealth = self.wage ** 2 

    def calculate_political_power(self):
        """calculate base political power from wealth (and votes if applicable)"""
        # Example: Political power could be a function of income and size.
        self.political_power = self.income / self.size 

    def consume_goods(self, market):
        for good, quantity in self.needs.items():
            market.buy_good(self, good, (quantity * self.size))

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
    
############################################################################
#now the actual buildings and jobs for the colony
############################################################################    

# With the help of chatgpt, I have come up with a formula for balancing capital and labor intensity:

# For a building:
# total_investment = construction_cost + (upkeep * N_ticks) + (sum(input_goods.values()) * N_ticks)
# labor_investment = jobs * wage * N_ticks

# Capital-to-labor ratio (K/L)
# capital_intensity = total_investment / max(labor_investment, 1)

# Profit per tick (simplified)
# profit_per_tick = (output_value - input_cost - upkeep - total_wages)

# Gonna initially aim for 5 million workers per building level
# Also Gonna initially aim to just copy Stellaris, and add my own flavor as we go.
# When in doubt, use Labor Theory of Value
# Stellaris Buildings: 
    # Tier 1: upkeep 2, time 360, minerals 400
    # Tier 2: upkeep 5 + 1 rare, time 480, minerals 600 + 50 rare
    # Tier 3: upkeep 8 + 2 rare, time 600, minerals 800 + 100 rare

    # districts: upkeep 1, time 240, minerals 300

#input and output goods should be a list of dictionaries
# Remember to convert upkeep cost from energy credits to construction points later

# district buildings
class MiningBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name = "Mining District",
            building_type = "District",
            construction_cost = 300,
            construction_time = 240,
            upkeep = 1,
            input_goods = {},
            output_goods = {"Minerals": 4},
            jobs = [Job("Miner", 100, 5000000)],  # 5 million miners at a wage of $100 per idk amount of time
            levels = levels,
            colony = colony,
        )

class EnergyBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Energy District",
            building_type="District",
            construction_cost=300,
            construction_time=240,
            upkeep=1,
            input_goods={},  # No inputs required for energy production
            output_goods={"Energy Credits": 6},  # Produces 6 energy credits per tick
            jobs=[Job("Technician", 120, 5000000)],  # 5 million technicians at $120 wage
            levels=levels,
            colony=colony,
        )

class FarmBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Farm District",
            building_type="District",
            construction_cost=300,
            construction_time=240,
            upkeep=1,
            input_goods={},  # No inputs required for food production
            output_goods={"Food": 4},  # Produces 4 food per tick
            jobs=[Job("Farmer", 100, 5000000)],  # 5 million farmers at $100 wage
            levels=levels,
            colony=colony,
        )

class CityDistrict(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="City District", #or urban center
            building_type="District",
            construction_cost=300,
            construction_time=240,
            upkeep=1,
            input_goods={},
            output_goods={"Housing": 5}, #later will add services production
            jobs=[Job("Urban Worker", 110, 5000000)],  # 5 million urban workers at $110 wage
            levels=levels,
            colony=colony,
        )

# industrial and urban tier 1 buildings

class ResearchLab(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Research Lab",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Consumer Goods": 2},
            output_goods={"Research Points": 10},
            jobs=[Job("Scientist", 150, 5000000)],  # 5 million scientists at $150 wage
            levels=levels,
            colony=colony,
        )

class ConsumerGoodsFactory(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Consumer Goods Factory",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Minerals": 6},
            output_goods={"Consumer Goods": 6},
            jobs=[Job("Factory Worker", 120, 5000000)],  # 5 million factory workers at $120 wage
            levels=levels,
            colony=colony,
        )

class AlloyFoundry(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Alloy Foundry",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Minerals": 6},
            output_goods={"Alloys": 3},
            jobs=[Job("Metal Worker", 130, 5000000)],  # 5 million metal workers at $130 wage
            levels=levels,
            colony=colony,
        )


class AdministrativeBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Administrative Building",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Consumer Goods": 2},
            output_goods={"Unity": 4},
            jobs=[Job("Bureaucrat", 150, 5000000)],  # 5 million Bureacrats at $150 wage
            levels=levels,
            colony=colony,
        )

class HoloTheater(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="HoloTheater",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Consumer Goods": 1},
            output_goods={"Amenities": 10},  # Produces happiness
            jobs=[Job("Entertainment Worker", 120, 5000000)],  # 5 million entertainment workers at $120 wage
            levels=levels,
            colony=colony,
        )

class HydroponicsFarm(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Hydroponics Farm",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Energy": 4},
            output_goods={"Food": 6},
            jobs=[Job("Hydroponics Technician", 130, 5000000)],  # 5 million hydroponics technicians at $130 wage
            levels=levels,
            colony=colony,
        )

class HealthcareBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Healthcare Building",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods={"Consumer Goods": 1},
            output_goods={"Health Services": 10}, # in stellaris, output is 4 amenities, 5% growth, and 2.5% habitability
            jobs=[Job("Healthcare Worker", 140, 5000000)],  # 5 million healthcare workers at $140 wage
            levels=levels,
            colony=colony,
        )

class RobotAssemblyPlant(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Robot Assembly Plant",
            building_type="Urban",
            construction_cost=600,
            construction_time=360,
            upkeep=5,
            input_goods={"Alloys": 2},
            output_goods={"Robots": 2},  # Produces 2 growth points per tick towards robots
            jobs=[Job("Robot Technician", 150, 5000000)],  # 5 million robot technicians at $150 wage
            levels=levels,
            colony=colony,
        )

class PoliceBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Police Building",
            building_type="Urban",
            construction_cost=400,
            construction_time=360,
            upkeep=2,
            input_goods=None,  # No inputs required for police building
            output_goods={"Crime": -25},  # Reduces crime by 25%
            # In Stellaris, each enforcer produces 1 stability, -25 crime, and 2 defense army
            jobs=[Job("Police Officer", 130, 5000000)],  # 5 million police officers at $130 wage
            levels=levels,
            colony=colony,
        )

#special resource buildings

class Refinery(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Refinery",
            building_type="Urban",
            construction_cost=500,
            construction_time=480,
            upkeep=3,
            input_goods={"Minerals": 10},
            output_goods={"Refined Goods": 2},  # Produces 4 refined strategic resources
            jobs=[Job("Refinery Worker", 120, 5000000)],  # 5 million refinery workers at $120 wage
            levels=levels,
            colony=colony,
        )

class HarvesterBuilding(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Harvester Building",
            building_type="Urban",
            construction_cost=200,
            construction_time=360,
            upkeep=1,
            input_goods=None,  # No inputs required for harvester building
            output_goods={"Refined Goods": 2},  # Produces 2 exotic gas
            jobs=[Job("Gas Harvester", 120, 5000000)],  # 5 million gas harvesters at $120 wage
            levels=levels,
            colony=colony,
        )

# Specialization buildings

class ResearchInstitute(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Research Institute",
            building_type="Specialization",
            construction_cost=600,
            construction_time=480,
            upkeep=5,
            input_goods={"Consumer Goods": 2}, #also 1 exotic gas
            output_goods={"Research Points": 1.15},  # 15% more research points from planet output
            jobs=[Job("Senior Researcher", 200, 5000000)],  # 5 million senior researchers at $200 wage
            levels=levels,
            colony=colony,
        )

# military buildings    

class NavalBase(Building):
    def __init__(self, colony, levels=1):
        super().__init__(
            name="Naval Base",
            building_type="Urban",
            construction_cost=400,
            construction_time=240,
            upkeep=2,
            input_goods=None,  # No inputs required for naval base
            output_goods={"Manpower": 5000000},  # Produces 5 million manpower
            # In Stellaris, soldiers each produce 4 naval cap, 0.25 stability, and 3 defense army
            jobs=[Job("Naval Officer", 200, 5000000)],  # 5 million naval officers at $200 wage
            levels=levels,
            colony=colony,
        )
# This file will house all things directly related to the economy model. Unless it gets too long.
#Each good is a dictionary, unless it needs to be modelled as a class later. They don't really do much tho.
class Market:
    def __init__(self, owner):
        self.owner = owner
        # List of goods as dictionaries
        self.goods = []  # (list of dictionaries) Example: [{"name": "food", "base_price": 10, "supply": 100, "demand": 80}]
        self.national_ledger = 0  # Optional: Track total wealth in the market

    def add_good(self, name, category, base_price):
        # Add a new good to the market
        good = {
            "name": name,
            "category": category,
            "base_price": base_price,
            "current_price": base_price,
            "supply": 0,
            "demand": 0
        }
        self.goods.append(good)

    def get_good(self, name):
        # Find a good by name
        for good in self.goods:
            if good["name"] == name:
                return good
        return None

    def update_prices(self, k=1.5, price_min=0.5, price_max=2.0):
        # Update prices for all goods
        for good in self.goods:
            if good["demand"] > 0:
                sdr = good["supply"] / good["demand"]
            else:
                sdr = 1

            # Continuous price formula
            new_price = good["base_price"] * (sdr ** -k)
            good["current_price"] = max(price_min * good["base_price"], min(new_price, price_max * good["base_price"]))

            #reset supply and demand for next update. also log it to track stats just prior to this
            good["supply"] = 0 
            good["demand"] = 0

    def buy_good(self, name, quantity):
        # Buyer purchases goods
        good = self.get_good(name)
        buy_price = good["current_price"] * quantity
        good["demand"] += quantity
        return buy_price

    def sell_good(self, name, quantity):
        # Seller adds goods to the market
        good = self.get_good(name)
        sell_price = good["current_price"] * quantity
        good["supply"] += quantity
        return sell_price
    

class Bank:
    """hypothetical bank class to manage deposits and loans, shoud I ever decide to add a banking system."""
    def __init__(self, base_interest_rate=0.03, initial_capital=1_000_000):
        self.base_interest_rate = base_interest_rate  # a starting baseline
        self.deposits = 0.0   # Total deposits held
        self.loans = 0.0      # Total outstanding loans
        self.available_capital = initial_capital  # a buffer the bank holds
        self.default_rate = 0.0  # Could be updated from simulated default events

    def register_deposit(self, amount: float):
        self.deposits += amount

    def register_loan(self, amount: float):
        self.loans += amount

    def compute_interest_rate(self):
        """
        Compute a dynamic interest rate emergently.
        
        For example:
          - If loan-to-deposit ratio (L/D) is higher than a target (say 1.0), 
            the bank tightens credit and raises its interest rate.
          - A risk or default premium could be added based on a simplistic default factor.
        """
        # Avoid division by zero; if no deposits, assume a tight credit market
        ld_ratio = self.loans / self.deposits if self.deposits > 0 else 1.5
        
        # A simplistic emergent formula:
        # Increase the rate if demands for credit are high (ld_ratio > 1).
        risk_premium = self.default_rate * 0.05  # This term can be tuned
        dynamic_rate = self.base_interest_rate + 0.1 * (ld_ratio - 1) + risk_premium
        
        # Ensure the rate doesn't go negative
        return max(dynamic_rate, 0.001)
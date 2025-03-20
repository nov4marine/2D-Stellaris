# This file will house all things directly related to the economy model. Unless it gets too long.

class Market:
    def __init__(self):
        # List of goods as dictionaries
        self.goods = []  # Example: [{"name": "food", "base_price": 10, "supply": 100, "demand": 80}]
        self.national_ledger = 0  # Optional: Track total wealth in the market

    def add_good(self, name, base_price, supply=0):
        # Add a new good to the market
        good = {
            "name": name,
            "base_price": base_price,
            "current_price": base_price,
            "supply": supply,
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
                sdr = good["current price"]

            # Continuous price formula
            new_price = good["base_price"] * (sdr ** -k)
            good["current_price"] = max(price_min * good["base_price"], min(new_price, price_max * good["base_price"]))

    def buy_good(self, buyer, name, quantity):
        # Buyer purchases goods
        good = self.get_good(name)
        if good and good["supply"] >= quantity:
            cost = good["current_price"] * quantity
            if buyer.wealth >= cost:
                buyer.wealth -= cost
                good["supply"] -= quantity
                good["demand"] += quantity
                return True
        return False

    def sell_good(self, seller, name, quantity):
        # Seller adds goods to the market
        good = self.get_good(name)
        if good:
            revenue = good["current_price"] * quantity
            seller.wealth += revenue
            good["supply"] += quantity
            return True
        return False

class Pop:
    def __init__(self, pop_type, size, wealth, needs):
        self.type = pop_type
        self.size = size
        self.wealth = wealth
        self.needs = needs  # Example: {"food": 5, "consumer_goods": 2}
        self.happiness = 100

    def consume_goods(self, market):
        for good, quantity in self.needs.items():
            if market.buy_good(self, good, quantity):
                continue
            else:
                self.happiness -= 10  # Penalize unmet needs


class Building:
    def __init__(self, name, building_type, input_goods, output_goods, efficiency=1.0):
        self.name = name
        self.type = building_type
        self.input_goods = input_goods  # Example: {"minerals": 20}
        self.output_goods = output_goods  # Example: {"steel": 10}
        self.efficiency = efficiency

    def operate(self, market):
        # Buy inputs
        for good, quantity in self.input_goods.items():
            if not market.buy_good(self, good, quantity * self.efficiency):
                return False  # Stop if inputs are insufficient

        # Sell outputs
        for good, quantity in self.output_goods.items():
            market.sell_good(self, good, quantity * self.efficiency)
        return True

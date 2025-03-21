# This file will house all things directly related to the economy model. Unless it gets too long.

class Market:
    def __init__(self, owner):
        self.owner = owner
        # List of goods as dictionaries
        self.goods = []  # Example: [{"name": "food", "base_price": 10, "supply": 100, "demand": 80}]
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
    
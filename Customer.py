class Customer:
    def __init__(self, demand, location):
        self.demand_ = demand
        self.location_ = location

    def demand(self):
        return self.demand_

    def location(self):
        return self.location_

class Facility:
    def __init__(self, buildCost, capacity, location):
        self.buildCost_ = buildCost
        self.capacity_ = capacity
        self.location_ = location

    def location(self):
        return self.location_

    def capacity(self):
        return self.capacity_

    def buildCost(self):
        return self.buildCost_


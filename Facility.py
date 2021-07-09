class Facility:
    def __init__(self, buildCost_, capacity_, location_, index_):
        self.buildCost = buildCost_
        self.capacity = capacity_
        self.location = location_
        self.index = index_
        self.facility_customers = []
        self.is_open = False


# a representation of a delivery truck
# uses a list of packages to represent its cargo bay
# holds its current_location and a clock to track its progress
class Truck:

    def __init__(self, new_number, new_clock, new_location):
        self.number = new_number
        self.clock = new_clock
        self.current_location = new_location
        self.speed = 18
        self.capacity = 16
        self.cargo = []
        self.mileage = 0
        self.full = False


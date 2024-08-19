# a collection of methods used to load data in from csv files
import csv
from graph import Location
from package_hash_table import *

# loads the package data from the packages csv file
# returns hash table with the package data
def package(file):
    packages = HashTable()

    with open(file) as package_csv:
        package_data = csv.reader(package_csv, delimiter=',')
        next(package_data)

        for package in package_data:
            package_id = package[0]
            address = package[1]
            city = package[2]
            zip_code = package[3]
            deadline = package[4]
            mass = package[5]
            status = "at hub"

            next_package = Package(int(package_id), address, city, zip_code, deadline, mass, status)

            packages.insert(next_package.package_id, next_package)

        return packages

# loads the location data from the locations csv file
# returns dictionary with the location data ('address' : Location)
def location(file):
    locations = {}
    with open(file) as location_csv:
        location_data = csv.reader(location_csv, delimiter=',')
        next(location_data) #skip header

        for loc in location_data:
            address = loc[0]
            locations[address] = Location(address)

        return locations

# loads the distance data from the distances csv file
# returns a list of tuples in the form of [(starting_location, ending_location, distance between the 2 locations)]
def distance(file ,locations):
    distances = []

    with open(file) as distance_csv:
        distance_data = csv.reader(distance_csv, delimiter=',')
        next(distance_data) #skip header

        for dist in distance_data:

            # gets the appropriate object references from the location dictionary
            from_location = locations[dist[0]]
            to_location = locations[dist[1]]

            # string to float
            distance = float(dist[2])

            # (Location, Location, float)
            distances.append((from_location, to_location, distance))

        return distances

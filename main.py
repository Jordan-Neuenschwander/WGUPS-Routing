# Jordan Neuenschwander
# ID: 001043915
# 8/25/2021

import datetime
import load
from truck import *
from datetime import *
from graph import *
import copy


# returns the miles between 2 locations
# O(1), lookup in a hash table
def distance_between(from_location, to_location):
    # if the locations are the same return a large distance value to effectively ignore loops in the graph
    if from_location == to_location:
        return 9999
    return graph.distances[from_location, to_location]


# fill the cargos of truck 1 and 2
# the packages were chosen to meet the delivery deadlines and the requirements of the special notes
# packages with the same destination are loaded together
# minimal attention was given to the general proximity of all the loaded packages
# having nearby neighbor
# O(n), n being packages in the trucks cargo
def load_trucks():

    # Load truck_1
    truck_1.cargo.append(packages.search(25))
    truck_1.cargo.append(packages.search(26))
    truck_1.cargo.append(packages.search(6))
    truck_1.cargo.append(packages.search(1))
    truck_1.cargo.append(packages.search(2))
    truck_1.cargo.append(packages.search(4))
    truck_1.cargo.append(packages.search(40))
    truck_1.cargo.append(packages.search(22))
    truck_1.cargo.append(packages.search(17))
    truck_1.cargo.append(packages.search(11))
    truck_1.cargo.append(packages.search(12))
    truck_1.cargo.append(packages.search(23))
    truck_1.cargo.append(packages.search(24))
    truck_1.cargo.append(packages.search(32))
    truck_1.cargo.append(packages.search(33))
    truck_1.cargo.append(packages.search(31))

    for p1 in truck_1.cargo:
        p1.status = 'on truck #1'
        p1.loaded_at = truck_1.clock.time()

    # Load truck_2
    truck_2.cargo.append(packages.search(13))
    truck_2.cargo.append(packages.search(15))
    truck_2.cargo.append(packages.search(19))
    truck_2.cargo.append(packages.search(39))
    truck_2.cargo.append(packages.search(16))
    truck_2.cargo.append(packages.search(34))
    truck_2.cargo.append(packages.search(14))
    truck_2.cargo.append(packages.search(30))
    truck_2.cargo.append(packages.search(5))
    truck_2.cargo.append(packages.search(37))
    truck_2.cargo.append(packages.search(38))
    truck_2.cargo.append(packages.search(10))
    truck_2.cargo.append(packages.search(7))
    truck_2.cargo.append(packages.search(29))
    truck_2.cargo.append(packages.search(20))
    truck_2.cargo.append(packages.search(21))
    truck_2.full = True

    for p2 in truck_2.cargo:
        p2.status = 'on truck #2'
        p2.loaded_at = truck_2.clock.time()


# fill the cargo of truck 2 for its second run
# these are the remaining packages, mostly ones that were required to be on truck_2 and are not in very close proximity
# O(n), n being packages in the trucks cargo
def load_truck2():

    truck_2.cargo.append(packages.search(3))
    truck_2.cargo.append(packages.search(8))
    truck_2.cargo.append(packages.search(9))
    truck_2.cargo.append(packages.search(18))
    truck_2.cargo.append(packages.search(27))
    truck_2.cargo.append(packages.search(28))
    truck_2.cargo.append(packages.search(35))
    truck_2.cargo.append(packages.search(36))

    for package in truck_2.cargo:
        package.status = 'on truck #2'
        package.loaded_at = truck_2.clock.time()


# uses the nearest neighbor algorithm to traverse the graph and deliver packages
# delivers all the packages in truck's cargo
# O(c²+v) c = packages in the truck’s cargo 	v = vertexes in the graph
def deliver(truck):
    while truck.cargo:

        # get the package that has the closest destination
        destination = next_delivery(truck.cargo, truck.current_location)
        next_stop = destination[0]
        distance = destination[1]

        #  add how long this delivery takes to the clock
        minutes_taken = (distance / (truck.speed / 60))
        truck.clock += timedelta(minutes=minutes_taken)

        # add the distance driven to the trucks odometer
        truck.mileage += distance

        # logs the mileage change so we can audit mileage by time (time, miles driven)
        total_mileage.append((truck.clock.time(), distance))

        # set the truck current location to the package delivery point
        truck.current_location = next_stop

        # holds packages that have been delivered to this location
        remove_packages = []

        # find packages that get delivered at this address
        for p in truck.cargo:
            if p.address == next_stop.address:
                p.status = 'delivered {0} by truck_{1}'.format(truck.clock.time(), truck.number)
                p.delivered_at = truck.clock.time()
                remove_packages.append(p)

        # remove the packages from truck cargo
        for p in remove_packages:
            truck.cargo.remove(p)

    # Runs when the cargo is empty and all packages have been delivered
    # Computes the mileage and time taken to return to the hub
    distance = distance_between(truck.current_location, locations['4001 South 700 East'])

    minutes_taken = (distance / (truck.speed / 60))
    truck.mileage += distance

    truck.clock += timedelta(minutes=minutes_taken)
    total_mileage.append((truck.clock.time(), distance))

    # truck has returned to the hub
    truck.current_location = locations['4001 South 700 East']


# version of the nearest neighbor algorithm
# finds the package in the truck's cargo with the closest delivery address to the current_location
# O(n)
def next_delivery(cargo, current_location):
    min_distance = float('inf')
    min_location = None
    # loop until the min distance is found and store the location
    for p in cargo:
        if distance_between(current_location, locations[p.address]) < min_distance:
            min_distance = distance_between(current_location, locations[p.address])
            min_location = locations[p.address]

    # (Location, float)
    return min_location, min_distance


# reads a log of mileage and returns total mileage driven at a given time
# O(n)
def get_miles(miles_search_time):
    mileage = 0

    # entry is a tuple of a timestamp and miles driven (timestamp, miles driven)
    for entry in total_mileage:
        time_entry = entry[0]

        # if miles were logged before search_time then add the logged miles to the total mileage
        if time_entry < miles_search_time:
            mileage += entry[1]

    return mileage


# creates a snapshot of the packages hash table at a given time
# O(n)
def get_packages(package_search_time):
    report = copy.deepcopy(packages)

    for i in range(1, 41):
        p = report.search(i)
        delivery_time = p.delivered_at
        loaded_time = p.loaded_at

        # if package has been delivered by search_time then leave the status as delivered
        if delivery_time <= package_search_time:
            continue

        # if package has been loaded but not delivered by search_time then its en route
        elif loaded_time <= package_search_time:
            p.status = 'en route'

        # if package has not been loaded nor delivered by search_time then its at the hub
        elif loaded_time > package_search_time and delivery_time > package_search_time:
            p.status = 'at hub'

    return report


# counts the number of packages that were delivered by their deadline
# O(n)
def on_time():
    delivered_on_time = 0
    for i in range(1, 41):
        p = packages.search(i)

        if p.deadline == 'EOD':
            deadline = '17:00'
        else:
            deadline = p.deadline

        deadline = datetime.strptime(deadline, '%H:%M').time()

        if deadline > p.delivered_at:
            delivered_on_time += 1

    if delivered_on_time == 40:
        return 'ALL'
    else:
        return 'NOT ALL'


# prints a report detailing the status of packages and the total mileage driven at a given time
# printed report can be copied into a text file and opened as a csv in excel using the | as the delimiter
def print_report(report_time_input):
    # convert user input string into datetime.time object
    report_time = datetime.strptime(report_time_input, '%H:%M')
    report_time = report_time.time()


    print('==================================================================')
    print('                   Package Report for {0}'.format(report_time))
    print('==================================================================')

    # total miles driven by both trucks at search_time
    print('TOTAL MILEAGE = {0} miles'.format(get_miles(report_time)))

    # get the state of the package hash table at search_time
    report_packages = get_packages(report_time)

    # print the package report
    print('ID |      Address      |     City     | Zip Code | Deadline | Weight | Status')
    for i in range(1, 41):
        p = report_packages.search(i)

        # package_id == 9 receives a new address at 10:20
        if p.package_id == 9 and report_time > datetime.strptime('10:20', '%H:%M').time():
            p.address = '410 S State St'

        print('{0} | {1} | {2} | {3} | {4} | {5} | {6}'.format(p.package_id, p.address, p.city, p.zip_code, p.deadline, p.mass, p.status))

    print('')


## START OF MAIN ##


# uses methods in the load namespace to load data in from the csv files

# dictionary of locations ('address': Location)
locations = load.location('locations.csv')

# custom hash table filled with packages (package_id: Package)
packages = load.package('packages.csv')

# a list of tuples containing 2 Locations and distance between them [(from_location, to_location, distance)]
distances = load.distance('distances.csv', locations)

# custom graph data structure
graph = Graph()

# add all the locations to the graph as vertices
for location in locations.items():
    graph.add_location(location[1])

# create all the edges between the vertices
for line in distances:
    graph.add_line(line[0], line[1], line[2])

# create the trucks, initialize their clocks to their start times and their starting location to the hub
# truck 1 waits for the airline packages at 9:05 and then leaves
truck_1 = Truck(1, datetime(2021, 1, 1, 9, 5), locations['4001 South 700 East'])
truck_2 = Truck(2, datetime(2021, 1, 1, 8), locations['4001 South 700 East'])

# list of tuples [(timestamp, miles driven)
total_mileage = []

# fill both truck's cargo with packages
load_trucks()

# deliver the packages
deliver(truck_1)
deliver(truck_2)

# truck 2 gets back to the hub sometime before 9:50, wait until 10:20
truck_2.clock = datetime(2021, 1, 1, 10, 20)

# package id 9 gets new address @ 10:20
package = packages.search(9)
package.address = '410 S State St'

# put the remaining packages into truck 2
load_truck2()

# deliver the packages
deliver(truck_2)

# all packages have now been delivered

# menu for user input
isExit = True
while isExit:

    print('1. Package and Mileage Report')
    print('2. End of Day Totals')
    print('3. Exit')
    option = input("Choose an option (1, 2, 3): ")
    if option == '1':
        print('')
        search_time = input("Enter the time of the report (HH:MM): ")
        print_report(search_time)
    elif option == '2':
        print('')
        print("Total Miles Driven: {0}".format(truck_1.mileage + truck_2.mileage))

        print("Packages delivered on time:  {0}".format(on_time()))

        print("Truck 1 finished its day at: {0}".format(truck_1.clock.time()))
        print("Truck 2 finished its day at: {0}".format(truck_2.clock.time()))
    elif option == '3':
        isExit = False
    else:
        print('Invalid Choice')
        print('')

    search_time = None
    print('')

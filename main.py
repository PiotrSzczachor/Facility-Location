from Customer import Customer
from Facility import Facility
import math
import numpy as np
import random


# Making numpy array with with distance between facilities (rows) and customers (columns)
def np_distance_array():
    array = np.zeros((facilities_amount, customers_amount))
    for i in range(0, facilities_amount):
        for j in range(0, customers_amount):
            array[i][j] = distance(facilities[i], customers[j])
    return array


# Calculating whole cost of the solution
def calculating_cost():
    cost = 0.0
    for customer_ in customers:
        cost += distance(customer_, customer_.assigned_facility)
    for facility_ in facilities:
        if facility_.is_open:
            cost += facility_.buildCost
    return cost


# Assigning customer to the closest allowed facility without looking at it's open cost
def greedy_assignment(not_allowed):
    solution = []
    for i in range(0, customers_amount):
        solution.append(-1)
    for customer_index in range(0, customers_amount):
        is_feasible = False
        min_distance = np.inf
        min_index = -1
        for facility_index in range(0, facilities_amount):
            cond_1 = dist_array[facility_index][customer_index] < min_distance
            cond_2 = customers[customer_index].demand <= facilities[facility_index].free_capacity
            cond_3 = facilities[facility_index] not in not_allowed
            if cond_1 and cond_2 and cond_3:
                min_index = facility_index
                min_distance = dist_array[facility_index][customer_index]
                is_feasible = True
        # If we can't assign customer to any facility the solution is infeasible
        if not is_feasible:
            return np.inf, solution
        facilities[min_index].facility_customers.append(customers[customer_index])
        facilities[min_index].free_capacity -= customers[customer_index].demand
        facilities[min_index].is_open = True
        customers[customer_index].assigned_facility = facilities[min_index]
    for i in range(0, customers_amount):
        solution[i] = customers[i].assigned_facility.index
    objective = calculating_cost()
    return objective, solution


# Calculating distance between customer and facility
def distance(customer_, facility_):
    dist = math.dist(customer_.location, facility_.location)
    return dist


# Making neighborhood
def making_neighborhood():
    neighbors = []
    number_of_operations = facilities_amount
    opened_facilities = []
    closed_facilities = []
    for i in range(0, facilities_amount):
        if facilities[i].is_open:
            opened_facilities.append(facilities[i])
        else:
            closed_facilities.append(facilities[i])

    # Swapping random facilities (closed and opened)
    open_amount = len(opened_facilities)
    close_amount = len(closed_facilities)
    # We can swap only if there are some closed and opened facilities
    multiplier = random.randint(1, 3)
    for i in range(0, multiplier * number_of_operations):
        if close_amount != 0 and open_amount != 0:
            opened_index = random.randint(0, open_amount - 1)
            closed_index = random.randint(0, close_amount - 1)
            facility1 = opened_facilities[opened_index]
            facility2 = closed_facilities[closed_index]
            size = facility1.capacity - facility1.free_capacity
            if size <= facility2.capacity:
                facility1.is_open = False
                facility2.is_open = True
                facility2.facility_customers = facility1.facility_customers
                for custom in facility1.facility_customers:
                    custom.assigned_facility = facility2
                facility2.free_capacity = facility2.capacity - size
                facility1.free_capacity = facility1.capacity
                opened_facilities.remove(facility1)
                closed_facilities.remove(facility2)
                opened_facilities.append(facility2)
                closed_facilities.append(facility1)
            solution = []
            for i in range(0, customers_amount):
                solution.append(customers[i].assigned_facility.index)
            cost = calculating_cost()
            neighbors.append([cost, solution])

    # Sorting neighbors list from lowest to highest cost
    for i in range(0, len(neighbors)):
        for j in range(0, len(neighbors) - 1):
            if neighbors[j][0] > neighbors[j + 1][0]:
                tmp = neighbors[j][0]
                neighbors[j][0] = neighbors[j + 1][0]
                neighbors[j + 1][0] = tmp
    # print(neighbors)

    return neighbors


# Tabu search
def tabu_search(actually_solution, actually_cost):
    number_of_iterations = facilities_amount
    tabu_list = [actually_solution]
    curr_solution = actually_solution
    curr_cost = actually_cost
    best_sollution = actually_solution
    best_cost = actually_cost
    for i in range(0, number_of_iterations):
        neighbors = making_neighborhood()
        # Taking neighbor with smallest cost which is not in tabu list
        for j in range(0, len(neighbors)):
            if neighbors[j][1] not in tabu_list:
                curr_cost = neighbors[j][0]
                curr_solution = neighbors[j][1]
                tabu_list.append(curr_solution)
                break
        if curr_cost < best_cost:
            best_cost = curr_cost
            best_sollution = curr_solution

    return best_cost, best_sollution


# Solving the problem
def solve():
    starting_cost, starting_solution = greedy_assignment([])
    cost, solution = tabu_search(starting_solution, starting_cost)
    print(cost)
    print(solution)


# Reading input from file
customers = []
facilities = []

data = open("data/fl_16_1", "r")
data_list = data.readlines()

facilities_amount = 0
customers_amount = 0

j = 0
for i in range(0, 2):
    tmp = ""
    while data_list[0][j] != " ":
        if data_list[0][j] == "\n":
            break
        tmp += data_list[0][j]
        j += 1
    if i == 0:
        facilities_amount = int(tmp)
        j += 1
    else:
        customers_amount = int(tmp)

counter = 0
j = 0
for line in data_list:
    j += 1
    if line == data_list[0]:
        continue
    else:
        open_cost = 0
        cap = 0
        demand = 0
        location_x = 0.0
        location_y = 0.0
        location = []
        if j < facilities_amount + 2:
            k = 0
            for i in range(0, 4):
                tmp = ""
                while line[k] != " ":
                    if line[k] == "\n":
                        break
                    tmp += line[k]
                    k += 1
                if i == 0:
                    open_cost = float(tmp)
                    k += 1
                if i == 1:
                    cap = int(tmp)
                    k += 1
                if i == 2:
                    location_x = float(tmp)
                    k += 1
                if i == 3:
                    location_y = float(tmp)
                    location.append(location_x)
                    location.append(location_y)
                    k += 1
            facility = Facility(open_cost, cap, location, counter)
            facilities.append(facility)
            counter += 1
        else:
            k = 0
            for i in range(0, 3):
                tmp = ""
                while line[k] != " ":
                    if line[k] == "\n":
                        break
                    tmp += line[k]
                    k += 1
                if i == 0:
                    demand = int(tmp)
                    k += 1
                if i == 1:
                    location_x = float(tmp)
                    k += 1
                if i == 2:
                    location_y = float(tmp)
                    location.append(location_x)
                    location.append(location_y)
                    k += 1
            customer = Customer(demand, location)
            customers.append(customer)

data.close()

dist_array = np_distance_array()
solve()
# print(greedy_assignment([]))

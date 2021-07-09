from Customer import Customer
from Facility import Facility
import math
import numpy as np


def calculating_cost():
    cost = 0.0
    for customer_ in customers:
        cost += distance(customer_, customer_.assigned_facility)
    for facility_ in facilities:
        if facility_.is_open:
            cost += facility_.buildCost
    return cost


def starting_assignment():
    for customer_index in range(0, customers_amount):
        min_distance = np.inf
        min_index = -1
        for facility_index in range(0, facilities_amount):
            cond_1 = dist_array[facility_index][customer_index] < min_distance
            cond_2 = customers[customer_index].demand <= facilities[facility_index].capacity
            if cond_1 and cond_2:
                min_index = facility_index
                min_distance = dist_array[facility_index][customer_index]
        facilities[min_index].facility_customers.append(customers[customer_index])
        facilities[min_index].capacity -= customers[customer_index].demand
        facilities[min_index].is_open = True
        customers[customer_index].assigned_facility = facilities[min_index]


def distance(customer_, facility_):
    dist = math.dist(customer_.location, facility_.location)
    return dist


# Reading input from file

customers = []
facilities = []

data = open("data/fl_3_1", "r")
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

print(data_list)
print(facilities_amount)
print(customers_amount)

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
                    open_cost = int(tmp)
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
            print(open_cost, cap, location)
            facility = Facility(open_cost, cap, location, counter)
            facilities.append(facility)
            counter += 1
            print(facilities)
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
            print(demand, location)
            customer = Customer(demand, location)
            customers.append(customer)
            print(customers)
data.close()

# Making numpy array with with distance between facilities (rows) and customers (columns)

dist_array = np.zeros((facilities_amount, customers_amount))
for i in range(0, facilities_amount):
    for j in range(0, customers_amount):
        dist_array[i][j] = distance(facilities[i], customers[j])
print(dist_array)

tabu_list = []

starting_assignment()
for i in range(0, customers_amount):
    print(customers[i].assigned_facility.index)

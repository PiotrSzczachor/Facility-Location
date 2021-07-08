from Customer import Customer
from Facility import Facility
import math


def distance(customer, facility):
    dist = math.dist(customer.location_, facility.location_)
    return dist


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

print(data_list)
print(facilities_amount)
print(customers_amount)

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
            facility = Facility(open_cost, cap, location)
            facilities.append(facility)
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
# print(distance(c1, f1))

from pulp import *
from Customer import Customer
from Facility import Facility
from main import distance

customers = []
facilities = []

data = open("data/fl_16_2", "r")
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

# Creating variables 'y' (0, 1) for each facility which are representing if it is open or not

variables_y = []
for i in range(0, facilities_amount):
    var = LpVariable(f"y{i}", cat="Binary")
    variables_y.append(var)



variables_x = []
for i in range(0, facilities_amount):
    for j in range(0, customers_amount):
        number = str(i) + str(j)
        var = LpVariable(f"x{number}", cat="Binary")
        variables_x.append(var)

objective = 0
for i in range(0, facilities_amount):
    objective += facilities[i].buildCost * variables_x[i]

counter = 0
for i in range(0, facilities_amount):
    for j in range(0, customers_amount):
        objective += distance(customers[j], facilities[i]) * variables_x[counter]
        counter += 1

# Adding objective to problem

problem = LpProblem("Facility_location", LpMinimize)
problem += objective

# Demand constraint
starting_index = 0
for i in range(0, customers_amount):
    suma = 0
    index = starting_index
    for j in range(0, facilities_amount):
        suma += variables_x[index]
        index += customers_amount
    starting_index += 1
    problem += suma == customers[i].demand


# Capacity constraint
counter = 0
for i in range(0, facilities_amount):
    suma = 0
    for j in range(0, customers_amount):
        suma += variables_x[counter]
        counter += 1
    problem += suma <= facilities[i].capacity * variables_y[i]


for i in range(0, len(variables_x)):
    problem += variables_x[i] >= 0

suma = 0
for i in range(0, len(variables_y)):
    suma += variables_y[i]
problem += suma <= facilities_amount
problem += suma >= 0


print(problem.solve())

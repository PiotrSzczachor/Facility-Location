from Customer import Customer
from Facility import Facility
import math


def distance(customer, facility):
    dist = math.dist(customer.location_, facility.location_)
    return dist


# facilitiesAmount = int(input())
# customersAmount = int(input())

f1 = Facility(10, 10, [1, 2])
c1 = Customer(5, [3, 5])
print(distance(c1, f1))

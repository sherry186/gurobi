from huristic1_1_2 import huristic1_1_2
from huristic1_2_2 import huristic1_2_2
from huristic2_1_2 import huristic2_1_2
from huristic2_2_2 import huristic2_2_2


# root = 'C:/Users/user/gurobi/CA2/tests/test'
# subfileName = ".csv"

# for i in range(10):
makespan, tardyamount = huristic1_2_2("C:/Users/user/gurobi/CA2/to students/data/instance1.csv")
print ('makespan', makespan, 'tardyamount', tardyamount)

from huristic1_1_2 import huristic1_1_2
from huristic1_2_2 import huristic1_2_2
from huristic2_1_2 import huristic2_1_2
from huristic2_2_2 import huristic2_2_2


root = 'C:/Users/user/gurobi/CA2/tests/test'
subfileName = ".csv"

for i in range(6, 10):
    path = root+ str(i) + subfileName
    print ('path:', path)
    makespan, tardyamount = huristic1_2_2(path)
    print ('makespan', makespan, 'tardyamount', tardyamount)


from huristic1_1_2 import huristic1_1_2
from huristic1_2_2 import huristic1_2_2
from huristic2_1_2 import huristic2_1_2
from huristic2_2_2 import huristic2_2_2


root = 'C:/Users/user/gurobi/CA2/tests/test'
subfileName = ".csv"


tardyamountAvg1_2_2 = 0
for i in range(10):
    path = root+ str(i) + subfileName
    # print ('path:', path)
    makespan, tardyamount = huristic1_2_2(path)
    tardyamountAvg1_2_2 += tardyamount
    # print ('makespan', makespan, 'tardyamount', tardyamount)
tardyamountAvg1_2_2 = tardyamountAvg1_2_2/10
print("tardy 1-2-2:", tardyamountAvg1_2_2)

makespan, tardyamount = huristic1_1_2("C:/Users/user/gurobi/CA2/tests/test1.csv")
print("test1 , 1-2-2", makespan, tardyamount)

tardyamountAvg1_1_2 = 0
for i in range(10):
    path = root+ str(i) + subfileName
    # print ('path:', path)
    makespan, tardyamount = huristic1_1_2(path)
    tardyamountAvg1_1_2 += tardyamount
    # print ('makespan', makespan, 'tardyamount', tardyamount)
tardyamountAvg1_1_2 = tardyamountAvg1_1_2/10
print("tardy 1-1-2:", tardyamountAvg1_1_2)

tardyamount2_1_2 = 0
for i in range(10):
    path = root+ str(i) + subfileName
    # print ('path:', path)
    makespan, tardyamount = huristic2_1_2(path)
    tardyamount2_1_2 += tardyamount
    # print ('makespan', makespan, 'tardyamount', tardyamount)
tardyamount2_1_2 = tardyamount2_1_2/10
print("tardy 2-1-2", tardyamount2_1_2)

tardyamount2_2_2 = 0
for i in range(10):
    path = root+ str(i) + subfileName
    # print ('path:', path)
    makespan, tardyamount = huristic2_2_2(path)
    tardyamount2_2_2 += tardyamount
    # print ('makespan', makespan, 'tardyamount', tardyamount)
tardyamount2_2_2 = tardyamount2_2_2/10
print("tardy 2-2-2", tardyamount2_2_2)

makespan, tardyamount = huristic2_2_2("C:/Users/user/gurobi/CA2/tests/test1.csv")
print("test1 , 2-2-2", makespan, tardyamount)
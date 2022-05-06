from huristic_paper import huristicPaper


root = 'C:/Users/user/gurobi/CA2/tests/test'
subfileName = ".csv"


tardyamount2_2_2 = 0
for i in range(0, 10):
    path = root+ str(i) + subfileName
    print ('path:', path)
    makespan, tardyamount, resultList = huristicPaper(path)
    
    print('tardyamount', tardyamount)
    print('makespan', makespan)
    print('resultList', resultList)


   
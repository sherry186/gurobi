import copy
from unittest import result
from huristicPaper import huristicPaper
from random import shuffle
import pandas as pd

def isLegalPosi(insert_job, insert_job_protime, max_makespan_machine, newStruct, resultList):
    isLegal = True
    for i in range(newStruct[max_makespan_machine]["jobList"].index(insert_job), len(newStruct[max_makespan_machine]["jobList"])):
        move_job = newStruct[max_makespan_machine][i]
        if(move_job.first == 1):
            move_job_stage1 = move_job
            move_job_stage1.first -= 1
            if(resultList[move_job][1] - insert_job_protime < resultList[move_job_stage1][2]):
                isLegal = False
                
    return isLegal          
    

def RandomOpt(makespan, tardyAmount, resultList, dueList):
    newStruct = {} #length = machine number
    hasTried = {}

    ################ Step 1: 整理一個新的dictionary ################

    for i in resultList.keys():
        hasTried[i] = False
        if(resultList[i][0] not in newStruct.keys()):
            newStruct[resultList[i][0]] = {}
            newStruct[resultList[i][0]]["makespan"] = resultList[i][2]
            newStruct[resultList[i][0]]["jobList"] = [i]
        else:
            if(resultList[i][2] > newStruct[resultList[i][0]]["makespan"]):
                newStruct[resultList[i][0]]["makespan"] = resultList[i][2]



            # 從第一個元素開始看當前i的start time 是否大於他的end time
            totalLen = len(newStruct[resultList[i][0]]["jobList"])
            for j in range(totalLen-1,-1):
                curKey = newStruct[resultList[i][0]]["jobList"][j]
                if(resultList[curKey][2] <= resultList[i][1]):
                    newStruct[resultList[i][0]]["jobList"].insert(j+1, i)
                    break
                elif(j == 0 and resultList[curKey][1] >= resultList[i][2]):
                    newStruct[resultList[i][0]]["jobList"].insert(j, i)
                    break
    print("==========================================")
    for i in newStruct:
        print(i, "->", newStruct[i])

    opt_tardy = tardyAmount
    opt_makespan = makespan

    ################ Step 2: 找合法的min. makespan and max. makespan machine ################

    ###### 2.1 找max. makespan 機器 #######
    '''
    newStruct = {
        "M": {
            "makespan": ,
            "resultList"
        }
    }
    '''

    # construct a sorted structure
    sort_orders = sorted(newStruct.items()["makespan"], key=lambda x: x[1], reverse=True)


    # max_makespan = -99999
    # max_makespan_machine = -1
    # for k in newStruct:
    #     if(newStruct[k]["makespan"] > max_makespan):
    #         max_makespan = newStruct[k]["makespan"]
    #         max_makespan_machine = k
    
    # max_makespan_machine




    # 找 max. machine


    return 0



# Timer


filepath = "data/instance 2.csv"
makespan, tardyAmount, resultList = huristicPaper(filepath)
for i in resultList:
    print(i, " -> ", resultList[i])
print(resultList)

# Check and import due time
df = pd.read_csv(filepath)
dueList = {}
for index, row in df.iterrows():
    dueList[index] = row['Due Time']

status = {
    "M1": {
        "(0,1)": False,
        "(1,1)": False
    }
}

False in status["M1"].values 

# while(Timer > 30):
for i in range(10):
    RandomOpt(makespan, tardyAmount, resultList, dueList)









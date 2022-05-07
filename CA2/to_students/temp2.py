import copy
from unittest import result
from huristicPaper import huristicPaper
from random import shuffle
import random
import pandas as pd
import time

tic = time.perf_counter()

df = pd.read_csv('./data/instance 3.csv')

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

def MachineCanDoJob(job, machine, df):
    if(type(df['Stage-2 Machines'][job[1]-1]) == float):
        return False
    # print("Job = ", job)
    # print("Machine = ", machine)
    if(job[0] == 0):
        if(df['Stage-1 Machines'][job[1]-1].find(str(machine)) == -1):
            return False
        else:
            return True
    else:
        if(df['Stage-2 Machines'][job[1]-1].find(str(machine)) == -1):
            return False
        else:
            return True



def RandomOpt(makespan, tardyAmount, resultList, dueList, startTime, job_amount, df):
    # print("debug")
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
    # print("==========================================")
    # for i in newStruct:
    #     print(i, "->", newStruct[i])

    opt_tardy = tardyAmount
    opt_makespan = makespan
    while(time.perf_counter() - startTime  < 50):
        # timer += 20
        ################ Step 2: 找合法的min. makespan and max. makespan machine ################

        ###### 2.1 找max. makespan 機器 #######

        # construct a sorted structure

        max_makespan = -99999
        max_makespan_machine = -1
        min_makespan = 99999
        min_makespan_machine = -1
        
        # method = random.randint(0,1) # 0: max machine, 1: random machine
        # if(method):
        #     for k in newStruct:
        #         if(newStruct[k]["makespan"] > max_makespan):
        #             max_makespan = newStruct[k]["makespan"]
        #             max_makespan_machine = k
        # else:
        max_makespan_machine = random.randint(0,len(newStruct)-1)
        max_makespan = newStruct[max_makespan_machine]["makespan"]
            
            
        ###### 2.2 隨機抓一個max. makespan 裡面的 work #######

        # generate selected work
        # insert_job_list = copy.deepcopy(newStruct[max_makespan_machine]["jobList"])
        # shuffle(insert_job_list)
        # selected_work = insert_job_list[0] #(0,1)

        # print("========== New Struct ==========")
        # print(newStruct)
        # print("================================")
        selected_index = random.randint(0,len(newStruct[max_makespan_machine]["jobList"])-1)
        selected_work = newStruct[max_makespan_machine]["jobList"][selected_index]
        

        ###### 2.3 min. makespan 機器 #######

        for cur_machine in newStruct:
            if(newStruct[cur_machine]["makespan"] < min_makespan and MachineCanDoJob(selected_work, cur_machine, df)):
                min_makespan = newStruct[cur_machine]["makespan"]
                min_makespan_machine = cur_machine

        if(min_makespan_machine == -1):
            continue
        
        ################ Step 3: 看一下移除selected work 之後，後面的元素是否有往前挪移的必要性 ################
        
        
        # need_to_move_front = True
        # # 如果過期ㄌ，就不一定要往前挪移
        # if(dueList[selected_work.second] < resultList[selected_work][2]):
        #     need_to_move_front = False


        
        # if(need_to_move_front):


        selected_index_on_origin_machine = newStruct[max_makespan_machine]["jobList"].index(selected_work)
        # 檢查如果把後面的東西往前挪，順序會不會壞掉 = 檢查
        toBreak = False
        for i in range(selected_index_on_origin_machine+1, len(newStruct[max_makespan_machine]["jobList"])):
            
            if(isLegalPosi(selected_work, selected_process_time, max_makespan_machine, newStruct, resultList) == False):
                toBreak = True
                break
        if(toBreak):
            continue
        
        ################ Step 4: # 插入 Process 並往後挪移 ################

        selected_process_time = resultList[selected_work][2] - resultList[selected_work][1]
        insert_index = -1
        final_push_value = -1
        # 插入 Process 並往後挪移
        # print("min_makespan_machine = ", min_makespan_machine)
        if(len(newStruct[min_makespan_machine]["jobList"]) < 2):
            continue
        for i in range(len(newStruct[min_makespan_machine]["jobList"]) - 2, -1):
            first_work = newStruct[min_makespan_machine]["jobList"][i]
            second_work = newStruct[min_makespan_machine]["jobList"][i+1]


            correct_ans = True
            # if selected_work is stage 1
            if(selected_work[0] == 0):
                if(resultList[first_work][2] + selected_process_time < resultList[(1,selected_work[1])][1]):
                    # 檢查後面往後推會不會非法
                    push_value = selected_process_time - (resultList[second_work][1] - resultList[first_work][2])
                                # i+1 ~ end
                    for check_index in range(i+1, len(newStruct[min_makespan_machine]["jobList"])):
                        check_work = newStruct[min_makespan_machine]["jobList"][check_index]
                        # 他是第一個stage
                        if(check_work[0] == 0 and resultList[check_work][2] + push_value > resultList[(1, check_work[1])][1]):
                            correct_ans = False
                            break
                    if(correct_ans):
                        insert_index = i+1
                        final_push_value = push_value
                        break
                else:
                    continue
            # if selected_work is stage 2
            else:
                if(resultList[first_work][2] > resultList[(0,selected_work[1])][2]):
                    # 檢查後面往後推會不會非法
                    push_value = selected_process_time - (resultList[second_work][1] - resultList[first_work][2])
                                # i+1 ~ end
                    for check_index in range(i+1, len(newStruct[min_makespan_machine]["jobList"])):
                        check_work = newStruct[min_makespan_machine]["jobList"][check_index]
                        # 他是第一個stage
                        if(check_work[0] == 0 and resultList[check_work][2] + push_value > resultList[(1, check_work[1])][1]):
                            correct_ans = False
                            break
                    if(correct_ans):
                        insert_index = i+1
                        final_push_value = push_value
                        break
                else:
                    continue

        if(insert_index == -1):
            continue

        # Check tardy
        ## Copy and Update resultList and newStruct
        tempResultList = copy.deepcopy(resultList)
        tempNewStruct = copy.deepcopy(newStruct)
        
        ### Update selected_work's machine_no, start_time, end_time
        tempResultList[selected_work][0] = min_makespan_machine
        # print("insert_index = ", insert_index)
        previous_work = tempNewStruct[min_makespan_machine]["jobList"][insert_index-1]
        tempResultList[selected_work][1] = tempResultList[previous_work][2]
        tempResultList[selected_work][2] = tempResultList[selected_work][1] + selected_process_time
        tempNewStruct[max_makespan_machine]["jobList"].remove(selected_work)
        tempNewStruct[min_makespan_machine]["jobList"].insert(insert_index, selected_work)
        tempNewStruct[max_makespan_machine]["makespan"] = tempNewStruct[max_makespan_machine]["makespan"] - selected_process_time
        tempNewStruct[min_makespan_machine]["makespan"] = tempNewStruct[min_makespan_machine]["makespan"] + final_push_value

        ### Update origin work's start_time, end_time
        for i in range(selected_index_on_origin_machine + 1 , len(newStruct[max_makespan_machine]["jobList"])):
            # 更新start_time, end_time
            curWork = newStruct[max_makespan_machine]["jobList"][i]
            tempResultList[curWork][1] += final_push_value
            tempResultList[curWork][2] += final_push_value

        ### Update new work's machine start_time, end_time
        for i in range(insert_index + 1 , len(newStruct[min_makespan_machine]["jobList"])):
            # 更新start_time, end_time
            curWork = newStruct[min_makespan_machine]["jobList"][i]
            tempResultList[curWork][1] += final_push_value
            tempResultList[curWork][2] += final_push_value
        
        new_tardy_Amount = 0
        for j in range(job_amount):
            completionTime = 0
            if((1, j) in tempResultList.keys()):
                completionTime = tempResultList[1, j][2]
            else:
                completionTime = tempResultList[0, j][2]
            if(completionTime - df['Due Time'][j] > 0):
                new_tardy_Amount += 1    
        
            
        # Check makespan
        ####### final_push_value
        new_makespan = newStruct[min_makespan_machine]["makespan"] + final_push_value
        if(new_makespan > max_makespan):
            new_max_makespan = new_makespan
        else:
            new_max_makespan = max_makespan
            
            
        # 看有沒有變好
        if(new_tardy_Amount < opt_tardy or (new_tardy_Amount == opt_tardy and new_max_makespan < opt_makespan)):
            resultList = tempResultList
            newStruct = tempNewStruct
            opt_tardy = new_tardy_Amount
            opt_makespan = new_max_makespan

        '''
        newStruct = {
            Machine_No: {
                "makespan": INT,
                "jobList": [tuple]
            }
        }
        '''




        # 找 max. machine


    return opt_tardy, opt_makespan



# Timer


filepath = "../500tests/test0.csv"
makespan, tardyAmount, resultList = huristicPaper(filepath)
# for i in resultList:
#     print(i, " -> ", resultList[i])
# print(resultList)

# Check and import due time
df = pd.read_csv(filepath)
dueList = {}
for index, row in df.iterrows():
    dueList[index] = row['Due Time']

# status = {
#     "M1": {
#         "(0,1)": False,
#         "(1,1)": False
#     }
# }

# False in status["M1"].values 

job_amount = len(df)

opt_tardy = -1
opt_makespan = -1

print("Original tardy = ", tardyAmount)
print("Original makespan = ", makespan)
print("=====================")
print("=====================")
print("=====================")

# for i in range(10):
# while(True):
opt_tardy, opt_makespan = RandomOpt(makespan, tardyAmount, resultList, dueList, tic, job_amount, df)


print("optimal makespan = ", opt_makespan)
print("optimal tardy = ", opt_tardy)







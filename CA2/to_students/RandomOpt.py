import copy
from unittest import result
from huristicPaper import huristicPaper
from random import shuffle
import pandas as pd
def RandomOpt(makespan, tardyAmount, resultList, dueList):
    newStruct = {} #length = machine number
    hasTried = {}

    ######## Step 1: 整理一個新的dictionary ########
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

    iterateTime = 5
    opt_tardy = tardyAmount
    opt_makespan = makespan

    #####################################################################

    # 找最大 makespan 的機器
    max_makespan = -99999
    max_makespan_machine = -1
    min_makespan = 99999
    min_makespan_machine = -1
    
    for i in range(len(newStruct)):
        if(newStruct[i]["makespan"] > max_makespan):
            max_makespan = newStruct[i]["makespan"]
            max_makespan_machine = i
        if(newStruct[i]["makespan"] < min_makespan):
            min_makespan = newStruct[i]["makespan"]
            min_makespan_machine = i

    ### 在max. makespan的機器上隨機挑一個沒被挑過的 (stage, job)
    
    insert_job_list = copy.deepcopy(newStruct[max_makespan_machine]["jobList"])
    shuffle(insert_job_list)

    

    insert_job = insert_job_list[0]
    for i in range(len(insert_job_list)):
        if(hasTried[insert_job_list[i]] == False):
            # check remove insert job 後，後面的任務會不會變成非法的
            original_index = newStruct[max_makespan_machine]["jobList"].index(insert_job_list)
            original_processing_time = resultList[insert_job_list][2] - resultList[insert_job_list][1]

            valid = True
            for k in range(original_index+1, len(newStruct[max_makespan_machine]["jobList"])):
                # 檢查要移動的job能不能在目標machine上執行
                # if():

                # cur_stage_job = newStruct[max_makespan_machine]["jobList"][k]
                # 如果是同一台machine呢
                if(cur_stage_job.first == 1 and resultList[cur_stage_job][2]-original_processing_time < resultList[(0, cur_stage_job.second)][1]):
                    valid = False
                    break
            if(valid == False):
                continue



            hasTried[insert_job_list[i]] = True
            insert_job = insert_job_list[i]
            break
    
    print(insert_job) #(stage, job_no)
    insert_job_protime = resultList[insert_job][2] - resultList[insert_job][1]

    # tbd: check remove insert job 後，後面的任務會不會變成非法的


    ### 試試看所有min. makespan 的機器上可插入的位置，看更新後的makespan有沒有小於目前的最佳值
    #### 可插入＝要插入位置前一個job（J_e）的end time + stage 1 process time < stage 2 start time
    ##### 看要插入位置後一個job（J_s）的start time - 要插入位置前一個job（J_e）的end time > insert_job_protime
    for i in range(len(newStruct[min_makespan_machine]["jobList"])-1, 0):
        curWork = newStruct[min_makespan_machine]["jobList"][i] #(stage, job_no)
        # 插入的位置對insert job本身來說是否合法
        if(insert_job.first == 0):
            insert_second_stage = insert_job
            insert_second_stage.first += 1 #(stage, job)
            # 如果最早的完成時間會晚於第二階段的開始時間
            if(resultList[curWork][2] + insert_job_protime > resultList[insert_second_stage][1]):
                continue         
        else:
            insert_first_stage = insert_job
            insert_first_stage.first -= 1
            # 如果開始位置已經比第一階段的結束時間來的早了
            if(resultList[curWork][2] < resultList[insert_first_stage][2]):
                continue

        # 有沒有足夠的空隙，讓機器後面的元素都不用被更動
        after_curWork = newStruct[min_makespan_machine]["jobList"][i+1]
        if(resultList[after_curWork][1] - resultList[curWork][2] > insert_job_protime):
            # Insert
            newStruct[min_makespan_machine]["jobList"].insert(i+1, insert_job)
            # Remove
            newStruct[max_makespan_machine]["jobList"].remove(insert_job)
            # Update makespan
            lastElement = newStruct[max_makespan_machine][-1]
            newStruct[max_makespan_machine]["makespan"] = resultList[lastElement][2]
            # Update resultList 
            oldEndTime = resultList[insert_job][2]
            resultList[insert_job][0] = min_makespan_machine
            resultList[insert_job][1] = resultList[curWork][2]
            resultList[insert_job][2] = resultList[insert_job][1] + insert_job_protime

            # Update optimal solution

            if(oldEndTime > dueList[insert_job.first] and resultList[insert_job][2] < dueList[insert_job.first]):
                opt_tardy -= 1
            # 重新去找最長的makespan
            temp_max_makespan = -1
            for i in resultList.keys():
                if(resultList[i][2] > temp_max_makespan):
                    temp_max_makespan = resultList[i][2]
            if(temp_max_makespan < opt_makespan):
                opt_makespan = temp_max_makespan
            break

        # 若沒有不需更動的空隙，從最後開始插入
        # 檢查欲插入位置後的工作會不會因此不合法
        # 插入並移動後續工作

    
    
    
    ### -> 如果有小於目前最佳值tardy的話，更新result list and new structure

    ### 回傳新的result list, tardy and makespan

    return 0





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

RandomOpt(makespan, tardyAmount, resultList, dueList)
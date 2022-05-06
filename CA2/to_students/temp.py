from huristicPaper import huristicPaper
def RandomOpt(resultList):
    newStruct = {} #length = machine number

    ######## Step 1: 整理一個新的dictionary ########
    for i in resultList.keys():
        if(resultList[i][0] not in newStruct.keys()):
            newStruct[resultList[i][0]] = {}
            newStruct[resultList[i][0]]["makespan"] = resultList[i][2]
            newStruct[resultList[i][0]]["jobList"] = [i]
        else:
            if(resultList[i][2] > newStruct[resultList[i][0]]["makespan"]):
                newStruct[resultList[i][0]]["makespan"] = resultList[i][2]



            # 從第一個元素開始看當前i的start time 是否大於他的end time
            totalLen = len(newStruct[resultList[i][0]]["jobList"])
            for j in range(totalLen-1,-1,-1):
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
    ### 在max. makespan的機器上隨機挑一個沒被挑過的 (stage, job)
    
    ### 試試看所有min. makespan 的機器上可插入的位置，看更新後的makespan有沒有小於目前的最佳值
    ### -> 如果有小於目前最佳值tardy的話，更新result list and new structure

    ### 回傳新的result list, tardy and makespan

    return 0


filepath = "data/instance 2.csv"
makespan, tardyAmount, resultList = huristicPaper(filepath)
count = 0
for i in resultList:
    print(i, " -> ", resultList[i])
    count += 1
# print("count = ", count)
RandomOpt(resultList)
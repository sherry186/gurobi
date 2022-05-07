import pandas as pd
# import os
import math
# from tardy import gantt_plot_2_3

'''
compare tardy amount
Input: p1i, p1j, p2i, p2j, P, D, startTime, J, Scheduled
Output: p1's tardy amount > p2'stardy amount ?
'''
def compareTardy(p1i, p1j, p2i, p2j, P, D, startTime1, startTime2, J, Scheduled):

    ## counting p1
    p1Count = 0
    for j in range(J):
        if j != p1j:
            if Scheduled[j] == 0:
                if startTime1 + P[p1i, p1j] + P[0, j] + P[1, j] - D[j] < 0:
                    p1Count += 1
            elif Scheduled[j] == 1:
                if startTime1 + P[p1i, p1j]  + P[1, j] - D[j] < 0:
                    p1Count += 1
                
    
    ## counting p2
    p2Count = 0
    for j in range(J):
        if j != p2j:
            if Scheduled[j] == 0:
                if startTime2 + P[p2i, p2j] + P[0, j] + P[1, j] - D[j] < 0:
                    p2Count += 1
            elif Scheduled[j] == 1:
                if startTime2 + P[p2i, p2j]  + P[1, j] - D[j] < 0:
                    p2Count += 1

    # print(p1Count, p2Count)
    
    return p1Count > p2Count 

def equalTardy(p1i, p1j, p2i, p2j, P, D, startTime1, startTime2, J, Scheduled):

    ## counting p1
    p1Count = 0
    for j in range(J):
        if j != p1j:
            if Scheduled[j] == 0:
                if startTime1 + P[p1i, p1j] + P[0, j] + P[1, j] - D[j] < 0:
                    p1Count += 1
            elif Scheduled[j] == 1:
                if startTime1 + P[p1i, p1j]  + P[1, j] - D[j] < 0:
                    p1Count += 1
                
    
    ## counting p2
    p2Count = 0
    for j in range(J):
        if j != p2j:
            if Scheduled[j] == 0:
                if startTime2 + P[p2i, p2j] + P[0, j] + P[1, j] - D[j] < 0:
                    p2Count += 1
            elif Scheduled[j] == 1:
                if startTime2 + P[p2i, p2j]  + P[1, j] - D[j] < 0:
                    p2Count += 1

    # print(p1Count, p2Count)
    
    return p1Count == p2Count 


'''
acts
'''
def compareACTs(p1i, p1j, p2i, p2j, D, P, startTime1, startTime2, K, P_bar):
    # ACTS_APDi (priority_index)= exp(max(d_i - p_i - t, 0) / K_1*p_bar) * exp(-1/APDi) // 挑出一個 job_stage
    # actP1 = 0
    actP1 = math.exp(max(D[p1j] - P[p1i, p1j] - startTime1, 0)/K*P_bar) * math.exp(-1/(math.log(D[p1j])/(P[0,p1j] + P[1, p1j])))
    actP2 = math.exp(max(D[p2j] - P[p2i, p2j] - startTime2, 0)/K*P_bar) * math.exp(-1/(math.log(D[p2j])/(P[0,p2j] + P[1, p2j])))


    return actP1 > actP2



'''
compare make span
Input: p1i, p1j, p2i, p2j, P, Machine amount, J
Output: p1's makespan > p2's makespan?
'''

def compareMakeSpan(p1i, p1j, p2i, p2j, P, M, J):
    sum = 0
    for i in range(2):
        for j in range(J):
            sum += P[i, j]
    
    p1MakeSpan = P[p1i, p1j] + (sum - P[p1i, p1j])/(J*2-1)*((J*2)/M -1)
    p2MakeSpan = P[p2i, p2j] + (sum - P[p2i, p2j])/(J*2-1)*((J*2)/M -1)
    # print(p1MakeSpan)
    # print(p2MakeSpan)

    return p1MakeSpan > p2MakeSpan


'''
chooseMachineByProcessTime
Input: MT
Output: chosen machine index and it's current processing time
'''
def chooseMachineByProcessTime(MT):
    # chosenM = 0
    # min = MT[0]
    # for i in range(len(MT)):
    #     if(MT[i] < min):
    #         min = MT[i]
    #         chosenM = i
    MTdic = {}
    for i in range(len(MT)):
        MTdic[i] = MT[i]
    
    returnList = sorted(MTdic.items(), key=lambda x:x[1])

    return returnList


'''
chooseMachineByFormulation
Input: pi, pj, MT, M, D
Output: chosen machine index
'''
def chooseMachineByFormulation(pi, pj, MT, M, D):
    chosenM = 0
    minMT = 99999
    for i in range(len(MT)):
        if(D[pi, pj] - (MT[i] + P[pi, pj]) < minMT and i in M[pi, pj]):
            minMT = D[pi, pj] - (MT[i] + P[pi, pj])
            chosenM = i

    return chosenM


    

### def

### def
def heuristic_algorithm(file_path):
    df = pd.read_csv(file_path)
    # df = pd.read_csv("C:/Users/user/gurobi/CA2/to students/data/instance1.csv")
    # print(df)
    # print(df['Due Time'].size)

    
    max_amount = 0
    for index, row in df.iterrows():
        x1 = row['Stage-1 Machines'].split(',')
        for element in x1:
            num = int(element)
            if(num > max_amount):
                max_amount = num

        temp = row['Stage-2 Machines']
        if(pd.isna(temp) == False):
            x2 = temp.split(',')
            for element in x2:
                num = int(element)
                if(num > max_amount):
                    max_amount = num


    J = df['Job ID'].size
    MT = [0 for i in range(0, max_amount)] # the amount of time Mi have processed, choose machine -> [(哪個machine, 它的MT), (哪個machine, 它的mt),.........]
    Mdefault = [i for i in range(1, max_amount+1)]

    # print("MT", MT)
    # print("Mdefault:", Mdefault)

    Scheduled = [] ## job j's next is which stage? 

    P = {} #Pij
    D = {} #Dj
    M = {} #Pij can do on Mlist ##normal index
    P_bar = 0
    for j in range(J):
        P[0,j] = df['Stage-1 Processing Time'][j]
        P[1,j] = df['Stage-2 Processing Time'][j]
        P_bar += (df['Stage-1 Processing Time'][j] + df['Stage-2 Processing Time'][j])
        D[j] = df['Due Time'][j]
        s1 = str(df['Stage-1 Machines'][j])
        s2 = str(df['Stage-2 Machines'][j])
        M[0,j] = s1.split(",")
        M[1,j] = s2.split(",")
        if M[0, j] != ['nan']:
            M[0,j] = [int(i) for i in M[0,j]]
        else:
            M[0,j] = Mdefault

        if M[1,j] != ['nan']:
            M[1,j] = [int(i) for i in M[1,j]]
        else:
            M[1,j] = Mdefault

        Scheduled.append(0)

    P_bar = P_bar/(J*2)

    R = 0.4 #hyper...
    K = math.log(J/max_amount)*1.2 - R ## some constant from paper

    machinePriortylist = chooseMachineByProcessTime(MT)

    resultList = {} ##(i, j)->[m, starttime, endtime]  list, Pij assigned to m on starttime// normal index
    while 0 in Scheduled or 1 in Scheduled:

        machinePriortylist = chooseMachineByProcessTime(MT) 
        data = [] ### [i, j, startime] Pij, last process's startime 選的machine可以做的process
        priorityInd = 0 
        chosenMachineInd, startTime =  machinePriortylist[priorityInd][0], machinePriortylist[priorityInd][1] # 

        while(len(data) == 0):
            chosenMachineInd, startTime = machinePriortylist[priorityInd][0], machinePriortylist[priorityInd][1]
            for j in range(len(Scheduled)):
                if Scheduled[j] != 2 and chosenMachineInd+1 in M[Scheduled[j], j]:
                    if Scheduled[j] == 1:
                        # data.append([Scheduled[j], j, resultList[0, j][1]+ P[0, j]])
                        data.append([Scheduled[j], j, resultList[0, j][2]])
                    else:
                        data.append([Scheduled[j], j, 0])
            priorityInd += 1 
            
        bestJob = data[0]
        for u in range(1, len(data)):
            if compareACTs(bestJob[0], bestJob[1], data[u][0], data[u][1], D, P, max(startTime, bestJob[2]), max(startTime, data[u][2]), K, P_bar):
                bestJob = data[u]
            # if compareACTs(bestJob[0], bestJob[1], data[u][0], data[u][1], P, D, max(startTime, bestJob[2]), max(startTime, data[u][2]), J, Scheduled):
        
        if(P[bestJob[0], bestJob[1]]):
            MT[chosenMachineInd] = max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]
            
        resultList[bestJob[0], bestJob[1]] = [chosenMachineInd, max(startTime, bestJob[2]), max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]]
        Scheduled[bestJob[1]] += 1

        if(bestJob[0] == 1 and max(startTime, bestJob[2]) == bestJob[2]): ## 挑的是stage2，而且前面有一段空檔
            for job in data:
                if job != bestJob and job[0] == 0: ## 找一個能做的stage1
                    if P[bestJob[0], bestJob[1]]: ## 如果那個stage2 本身是有東西的(p不為0)
                        if(P[job[0],job[1]] <= bestJob[2] - startTime): ## 先該job檢查能不能塞
                            resultList[job[0], job[1]] = [chosenMachineInd, max(startTime, job[2]), max(startTime, job[2]) + P[job[0], job[1]]]
                            Scheduled[job[1]] += 1
                            break



    # print("result list", resultList)
    ## result
    tardyAmount = 0
    makespan = 0
    for j in range(J):
        completionTime = 0
        if((1, j) in resultList.keys()):
            completionTime = resultList[1, j][2]
        else:
            completionTime = resultList[0, j][2]


        if(completionTime - D[j] > 0):
            tardyAmount += 1

        if(completionTime > makespan):
            makespan = completionTime
    
    # end time of Pji
    completion_time = []
    for j in range(J):
        temp = []
        for i in range(2):
            temp.append(resultList[i, j][2])
        completion_time.append(temp)

    machine = []
    for j in range(J):
        temp = []
        for i in range(2):
            temp.append(resultList[i, j][0] + 1)
        machine.append(temp)

    


    return machine, completion_time

# m, c = heuristic_algorithm('C:/Users/user/gurobi/CA2/data/instance1.csv')
# print(m)
# print(c)
# def heuristic_algorithm(file_path):
    
#     '''
#     1. Write your heuristic algorithm here.
#     2. We would call this function in CA2_grading_program.py to evaluate your algorithm.
#     3. Please do not change the function name and the file name.
#     4. The parameter is the file path of a data file, whose format is specified in the document. 
#     5. You need to return your schedule in two lists "machine" and "completion_time".
#         (a) machine[j][0] is the machine ID of the machine to process the first stage of job j + 1, and 
#             machine[j][1] is the machine to process the second stage of job j + 1.
#         (b) completion_time[j][0] is the completion time of the first stage of job j + 1, and 
#             completion_time[j][1] is the completion time of the second stage of job j + 1. 
#         Note 1. If you have n jobs, both the two lists are n by 2 (n rows, 2 columns). 
#         Note 2. In the list "machine", you should record the IDs of machines 
#                 (i.e., to let machine 1 process the first stage of job 1, 
#                 you should have machine[0][0] == 1 rather than machine[0][0] == 0).
#     6. You only need to submit this algorithm_module.py.
#     '''
    
#     import csv
    
#     # read data and store the information into your self-defined variables
#     fp = open(file_path, 'r', newline = '')
#     header = fp.readline() 
#     reader = csv.reader(fp, delimiter = ',')
#     # for a_row in reader:
#     #     print(a_row) # a_row is a list
#     # ...
    
    
    

#     # start your algorithm here
#     machine = []
#     completion_time = []
#     # ...  
    
    
    
#     return machine, completion_time


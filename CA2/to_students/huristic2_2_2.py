import pandas as pd
import os
from dotenv import load_dotenv
from tardy import gantt_plot_2_3

load_dotenv()

serverIP = os.getenv("myPath")
print(serverIP)

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
def huristic2_2_2(fileName):
    df = pd.read_csv(fileName)
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
    MT = [0 for i in range(0, max_amount)] # the amount of time Mi have processed
    Mdefault = [i for i in range(1, max_amount+1)]

    # print("MT", MT)
    # print("Mdefault:", Mdefault)

    Scheduled = [] ## job j's next is which stage?

    P = {} #Pij
    D = {} #Dj
    M = {} #Pij can do on Mlist ##normal index

    for j in range(J):
        P[0,j] = df['Stage-1 Processing Time'][j]
        P[1,j] = df['Stage-2 Processing Time'][j]
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

    # print("P", P)
    # print("D", D)
    # print("M", M)

    # print(compareTardy(0, 9, 0, 1, P, D,0, 0, J, Scheduled))
    # print(compareMakeSpan(0, 9, 0, 1, P, len(MT), J))

    ## -----------------------

    machinePriortylist = chooseMachineByProcessTime(MT)
    # print("machinePriortylist1", machinePriortylist)

    # print("P", P)
    # print("D", D)
    # print("M", M)

    # print(compareTardy(0, 9, 0, 1, P, D,0, J, Scheduled))
    # print(compareMakeSpan(0, 9, 0, 1, P, len(MT), J))
    # print(chooseMachineByProcessTime(0, 3, MT, M))

    ### -----------------------

    # machinePriortylist = chooseMachineByProcessTime(MT)
    # print(machinePriortylist)

    ### huristic part
    resultList = {} ##(i, j)->[m, starttime, endtime]  list, Pij assigned to m on starttime// normal index
    while 0 in Scheduled or 1 in Scheduled:
        # print(chosenMachineInd, startTime)
        # print("Scheduled:", Scheduled)
        machinePriortylist = chooseMachineByProcessTime(MT)
        # print("machine priority list:", machinePriortylist)
        data = [] ### [i, j, startime] Pij, last process's startime
        priorityInd = 0
        chosenMachineInd, startTime = 0, 0
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

        # print("data:", data)
        # break
        if data != []:
            bestJob = data[0]
            for u in range(1, len(data)):
                if compareTardy(bestJob[0], bestJob[1], data[u][0], data[u][1], P, D, max(startTime, bestJob[2]), max(startTime, data[u][2]), J, Scheduled):
                    bestJob = data[u]
                elif equalTardy(bestJob[0], bestJob[1], data[u][0], data[u][1], P, D, max(startTime, bestJob[2]), max(startTime, data[u][2]), J, Scheduled) and compareMakeSpan(bestJob[0], bestJob[1], data[u][0], data[u][1], P, len(MT), J):
                    bestJob = data[u]


            MT[chosenMachineInd] = max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]
            Scheduled[bestJob[1]] += 1
            resultList[bestJob[0], bestJob[1]] = [chosenMachineInd, max(startTime, bestJob[2]), max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]]


    # print("result list", resultList)
    print("fileName", fileName)
    x = []
    for j in range(J):
        temp = []
        for i in range(2):
            temp.append(resultList[i, j][2])
        x.append(temp)

    print('x', x)

    Plist = []
    for j in range(J):
        temp = []
        for i in range(2):
            temp.append(P[i,j])
        Plist.append(temp)
    print('Plist', Plist)
    
    y = []
    for j in range(J):
        tempj = []
        for i in range(2):
            tempi = []
            for m in range(max_amount):
                if(resultList[i,j][0] == m):
                    tempi.append(1)
                else:
                    tempi.append(0)
            tempj.append(tempi)
        y.append(tempj)
    print('y', y)
    
    gantt_plot_2_3(x, Plist, y, 3)

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

    # print("makespan:", makespan)
    # print("tardy amount:", tardyAmount)

    return makespan, tardyAmount 






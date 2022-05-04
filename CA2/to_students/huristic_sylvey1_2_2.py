import pandas as pd
import os
from dotenv import load_dotenv
from tardy import compareSlackTime
from tardy import equalSlackTime
from tardy import gantt_plot_2_3
from tardy import chooseMachineByProcessTime
from tardy import compareTardy
from tardy import equalTardy
from tardy import compareMakeSpan

def huristic_sylvey(fileName):
    df = pd.read_csv(fileName)
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


    resultList = {}
    for j in range(J):
        for m in M[0, j]:
            if(MT[m-1] == 0):
                Scheduled[j] += 1
                MT[m-1] += P[0,j]
                resultList[0, j] = [m-1, 0, MT[m-1]]
                break

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
                if(Scheduled[bestJob[1]] > Scheduled[data[u][1]]):
                    bestJob = data[u]
                elif Scheduled[bestJob[1]] == Scheduled[data[u][1]] and compareSlackTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, max(startTime, bestJob[2]), max(startTime, data[u][2]), D):
                    bestJob = data[u]
                elif Scheduled[bestJob[1]] == Scheduled[data[u][1]] and equalSlackTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, max(startTime, bestJob[2]), max(startTime, data[u][2]), D) and compareMakeSpan(bestJob[0], bestJob[1], data[u][0], data[u][1], P, len(MT), J):
                    bestJob = data[u]


            MT[chosenMachineInd] = max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]
            Scheduled[bestJob[1]] += 1
            resultList[bestJob[0], bestJob[1]] = [chosenMachineInd, max(startTime, bestJob[2]), max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]]

    print(resultList)

    # result evaluation
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

    print("makespan:", makespan)
    print("tardy amount:", tardyAmount)

    ##plot 
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


huristic_sylvey("C:/Users/user/gurobi/CA2/tests/test1.csv")
    

import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

serverIP = os.getenv("myPath")
print(serverIP)

'''
compare slack time
Input: p1i, p1j, p2i, p2j, P, MT, D
Output: p1's slack time > p2's slack time?
'''

def compareSlackTime(p1i, p1j, p2i, p2j, P, startTime1, startTime2, D):
    p1SlackTime = D[p1j] - (startTime1 + P[p1i, p1j])
    p2SlackTime = D[p2j] - (startTime2 + P[p2i, p2j])
    print(p1SlackTime)
    print(p2SlackTime)

    return p1SlackTime > p2SlackTime

def equalSlackTime(p1i, p1j, p2i, p2j, P, startTime1, startTime2, D):
    p1SlackTime = D[p1j] - (startTime1 + P[p1i, p1j])
    p2SlackTime = D[p2j] - (startTime2 + P[p2i, p2j])
    print(p1SlackTime)
    print(p2SlackTime)

    return p1SlackTime == p2SlackTime

'''
compare process time
Input: p1i, p1j, p2i, p2j, P
Output: p1's process time > p2's process time?
'''

def compareProcessTime(p1i, p1j, p2i, p2j, P):
    
    return P[p1i, p1j] > P[p2i, p2j]


'''
chooseMachineByProcessTime
Input: MT
Output: chosen machine index and it's current processing time
'''
def chooseMachineByProcessTime( MT):
    chosenM = 0
    min = MT[0]
    for i in range(len(MT)):
        if(MT[i] < min):
            min = MT[i]
            chosenM = i
    
    return chosenM, min

df = pd.read_csv(serverIP)
# df = pd.read_csv("C:/Users/user/gurobi/CA2/to students/data/instance1.csv")

J = df['Job ID'].size
MT = [0, 0, 0, 0, 0] # the amount of time Mi have processed
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
        M[0,j] = []

    if M[1,j] != ['nan']:
        M[1,j] = [int(i) for i in M[1,j]]
    else:
        M[1,j] = []
    
    Scheduled.append(0)


### huristic part
resultList = {} ##(i, j)->[m, starttime]  list, Pij assigned to m on starttime// normal index
for k in range(2 * J):
    chosenMachineInd, startTime = chooseMachineByProcessTime(MT)
    print(chosenMachineInd, startTime)
    
    data = [] ### [i, j, startime] Pij, last process's startime
    for j in range(len(Scheduled)):
        if Scheduled[j] != 2 and chosenMachineInd+1 in M[Scheduled[j], j]:
            if Scheduled[j] == 1:
                data.append([Scheduled[j], j, resultList[0, j][1]+ P[0, j]])
            else:
                data.append([Scheduled[j], j, 0])
    # break
    if data != []:
        bestJob = data[0]
        for u in range(1, len(data)):
            if compareSlackTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, max(startTime, bestJob[2]), max(startTime, data[u][2]), D):
                bestJob = data[u]
            elif equalSlackTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, max(startTime, bestJob[2]), max(startTime, data[u][2]), D) and compareProcessTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, len(MT), J):
                bestJob = data[u]

        
        MT[chosenMachineInd] = max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]
        Scheduled[bestJob[1]] += 1
        resultList[bestJob[0], bestJob[1]] = [chosenMachineInd, max(startTime, bestJob[2])]

print("result list", resultList)
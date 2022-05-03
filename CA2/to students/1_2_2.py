import pandas as pd


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

    print(p1Count, p2Count)
    
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

    print(p1Count, p2Count)
    
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
    print(p1MakeSpan)
    print(p2MakeSpan)

    return p1MakeSpan > p2MakeSpan

    
'''
compare slack time
Input: p1i, p1j, p2i, p2j, P, MT, D
Output: p1's slack time > p2's slack time?
'''

def compareSlackTime(p1i, p1j, p2i, p2j, P, M, D):
    p1SlackTime = D[p1j] - (min(MT) + P[p1i, p1j])
    p2SlackTime = D[p2j] - (min(MT) + P[p2i, p2j])
    # print(p1SlackTime)
    # print(p2SlackTime)

    return p1SlackTime > p2SlackTime

def equalSlackTime(p1i, p1j, p2i, p2j, P, M, D):
    p1SlackTime = D[p1j] - (min(MT) + P[p1i, p1j])
    p2SlackTime = D[p2j] - (min(MT) + P[p2i, p2j])
    # print(p1SlackTime)
    # print(p2SlackTime)

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



df = pd.read_csv("C:/Users/user/gurobi/CA2/to students/data/instance1.csv")
# print(df)
# print(df['Due Time'].size)

J = df['Job ID'].size
MT = [0, 0, 0, 0, 0] # the amount of time Mi have processed
Scheduled = []

P = {} #Pij
D = {} #Dj
M = {} #Pij can do on M

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

# print("P", P)
# print("D", D)
# print("M", M)

# print(compareTardy(0, 9, 0, 1, P, D,0, J, Scheduled))
# print(compareMakeSpan(0, 9, 0, 1, P, len(MT), J))
# print(chooseMachineByProcessTime(0, 3, MT, M))




### huristic part
resultList = {} ##(i, j)->[m, starttime]  list, Pij assigned to m on starttime// normal index
for k in range(2 * J):
    chosenMachineInd, startTime = chooseMachineByProcessTime(MT)
    print(chosenMachineInd, startTime)
    
    data = [] ### [i, j, startime] Pij, last process's startime
    for j in range(len(Scheduled)):
        if Scheduled[j] != 2 and chosenMachineInd+1 in M[Scheduled[j], j]:
            if Scheduled[j] == 1:
                data.append([Scheduled[j], j, resultList[0, j][1]])
            else:
                data.append([Scheduled[j], j, 0])
    
    print(data)
    # break
    if data != []:
        bestJob = data[0]
        for u in range(1, len(data)):
            if compareSlackTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, M, D):
                bestJob = data[u]
            elif equalSlackTime(bestJob[0], bestJob[1], data[u][0], data[u][1], P, M, D) and compareMakeSpan(bestJob[0], bestJob[1], data[u][0], data[u][1], P, len(MT), J):
                bestJob = data[u]

        
        MT[chosenMachineInd] = max(startTime, bestJob[2]) + P[bestJob[0],bestJob[1]]
        Scheduled[bestJob[1]] += 1
        resultList[bestJob[0], bestJob[1]] = [chosenMachineInd, max(startTime, bestJob[2])]

print("result list", resultList)



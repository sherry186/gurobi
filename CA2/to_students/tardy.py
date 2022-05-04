import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# serverIP = os.getenv("myPath")
# print(serverIP)

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
compare slack time
Input: p1i, p1j, p2i, p2j, P, MT, D
Output: p1's slack time > p2's slack time?
'''

def compareSlackTime(p1i, p1j, p2i, p2j, P, M, D):
    p1SlackTime = D[p1j] - (min(MT) + P[p1i, p1j])
    p2SlackTime = D[p2j] - (min(MT) + P[p2i, p2j])
    print(p1SlackTime)
    print(p2SlackTime)

    return p1SlackTime > p2SlackTime


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
compare process time
Input: p1i, p1j, p2i, p2j, P
Output: p1's process time > p2's process time?
'''

def compareProcessTime(p1i, p1j, p2i, p2j, P):
    
    return P[p1i, p1j] > P[p2i, p2j]

    

### def

# df = pd.read_csv(serverIP)
# df = pd.read_csv("C:/Users/user/gurobi/CA2/to students/data/instance1.csv")
# print(df)
# print(df['Due Time'].size)

# max_amount = 0
# for index, row in df.iterrows():
#     x1 = row['Stage-1 Machines'].split(',')
#     for element in x1:
#         num = int(element)
#         if(num > max_amount):
#             max_amount = num
            
#     temp = row['Stage-2 Machines']
#     if(pd.isna(temp) == False):
#         x2 = temp.split(',')
#         for element in x2:
#             num = int(element)
#             if(num > max_amount):
#                 max_amount = num


# J = df['Job ID'].size
# MT = [0 for i in range(0, max_amount)] # the amount of time Mi have processed
# Mdefault = [i for i in range(1, max_amount+1)]

# print("MT", MT)
# print("Mdefault:", Mdefault)

# Scheduled = [] ## job j's next is which stage?

# P = {} #Pij
# D = {} #Dj
# M = {} #Pij can do on Mlist ##normal index

# for j in range(J):
#     P[0,j] = df['Stage-1 Processing Time'][j]
#     P[1,j] = df['Stage-2 Processing Time'][j]
#     D[j] = df['Due Time'][j]
#     s1 = str(df['Stage-1 Machines'][j])
#     s2 = str(df['Stage-2 Machines'][j])
#     M[0,j] = s1.split(",")
#     M[1,j] = s2.split(",")
#     if M[0, j] != ['nan']:
#         M[0,j] = [int(i) for i in M[0,j]]
#     else:
#         M[0,j] = Mdefault

#     if M[1,j] != ['nan']:
#         M[1,j] = [int(i) for i in M[1,j]]
#     else:
#         M[1,j] = Mdefault
    
#     Scheduled.append(0)

# print("P", P)
# print("D", D)
# print("M", M)

# print(compareTardy(0, 9, 0, 1, P, D,0, 0, J, Scheduled))
# print(compareMakeSpan(0, 9, 0, 1, P, len(MT), J))

## -----------------------

# machinePriortylist = chooseMachineByProcessTime(MT)
# print("machinePriortylist1", machinePriortylist)

import plotly.express as px

# display settings
from IPython.display import display
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option('display.float_format', lambda x: '%.4f' % x)


# 第二、三題的甘特圖
def gantt_plot_2_3(x_opt, P, y_opt, problem_no, open_hour=0, open_min=0):
    import datetime

    I = len(x_opt)
    S = len(x_opt[0])
    M = len(y_opt[0][0])
    schedule_df = pd.DataFrame()
    open_time = datetime.datetime(2000, 1, 1, hour=open_hour, minute=open_min)
    schedule_df['START_TIME'] = [(open_time + datetime.timedelta(hours=x_opt[i][s]) - datetime.timedelta(hours=P[i][s])) for i in range(I) for s in range(S)]
    schedule_df['END_TIME'] = [(open_time + datetime.timedelta(hours=x_opt[i][s])) for i in range(I) for s in range(S)]

    machine_ID = []
    for i in range(I):
        for s in range(S):
            for m in range(M):
                if y_opt[i][s][m] == 1:
                    machine_ID.append(str(m + 1))
    schedule_df['Machine_ID'] = machine_ID

    schedule_df['Job_ID'] = [str(i + 1) for i in range(I) for s in range(S)]
    color_list = ["#C0392B", "#EC7063", "#1F618D", "#34495E", "#3498DB", "#1E8449", "#28B463", "#F1C40F", "#F39C12", "#A6ACAF", "#7D3C98", "#9B59B6", "#2C3E50", "#EF553B", "#636EFA", "#BDC3C7", "#F39C12"]
    fig = px.timeline(schedule_df, x_start="START_TIME", x_end="END_TIME", y="Machine_ID", color="Job_ID",
                      color_discrete_sequence=color_list[0:I],
                      category_orders={"Job_ID": [str(i+1) for i in range(I)], "Machine_ID": [str(m+1) for m in range(M)]},
                      title="Instance " + str(1) + " Problem " + str(problem_no) + " Gantt Chart")
    fig.update_xaxes(tickformat="%H:%M")
    fig.update_layout(legend_title="Lot ID")
    fig.show()
    fig.write_image("Instance " + str(1) + " Problem " + str(problem_no) + ".pdf")






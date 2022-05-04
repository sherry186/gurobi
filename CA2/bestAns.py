import pandas as pd
import openpyxl
from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np

def calculateIP(route):


    df = pd.read_csv(route)
    # calculate machine amount
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
    # max_amount
    M = max_amount

    I = len(df) # order num
    S = 2 # stage num


    orders = range(0, I)
    machines = range(0, M)
    stages = range(0, S)

    P = []
    for index, row in df.iterrows():
        P.append([])
        P[index].append(row['Stage-1 Processing Time'])
        P[index].append(row['Stage-2 Processing Time'])
    #capability of machines
    C =  []
    for i in range(I):
        C.append([])
        C[i].append([0 for i in range(M)])
        C[i].append([0 for i in range(M)])
    for index, row in df.iterrows():
        x1 = row['Stage-1 Machines'].split(',')
        for element in x1:
            num = int(element)
            C[index][0][num-1] = 1

            temp = row['Stage-2 Machines']
            if(pd.isna(temp) == False):
                x2 = temp.split(',')
                for element in x2:
                    num = int(element)
                    C[index][1][num-1] = 1
    #Due Time
    D = []
    for index, row in df.iterrows():
        D.append(row['Due Time'])


    ########## Step 1:calculate delay machine ##############


    #Decision variable: Delay
    Q3_delay = Model('Q3-delay')
    Q3_delay.setParam('Timelimit', 360)


    # x_is is the finish time of order i at stage s
    x = {}
    for i in orders:
        x[i] = {}
        for s in stages:
            x[i][s] = Q3_delay.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = "x_" + str(i) + "," + str(s))

    # y_ism = 1 if order i process on machine m  at stage s otherwise 0
    y = {}
    for i in orders:
        y[i] = {}
        for s in stages:
            y[i][s] = {}
            for m in machines:
                y[i][s][m] = Q3_delay.addVar(lb = 0, vtype = GRB.BINARY, name = "y_" + str(i) + "," + str(s) + "," + str(m))
            
    # z_isjt = 1 if order i's stage s process before order j's stage t and they both process on the same machine otherwise 0
    z = {}
    for i in orders:
        z[i] = {}
        for s in stages:
            z[i][s] = {}
            for j in orders:
                z[i][s][j] = {}
                for t in stages:
                    z[i][s][j][t] = Q3_delay.addVar(lb = 0, vtype = GRB.BINARY, name = "z_" + str(i) + "," + str(s) + "," + str(j) + "," + str(t))
            
    # l_i = 1 if order i is late otherwise 0
    l = {}
    for i in orders:
        l[i] = Q3_delay.addVar(lb = 0, vtype = GRB.BINARY, name = "l_" + str(i))

    Q3_delay.update()

    #Setting the objective function
    Q3_delay.setObjective(quicksum(l[i] for i in orders), GRB.MINIMIZE)

    #Add constraint
    Q3_delay.addConstrs((x[j][t] + P[i][s] - x[i][s] <= (quicksum(P[i][s] for i in orders for s in stages)+P[i][s]) * (z[i][s][j][t] + 2-y[i][s][m]-y[j][t][m]) for i in orders for j in range(i+1, I) for m in machines for s in stages for t in stages), 'constraints for x_is, z_isjt')
    Q3_delay.addConstrs((x[i][s] + P[j][t] - x[j][t] <= (quicksum(P[i][s] for i in orders for s in stages)+P[j][t]) * (1-z[i][s][j][t] + 2-y[i][s][m]-y[j][t][m]) for i in orders for j in range(i+1, I) for m in machines for s in stages for t in stages), 'constraints for x_is, z_isjt')
    Q3_delay.addConstrs((x[i][1] <= D[i] + quicksum(P[i][s] for s in stages for i in orders) * l[i] for i in orders), 'constraints for l_i')
    Q3_delay.addConstrs((quicksum(y[i][s][m] for m in machines) == 1 for i in orders for s in stages), 'allocate orders to machines')
    Q3_delay.addConstrs((x[i][s] >= P[i][s] for i in orders for s in stages), 'minimum x_i')
    Q3_delay.addConstrs((x[i][1] >= x[i][0] + P[i][1] for i in orders), 'stage 2 should start after stage 1 is finished')


    Q3_delay.addConstrs((y[i][s][m] <= (1 if C[i][s][m] == 0 else 1) for i in orders for s in stages for m in machines), 'constraints machines')
    Q3_delay.update()

    # Run Program
    Q3_delay.optimize()
    obj_val_delay = Q3_delay.objVal

    ########## Step 2:calculate makespan ##############
    # Decision variable
    Q3_makespan = Model('Q3-makespan')
    Q3_makespan.setParam('Timelimit', 360)

    # x_is is the finish time of order i at stage s
    x = {}
    for i in orders:
        x[i] = {}
        for s in stages:
            x[i][s] = Q3_makespan.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = "x_" + str(i) + "," + str(s))

    # y_ism = 1 if order i process on machine m  at stage s otherwise 0
    y = {}
    for i in orders:
        y[i] = {}
        for s in stages:
            y[i][s] = {}
            for m in machines:
                y[i][s][m] = Q3_makespan.addVar(lb = 0, vtype = GRB.BINARY, name = "y_" + str(i) + "," + str(s) + "," + str(m))
            
    # z_isjt = 1 if order i's stage s process before order j's stage t and they both process on the same machine otherwise 0
    z = {}
    for i in orders:
        z[i] = {}
        for s in stages:
            z[i][s] = {}
            for j in orders:
                z[i][s][j] = {}
                for t in stages:
                    z[i][s][j][t] = Q3_makespan.addVar(lb = 0, vtype = GRB.BINARY, name = "z_" + str(i) + "," + str(s) + "," + str(j) + "," + str(t))
            
    # l_i = 1 if order i is late otherwise 0
    l = {}
    for i in orders:
        l[i] = Q3_makespan.addVar(lb = 0, vtype = GRB.BINARY, name = "l_" + str(i))

    # w is the makespan of the solution
    w = Q3_makespan.addVar(lb = 0, vtype = GRB.CONTINUOUS, name = "w")

    Q3_makespan.update()

    #Setting objective function
    Q3_makespan.setObjective(w, GRB.MINIMIZE)

    #Add constraint
    Q3_makespan.addConstrs((x[j][t] + P[i][s] - x[i][s] <= (quicksum(P[i][s] for i in orders for s in stages)+P[i][s]) * (z[i][s][j][t] + 2-y[i][s][m]-y[j][t][m]) for i in orders for j in range(i+1, I) for m in machines for s in stages for t in stages), 'constraints for x_is, z_isjt')
    Q3_makespan.addConstrs((x[i][s] + P[j][t] - x[j][t] <= (quicksum(P[i][s] for i in orders for s in stages)+P[j][t]) * (1-z[i][s][j][t] + 2-y[i][s][m]-y[j][t][m]) for i in orders for j in range(i+1, I) for m in machines for s in stages for t in stages), 'constraints for x_is, z_isjt')
    Q3_makespan.addConstrs((x[i][1] <= D[i] + quicksum(P[i][s] for s in stages for i in orders) * l[i] for i in orders), 'constraints for l_i')
    Q3_makespan.addConstrs((quicksum(y[i][s][m] for m in machines) == 1 for i in orders for s in stages), 'allocate orders to machines')
    Q3_makespan.addConstrs((x[i][s] >= P[i][s] for i in orders for s in stages), 'minimum x_i')
    Q3_makespan.addConstrs((x[i][1] >= x[i][0] + P[i][1] for i in orders), 'stage 2 should start after stage 1 is finished')
    # C_ism
    Q3_makespan.addConstrs((y[i][s][m] <= (1 if C[i][s][m] == 0 else 1) for i in orders for s in stages for m in machines), 'constraints for cook machines')
    Q3_makespan.addConstrs((w >= x[i][1] for i in orders), 'makespan')
    Q3_makespan.addConstr((quicksum(l[i] for i in orders) == obj_val_delay), 'delay num')
    # Q3_makespan.addConstr((w == 6.1), 'delay num')

    Q3_makespan.update()
    
    #Run program
    Q3_makespan.optimize()

    obj_val_makespan = Q3_makespan.objVal

    return obj_val_delay, obj_val_makespan

fileName = "tests/test0.csv"
delay, makespan = calculateIP(fileName)

print("Delay Job = ", delay)
print("Makespan = ", makespan)
import pandas as pd
import numpy as np
import random as rand


def instance_creator():
    testnum = 0
    while(testnum != 500):
        # 隨機產生 job 數量
        jobNO = rand.randrange(10, 998)  # jobNo

        # 根據 jobNO 隨機產生相對應變數
        jobID = list(range(1, jobNO+2))
        stage1P = (np.random.rand(1, jobNO+1) * 10).flatten()
        stage2P = (np.random.rand(1, jobNO+1) * 10).flatten()
        dueTime = []
        for i in range(jobNO+1):
            d = rand.uniform(stage1P[i] + stage2P[i], 24.0)
            dueTime.append(d)

        # 規定 Machine 數
        machineNo = rand.randrange(1, 20)
        machines = list(range(1, machineNo+1))
        print(stage1P.sum() + stage2P.sum())
        if(stage1P.sum() + stage2P.sum() > machineNo * 24):
            continue
        else:
            testnum += 1

        # 產生 Machine lists
        stage1Machines = []
        for i in range(0, jobNO+1):
            machine_st1 = rand.sample(
                machines, rand.randrange(1, machineNo+1, 1))
            machine_st1.sort()
            machine_st1_string = ','.join(str(e) for e in machine_st1)
            if(isinstance(machine_st1_string, str) == False):
                machine_st1_string = str(machine_st1_string)
            stage1Machines.append(machine_st1_string)

        stage2Machines = []
        for i in range(0, jobNO+1):
            no_stage2 = np.random.binomial(1, rand.uniform(1/8, 1/4))
            if(no_stage2):
                stage2Machines.append('N/A')
                stage2P[i] = 0
            else:
                machine_st1 = rand.sample(
                    machines, rand.randrange(1, machineNo+1, 1))
                machine_st1.sort()
                machine_st1_string = ','.join(str(e) for e in machine_st1)
                stage2Machines.append(machine_st1_string)

        d = {'Job ID': jobID,
             'Stage-1 Processing Time': stage1P,
             'Stage-2 Processing Time': stage2P,
             'Stage-1 Machines': stage1Machines,
             'Stage-2 Machines': stage2Machines,
             'Due Time': dueTime}

        df = pd.DataFrame(data=d, index=jobID)
        testName = 'test' + str(testnum)
        df.to_csv(
            'C:/Users/hsiao/OneDrive/文件/GitHub/gurobi/CA2/500tests/' + testName + '.csv')


instance_creator()

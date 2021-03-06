import pandas as pd
import numpy as np
import random as rand

# job 數

# machine 數

# stage1 stage2 prcoess time

# due time

# 是否有 stage 2


def instance_creator():
    for testnum in range(30):
        # 隨機產生 job 數量
        testCaseNo = rand.randrange(10, 30)

        # 根據 testCaseNo 隨機產生相對應變數
        jobID = list(range(1, testCaseNo+2))
        stage1P = (np.random.rand(1, testCaseNo+1) * 10).flatten()
        stage2P = (np.random.rand(1, testCaseNo+1) * 10).flatten()
        dueTime = []
        for i in range(testCaseNo+1):
            d = rand.uniform(stage1P[i] + stage2P[i], 24.0)
            dueTime.append(d)

        # 規定 Machine 數
        machineNo = rand.randrange(1, 20)
        machines = list(range(1, machineNo+1))

        # 產生 Machine lists
        stage1Machines = []
        for i in range(0, testCaseNo+1):
            machine_st1 = rand.sample(
                machines, rand.randrange(1, machineNo+1, 1))
            machine_st1.sort()
            machine_st1_string = ','.join(str(e) for e in machine_st1)
            stage1Machines.append(machine_st1_string)

        stage2Machines = []
        for i in range(0, testCaseNo+1):
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
        df['Stage-1 Machines'] = df['Stage-1 Machines'].astype(str)
        df['Stage-2 Machines'] = df['Stage-2 Machines'].astype(str)
        testName = 'test' + str(testnum)
        df.to_csv('./tests/' + testName + '.csv')


instance_creator()

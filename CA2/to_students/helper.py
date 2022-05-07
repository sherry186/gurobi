

import pandas as pd
import time

df = pd.read_csv('./to_students/data/instance 2.csv')

tic = time.perf_counter()


def ParseMachines(machineString):
    return machineString.split(",")


def MachineCanDoJob(job, machine):
    if(job[0] == 0):
        if(df['Stage-1 Machines'][job[1]-1].find(str(machine)) == -1):
            return False
        else:
            return True
    else:
        if(df['Stage-2 Machines'][job[1]-1].find(str(machine)) == -1):
            return False
        else:
            return True


print(MachineCanDoJob((0, 11), 1))

while(time.perf_counter() - tic < 10):
    continue

print(ParseMachines("1"))

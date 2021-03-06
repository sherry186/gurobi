from distutils.log import error
from huristicPaperStage1insertFixStage2 import huristicPaperStage1InsertFixStage2
from huristicPaper import huristicPaper
from huristic_sylvey_2_2_2 import huristic_sylvey
from huristic1_1_2 import huristic1_1_2
from huristicPaperStage1first import huristicPaperStage1First
from huristicPaperStage1insert import huristicPaperStage1Insert
from huristicPaperStage1insertFix import huristicPaperStage1InsertFix
# from huristicPaperStage1insertFixStage2 import huri
import csv


root = 'C:/Users/user/gurobi/CA2/500tests/test'
subfileName = ".csv"


# 開啟輸出的 CSV 檔案
# with open('huristicPaperStage1Insert.csv', 'w', newline='') as csvfile:
#   # 建立 CSV 檔寫入器
#   writer = csv.writer(csvfile)

#   # 寫入一列資料
#   writer.writerow(['path', 'tardy', 'makespan'])

#   tardyamount2_2_2 = 0
#   for i in range(0, 500):
#       path = root+ str(i) + subfileName
#       makespan, tardyamount = 0, 0
#       print(path)
#       try:
#         makespan, tardyamount = huristicPaperStage1Insert(path)
#         print(makespan, tardyamount)
#       except: 
#         # print(error)
#         continue
      
#       writer.writerow([path, tardyamount, makespan])

# with open('huristicPaperStage1First.csv', 'w', newline='') as csvfile:
#   # 建立 CSV 檔寫入器
#   writer = csv.writer(csvfile)

#   # 寫入一列資料
#   writer.writerow(['path', 'tardy', 'makespan'])

#   tardyamount2_2_2 = 0
#   for i in range(0, 500):
#       path = root+ str(i) + subfileName
#       makespan, tardyamount = 0, 0
#       print(path)
#       try:
#         makespan, tardyamount = huristicPaperStage1First(path)
#         print(makespan, tardyamount)
#       except: 
#         # print(error)
#         continue
      
#       writer.writerow([path, tardyamount, makespan])

# with open('huristicPaper.csv', 'w', newline='') as csvfile:
#   # 建立 CSV 檔寫入器
#   writer = csv.writer(csvfile)

#   # 寫入一列資料
#   writer.writerow(['path', 'tardy', 'makespan'])

#   tardyamount2_2_2 = 0
#   for i in range(0, 500):
#       path = root+ str(i) + subfileName
#       makespan, tardyamount = 0, 0
#       print(path)
#       try:
#         makespan, tardyamount = huristicPaper(path)
#         print(makespan, tardyamount)
#       except: 
#         # print(error)
#         continue
      
#       writer.writerow([path, tardyamount, makespan])

# with open('huristic1_1_2.csv', 'w', newline='') as csvfile:
#   # 建立 CSV 檔寫入器
#   writer = csv.writer(csvfile)

#   # 寫入一列資料
#   writer.writerow(['path', 'tardy', 'makespan'])

#   tardyamount2_2_2 = 0
#   for i in range(0, 500):
#       path = root+ str(i) + subfileName
#       makespan, tardyamount = 0, 0
#       print(path)
#       try:
#         makespan, tardyamount = huristic1_1_2(path)
#         print(makespan, tardyamount)
#       except: 
#         # print(error)
#         continue
      
#       writer.writerow([path, tardyamount, makespan])
     
    
with open('huristicPaperStageInsertFix.csv', 'w', newline='') as csvfile:
  # 建立 CSV 檔寫入器
  writer = csv.writer(csvfile)

  # 寫入一列資料
  writer.writerow(['path', 'tardy', 'makespan', 'tardy2', 'makespan2'])

  tardyamount2_2_2 = 0
  for i in range(500):
      path = root + str(i) + subfileName
      makespan, tardyamount = 0, 0
      makespan2, tardyamount2 = 0, 0
      print(path)
      try:
        makespan, tardyamount = huristicPaperStage1InsertFix(path)
        print(makespan, tardyamount)
      except: 
        # print(error)
        continue

      try:
        makespan2, tardyamount2 = huristicPaperStage1InsertFixStage2(path)
        print(makespan2, tardyamount2)
      except: 
        # print(error)
        continue
      
      writer.writerow([path, tardyamount, makespan, tardyamount2, makespan2])
 

# with open('huristicPaperStageInsertFixStage2Instance.csv', 'w', newline='') as csvfile:
#   # 建立 CSV 檔寫入器
#   writer = csv.writer(csvfile)

#   # 寫入一列資料
#   writer.writerow(['path', 'tardy', 'makespan'])

#   tardyamount2_2_2 = 0
#   for i in range(1, 6):
#       path = root + str(i) + subfileName
#       makespan, tardyamount = 0, 0
#       print(path)
      
      
#       writer.writerow([path, tardyamount, makespan])
 



   
from huristicPaper import huristicPaper
from huristic_sylvey_2_2_2 import huristic_sylvey
from huristic1_1_2 import huristic1_1_2
import csv

root = 'C:/Users/user/gurobi/CA2/500tests/test'
subfileName = ".csv"


# 開啟輸出的 CSV 檔案
with open('output.csv', 'w', newline='') as csvfile:
  # 建立 CSV 檔寫入器
  writer = csv.writer(csvfile)

  # 寫入一列資料
  writer.writerow(['path', 'tardy', 'makespan'])

  tardyamount2_2_2 = 0
  for i in range(0, 500):
      path = root+ str(i) + subfileName
      makespan, tardyamount = huristicPaper(path)
      writer.writerow([path, tardyamount, makespan])







    
    # print('tardyamount', tardyamount)
    # print('makespan', makespan)
    # # print('resultList', resultList)
    # print('\n')

    # makespan, tardyamount = huristic_sylvey(path)
    
    # print('tardyamount', tardyamount)
    # print('makespan', makespan)
    # # print('resultList', resultList)
    # print('\n')

    # makespan, tardyamount = huristic1_1_2(path)
    
    # print('tardyamount', tardyamount)
    # print('makespan', makespan)
    # # print('resultList', resultList)
    # print('\n')
    # print('======================================')



   
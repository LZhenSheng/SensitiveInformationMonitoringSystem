import os

import xlwt

def save(data):
    os.remove('tools/mydata.xls')
    xls = xlwt.Workbook()
    k=0
    sht1 = xls.add_sheet('sheet1', cell_overwrite_ok=True)
    print(data)
    print(len(data))
    for key in data:
        sht1.write(k,0,key)
        sht1.write(k,1,data.get(key))
        k=k+1
    xls.save('tools/mydata.xls')
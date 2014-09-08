from xlwt import Workbook
from pymongo import *

#from VictoriaConfig import *
from lowesConfig import *

def xlsWrite(catalog_list,filename):
        book = Workbook()
        sheet = book.add_sheet("sheet")
        attribute_list = ["product_id","title","price","category","brand","page_url","img_url"]
        i = 0
        for attribute in attribute_list:
            sheet.write(0,i,attribute)
            i += 1

        for i in range(5):
            sheet.col(i).width = 5000

        row_index = 1
        for item in catalog_list:
            col_index = 0
            curr_row = sheet.row(row_index)
            row_index += 1
            for attribute in attribute_list:
                if attribute in item:
                    curr_row.write(col_index,item[attribute])
                col_index += 1
        book.save(filename)


db = Connection()[db_name]["data"]
catalog_list = []
for item in db.find():
    catalog_list.append(item)

xlsWrite(catalog_list,filename)
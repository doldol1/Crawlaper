import xlsxwriter
import xlrd
import os

def filter(file_names):
    
    #통합할 파일
    wt_app_sheetnum=1
    wt_app_workbook=xlsxwriter.Workbook('integrated_file.xlsx', {'strings_to_urls':False})
    wt_app_worksheet=wt_app_workbook.add_worksheet()

    #쓸 파일의 row, col
    wt_row=0
    wt_col=0

    for file_name in file_names:

        if 'xls' or 'xlsx' in file_name:
            #기사 선별
            ex_path=os.getcwd()+'\\'+file_name
            print(ex_path)
            #읽을 파일
            rd_workbook=xlrd.open_workbook(ex_path)
            rd_worksheet=rd_workbook.sheet_by_index(0)
            


            #읽은 엑셀 파일의 총 row와 col수
            tot_rows=rd_worksheet.nrows
                
            #읽을 엑셀 파일 row, col
            for row in range(0, tot_rows):
                for value in rd_worksheet.row_values(row):
                    wt_app_worksheet.write(wt_row, wt_col, value)
                    wt_col=wt_col+1
                
                wt_row+=1
                wt_col=0
    wt_app_workbook.close()
    
def main():
    file_names=os.listdir(os.getcwd())
    filter(file_names)

if __name__ == '__main__':
    main()
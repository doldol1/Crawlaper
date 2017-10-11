#string refiner: remove special character
import re
import xlrd
import xlwt
import os

#file_name='D:\scrapper\노화\\2007~2008년 노화 뉴스 스크래핑.xls'

def refiner(file_name):
    #사용할 엑셀 sheet번호
    wt_sheetnum=1
    
    #엑셀 읽기
    rd_workbook=xlrd.open_workbook(file_name)
    rd_worksheet=rd_workbook.sheet_by_index(0)

    #엑셀 쓰기
    wt_workbook=xlwt.Workbook(encoding='utf-8')
    wt_worksheet=wt_workbook.add_sheet('Sheet'+str(wt_sheetnum))
    
    #읽은 엑셀 파일의 총 row와 col수
    tot_rows=rd_worksheet.nrows
    tot_cols=rd_worksheet.ncols

    #읽을 엑셀 파일 row, col
    rd_row=0
    rd_col=4

    #쓸 파일의 row, col
    wt_row=0
    wt_col=4
   

    while rd_row < tot_rows:
        while True:
        
            #print('{}, {}'.format(rd_row, rd_col))
            try:
                cell=rd_worksheet.cell_value(rd_row, rd_col)
            except:
                #print('개행 {}'.format(rd_row))
                rd_col=4
                wt_col=4
                break
            if cell:
                wt_worksheet.write(wt_row, wt_col, re.sub("[^().가-힣0-9a-zA-Z\\s]","",cell))
                rd_col+=1
                wt_col+=1
                #print(cell)
            else:
                rd_col=4
                wt_col=4
                break
            
        wt_row+=1
        rd_row+=1
        
    file_name=file_name.replace('.xls','')+'_ref.xls'
    wt_workbook.save(file_name)
    #wt_workbook.save('a.xls')
        
def main():
    file_list=os.listdir('D:\scrapper\삶의 질')
    print(file_list)
    for file_name in file_list:
        refiner('D:\scrapper\삶의 질\\'+file_name)
    refiner('D:\scrapper\삶의 질\\2016년 7월~2017년 5월 17일 \'삶의 질\' 뉴스 스크래핑.xls')
    
if __name__=='__main__':
    main()
    
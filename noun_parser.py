from konlpy.tag import Hannanum
import xlwt
import xlrd

file_name='D:\scrapper\사회적기업\원본\\2000~2010년 사회적기업 뉴스 스크래핑.xls'

def parser():
    
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

    #읽을 엑셀 파일 row, col변수 초기화
    rd_num_row=0
    rd_num_col=4

    #쓸 파일의 row
    wt_row_contents=0
    
    #쓸 파일의 col, inpagenum은 해당 기사 안에서 몇 번째 단어인지 넘버링할 때 사용할 col, pagenum은 해당 기사가 있는 원본 excel 파일의 row를 표시할 col, contentnum은 분리한 단어가 입력될 col을 의미한다.
    wt_col_inpagenum=0
    wt_col_pagenum=1
    wt_col_contentnum=2

    #각 셀 안에 들어갈 정보, inpage는 해당 기사 안에서 몇 번째 단어인지 표시, page는 몇 번째 기사에서 추출한 단어인지 표시, content는 추출한 단어 그 자체
    ct_inpage=1
    ct_page=str(rd_num_row+1)+'th page nouns'
    ct_content=''

    hannanum=Hannanum()

    print('분석할 엑셀 파일의 행 수는 '+str(tot_rows)+'이고 열 수는 '+str(tot_cols))

    while rd_num_row < tot_rows:

            
        ct_cell=rd_worksheet.cell_value(rd_num_row, rd_num_col)
        noun_list=hannanum.nouns(ct_cell)

        ct_inpage=1

        for ct_content in noun_list:
            print(str(wt_sheetnum)+'th Sheet, '+str(wt_row_contents)+'th row, '+str(ct_inpage)+'th noun is '+str(ct_content))
            if wt_row_contents > 65534:
                wt_sheetnum=wt_sheetnum+1
                wt_worksheet=wt_workbook.add_sheet('Sheet'+str(wt_sheetnum))
                wt_row_contents=0
            wt_worksheet.write(wt_row_contents, wt_col_inpagenum, str(ct_inpage))
            wt_worksheet.write(wt_row_contents, wt_col_pagenum, ct_page)
            wt_worksheet.write(wt_row_contents, wt_col_contentnum, ct_content)
            
            wt_row_contents=wt_row_contents+1
            ct_inpage=ct_inpage+1
        
        rd_num_row=rd_num_row+1
        ct_page=str(rd_num_row+1)+'th page nouns'
    
    wt_workbook.save('noun_result.xls')


def main():
    parser()

if __name__ == '__main__':
    main()
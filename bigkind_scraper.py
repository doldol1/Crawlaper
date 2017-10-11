#bigkind scraper

import urllib, urllib.request
import http.cookiejar
import pprint
import lxml.html
import bs4
import sys
import datetime
import re
import time


OR_URL='http://www.kinds.or.kr/'


#####20170703이전: 쿠키와 파라미터를 적용한 POST전송-

#####20170703: 꼭 쿠키가 필요한 것이 아니었음(쿠키 삭제). data에 들어갈 값을 모두 string 으로 해 주니 돌아가기 시작한다고 생각하였으나, 내부적으로 자바스크립트를 돌려서 값을 다시 받아오는 것을 확인 
######1차 목표: 페이지 내 값 추출.
######2차 목표: 검색결과 목록 페이지 이동
#########

# data={'pageInfo':'bksMain', 'login_chk':'null', 'LOGIN_SN':'null', 'LOGIN_NAME':'null', 'indexName':'news', 'keyword':'금강 둑', 'byLine':'', 'searchScope':'1', 'searchFtr':'1', 'startDate':'', 'endDate':'', 'sortMethod':'date', 'contentLength':'100', 'providerCode':'', 'categoryCode':'', 'incidentCode':'', 'dateCode':'', 'highlighting':'true', 'sessionUSID':'', 'sessionUUID':'test', 'listMode':'', 'categoryTab':'', 'newsId':'', 'filterProviderCode':'', 'filterCategoryCode':'', 'filterIncidentCode':'', 'filterDateCode':'', 'filterAnalysisCode':'', 'startNo':'1', 'resultNumber':'100', 'topmenuoff':'', 'resultState': '', 'keywordJson':'{"searchDetailTxt1":"금강 둑","agreeDetailTxt1":"","needDetailTxt1":"","exceptDetailTxt1":"","o_id":"option1","startDate":"","endDate":"","providerNm":"","categoryNm":"","incidentCategoryNm":"","providerCode":"","categoryCode":"","incidentCategoryCode":"","searchFtr":"1","searchScope":"1","searchKeyword":"금강 둑"}', 'keywordFilterJson':'', 'realKeyword':'', 'totalCount':'', 'interval':'', 'quotationKeyword1':'', 'quotationKeyword2':'', 'quotationKeyword3':'', 'searchFromUseYN':'N', 'mainTodayPersonYn':'', 'period':'all'}

data={'pageInfo':'newsResult', 'login_chk':'null', 'LOGIN_SN':'null', 'LOGIN_NAME':'null', 'indexName':'news', 'keyword':'금강 둑', 'byLine':'', 'searchScope':'1', 'searchFtr':'1', 'startDate':'', 'endDate':'', 'sortMethod':'date', 'contentLength':'100', 'providerCode':'', 'categoryCode':'', 'incidentCode':'', 'dateCode':'', 'highlighting':'true', 'sessionUSID':'', 'sessionUUID':'test', 'listMode':'', 'categoryTab':'', 'newsId':'', 'filterProviderCode':'', 'filterCategoryCode':'', 'filterIncidentCode':'', 'filterDateCode':'', 'filterAnalysisCode':'', 'startNo':'1', 'resultNumber':'100', 'topmenuoff':'', 'resultState':'detailSearch', 'keywordJson':'{"searchDetailTxt1":"금강 둑","agreeDetailTxt1":"","needDetailTxt1":"","exceptDetailTxt1":"","o_id":"option1","startDate":"","endDate":"","providerNm":"","categoryNm":"","incidentCategoryNm":"","providerCode":"","categoryCode":"","incidentCategoryCode":"","searchFtr":"1","searchScope":"1","searchKeyword":"금강 둑"}', 'keywordFilterJson':'', 'realKeyword':'', 'totalCount':'3868', 'interval':'', 'quotationKeyword1':'', 'quotationKeyword2':'', 'quotationKeyword3':'', 'searchFromUseYN':'N', 'mainTodayPersonYn':'', 'period':'all'}

url='http://www.kinds.or.kr/news/newsResult.do'


# res_file=open('res_file2.html', 'w', encoding='utf-8')
# s=response.read().decode('utf-8')
# res_file.write(s)

def html_extract(url, data):
    
    bs_list=[] #bs타입의 리턴값을 저장할 리스트
    webpage_no=1 #웹 페이지 번호
    error_count=0 #404 error 발생 횟수를 저장
    ##data encoding후 추출
    while webpage_no<=(int(data['totalCount'])/int(data['contentLength'])+1) :
        print(str(webpage_no)+'번째 페이지를 추출합니다.')
        #페이지 세팅
        data['startNo']=str(webpage_no)
        encoded_data=urllib.parse.urlencode(data).encode("utf-8")
        
        
        try: #페이지 받아오기(자주 끊기므로, exception처리)
            html_result=urllib.request.urlopen(url,encoded_data)
        except urllib.error.HTTPError:
            error_count+=1
            print('404 error is occured', error_count, 'time. Scraping will be retried, but if there are so many error(10 times), it will be cancelled')
            
            if error_count<20: #20회 이상 에러 발생시 강제 종료
                continue
            else:
                print('Error hell. Please execute script again. Maybe your network have some problem, or server does.')
                sys.exit(1) 
                break
        #bs객체화
        bs_result=bs4.BeautifulSoup(html_result, 'lxml', from_encoding='utf-8')
        bs_list.append(bs_result)
        webpage_no+=1
        # time.sleep(1)
        # max_page=bs_result.find("div", {"id":"resultExpression"}).get_text()
        # print('총 자료수는 '+max_page)
        # sys.exit(1)

        
###############홈페이지 내부의 문제로 아래 코드는 페이지-100건에서는 사용 불가.#############        
        #comments=bs_result.find_all(text=lambda text: isinstance(text, bs4.Comment))
        # for i in comments: #bigkind는 주석(comment)의 data_table_next의 유무로 페이지의 끝 확인
            # if i.count("data_table_next"):
                # k=i
                # break
            # else:
                # k=None
        
        # 마지막 페이지라면 종료, 아니라면 계속 찾기
        #if k and not bs_result.find(onclick='getSearchResultNew('+str(webpage_no+1)+')'): 
            # print(bs_result.find(onclick='getSearchResultNew('+str(webpage_no+1)+')'))
            #print(str(webpage_no)+'페이지는 마지막 페이지입니다.')
            #break
        #else:
            # print(bs_result.find(onclick='getSearchResultNew('+str(webpage_no+1)+')'))
            # webpage_no+=1
######################################################################
    return bs_list



def bs_extract(col, bs_list):
        
    col_datas=[]
    print(col+' 추출 작업을 시작했습니다.')
    ##if문을 활용하여 각 항목 추출
    if col=='제목':
        for bs_data in bs_list: #bs_list를 하나씩(한 페이지씩) 확인
            for raw_data in bs_data.find_all("div", {"class":"resTit"}): #한 페이지 안에 리스팅된 값들을 추출
                col_datas.append(raw_data.h3.get_text().strip('\n'))
    
    elif col=='언론사':
        for bs_data in bs_list: #bs_list를 하나씩(한 페이지씩) 확인
            for raw_data in bs_data.find_all("li", {"class":"resLogo list_provider"}):
                col_datas.append(raw_data.span.get_text())
    
    elif col=='기재일':
        for bs_data in bs_list: #bs_list를 하나씩(한 페이지씩) 확인
            for raw_data in bs_data.find_all("h3", {"class":"list_newsId"}):
                news_id=raw_data.attrs['id']
                ##list_newsId class를 통해 식별할 수 있는 h3 tag에서 id속성 추출 및 기재일로 가공
                date_data=news_id.split('.')[1]
                formed_date=date_data[:4]+'.'+date_data[4:6]+'.'+date_data[6:8]
                # print(formed_date)
                col_datas.append(formed_date)
    
    elif col=='본문': #본문의 경우, 직접 링크를 타고 들어가 본문 추출
        basic_url='http://www.kinds.or.kr/news/detailView.do?docId='
        page_count=1
        for bs_data in bs_list: #bs_list를 하나씩(한 페이지씩) 확인
            print(str(page_count)+'번째 페이지 추출이 진행중입니다.')
            for raw_data in bs_data.find_all("h3", {"class":"list_newsId"}):
                news_id=raw_data.attrs['id']
                ##list_newsId class를 통해 식별할 수 있는 h3 tag에서 뉴스 id추출
                id_date=news_id.split('_')
                whole_st=basic_url+id_date[1]
                ##링크를 타고 들어가 본문 파싱
                
                while True: #urlopen exception처리(자주 끊기므로)
                    try:
                        # print(whole_st)
                        html=urllib.request.urlopen(whole_st)
                    except urllib.error.HTTPError: 
                        continue
                    break
                
                bs=bs4.BeautifulSoup(html, 'lxml', from_encoding='utf-8')
                main_st=str(bs).split('CONTENT')[1].split('}')
                ##본문 중 분석에 방해되는 태그, 특수문자 제거(추후 가능하다면 정규식으로 교체)
                formed_st=main_st[0].replace('<br/>','')
                formed_st=formed_st.strip('":"')
                formed_st=formed_st.strip()
                formed_st=formed_st.replace('\\', ' ')#\를 구분자로 사용하기 때문에 본문의 \는 제거
                
                # print(formed_st)
                # time.sleep(2)
                col_datas.append(formed_st)
            page_count+=1
    else:
        print('Program has been currupted. Please call developer. bigman@kiost.ac.kr')
        sys.exit(1)
    return col_datas

def naming(data):
    file_name=str()
    
    if not data['startDate']:
        file_name+='처음부터'
    else:
        file_name+=data['startDate'].replace('-','_')
    
    if not data['endDate']:
        file_name+='~'+datetime.datetime.now().strftime('%Y_%m_%d')
    else:
        file_name+='~'+data['endDate'].replace('-','_')
    
    file_name+=' '+data['keyword']+' 관련 뉴스 스크래핑'    
    return file_name
    
    
def main(url, data):
    ##웹에서 source추출 함수(url, data) return list(bs)
    bs_list=html_extract(url, data)
    #print(bs_list)

    ##loop&flag:  각 수집정보(제목, 언론사, 기재일, 본문) 추출함수(list(bs)) retrun list(str)
    #cols=('제목', '언론사', '기재일', '본문')
    cols=['제목', '언론사', '기재일', '본문']
    insert_list=[]
    for col in cols:
        refined_list=bs_extract(col, bs_list)
        
        for index_num in range(0, len(refined_list)):
            
            if col=='제목':
                insert_list.append(refined_list[index_num])
            else:
                insert_list[index_num]=insert_list[index_num]+'\\'+refined_list[index_num]
    
    ##네이밍 함수(data) retrun str
    print('추출한 데이터를 파일로 만드는 중입니다.')
    file_name=naming(data)
    final_file=open(file_name+'.txt', 'w', encoding='utf-8')
    for file_st in insert_list:
        final_file.write(file_st+'\n')

    ##각 수집정보 통합, 저장 함수(list(str:제목), list(str:언론사), list(str:기재일), list(str:본문)) return list(str)
    ##main 함수에서 쓰기
    ##끝
    print('Complete all task')

if __name__=='__main__':
    main(url, data)
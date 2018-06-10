from . import Urllist_server
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib
import re
import xlsxwriter
import xlrd
import datetime

#기능성식품 전 기간, 모든 옵션 미적용
target_url='https://search.naver.com/search.naver?where=news&'\
'query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
'ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&'\
'ds=&de=&docid=&'\
'nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&'\
'mson=0&refresh_start=0&related=0'

target_url='https://search.naver.com/search.naver?ie=utf8&where=news&'\
'query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&'\
'ds=&de=&docid=&'\
'nso=so:r,p:all,a:all&mynews=1&cluster_rank=22&start=1&refresh_start=0'


#기능성식품 전 기간, 주류 언론사 옵션 적용-처음 들어갔을 때
target_url='https://search.naver.com/search.naver?where=news&'\
'query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
'ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&'\
'ds=2000.01.01&de=2017.10.16&docid=&'\
'nso=so%3Ar%2Cp%3Afrom20000101to20171016%2Ca%3Aall&mynews=1&'\
'mson=0&refresh_start=0&related=0'

#기능성식품 전 기간, 주류 언론사 옵션 적용-2페이지로 이동
target_url='https://search.naver.com/search.naver?ie=utf8&where=news&'\
'query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&'\
'ds=2000.01.01&de=2017.10.16&docid=&'\
'nso=so:r,p:from20000101to20171016,a:all&mynews=1&cluster_rank=11&start=11'

#기능성식품 전 기간, 주류 언론사 옵션 적용-다시 1페이지로 이동
target_url='https://search.naver.com/search.naver?ie=utf8&where=news&'\
'query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&'\
'ds=2000.01.01&de=2017.10.16&docid=&'\
'nso=so:r,p:from20000101to20171016,a:all&mynews=1&cluster_rank=21&start=1'
#https://search.naver.com/search.naver?ie=utf8&where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2000.01.01&de=2017.10.16&docid=&nso=so:r,p:from20000101to20171016,a:all&mynews=1&cluster_rank=21&start=1

#파리넬리(sample news)
target_url='https://search.naver.com/search.naver?'\
'ie=utf8&where=news&'\
'query=%ED%8C%8C%EB%A6%AC%EB%84%AC%EB%A6%AC&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&'\
'de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=54&start=1&'\
'refresh_start=0'

target_url='https://search.naver.com/search.naver?'\
'ie=utf8&where=news&'\
'query=%ED%8C%8C%EB%A6%AC%EB%84%AC%EB%A6%AC&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&'\
'de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=28&start=1&'\
'refresh_start=0'
#https://search.naver.com/search.naver?ie=utf8&where=news&query=%ED%8C%8C%EB%A6%AC%EB%84%AC%EB%A6%AC&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=54&start=1&refresh_start=0

#씨프(sample news)
# target_url='https://search.naver.com/search.naver?'\
# 'ie=utf8&where=news&query=%EC%94%A8%ED%94%84&'\
# 'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&'\
# 'de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=23&start=1&refresh_start=0'

# https://search.naver.com/search.naver?ie=utf8&where=news&query=%EC%94%A8%ED%94%84&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=23&start=1&refresh_start=0

# 사회적기업
# target_url='https://search.naver.com/search.naver?'\
# 'ie=utf8&where=news&'\
# 'query=%EC%82%AC%ED%9A%8C%EC%A0%81%EA%B8%B0%EC%97%85&'\
# 'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&'\
# 'docid=&nso=so:r,p:all,a:all&mynews=1&cluster_rank=40&start=1&refresh_start=0'

#모든 신문
target_url='https://search.naver.com/search.naver?where=news&'\
'query=%EC%82%AC%ED%9A%8C%EC%A0%81%EA%B8%B0%EC%97%85&'\
'ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&'\
'docid=&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&mson=0&refresh_start=0&'\
'related=0'

#주요신문만
target_url='https://search.naver.com/search.naver?where=news&'\
'query=%EC%82%AC%ED%9A%8C%EC%A0%81%EA%B8%B0%EC%97%85&'\
'ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&'\
'docid=&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&mson=0&refresh_start=0&'\
'related=0'

#어떤 조건인지 모르겠으나 랜덤하게 주요신문만 잡힐 때도 존재함, 다행이 제목+내용검색과 제목 검색은 nso=so:r,p:all,a:all과 nso=so:r,p:all,a:t로 조금씩 다름
target_url='https://search.naver.com/search.naver?ie=utf8&where=news&'\
'query=%EC%82%AC%ED%9A%8C%EC%A0%81%EA%B8%B0%EC%97%85&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&'\
'docid=&nso=so:r,p:all,a:all&mynews=1&cluster_rank=20&start=1&refresh_start=0'


target_url='https://search.naver.com/search.naver?&where=news&'\
'query=%EC%84%B8%EC%9B%94%ED%98%B8&'\
'sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&'\
'ds=2014.04.14&de=2018.03.05&docid=&nso=so:r,p:from20140414to20180305,a:all&'\
'mynews=1&cluster_rank=35&start=1&refresh_start=0'

target_url='https://search.naver.com/search.naver?&where=news&'\
'query=%EC%84%B8%EC%9B%94%ED%98%B8&'\
'sm=tab_pge&sort=0&photo=0&field=1&reporter_article=&pd=3&'\
'ds=2014.04.14&de=2018.03.05&docid=&'\
'nso=so:r,p:from20140414to20180305,a:t&mynews=1&cluster_rank=38&'\
'start=1&refresh_start=0'




#첫째 줄: 네이버 뉴스검색(모든 뉴스검색에 필수적으로 들어가는 요소)
#둘째 줄: query는 검색어를 말함. ASCII를 인코딩해야 됨



#url의 마지막에 있는 cluster_rank는 검색할 때마다 올라가는데, 줄여 줄 필요가 있어 보인다.

class data_box:
    def __init__(self):
        self.news_subject='default'
        self.news_date='default'
        self.news_press='default'
        self.news_link='default'
        self.news_text='default'

    
class Naver_crawler:
    def __init__(self):
        pass
    def url_setter(self, target_url):
        splited_url=target_url.split('&')
        
        for splited in range(len(splited_url)):
            if 'cluster_rank=' in splited_url[splited]:
                splited_url[splited]='cluster_rank=0'
            elif 'start=' in splited_url[splited]:
                if 'refresh_start' in splited_url[splited]:
                    continue
                else:
                    start_number=int(splited_url[splited].split('=')[1])
                    start_number+=10
                    splited_url[splited]='start='+str(start_number)
            
        target_url='&'.join(splited_url)
        
        return target_url
        
    def crawling(self, target_url, press_cookie=None):#말 그대로 크롤링에만 집중
        
        page_quit=True
        present_page='1'
        last_page=''
        source_stack=list()
        splited_url=target_url.split('&')
        


        for splited in range(len(splited_url)):
            if 'ds=' in splited_url[splited]:
                start_day=splited_url[splited].replace('ds=','')
            elif 'de=' in splited_url[splited]:
                end_day=splited_url[splited].replace('de=','')

                
        while int(present_page) < 410:#네이버가 한번에 내놓을 수 있는 검색결과 페이지가 400개 이기 때문에 넉넉함
            try:
                if press_cookie is not None:
                    req_instance=urllib.request.Request(target_url, headers=press_cookie)
                else:
                    req_instance=urllib.request.Request(target_url)
                # print(target_url)
                page_code=urllib.request.urlopen(req_instance)
                
            except urllib.error.URLError as e:
                print("Naver와 접속되지 않습니다. 다시 접속을 시도합니다.")
                
            bs_page=BeautifulSoup(page_code, 'lxml', from_encoding='utf-8')

            
            if bs_page.find('div',{'class':'paging'}).find('strong')==None:
                print('총 페이지는 {0}입니다.'.format(present_page))
                break
            else:
                present_page=bs_page.find('div',{'class':'paging'}).find('strong').get_text()
                if last_page==present_page:
                    print('총 페이지는 {0}입니다.'.format(present_page))
                    break
                last_page=present_page
                source_stack.append(bs_page)
                print('{0}~{1}에 해당되는 {2}페이지의 소스를 저장했습니다.'.format(start_day, end_day, present_page))
                target_url=self.url_setter(target_url)
                req_instance
                
        return source_stack

class Naver_scraper:
    def __init__(self):
        pass
    def scraping(self, source_stack):
        databox_list=list()
        datapage_num=1
        # for i in range(len(source_stack)):
            # print(str(i)+'번째 Data를 추출합니다.')
            # data_chunk=data_box()
            # for data in source_stack[i].find('ul', {'class':'type01'}).find_all('dl'):
        for source in source_stack:
            print(str(datapage_num)+'page의 Data를 추출합니다.')
            
            for data in source.find('ul', {'class':'type01'}).find_all('dl'):  
                data_chunk=data_box()
                data_chunk.news_subject=data.find('a').get_text()#제목 추출
                # print(data_chunk.news_subject)
                
                data_chunk.news_date=re.search('([0-9]{4}.[0-9]{2}.[0-9]{2})|([0-9]{1,2}일 전)|([0-9]{1,2}분 전)|([0-9]{1,2}시간 전)',data.dd.get_text()).group()#날자 추출(일반날자, 시간전, 일전)
                # print(data_chunk.news_date)

                data_chunk.news_press=data.dd.find('span').get_text()
                # print(data_chunk.news_press)

                data_chunk.news_link=data.find('dt').a['href']
                # print(data_chunk.news_link)

                if data.dd.a.get_text()=='네이버뉴스':
                    bs_tmp=BeautifulSoup(urllib.request.urlopen(data.dd.a['href']), 'lxml', from_encoding='utf-8')
                    if bs_tmp.find('div', {'id':'articleBodyContents'}):
                        data_chunk.news_text=bs_tmp.find('div', {'id':'articleBodyContents'}).get_text()
                    elif bs_tmp.find('div', {'id':'articeBody'}):
                        data_chunk.news_text=bs_tmp.find('div', {'id':'articeBody'}).get_text()
                    # print(data_chunk.news_text)
                else:
                    data_chunk.news_text='Because of irregular form, unable to scrape news.'
                    
                data_chunk.news_text=data_chunk.news_text.replace('// flash ','')
                data_chunk.news_text=data_chunk.news_text.replace('오류를 우회하기 위한 함수 추가','')
                data_chunk.news_text=data_chunk.news_text.replace('function', '')
                
                data_chunk.news_text=data_chunk.news_text.replace('_flash_removeCallback() {}', '')
                data_chunk.news_text=data_chunk.news_text.strip()
                # data_chunk.news_text=data_chunk.news_text.replace(',' , ' ') 엑셀 옵션일때는 안해도 됨
                data_chunk.news_text=data_chunk.news_text.replace('\n' , '')
                data_chunk.news_text=data_chunk.news_text.replace('\t' , ' ')

                databox_list.append(data_chunk)
                # print(data_chunk.news_subject)
            
            for tmp_data in databox_list:
                print(tmp_data.news_subject)
            datapage_num+=1
            # print('해당 url의 data추출이 끝났습니다.')
            
        return databox_list
        
class Naver_datasaver:
    def __init__(self, target_url):
        splited_url=target_url.split('&')
        for splited in range(len(splited_url)):
            if 'ds=' in splited_url[splited]:
                self.start_day=splited_url[splited].replace('ds=','')
            elif 'de=' in splited_url[splited]:
                self.end_day=splited_url[splited].replace('de=','')
            elif 'query=' in splited_url[splited]:
                self.query_name=splited_url[splited].replace('query=','')
                # self.query_name=self.query_name.decode()
                self.query_name=urllib.parse.unquote(urllib.parse.unquote(self.query_name))
                self.query_name=self.query_name.split('+')[0]
            else:
                pass
        

        
        self.saver_name=self.start_day+'-'+self.end_day+'년 '+self.query_name+' 뉴스 조사'
        print('저장될 파일의 이름은', self.saver_name, '입니다.')
    
    def save_excel(self, databox_list):
        wt_row=0
        wt_col=0
    
        wt_workbook=xlsxwriter.Workbook(self.saver_name+'.xlsx', {'strings_to_urls':False})
        wt_worksheet=wt_workbook.add_worksheet()
        
        for i in range(len(databox_list)):
            wt_worksheet.write(i,0,databox_list[i].news_subject)
            print(databox_list[i].news_subject)
            wt_worksheet.write(i,1,databox_list[i].news_date)
            wt_worksheet.write(i,2,databox_list[i].news_press)
            wt_worksheet.write(i,3,databox_list[i].news_link)
            wt_worksheet.write(i,4,databox_list[i].news_text)
        wt_workbook.close()
        
        
    def save_csv(self, databox_list):
        print('저장을 시작합니다.')
        # self.saver_name=self.saver_name+'.csv'
        file_stream=open(os.getcwd()+'//'+self.saver_name, 'w', encoding='utf-8')
        for data_chunk in databox_list:

            
            data_line=data_chunk.news_subject+','+data_chunk.news_date+','+data_chunk.news_press+','+data_chunk.news_link+','+data_chunk.news_text
            file_stream.write(data_line)
        file_stream.close()
        return
def main():
    list_instance=Urllist()
    crawler=Naver_crawler()
    scraper=Naver_scraper()
    
    press_cookie={'Cookie':'news_office_checked=1032,1005,2312,1020,2385,1021,1081,1022,2268,1023,1025,1028,1469'}
    
    the_list=list_instance.search_composer(target_url, start=datetime.date(2014,4,14))#총 url list추출
    
    print('리스트 측정이 끝났습니다.')
    # the_list=Urllist.search_composer(target_url) #만약 static method라면
    

    
    for list_url in the_list:#search_composer에서 추출한 url list에서 
        source_stack=crawler.crawling(list_url, press_cookie)
        
        databox_list=scraper.scraping(source_stack)
        the_saver=Naver_datasaver(list_url)
        print('파일 저장을 시작합니다.')
        the_saver.save_excel(databox_list)
        # for source in source_stack:
            # news_count=bs_instance.find('div',{'class': 'title_desc all_my'}).span.get_text()
            # print(re.search('[0-9]*,{0,1}[0-9]+건', news_count))
if __name__=='__main__':
    main()
from bs4 import BeautifulSoup
import urllib.request
import requests
import datetime
import re
import http.cookiejar
#이상한 검색어: asdkfdsl
# target_url='http://search.naver.com/search.naver?sm=tab_hty.top&where=news&'\
# 'query=asdkfdsl&'\
# 'oquery=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
# 'ie=utf8&tqi=TiH03spySDossvJNudwssssssvs-266552'

# https://search.naver.com/search.naver?where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=2000.01.01&de=2013.05.03&docid=&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&mson=0&refresh_start=0&related=0

# https://search.naver.com/search.naver?where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2000.01.01&de=2013.05.03&docid=&nso=so%3Ar%2Cp%3Afrom20000101to20130503%2Ca%3Aall&mynews=1&mson=0&refresh_start=0&related=0



#해당 기간에 없는 검색어: 용팔이
target_url='https://search.naver.com/search.naver?where=news&'\
'query=%EC%9A%A9%ED%8C%94%EC%9D%B4&'\
'ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&'\
'ds=2000.01.01&de=2000.01.02&docid=&'\
'nso=so%3Ar%2Cp%3Afrom20000101to20000102%2Ca%3Aall&mynews=0&'\
'mson=0&refresh_start=0&related=0'

#기능성식품 전 기간, 모든 옵션 미적용
target_url='https://search.naver.com/search.naver?where=news&'\
'query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
'ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&'\
'ds=&de=&docid=&'\
'nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&'\
'mson=0&refresh_start=0&related=0'

class Urllist:

    def __init__(self):

        self.MIN_RESULT=2500#최소한 이정도는 나올 수 있도록 기존에는 3000이었으나 루프가 많아져서 수정함
        self.MAX_RESULT=3900#결과가 더 나올 수 있으므로, 넉넉하게 여유 잡아
    
    def url_changer(self, target_url, start, end):
        splited_url=target_url.split('&')
        

        
        for splited in range(len(splited_url)):
            if 'ds=' in splited_url[splited]:
                splited_url[splited]="ds="+start.strftime("%Y.%m.%d")
                # print(start.strftime("%Y.%m.%d"))
            elif 'de=' in splited_url[splited]:
                splited_url[splited]="de="+end.strftime("%Y.%m.%d")
                # print(end.strftime("%Y.%m.%d"))
            elif 'pd=' in splited_url[splited]:
                splited_url[splited]="pd=3"
            elif 'nso=':#언론사와도 관련있는 듯 하니.. 참고
                if 'from' in splited_url[splited]:
                    tmp_nso=splited_url[splited].split('from')[0]
                    splited_url[splited]=tmp_nso+'from'+start.strftime("%Y%m%d")+'to'+end.strftime("%Y%m%d")+'%2Ca%3Aall'
                elif 'all' in splited_url[splited]:
                    splited_url[splited]=splited_url[splited].replace('all','')+'from'+start.strftime("%Y%m%d")+'to'+end.strftime("%Y%m%d")+'%2Ca%3Aall'
                    
            else:
                pass
        
        reunited_url='&'.join(splited_url)

        return reunited_url    
        
    
    def news_counter(self, bs_instance):
        news_count=bs_instance.find('div',{'class': 'title_desc all_my'}).span.get_text()
        
        news_count=int(re.search('[0-9]*,{0,1}[0-9]+건', news_count).group().replace(',','').replace('건', ''))
        return news_count
        
    
    def search_composer(self, target_url, url_list=None, start=datetime.date(2000,1,1), end=datetime.date.today()):
        
        url_list=url_list if url_list is not None else list()
        if end>datetime.date.today():
            end=datetime.date.today()
        composed_url=self.url_changer(target_url, start, end)
        
        html=None
        press_cookie={'Cookie':'news_office_checked=1032,1005,2312,1020,2385,1021,1081,1022,2268,1023,1025,1028,1469'}
        
        while html==None:
            try:
                
                req_instance=urllib.request.Request(composed_url, headers=press_cookie)
                html=urllib.request.urlopen(req_instance)

                
            except urllib.error.URLError as e:
                print(e)
                print("Naver와 접속되지 않습니다. 다시 접속을 시도합니다.")
                continue
            
        bs_instance=BeautifulSoup(html, 'lxml', from_encoding='utf-8')
            
        pivot=end-start
        
        if bs_instance.find('div', {'class':'noresult_tab'}):#범위 내 검색결과 없음
            if (start==datetime.date(2000,1,1)) & (end>=datetime.date.today()):#전체 없음
                print('검색 결과값이 존재하지 않습니다.')
                return url_list
            else:#여기에만 없음
                return self.search_composer(composed_url, url_list, start, start+pivot*1.25)
       

        else:#검색결과가 존재한다면 재귀형식으로 작동하는 알고리즘 작성
            news_count=self.news_counter(bs_instance)
            
            if (start==datetime.date(2000,1,1)) & (end>=datetime.date.today()):#전체 없음
                print('총',news_count,'개의 뉴스가 있습니다.')
            # if news_count>=4000 & news_count<=6000:
                # pivot=pivot/2
            # print('{0} to {1}: {2} data is searched'.format(start, end, news_count))
            if self.MAX_RESULT<news_count:
                # print('뉴스가 지나치게 많으니, 범위를 줄입니다.')
                return self.search_composer(composed_url, url_list, start, start+pivot*0.5)
            else:
                if self.MIN_RESULT>news_count:
                    if end==datetime.date.today():
                        url_list.append(composed_url)
                        print("{0} to {1}: {2} data is searched, append. I know it's not enough size, but it is the last result.".format(start, end, news_count))
                        return url_list
                    elif end>datetime.date.today():
                        print('Error: Future news')
                        return None
                    else:
                        # print('뉴스가 지나치게 적으니, 범위를 늘립니다.')
                        return self.search_composer(composed_url, url_list, start, start+pivot*1.25)
                else:
                    url_list.append(composed_url)
                    if end==datetime.date.today():
                        print('{0} to {1}: {2} data is searched, append. And this is the last'.format(start, end, news_count))
                        return url_list
                    elif end>datetime.date.today():
                        print('Error: Future news')
                        return None
                    else:
                        print('{0} to {1}: {2} data is searched, append'.format(start, end, news_count))
                        return self.search_composer(composed_url, url_list, end+datetime.timedelta(days=1), end+datetime.timedelta(days=1)+pivot*1.5)
                        

def main():
    listed=Urllist()
    the_list=listed.search_composer(target_url)
            
if __name__=='__main__':
    main()
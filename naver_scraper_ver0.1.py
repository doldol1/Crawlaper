#다시 만들어야 된다.. 젠장...
#변경된  스크래퍼는 GET방식으로 쿼리문이 비교적 간단해짐.. 여전히 4,000개 검색이 한계치임
#cluster_rank라는 요상한 쿼리가 생겼는데... hop의 횟수를 확인하는 파라미터인듯 하다... 만약 계속적인 정보 수집시 문제가 될 수 있으므로 0으로 초기화하는 것이 좋을 듯
#페이지 이동과 끝

from bs4 import BeautifulSoup
import urllib.request
import xlwt
import datetime
import re
'''
https://search.naver.com/search.naver?where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=&mynews=1&mson=0&refresh_start=0&related=0

https://search.naver.com/search.naver?ie=utf8&where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=1&cluster_rank=52&start=1&refresh_start=0

https://search.naver.com/search.naver?where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&mynews=1&mson=0&refresh_start=0&related=0


https://search.naver.com/search.naver?ie=utf8&where=news&query=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=1&cluster_rank=39&start=11&refresh_start=0
'''
#이상한 검색어: asdkfdsl
# target_url='http://search.naver.com/search.naver?sm=tab_hty.top&where=news&'\
# 'query=asdkfdsl&'\
# 'oquery=%EA%B8%B0%EB%8A%A5%EC%84%B1%EC%8B%9D%ED%92%88&'\
# 'ie=utf8&tqi=TiH03spySDossvJNudwssssssvs-266552'

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



MIN_RESULT=3000#최소한 이정도는 나올 수 있도록
MAX_RESULT=3900#결과가 더 나올 수 있으므로, 넉넉하게 여유 잡아

def url_changer(target_url, start, end):
    splited_url=target_url.split('&')
    
    for splited in range(len(splited_url)):
        if 'ds=' in splited_url[splited]:
            splited_url[splited]=='ds='+start.strftime("%Y.%m.%d")
            print(start.strftime("%Y.%m.%d"))
        elif 'de=' in splited_url[splited]:
            splited_url[splited]=='de='+end.strftime("%Y.%m.%d")
            print(end.strftime("%Y.%m.%d"))
        else:
            pass
    
    reunited_url='&'.join(splited_url)
    # print(target_url,'에서',reunited_url,'로 url이 변경되었습니다.')
    
    return reunited_url

def search_composer(target_url, url_list, start=datetime.date(2000,1,1), end=datetime.date.today()):

    composed_url=url_changer(target_url, start, end)
    # composed_url=target_url#임시 코드 위의 composed_url=url_changer(target_url, start, end)로 수정해야 함
    html=urllib.request.urlopen(composed_url)
    bs_instance=BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    
    if bs_instance.find('div', {'class':'noresult_tab'}):#범위 내 검색결과 없음
        if (start==datetime.date(2000,1,1)) & (end==datetime.date.today()):#전체 없음
            print('검색 결과값이 존재하지 않습니다.')
        else:#여기에만 없음
            return search_composer(composed_url, start, start+datetime.timedelta(365), url_list)
    else:#검색결과가 존재한다면 재귀형식으로 작동하는 알고리즘 작성
        print('it soom!')

'''
    
    if bs_instance.find('span', {'class': 'result_num'}):
        num_result=bs_instance.find('span', {'class': 'result_num'}).get_text()
        
        num_result=int(re.search('[0-9]*,{0,1}[0-9]+건', num_result).group().replace(',','').replace('건', ''))
        # print(num_result)
        td=end-start
        pivot=td#(3900/num_result)*td
        #pivot이 13035.714일 때 1년
        # print(pivot)
        
        if MIN_RESULT > num_result: ##최저기준치보다 결과값이 적을 때
            if datetime.date.today() < end:
                print('마지막 자료의 개수는',num_result,'개 이고',start.isoformat(),'부터', datetime.date.today(),'까지로 적당하므로, 리스트에 추가합니다.')
                url_list.append(url_changer(composed_url, start, datetime.date.today()))
                if url_list[-1] == url_list[-2]:
                    url_list.pop()
                return url_list
            else:
                # print('자료의 개수는',num_result,'개 이고',start.isoformat(),'부터', end.isoformat(),'까지는 너무 짧습니다.')
                return search_composer(composed_url, url_list, start, start+pivot*2)
        
        elif MAX_RESULT < num_result: ##최고기준치보다 결과값이 많을 때
            # print('자료의 개수는',num_result,'개 이고',start.isoformat(),'부터', end.isoformat(),'까지는 너무 깁니다.')
            return search_composer(composed_url, url_list, start, start+pivot*0.75)
        
        else:
            print('자료의 개수는',num_result,'개 이고',start.isoformat(),'부터', end.isoformat(),'까지로 적당하므로, 리스트에 추가합니다.')
            url_list.append(composed_url)
            # search_composer(composed_url, url_list, start+pivot, end+pivot)
            return search_composer(composed_url, url_list, start+datetime.timedelta(1)+pivot, end+pivot)
    else:
        if (start==datetime.date(2000,1,1)) & (end==datetime.date.today()):
            print('검색 결과값이 존재하지 않습니다.')
        else:
            print('해당 페이지의 값이 존재하지 않습니다.')
            return search_composer(composed_url, start, start+datetime.timedelta(365), url_list)
'''
# 메인 함수
def main():
    OR_URLS=list()
    OR_URLS=search_composer(target_url, OR_URLS)
    print('url 추출 작업 완료')
    get_text(OR_URLS=OR_URLS, OUTPUT_FILE_NAME=OUTPUT_FILE_NAME)
    
if __name__ == '__main__':
    main()
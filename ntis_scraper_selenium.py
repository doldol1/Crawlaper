from selenium import webdriver
from selenium.webdriver.support.ui import Select
from collections import defaultdict
import bs4
import sys
import re
'''
chrome_driver=webdriver.Chrome('D:/scrapper/web_driver/chromedriver.exe')

other_page=webdriver.Chrome('D:/scrapper/web_driver/chromedriver.exe')
#chrome_driver.implicitly_wait(3)

# chrome_driver.get('https://nid.naver.com/nidlogin.login')
chrome_driver.get('https://sso2.ntis.go.kr/3rdParty/loginFormPageID.jsp')

# chrome_driver.find_element_by_name('id').send_keys('waderer')
# chrome_driver.find_element_by_name('pw').send_keys('mt321671')
chrome_driver.find_element_by_name('userid').send_keys('doldol1')
chrome_driver.find_element_by_name('password').send_keys('Fish5321671!')

chrome_driver.find_element_by_class_name('btn_blue').click()

other_page.implicitly_wait(3)

other_page.get('http://rndgate.ntis.go.kr/switch.do?prefix=/ia/info&page=/ProjectGroup.do?method=iaProjectSubjectList&searchVO.yrFrom=2016&searchVO.yrTo=2016')
# chrome_driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
'''
# chrome_driver=webdriver.Chrome('D:/scrapper/web_driver/chromedriver.exe')

# chrome_driver.get('http://rndgate.ntis.go.kr/switch.do?prefix=/ia/info&page=/ProjectGroup.do?method=iaProjectSubjectList&searchVO.yrFrom=2016&searchVO.yrTo=2016')
# print(chrome_driver.window_handles)
# chrome_driver.find_element(By.LINK_TEXT, '로그인').click()
# chrome_driver.find_element_by_link_text("로그인").click()
# print(chrome_driver.window_handles)

# main_window=chrome_driver.window_handles[0]
# chrome_driver.switch_to.window(chrome_driver.window_handles[1])

# chrome_driver.find_element_by_name('userid').send_keys('doldol1')
# chrome_driver.find_element_by_name('password').send_keys('Fish5321671!')

# chrome_driver.find_element_by_class_name('btn_blue').click()

# chrome_driver.switch_to.window(main_window)

# html=chrome_driver.page_source

# soup=bs4.BeautifulSoup(html, 'lxml')

# res_file=open('res_file2.html', 'w', encoding='utf-8')
# s=soup.read().decode('utf-8')
# res_file.write(str(soup))

# print(str(soup))

####################NTIS Scaper Logic######################
## 1. NTIS의 검색페이지('http://rndgate.ntis.go.kr/switch.do?prefix=/ia/info&page=/ProjectGroup.do?method=iaProjectSubjectList&searchVO.yrFrom=2016&searchVO.yrTo=2016') 접속
## 2. NTIS로그인(Selenium)
## 3. 검색에 입력(Scraping대상이 많기 때문에 저장까지 마친 뒤 다음 검색어로 이동)
 ## 4. 페이지 수집(for search_box in '연구내용', '한글키워드', '영문키워드')
 ## -Scraping할 페이지 이동
 ## -먼저 각 페이지의 목록 수집
 ## -해당 페이지 목록 수집 뒤 각각의 세부 링크 정보 수집
 ## -모든 페이지의 Scraping
 ## 5. parsing 및 텍스트 정제, 중복 데이터 처리
 ## 6. 저장(css)
###########################################################
url='http://rndgate.ntis.go.kr/switch.do?prefix=/ia/info&page=/ProjectGroup.do?method=iaProjectSubjectList&searchVO.yrFrom=2016&searchVO.yrTo=2016'

keyword_list=['해양', '갈조류', '연어알', '감태', '우뭇가사리', '개다시마', '전복', '개청각', '진주', '구멍쇠미역', '참미역', '캐비어', '글루코사민', '김', '큰실말', '나래미역', '클로렐라', '납작파래', '키토산', '다시마', '톳', '돌미역', '퉁퉁마디', '멸치', '모자반', '플랑크톤', '미세조류', '함초', '미역', '해삼', '미역귀', '해조', '바다포도', '해조류', '불가사리', '상어연골', '스피룰리나', '스피루리나', '어류 콜라겐', '콜라겐']

eng_keywords=['ocean','brown algae','salmon roe','kajime','Gelidiumamansii','Kjellmaniella crassifolia','abalone','Codium dichotomum', 'pearl', 'Agarum cribrosum', 'Kjellmaniella gyrata', 'caviar', 'glucosamine', 'laver', 'phaeophyta', 'Alaria esculenta', 'chlorella', 'green confertii', 'chitosan', 'laminaria', 'hijiki', 'Brown Rock Seaweed', 'Salicornia europaea Linnaeus', 'engraulis japonicus', 'Sargassum fulvellum', 'plankton', 'microalgae', 'Salicornia europaea Linnaeus', 'Undaria pinnatifida','sea cucumber', 'Undaria pinnatifida', 'seaweed', 'Caulerpa lentillifera', 'seaweed', 'starfish', 'Shark cartilage', 'spirulina', 'spirulina', 'fish collagen', 'collagen']

keyword_list=['갈조류']

eng_keywords=['brown algae']


###완료 리스트###
## keyword_list=['해양','갈조류','연어알','감태','우뭇가사리','개다시마','전복','개청각','진주','구멍쇠미역','참미역','캐비어','글루코사민','김','큰실말', '나래미역', '클로렐라', '납작파래', '키토산', '다시마', '톳', '돌미역', '퉁퉁마디', '멸치', '모자반', '플랑크톤', '미세조류', '함초', '미역','해삼', '미역귀', '해조', '바다포도', '상어연골', '스피룰리나', '스피루리나', '어류 콜라겐', ]

## eng_keywords=['ocean','brown algae','salmon roe','kajime','Gelidiumamansii', 'Kjellmaniella crassifolia','abalone','Codium dichotomum','pearl','Agarum cribrosum', 'Kjellmaniella gyrata', 'caviar', 'glucosamine','laver','phaeophyta','Alaria esculenta','chlorella','green confertii','chitosan','laminaria', 'hijiki', 'Brown Rock Seaweed', 'Salicornia europaea Linnaeus', 'engraulis japonicus', 'Sargassum fulvellum', 'plankton', 'microalgae', 'Salicornia europaea Linnaeus', 'Undaria pinnatifida','sea cucumber', 'Undaria pinnatifida', 'seaweed', 'Caulerpa lentillifera','Shark cartilage', 'spirulina', 'spirulina', 'fish collagen', ]
################
# keyword_list= ['글루코사민','김','큰실말']
# eng_keywords=['glucosamine','laver','phaeophyta']
# keyword_list= ['해조류', '불가사리',]
# eng_keywords=[ 'seaweed', 'starfish',]

# keyword_list=['망고']
# eng_keywords=['mango']





# def dd_init():
    # data_dic=defaultdict(list)
    
    # return data_dic
    
#문제: 공동연구안나옴(체크된 항목없음)
def data_save(keyword, data_extracted):
    file_name=keyword+'관련 연구 사업 검색결과.txt'
    file_instance=open(file_name, 'w', encoding='utf-8')
    for writing_list in data_extracted:
        for element_index in range(len(writing_list)):
            if element_index == 29:
                file_instance.write(writing_list[-2])
            elif element_index == 30:
                file_instance.write(writing_list[-1])
            elif element_index > 31:
                file_instance.write(writing_list[element_index-2])
            else:
                file_instance.write(writing_list[element_index])
            # if len(writing_list) == writing_element+1:
                # print('줄바꿈')
                # file_instance.write('\n')
            # else:
            file_instance.write(',')
        file_instance.write('\n')
    file_instance.close()
    return True    
    
    
def data_refiner(total_data):
    black_set=set()
    count_dup=0
    for list_index in range(len(total_data)):
        for inspect_index in range(list_index+1, len(total_data)):## 인덱스 조정이 필요 2017.07.24
            if total_data[list_index][8]==total_data[inspect_index][8]:
                # del total_data[inspect_index]
                # print('중복 데이터 '+str(total_data[list_index][8])+'가 발견되었고, 해당 데이터는 삭제될 것입니다.')
                black_set.add(inspect_index)
                # count_dup+=1
    count_dup=len(black_set)
    print('count_dup:', count_dup)

    for black in sorted(black_set, reverse=True):
        # print(str(black)+'번의 과제번호는 '+total_data[black][8]+'이며, 삭제되었습니다.')
        del total_data[black]
        count_dup-=1
    print('count_dup:', count_dup)

    for list_index in range(len(total_data)):##데이터(문자열) 정리
        ##콤마 제거
        for data_index in range(len(total_data[list_index])):
            # if total_data[list_index][data_index].count(','):
            total_data[list_index][data_index]=total_data[list_index][data_index].replace(',', '')
            total_data[list_index][data_index]=total_data[list_index][data_index].replace('\n', '')
            total_data[list_index][data_index]=total_data[list_index][data_index].replace('\t', '')
            total_data[list_index][data_index]=total_data[list_index][data_index].replace('Nodata', '')
            # if(list_index==1):
                # print(total_data[list_index][data_index])            
            ##특수문자 제거
            # total_data[list_index][data_index]=re.sub("[^().,가-힣0-9a-zA-Z]","",total_data[list_index][data_index])
    return total_data
    
    
def detail_extract(web_driver, data_list):
    bs_tmp=bs4.BeautifulSoup(web_driver.page_source, 'lxml')
    for i in range(1,len(bs_tmp.find('table', {'class':'basic_list'}).tbody.find_all('tr'))+1) :##각 세부사항 페이지를 돌 루프.. 실질적으로 노가다 필요함
        # web_driver.find_element_by_xpath("//table[@class='basic_list']/tbody/tr["+str(i)+"]/td[6]/a").click()
        sr_btn=web_driver.find_element_by_xpath("//table[@class='basic_list']/tbody/tr["+str(i)+"]/td[6]/a")
        web_driver.execute_script("arguments[0].click()",sr_btn)
        bs_detail=bs4.BeautifulSoup(web_driver.page_source, 'lxml')
        # if i==1:#범례?('과제고유번호', 총연구기관' 등)
            # for chart in bs_detail.find('div', {'id':'divMain'}).find_all('th'):
                # print(chart.get_text().strip())
                # data_list[i].append(chart.get_text().strip())

        for value in bs_detail.find('div', {'id':'divMain'}).find_all('td'):##값 추출
            if value.find('a'):
                # print(value.find('a').get_text().strip())
                data_list[i-1].append(value.find('a').get_text().strip())
            elif value.find('input'):
                for check_check in value.find_all('input'):
                    if re.search(str(check_check), 'checked'):
                        # print(check_check.attrs['title'].strip())
                        data_list[i-1].append(check_check.attrs['title'].strip())
            elif value.get_text().find('showChart')!=-1: ##showChart 값은 필요 없으므로 제외. find는 값이 없을 때 -1을 리턴함
                # print(value.get_text().find('showChart'))
                pass
            else:
                # print(value.get_text().strip())
                data_list[i-1].append(value.get_text().strip())
        #사이트 구조 상 일관적인 논리로 풀어가기 어려운 면이 있어 요약서의 연구목표와 연구내용은 노가다...
        summary_list=bs_detail.find('div', {'id':'divSummary'}).table.tbody.find_all('td',{'class':'view_p30'})
        # print(summary_list[0].get_text().strip())
        data_list[i-1].append(summary_list[0].get_text().strip())
        # print(summary_list[1].get_text().strip())
        data_list[i-1].append(summary_list[1].get_text().strip())
            
        web_driver.execute_script('window.history.go(-1)')        
        
    return data_list
        
def list_extract(bs_html, data_list):
    # th_row_el=list()
    # for th_row in bs_html.find('table', {'class':'basic_list'}).thead.tr.find_all('th'):#테이블 맨 위 범례?(연도, 신부처 등) 추출
        # if th_row.find('a') is not None:
            # th_row_el.append(th_row.find('a').get_text())
        # else:
            # th_row_el.append(th_row.get_text())
    # data_list.append(th_row_el)
    
    for table_row in bs_html.find('table', {'class':'basic_list'}).tbody.find_all('tr'):#각 테이블의 행 추출
        row_el=list()
        for ele in table_row.find_all('td'):#하나의 행에 들어 있는 원소 추출
            if re.search(ele.get_text(),'[A-za-z0-9가-힣]+'):#공란일 경우 Nodata
                row_el.append('Nodata')
            elif ele.find('img'):#이미지 파일(주관, 협동, 위탁)일 경우 해당 단어
                if ele.find('img').attrs['alt'] == '주관':
                    row_el.append('주관')
                elif ele.find('img').attrs['alt'] == '협동':
                    row_el.append('협동')
                elif ele.find('img').attrs['alt'] == '위탁':
                    row_el.append('위탁')
                else:
                    row_el.append('Nodata')
            else:#나머지는 일반적인 data
                row_el.append(ele.get_text().strip())
        # print('row의 값은',row_el)
        data_list.append(row_el)
    # print(data_list)
    return data_list

    
    # assert False

def extract_operator(web_driver, ntis_keyword, eng_keyword):
    total_data=list()

##############selenium으로 접근######################################    
    point_list=['연구내용', '한글키워드', '영문키워드']
    for point in point_list: ##루프: '연구내용', '한글키워드', '영문키워드'항목에 각각 ntis_keyword삽입
        if point=="연구내용":
            
            # web_driver.find_element_by_id("searchMoreBtn").click()
            sr_btn=web_driver.find_element_by_id("searchMoreBtn")
            web_driver.execute_script("arguments[0].click()",sr_btn)
            
            web_driver.find_element_by_id("pjSum0").click()

            # web_driver.find_element_by_id("BT(생명공학기술)").click()
            sr_btn=web_driver.find_element_by_id("BT(생명공학기술)")
            web_driver.execute_script("arguments[0].click()",sr_btn)
            
            select_from=Select(web_driver.find_element_by_name("yrFrom_h"))
            select_from.select_by_value("2004")
            select_to=Select(web_driver.find_element_by_name("yrTo_h"))
            select_to.select_by_value("2016")
            web_driver.find_element_by_name("searchVO.pj_cont").send_keys(ntis_keyword)
            
        elif point=="한글키워드":#넘어가는 과정에서의 버그 잡아야함
            web_driver.find_element_by_name("searchVO.pj_han_key").send_keys(ntis_keyword)
            
        elif point=="영문키워드":
            web_driver.find_element_by_name("searchVO.pj_eng_key").send_keys(eng_keyword)
            
        else:
            print('연구내용, 한글키워드, 영문키워드 모두 아닌 값이 발생했습니다.')
            sys.exit(1)
        
        # web_driver.find_element_by_xpath("//a[@href='javascript:goSearch();']").click()
        sr_btn=web_driver.find_element_by_xpath("//a[@href='javascript:goSearch();']")
        web_driver.execute_script("arguments[0].click()",sr_btn)
###################################################################
        
        bs_html=bs4.BeautifulSoup(web_driver.page_source, 'lxml')
        

        
        
        if bs_html.find('table', {'class': 'basic_list'}).tbody.tr.td.get_text().count('검색된 결과가 없습니다.') > 0:
            if point is not "영문키워드":
                print(ntis_keyword+'에서 '+point+'의 검색 결과가 없습니다.')
            else:
                print(eng_keyword+'에서 '+point+'의 검색 결과가 없습니다.')
            web_driver.find_element_by_id("searchMoreBtn").click()
            web_driver.find_element_by_name("searchVO.pj_cont").clear()
            web_driver.find_element_by_name("searchVO.pj_han_key").clear()
            web_driver.find_element_by_name("searchVO.pj_eng_key").clear()
            continue
        tot_num=bs_html.find('h3', {'class':'t_head'}).span.get_text().split('(')[0]
        sec_num=bs_html.find('h3', {'class':'t_head'}).span.get_text().split('(')[1]
        
        # print(tot_num)
        # print(sec_num)
        #
        page_num=(int(re.search('[0-9]*,{0,1}[0-9]+건',tot_num).group().replace(',','').replace('건',''))-int(re.search('[0-9]*,{0,1}[0-9]+건',sec_num).group().replace(',','').replace('건',''))-1)//10+1
            
        # assert False
        # page_num=int(int(re.search('=[0-9]+' ,bs_html.find("a", {"name":"L"}).attrs["href"]).group().strip('='))/10+1)#검색결과목록 페이지의 수
        # except AttributeError:
            # print('페이지 리스트를 찾지 못했습니다. 페이지가 하나인 것으로 간주하고 진행합니다.')
            # page_num=2
        current_page=1#현재 데이터를 추출하고 있는 페이지
        print(ntis_keyword+'의'+point+'는 '+str(page_num)+'페이지입니다.')
        while current_page <= page_num: ##검색 결과 목록 페이지가 끝날 때까지(if numbered a tag attr.href == '끝' a tag attr.href)
            print(point+'의 '+str(current_page)+'page 진행중')
            
            data_list=[]#한 페이지의
            bs_html=bs4.BeautifulSoup(web_driver.page_source, 'lxml')
            
            data_list=list_extract(bs_html, data_list) #목록 페이지 정보 추출
            data_list=detail_extract(web_driver, data_list)#세부사항 추출, 이 둘을 합치는 작업도 같이 처리됨
            # print(str(data_list))
            # assert False
            # print(data_list)
            total_data+=data_list#list_extract와 detail_extract의 data가 합쳐진 data_list를 저장 
            # if current_page !=page_num:
            current_page+=1
            
            if page_num <= 1 or current_page > page_num :
                pass
            else:
                # web_driver.find_element_by_link_text(str(current_page)).click()
                sr_btn=web_driver.find_element_by_link_text(str(current_page))
                web_driver.execute_script("arguments[0].click()",sr_btn)

            # assert False
            # web_driver.implicitly_wait(1)


        #검색 창 초기화
        # web_driver.find_element_by_id("searchMoreBtn").click()
        sr_btn=web_driver.find_element_by_id("searchMoreBtn")
        web_driver.execute_script("arguments[0].click()",sr_btn)
        
        web_driver.find_element_by_name("searchVO.pj_cont").clear()
        web_driver.find_element_by_name("searchVO.pj_han_key").clear()
        web_driver.find_element_by_name("searchVO.pj_eng_key").clear()
        
    total_data=data_refiner(total_data)
    # web_driver.find_element_by_xpath("//div[@class='serviceHead']/ul/li[4]/a").click()
    sr_btn=web_driver.find_element_by_id("searchMoreBtn")
    web_driver.execute_script("arguments[0].click()",sr_btn)
    # print(total_data)    

     ##루프 안의 항목들은 list에 list형식으로 저장하며, 
     ##루프: 
      ##각 항목에 대한 목록 Scraping. 
      ##루프: 목록의 세부사항(과제의 세부사항) Scraping
       ##추출 전 과제고유번호로 중복검사 
      ## 중복검사시 중복으로 밝혀질 경우 저장하지 않도록 함.
    return total_data
    
def ntis_connect(web_driver, url, id='doldol1', pw='Fish5321671!'):
    
    ##url로 이동 
    web_driver.get(url)
    # web_driver.find_element_by_link_text("로그인").click()
    element=web_driver.find_element_by_link_text("로그인")
    web_driver.execute_script("arguments[0].click()",element)
    ##id, pw 로그인
    main_window=web_driver.window_handles[0]
    web_driver.switch_to.window(web_driver.window_handles[1])
    web_driver.find_element_by_name('userid').send_keys(id)
    web_driver.find_element_by_name('password').send_keys(pw)
    web_driver.find_element_by_class_name('btn_blue').click()
    web_driver.switch_to.window(main_window)
    ##selenium 객체 리턴
    return web_driver

            
    
def main():
    web_driver=webdriver.Chrome('D:/scrapper/web_driver/chromedriver.exe')
    ##접속 및 로그인 함수 사용 및 객체 받기
    web_driver=ntis_connect(web_driver, url)
    ##루프: 모든 키워드 검색이 끝날 때까지
    for i in range(len(keyword_list)):
#        try:
            # print(keyword_list[i])
        data_extracted=extract_operator(web_driver, keyword_list[i], eng_keywords[i])##검색어 입력 및 페이지 수집(각 키워드에 대해 for문 돌림, '연구내용', '한글키워드', '영문키워드'는 한 루프에서 모두 처리)+파싱 및 텍스트 정제, 중복 데이터 처리
            # print('입니다.')
#        except:
#        continue
        print('파일화')
        data_save(keyword_list[i], data_extracted)
        i+=1
        # break
        ##키워드별 저장
    ##최종중복검사 새 파일 생성
    
    

if __name__=='__main__':
    main()
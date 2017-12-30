from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as EC
from collections import defaultdict
from seleniumrequests import Firefox
import bs4
import sys
import re
from bs4 import BeautifulSoup
import time

# url='http://qy1.sfda.gov.cn/datasearch/face3/base.jsp?'\
# 'tableId=68&tableName=TABLE68&'\
# 'title=%B9%FA%B2%FA%CC%D8%CA%E2%D3%C3%CD%BE%BB%AF%D7%B1%C6%B7&'\
# 'bcId=138009396676753955941050804482'

##################################
##커뮤니티에서 알려준 풀 문장
url='http://qy1.sfda.gov.cn/datasearch/face3/search.jsp?'\
'tableId=68&bcId=138009396676753955941050804482&'\
'tableName=TABLE68&viewtitleName=COLUMN787&'\
'viewsubTitleName=COLUMN793%2CCOLUMN789&'\
'tableView=%E5%9B%BD%E4%BA%A7%E7%89%B9%E6%AE'\
'%8A%E7%94%A8%E9%80%94%E5%8C%96%E5%A6%86%E5'\
'%93%81&curstart=1'
#####################################

# target_url='http://app1.sfda.gov.cn/datasearch/face3/base.jsp?'\
# 'tableId=30&tableName=TABLE30&'\
# 'title=%B9%FA%B2%FA%B1%A3%BD%A1%CA%B3%C6%B7&'\
# 'bcId=118103385532690845640177699192'

def chkURL(i, URL):
    #네이버 뉴스 특성상 URL의 맨 뒤에 page='페이지번호n'이 있으며 if-elif문은 URL의 '페이지번호n'을 바꿔주는 역할을 한다.
    
    if URL.count('page=') is 0:
        URL=URL+'&page=1'
    if i >= 1 and i < 10:
        URL=URL[:-1]+str(i)
    elif i >= 10 and i < 100:
        if i==10:
            URL=URL[:-1]+str(i)
        else:
            URL=URL[:-2]+str(i)
    elif i >= 100 and i < 1000:
        if i==100:
            URL=URL[:-2]+str(i)
        else:
            URL=URL[:-3]+str(i)
    elif i >= 1000 and i < 10000:
        if i==1000:
            URL=URL[:-3]+str(i)
        else:
            URL=URL[:-4]+str(i)
    elif i >= 10000 and i < 100000:
        if i==10000:
            URL=URL[:-4]+str(i)
        else:
            URL=URL[:-5]+str(i)
    elif i >= 100000 and i < 1000000:
        if i==100000:
            URL=URL[:-5]+str(i)
        else:
            URL=URL[:-6]+str(i)
    elif i >= 1000000 and i < 10000000:
        if i==1000000:
            URL=URL[:-6]+str(i)
        else:
            URL=URL[:-7]+str(i)

    return URL




txt_file=open('chbio_cos.txt', 'w', encoding='utf-8')

j=1
while(j<=2235):
    # web_driver=webdriver.Chrome('D:\scrapper\web_driver\chromedriver.exe')
    web_driver=Firefox()
    # web_driver.get(url)
    web_driver.request('POST', url, data={"tableId": "68", "State":"1", "bcId":"138009396676753955941050804482")
    bs_tmp=BeautifulSoup(web_driver.page_source, 'lxml')
    the_list=bs_tmp.find_all('a')
    
    for i in the_list:
        print(i.get_text())
        txt_file.write(i.get_text()+'\n')

    # web_driver.find_element_by_name('goInt').clear()
    # web_driver.find_element_by_name('goInt').send_keys(str(j))
    # web_driver.find_element_by_xpath("//div[@id='content']/div/table[4]/tbody/tr/td[7]/input").click()
    j+=1
    url=chkURL(j, url)
    web_driver.quit()
    time.sleep(5)
    # print(web_driver.find_element_by_xpath("//div[@id='content']/div/table[4]/tbody/tr/td[1]").text)
    
    # web_driver.find_element_by_xpath("//div[@id='content']/div/table[@width='620']/tbody/tr/td[4]/img").click()






# print(bs_page.find('div',{'id':'content'}).find_all('a').get_text())
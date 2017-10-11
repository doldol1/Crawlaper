# 오지 않은 것에 대해 걱정하지 말고
# 어쩔 수 없는 일에 낙심하지 말자.
# 사람에게 기대하지 말고
# 스스로의 능력과 힘을 기르자.
# 누가, 언제 봐도 떳떳할 수 있는 말과 행동을 하자

# link_crawler.py
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.request import Request
import urllib.robotparser
import urllib.parse
import re
import datetime
import time
import random
import os
import pickle
import xlsxwriter

import csv

import lxml.html

FIELDS = ('area', 'population', 'iso', 'country', 'capital',
          'continent', 'tld', 'currency_code', 'currency_name', 'phone',
          'postal_code_format', 'postal_code_regex', 'languages','neighbours')



class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
        self.throttle=Throttle(delay)
        self.user_agent=user_agent
        self.proxies=proxies
        self.num_retries=num_retries
        self.cache=cache
    
    def __call__(self, url):
        result=None
        if self.cache:
            try:
                result=self.cache[url]
            except KeyError
                #url이 캐시에 있지 않음
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    #서버 오류, 캐시의 결과를 무시
                    #다시 다운로드
                    result=None
        if result is None:
            #결과를 캐시에서 가져오지 못함
            #따라서 다운로드 시도
            self.throttle.wait(url)
            proxy=random.choice(self.proxies) if self.proxies else None
            
            headers={'User-agent': self.user_agent}
            result=self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                #캐시에 결과가 저장됨
                self.cache[url]=result
        return result['html']
        
    def download(self, url, headers=None, user_agent='wswp', proxy=None, num_retries=2):
        print('Downloding:', url)
        headers = {'User-agent': user_agent}
        request = Request(url)
        opener = urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.request.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            html = urlopen(request).read().decode('utf-8')
        except HTTPError as e:
            print('Download error:', e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # 5xx HTTP 오류시 재시도
                    return download(url, num_retries - 1)
        return {'html': html, 'code': code}
        
class Throttle:
    """같은 도메인의 다운로드 사이에 지연을 추가한다
    """
    def __init__(self, delay):
        # 각 도메인의 다운로드 사이에 지연 시간
        self.delay = delay
        # 도메인을 마지막으로 접속한 시간
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # 도메인을 최근에 접속하였으며
                # 지연을 할 필요가 있다
                time.sleep(sleep_secs)
        # 최근에 접속한 시간 최신화
        self.domains[domain] = datetime.datetime.now()


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country',
                       'capital', 'continent', 'tld', 'currency_code',
                       'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages',
                       'neighbours')
        self.writer.writerow(self.fields)
    def __call__(self, url, html):
        if re.search('/view/', url):
            print(url)
            print(html)
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)



class DiskCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir=cache_dir
        self.max_length=100
    
    def url_to_path(self, url):
        """이 URL을 파일 시스템 경로로 설정
        """
        components=urlparse.urlsplit(url)
        #index.html을 빈 문자열이 있는 경로에 추가
        path=components.path
        if not path:
            path='/index.html'
        elif path.endswith('/'):
            path+='index.html'
        filename=components.netloc+path+components.query
        #잘못된 문자 교체
        filename=re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)
        #글자 수 최대 길이 제한
        filename='/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)
        
    def __getitem__(self, url):
        """이 URL로 디스크에서 데이터 읽기
        """
        path=self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                return pickle.load(fp)

def link_crawler(seed_url, link_regex, delay=1, max_depth=-1, headers=None, user_agent='wswp', proxy=None, scrape_callback=None, cache=None):
    crawl_queue = [seed_url]
    # 이전에 다운로드한 URL 저장
    seen = {seed_url: 0}
    
    num_urls=0
    rp=get_robots(seed_url)
    
    D=Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)
    
    
    # rp = urllib.robotparser.RobotFileParser()
    # rp.set_url('http://example.webscraping.com/robots.txt')
    # rp.read()

    # headers = headers or {}
    # throttle = Throttle(delay)

    while crawl_queue:
        url = crawl_queue.pop()
        depth=seen[url]
        #url이 robotx.txt 제한 사항을 전달했는지 확인
        if rp.can_fetch(user_agent, url):
            html=D(url)
            links=[]
            throttle.wait(url)
            html = download(url, headers)

            links = []
            if scrape_callback:
                print('come back')
                links.extend(scrape_callback(url, html) or [])

            depth = seen[url]
            if depth != max_depth:
                for link in get_links(html):
                    # 링크가 regexd와 일치하는지 확인
                    if re.match(link_regex, link):
                        # 절대 링크 생성
                        link = urllib.parse.urljoin(seed_url, link)
                        # 현재 링크가 이전에 다운로드한 링크인지 확인
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)
        else:
            print('Blocked by robots.txt:', seed_url)


def get_links(html):
    """html에서 링크 목록 반환
    """
    # 웹페이지에서 모든 링크를 추출하는 정규식
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # 웹페이지의 모든 링크 목록
    return webpage_regex.findall(html)

    
    
'''
def scrape_callback(url, html):
    if re.search('/view/', url):
        tree = lxml.html.fromstring(html)
        row = [tree.cssselect('table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content() for field in FIELDS]
        print(url, row)
'''

# link_crawler('http://example.webscraping.com', '/(index|view)', max_depth=-1, scrape_callback=ScrapeCallback())
link_crawler('http://example.webscraping.com', '/(index|view)', max_depth=-1) # 콜백 사용 안 함
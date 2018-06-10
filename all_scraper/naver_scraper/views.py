from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from .models import SearchCondition

from .Urllist_server import Urllist
from .file_integrate_server import filter

from .Naver_crawler_server import Naver_crawler
from .Naver_crawler_server import Naver_scraper
from .Naver_crawler_server import Naver_datasaver
import Urlmake_server

def index(request):
    return render(request, 'naver_scraper/index.html')
    
def crawling(request):
    condition=SearchCondition()
    
    condition.key_word=request.POST['key_word']
    condition.essential_word=request.POST['essential_word']
    condition.exact_word=request.POST['exact_word']
    condition.except_word=request.POST['except_word']
    
    if request.POST['ds']:
        condition.ds=datetime.strptime(request.POST['ds'], "%Y-%m-%d")
    else:
        condition.ds=datetime.strptime('2000-01-01', "%Y-%m-%d")
        
    if request.POST['de']:
        condition.de=datetime.strptime(request.POST['de'], "%Y-%m-%d")
    else:
        condition.de=datetime.today()
    
    condition.press_codes=request.POST['press_codes']
    condition.search_mode=request.POST['search_mode']
    
    gend_url=url_make(condition)
    
    list_instance=Urllist()
    crawler=Naver_crawler()
    scraper=Naver_scraper()
    saver=Naver_datasaver()
    
    list_instance.url_changer(gend_url, condtion.ds, condition.de)
    
    
    
    return HttpResponse(gend_url)
    
    
    
    
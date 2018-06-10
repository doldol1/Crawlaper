import urllib.parse
from datetime import datetime

def url_make(condition):

    sample_url='https://search.naver.com/search.naver?&where=news&'\
'query=%EC%84%B8%EC%9B%94%ED%98%B8&'\
'sm=tab_pge&sort=0&photo=0&field=1&reporter_article=&pd=3&'\
'ds=2014.04.14&de=2018.03.05&docid=&'\
'nso=so:r,p:from20140414to20180305,a:t&mynews=1&cluster_rank=38&'\
'start=1&refresh_start=0'

    splited_url=sample_url.split('&')
    
    dateDS_instance=condition.ds
    dateDE_instance=condition.de
    
    #################수정 필요#####################
    
    # if condition.ds:
        # dateDS_instance=datetime.strptime(condition.ds, "%Y-%m-%d")
    # else:
        # dateDS_instance=datetime.strptime('2000-01-01', "%Y-%m-%d")
        
    # if condition.de:
        # dateDE_instance=datetime.strptime(condition.de, "%Y-%m-%d")
    # else:
        # dateDE_instance=datetime.today()
    
    ############################################
    
    for splited in range(len(splited_url)):
        if 'query=' in splited_url[splited]:
            full_query=urllib.parse.quote(condition.key_word)+'+"'+urllib.parse.quote(condition.exact_word)+'"+'+urllib.parse.quote('+'+condition.essential_word)+'+-'+urllib.parse.quote(condition.except_word)
            splited_url[splited]="query="+full_query
            # print(splited_url[splited])
        
        elif 'ds=' in splited_url[splited]:
            splited_url[splited]="ds="+dateDS_instance.strftime("%Y.%m.%d")
            # print(splited_url[splited])
        
        elif 'de=' in splited_url[splited]:
            splited_url[splited]="de="+dateDE_instance.strftime("%Y.%m.%d")
            # print(splited_url[splited])

        elif 'pd=' in splited_url[splited]:
            splited_url[splited]="pd=3"
            # print(splited_url[splited])           
        
        elif 'nso=':#언론사와도 관련있는 듯 하니.. 참고
            if 'from' in splited_url[splited]:
                tmp_nso=splited_url[splited].split('from')[0]
                splited_url[splited]=tmp_nso+'from'+dateDS_instance.strftime("%Y%m%d")+'to'+dateDE_instance.strftime("%Y%m%d")+'%2Ca%3Aall'
                # print(splited_url[splited])
                
            elif 'all' in splited_url[splited]:
                splited_url[splited]=splited_url[splited].replace('all','')+'from'+dateDS_instance.strftime("%Y%m%d")+'to'+dateDE_instance.strftime("%Y%m%d")+'%2Ca%3Aall'
                # print(splited_url[splited])
                
        else:
            pass
                
    reunited_url='&'.join(splited_url)

    print(reunited_url)
    
    return reunited_url
#ntis 세부과제 스크래퍼


#러프한 기본 계획
#1. 위 URL로 Get접근하여 Key값 받기
#2. 로그인을 통한 SessionID획득
#3. POST로 request날림
#4. 결과값 받아서 추출, 가공

import urllib, urllib.request, urllib.parse
import bs4
import http.cookiejar
# url='http://rndgate.ntis.go.kr/switch.do?prefix=/ia/info&page=/ProjectGroup.do?method=iaProjectSubjectList&searchVO.yrFrom=2016&searchVO.yrTo=2016'

# url='http://sso2.ntis.go.kr/3rdParty/loginFormPageID.jsp'

url='http://rndgate.ntis.go.kr/ia/info/ProjectGroup.do'

headers={'Host': 'rndgate.ntis.go.kr', 'Connection': 'keep-alive', 'Content-Length': '1740', 'Cache-Control': 'max-age=0', 'Origin': 'http://rndgate.ntis.go.kr', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://rndgate.ntis.go.kr/ia/info/ProjectGroup.do', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4', 'Cookie': 'WMONID=DMj5TnVCJ18; -4279600797596526265_SALTLUX=%25ED%2595%25B4%25EC%2596%2591; HM_ID=11674993; InitechEamERCD=1001; InitechEamUURL=http%3A%2F%2Frndgate.ntis.go.kr%2Fia%2Fproject%2FProjectGroup%2FiaProjectSubjectList.jsp; _gat=1; JSESSIONID=Oe8X9PJhRxjT129k6UccJAQmSfKyFqlevme0n9xhQywvCFcd9SR81LUAAc4TnL5I.amV1c19kb21haW4vTVNfNzFfcm5kZ2F0ZQ==; _ga=GA1.3.552086769.1497332084; _gid=GA1.3.1575125760.1499848666'}

# data={'org.apache.struts.taglib.html.TOKEN':'c08a0f50c9645edb521ca2756ae03ea2', 'method':'iaProjectSubjectList', 'orderByTarget':'', 'orderByMethod':'', 'maxIndexPages':'10', 'maxPageItems':'10', 'pagerOffset':'0', 'searchVO.ynTopAdmin':'N', 'searchVO.yrFrom':'2016', 'searchVO.yrTo':'2016', 'searchVO.nmSubPj':'', 'searchVO.nmRSResp':'', 'searchVO.pjt_id':'', 'searchVO.dept_cd':'', 'searchVO.dept_o_cd':'', 'searchVO.dept_nm':'',  'searchVO.rsch_dev_cd':'', 'searchVO.rsch_dev_nm':'', 'searchVO.tech_period_cd':'', 'searchVO.tech_period_nm':'', 'searchVO.rsch_imp_cd':'', 'searchVO.rsch_imp_nm':'', 'searchVO.area_cd':'', 'searchVO.area_nm':'', 'searchVO.sci_cd':'ALL', 'searchVO.sci_nm':'', 'searchVO.sci_2009_cd':'', 'searchVO.sci_2009_nm':'', 'searchVO.econ_cd':'', 'searchVO.econ_nm':'', 'searchVO.econ_02_cd':'', 'searchVO.econ_02_nm':'', 'searchVO.t6_tech_div_cd':'202020000', 'searchVO.t6_tech_div_nm':'BT%28%BB%FD%B8%ED%B0%F8%C7%D0%B1%E2%BC%FA%29', 'searchVO.green_27_cd':'', 'searchVO.green_27_nm':'', 'searchVO.app_field_cd':'', 'searchVO.app_field_nm':'', 'searchVO.funsion_yn':'D', 'searchVO.dept_OnN':'', 'searchVO.deptAllC':'', 'searchVO.sciCdAll':'', 'searchVO.project_type':'', 'searchVO.trendSearchDetail':'N', 'searchVO.pjSum':'ALL', 'searchVO.dept_o_nm':'', 'target':'iaProjectSubjectList', 'tab_gb':'H', 'yrFrom_h':'2016', 'yrTo_h':'2016', 'nmSubPj_h':'', 'pjt_id_h':'', 'searchVO.nmPG':'', 'nmRSResp_h':'', 'searchVO.detail_bz_nm':'', 'searchVO.nmRsDept':'', 'searchVO.main_rsch_org_nm':'', 'pjSum':'1', 'pjSum':'2', 'pjSum':'3', 'pjSum':'4', 'pjSum':'5', 'pjSum':'6', 'searchVO.pj_target':'', 'searchVO.pj_cont':'%C7%D8%BE%E7', 'searchVO.pj_exp':'', 'searchVO.pj_han_key':'', 'searchVO.pj_eng_key':'', 'searchVO.CTGNINVEST_from':'', 'searchVO.CTGNINVEST_to':'', 'searchVO.MCFD_CASH_LOCAL_from':'', 'searchVO.MCFD_CASH_LOCAL_to':'', 'searchVO.MCFD_CASH_UNIV_from':'', 'searchVO.MCFD_CASH_UNIV_to':'', 'searchVO.MCFD_CASH_CO_from':'', 'searchVO.MCFD_CASH_CO_to':'', 'searchVO.MCFD_CASH_ETC_from':'', 'searchVO.MCFD_CASH_ETC_to':'', 'searchVO.TOT_BZ_AMT_from':'', 'searchVO.TOT_BZ_AMT_to':'', 't6_chk':'202020000', 'default_field':'on'}

data={'method':'iaProjectSubjectList', 'orderByTarget':'', 'orderByMethod':'', 'maxIndexPages':'10', 'maxPageItems':'10', 'pagerOffset':'0', 'searchVO.ynTopAdmin':'N', 'searchVO.yrFrom':'2016', 'searchVO.yrTo':'2016', 'searchVO.nmSubPj':'', 'searchVO.nmRSResp':'', 'searchVO.pjt_id':'', 'searchVO.dept_cd':'', 'searchVO.dept_o_cd':'', 'searchVO.dept_nm':'',  'searchVO.rsch_dev_cd':'', 'searchVO.rsch_dev_nm':'', 'searchVO.tech_period_cd':'', 'searchVO.tech_period_nm':'', 'searchVO.rsch_imp_cd':'', 'searchVO.rsch_imp_nm':'', 'searchVO.area_cd':'', 'searchVO.area_nm':'', 'searchVO.sci_cd':'ALL', 'searchVO.sci_nm':'', 'searchVO.sci_2009_cd':'', 'searchVO.sci_2009_nm':'', 'searchVO.econ_cd':'', 'searchVO.econ_nm':'', 'searchVO.econ_02_cd':'', 'searchVO.econ_02_nm':'', 'searchVO.t6_tech_div_cd':'202020000', 'searchVO.t6_tech_div_nm':'BT%28%BB%FD%B8%ED%B0%F8%C7%D0%B1%E2%BC%FA%29', 'searchVO.green_27_cd':'', 'searchVO.green_27_nm':'', 'searchVO.app_field_cd':'', 'searchVO.app_field_nm':'', 'searchVO.funsion_yn':'D', 'searchVO.dept_OnN':'', 'searchVO.deptAllC':'', 'searchVO.sciCdAll':'', 'searchVO.project_type':'', 'searchVO.trendSearchDetail':'N', 'searchVO.pjSum':'ALL', 'searchVO.dept_o_nm':'', 'target':'iaProjectSubjectList', 'tab_gb':'H', 'yrFrom_h':'2016', 'yrTo_h':'2016', 'nmSubPj_h':'', 'pjt_id_h':'', 'searchVO.nmPG':'', 'nmRSResp_h':'', 'searchVO.detail_bz_nm':'', 'searchVO.nmRsDept':'', 'searchVO.main_rsch_org_nm':'', 'pjSum':'1', 'pjSum':'2', 'pjSum':'3', 'pjSum':'4', 'pjSum':'5', 'pjSum':'6', 'searchVO.pj_target':'', 'searchVO.pj_cont':'%C7%D8%BE%E7', 'searchVO.pj_exp':'', 'searchVO.pj_han_key':'', 'searchVO.pj_eng_key':'', 'searchVO.CTGNINVEST_from':'', 'searchVO.CTGNINVEST_to':'', 'searchVO.MCFD_CASH_LOCAL_from':'', 'searchVO.MCFD_CASH_LOCAL_to':'', 'searchVO.MCFD_CASH_UNIV_from':'', 'searchVO.MCFD_CASH_UNIV_to':'', 'searchVO.MCFD_CASH_CO_from':'', 'searchVO.MCFD_CASH_CO_to':'', 'searchVO.MCFD_CASH_ETC_from':'', 'searchVO.MCFD_CASH_ETC_to':'', 'searchVO.TOT_BZ_AMT_from':'', 'searchVO.TOT_BZ_AMT_to':'', 't6_chk':'202020000', 'default_field':'on'}

# data={'userid':'doldol1', 'password':'Fish5321671!'}

# headers={'Connection':'keep-alive', 'Origin':'http://sso2.ntis.go.kr', 'Host':'sso2.ntis.go.kr',  'Upgrade-Insecure-Requests':'1', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 'Referer':'http://sso2.ntis.go.kr/3rdParty/loginFormPageID.jsp', 'Accept-Encoding':'gzip, deflate, br', 'Cookie':'JSESSIONID=ib8AjO8ogkRswULNV6zxLl34W5M8ajzsnHvvpRpiFOj5oOIV9BagZaSR5QB3SBPC.bnMxMHNzby9NUy0zMl9OVElTU1NPX25leGVzcw==; HM_ID=11674993; _gat=1; InitechEamERCD=1001; JSESSIONID=F8yp3zOtBbqYag8I4KWBu8lf1vSxzciRn8aR9yFGaiRE1e5n9U8Z2ClKXxyaDzIS.amV1c19kb21haW4vTVNfNzJfcm5kZ2F0ZQ==; _ga=GA1.3.552086769.1497332084; _gid=GA1.3.1575125760.1499848666; InitechEamUURL=http%3A%2F%2Frndgate.ntis.go.kr%3A%2Finitech%2Fsso%2FssoPopupLogin.jsp%3FUURL%3Dhttp%253A%2F%2Frndgate.ntis.go.kr%2Fswitch.do%253Fprefix%253D%2Fia%2Finfo%2526page%253D%2FProjectGroup.do%253Fmethod%253DiaProjectSubjectList%2526searchVO.yrFrom%253D2016%2526searchVO.yrTo%253D2016; InitechEamRTOA=1'}

# headers={'Host': 'sso2.ntis.go.kr', 'Connection': 'keep-alive', 'Content-Length': '38', 'Cache-Control': 'max-age=0', 'Origin': 'https://sso2.ntis.go.kr', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://sso2.ntis.go.kr/3rdParty/loginFormPageID.jsp', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4', 'Cookie': 'JSESSIONID=3F6e6kpzj94VSD1RBTYMbRUqknclpa1JzGCnJYcyiIU3pvLH9tFAhJnd3ioEiPeM.bnMxMHNzby9NUy0zMl9OVElTU1NPX25leGVzcw==; HM_ID=11674993; JSESSIONID=W5iE0EjD8htXgma2cg1maAJk714FP1y7zsOe1ixZgFIWA1HC9qq144Dy8IM83AOm.amV1c19kb21haW4vTVNfNzJfcm5kZ2F0ZQ==; _gat=1; InitechEamERCD=1001; _ga=GA1.3.552086769.1497332084; _gid=GA1.3.1575125760.1499848666; InitechEamUURL=http%3A%2F%2Frndgate.ntis.go.kr%3A%2Finitech%2Fsso%2FssoPopupLogin.jsp%3FUURL%3Dhttp%253A%2F%2Frndgate.ntis.go.kr%2Fswitch.do%253Fprefix%253D%2Fia%2Finfo%2526page%253D%2FProjectGroup.do%253Fmethod%253DiaProjectSubjectList%2526searchVO.yrFrom%253D2016%2526searchVO.yrTo%253D2016; InitechEamRTOA=1'}
################이런저런 트라이###############
# encoded_data=urllib.parse.urlencode(data).encode("utf-8")
# html=urllib.request.urlopen(url, encoded_data)
# bs_data=bs4.BeautifulSoup(html, 'lxml', from_encoding='utf-8')

# file_save=open('ex_file.html', 'w', encoding='utf-8')
# file_save.write(str(bs_data.get_text))
# file_save.close()

# cj=http.cookiejar()
# opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
# html=opener.open(LOGIN_URL).read()

encoded_data=urllib.parse.urlencode(data).encode("utf-8")
request_instance=urllib.request.Request(url, encoded_data, headers) #request세팅
response_instance=urllib.request.urlopen(request_instance) #오프너 계열의 클래스 반환
print('바듬!')
bs_data=bs4.BeautifulSoup(response_instance, 'lxml', from_encoding='utf-8')
print(str(bs_data))
import urllib, urllib.request

URL='https://apps.webofknowledge.com/Search.do?'\
'product=WOS&SID=Q26QVNMrbNVMsYnmfGK&search_mode=GeneralSearch&'\
'prID=099e1a33-875b-4614-84e5-37785340ea22'

post_body={"selectedIds":"",  "displayCitedRefs":"true",  "displayTimesCited":"true",  "viewType":"summary",  "product":"WOS",  "rurl":"https%3A%2F%2Fapps.webofknowledge.com%2Fsummary.do%3Fproduct%3DWOS%26search_mode%3DGeneralSearch%26qid%3D1%26SID%3DQ26QVNMrbNVMsYnmfGK",  "mark_id":"WOS",  "colName":"WOS",  "search_mode":"GeneralSearch",  "locale":"ko_KR",  "view_name":"WOS-summary", "sortBy":"PY.D;LD.D;SO.A;VL.D;PG.A;AU.A",  "mode":"OpenOutputService",  "qid":"1",  "SID":"Q26QVNMrbNVMsYnmfGK",  "format":"saveToFile",  "filters":"PMID USAGEIND AUTHORSIDENTIFIERS ACCESSION_NUM FUNDING SUBJECT_CATEGORY JCR_CATEGORY LANG IDS PAGEC SABBR CITREFC ISSN PUBINFO KEYWORDS CITTIMES ADDRS CONFERENCE_SPONSORS DOCTYPE CITREF ABSTRACT CONFERENCE_INFO SOURCE TITLE AUTHORS",  "mark_to":"500",  "mark_from":"1",  "queryNatural":"<b>출판 연도:</b> (2016)",  "count_new_items_marked":"0",  "use_two_ets":"false",  "IncitesEntitled":"no",  "value(record_select_type)":"range",  "markFrom":"1",  "markTo":"500",  "fields_selection":"PMID USAGEIND AUTHORSIDENTIFIERS ACCESSION_NUM FUNDING SUBJECT_CATEGORY JCR_CATEGORY LANG IDS PAGEC SABBR CITREFC ISSN PUBINFO KEYWORDS CITTIMES ADDRS CONFERENCE_SPONSORS DOCTYPE CITREF ABSTRACT CONFERENCE_INFO SOURCE TITLE AUTHORS",  "save_options":"tabWinUnicode"}
encoded_data=urllib.parse.urlencode(post_body).encode("utf-8")

request=urllib.request.Request(URL, encoded_data)
response=urllib.request.urlopen(request)
print(response.geturl())
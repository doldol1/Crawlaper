from django.db import models

# Create your models here.

##############Value######################

##SearchCondition class
##pk: auto-generated primary key
##keyword: keyword of crawler
##ds: start date, DateField.
##de: end date, DateField.
##search_mode: condition flag, 0 is subject only search, 1is subject+body search, IntegerField.
##press_code: code of newspaper press, CharField. In Naver, each press searching condition have their code. Daily newspaper press codes are
##1032, 1005, 2312, 1020, 2385, 1021, 1081, 1022, 2268, 1023, 1025, 1028, 1469
## and each codes are matched press name below:
## gyunghyang, kookmin, naeil, donga, maeil, munhwa, seoul, saegyae, asiatoday, josun, joongang, hangyurae, hankook
##comment: press informations are sent to server through cooke: news_office_checked=1032, 1005, 2312, ... If cookie have no news_office_checked, server will searching all news without press condition.
##essential_word: essential_word is for detailed search-'+' should be written in front of essential word, CharField
##exact_word: exact_word is for detailed search-it should be written between "". CharField
##except_word: except_word is for detailed search-'-' should be written in front of excepting word, CharField

##SearchResult class
##pk: auto-generated primary key
##news_subject: subject of news, CharField
##news_date: date of news published, DateField.
##news_press: press company of news, CharField.
##news_url: url of news published, CharField.
##news_body: body of news, CharField.
#################################################

from django.db import models

class SearchCondition(models.Model):
    key_word=models.CharField(max_length=500)
    ds=models.DateField('start date')
    de=models.DateField('end date')
    press_codes=models.CharField(max_length=500)
    search_mode=models.IntegerField()
    essential_word=models.CharField(max_length=200)
    exact_word=models.CharField(max_length=200)
    except_word=models.CharField(max_length=200)
    
    def __init__(self):
        print('SearchCondition instance created')


class SearchResult(models.Model):
    search_condition=models.ForeignKey(SearchCondition, on_delete=models.CASCADE)
    news_subject=models.CharField(max_length=1000)
    news_date=models.DateField('news published date')
    news_press=models.CharField(max_length=100)
    news_url=models.CharField(max_length=2000)
    news_body=models.CharField(max_length=100000)

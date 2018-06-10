from django.urls import path

from . import views

app_name='naver_scraper'
urlpatterns=[
        path('', views.index, name='index'),
        path('crawling/', views.crawling, name='naver_crawling'),
        ]

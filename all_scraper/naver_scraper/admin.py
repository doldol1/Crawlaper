from django.contrib import admin

from .models import SearchCondition, SearchResult
# Register your models here.

admin.site.register(SearchCondition)
admin.site.register(SearchResult)

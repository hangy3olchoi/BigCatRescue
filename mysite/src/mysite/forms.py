from django import forms

class CrawlerSearchForm(forms.Form): # crawling 구현관련
    search_word = forms.CharField(label='')
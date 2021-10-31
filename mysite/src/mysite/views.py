import re
import test
import urllib

from bs4 import BeautifulSoup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
import requests

from mysite.forms import CrawlerSearchForm


class HomeView(TemplateView):
    template_name = 'home.html'
    
class ChatbotView(TemplateView):
    template_name = 'chatbot.html'
    
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'
    
class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.owner:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
    
class CrawlerSearchFormView(FormView): # crawling 구현관련
    form_class = CrawlerSearchForm
    template_name = 'crawling.html'
    
    def form_valid(self, form):
        # base.html에 <input> 추가
        searchWord = form.cleaned_data['search_word']

        url = 'https://www.google.com/search?q='+str(searchWord)+'&tbm=isch&ved=2ahUKEwiHvMriwcjyAhXBIqYKHXUvDMsQ2-cCegQIABAA&oq='+str(searchWord)+'&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgsIABCABBCxAxCDATIFCAAQgAQ6CAgAELEDEIMBUN3qNFjF9jRgrPg0aABwAHgAgAHDAYgB1ASSAQMyLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=PUwkYcepE8HFmAX13rDYDA&bih=911&biw=958&hl=ko'

        response = requests.get(url)
        response.raise_for_status()
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # 이미지 검색 시 클래스명
        # select, find_all로 추출하는 것은 list로 추출.
        img_result = soup.select("img[class='yWs4tf']")
        link_result = soup.select("table[class='IkMU6e'] a[href]")
        text_result = soup.select("span[class='fYyStc']")
        
        # 추출한 태그는 'class'타입이기 때문에 str타입으로 변환 할 임시변수 선언.
        linkTemp = ""
        
        # 구글 도메인과 추출한 href속성값을 결합하면 정상적으로 작동하는 링크가 됨.
        google = 'https://www.google.com' 
        i = 0
        # str타입으로 변환한 변수를 담을 임시 리스트 선언
        temp_linkList = []
        for tag in link_result:
            # 'href'속성값만을 추출
            linkTemp = tag['href']
            # 템플릿 autoescape 활용을 위해 'str'타입으로 변환
            linkTemp2 = str(linkTemp)
            # 현재 'str'이기 때문에 템플릿에 적용할 태그를 문자엻 결합
            linkTemp3 = '<div class="image-container"><a href=' + google + linkTemp2 + '>'
            
            # 이미지 20개에 대한 링크가 총 40개 추출(이미지 당 2개)되어 절반은 버림.
                #(2번째 링크가 리디렉션없이 바로 이동해서 골라담음)
            if(i % 2 == 0):
                temp_linkList.append(linkTemp3)
            i = i +1
            
        # 추출한 태그는 'class'타입이기 때문에 str타입으로 변환 할 임시변수 선언
        temp = "" 
        # str타입으로 변환한 변수를 담을 임시 리스트 선언
        temp_imgList = []
        # <a>를 닫기 위해서 </a> 추가 'temp_linkList'에서 여는 태그만 결합
        for tag in img_result:
            temp = str(tag) + '</a></div>'
            temp_imgList.append(temp)
        
        # 추출한 태그는 'class'타입이기 때문에 str타입으로 변환 할 임시변수 선언
        textTemp = "" 
        # str타입으로 변환한 변수를 담을 임시 리스트 선언
            # 텍스트는 이미지 1개당 2개이기 때문에 1이미지, 1링크, 2텍스트를 한 세트 구분짓고자 두 개의 임시 리스트 선언.
        temp_textList1 = []
        temp_textList2 = []
        j = 0        
        for tag in text_result:
            textTemp = str(tag.get_text())
            
            # 짝수, 홀수에 따라 담길 리스트를 if문으로 구분.
            if(j % 2 == 0):
                temp_textList1.append(textTemp)
            else:
                temp_textList2.append(textTemp)
            
            # if문의 조건에 활용하기 위해서 카운트    
            j = j + 1
            
        last_List = []
        for x in range(0,len(temp_imgList)): 
            link = temp_linkList[x]
            img = temp_imgList[x]
            # last_List.append(temp_textList1[x]) # 
            # last_List.append(temp_textList2[x])
            last_List.append(link+img)
        
        print(last_List)

        context = {}
        
        context['form'] = form
        context['search_term'] = searchWord
        # 임시 리스트를 'context'딕셔너리에 key 'last_List'의 'value'로 'last_List'를 담는다
        # 리스트는 딕셔너리의 요소가 될 수 있다.
        context['last_List'] = last_List # 딕셔너리를 템플릿에서 호출하는 방법을 몰라서, 결국 리스트로만 마무리.
        
        return render(self.request, self.template_name, context)       
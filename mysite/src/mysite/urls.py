"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mysite.views import HomeView, UserCreateView, UserCreateDoneTV, ChatbotView,\
    CrawlerSearchFormView
from mysite.forms import CrawlerSearchForm



# from bookmark.models import Bookmark
# url 설계과정이 중요함.
# 리스트[] 속의 하나의 아이템이기 때문에 ','로 구분해줘야 함.
urlpatterns = [
    path('', HomeView.as_view(), name= 'home'),
    
    path('chatbot/', ChatbotView.as_view(), name= 'chatbot'),
    
    path('admin/', admin.site.urls),
    
    path('bookmark/', include('bookmark.urls')),
    
    path('blog/', include('blog.urls')),
    
    path('polls/', include('polls.urls')),
    
    path('photo/', include('photo.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    
    path('accounts/register/done', UserCreateDoneTV.as_view(), name='register_done'),
    
    path('crawling/', CrawlerSearchFormView.as_view(), name='crawling'), # crawling 구현관련 
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # media 파일 저장관련, pillow 다운필요.(파이썬 이미지 관리 패키지)


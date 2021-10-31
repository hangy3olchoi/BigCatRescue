from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q  # 검색기능 관련(색인)
from django.shortcuts import render  # 검색기능 관련
from django.urls.base import reverse_lazy
from django.views.generic import FormView  # 검색기능 관련
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.forms import PostSearchForm  # 검색기능 관련
from blog.models import Post
from mysite import settings  # 댓글기능 추가 시 임포트
from mysite.views import OwnerOnlyMixin


# Create your views here.
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    
    # 페이지 당 몇개의 글을 보여줄지 지정하는 모듈 
    paginate_by = 15
    
class PostDV(DetailView):
    model = Post
    
    # 댓글기능 추가를 위한 함수.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}-{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context
    
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'
    
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True
    
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'
    
class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'
    
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

# 태그와 관련된 오브젝트를 리스트로 보여줌.(VO의 형태) 
class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post
    
    # self는 'TaggedObjectLV'를 의미.
    def get_queryset(self):
        # 'self.kwargs.get('tag')'로 filter하겠다.
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))
    
    # **를 붙여줘야 dict형태로 리턴(*면 list형태)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'tagname'이라는 키로 인덱싱
        context['tagname'] = self.kwargs['tag']
        return context
    
# 검색기능 추가로 인해 작성한 class
class SearchFormView(FormView):
    form_class = PostSearchForm # blog.forms 생성
    template_name = 'blog/post_search.html'
    
    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        
        # Post는 blog의 vo클래스
        post_list = Post.objects.filter(
                Q(title__icontains=searchWord) 
              | Q(description__icontains=searchWord) 
              | Q(content__icontains=searchWord)
        ).distinct() # distinct()는 중복을 배제
        
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list
        
        return render(self.request, self.template_name, context)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content','image', 'tags'] # image 추가
    initial = {'slug': 'auto-filling-do-not-input'}
    #fields = ['title', 'description', 'content', 'tags'] # slug 필드 처리 방법2
    success_url = reverse_lazy('blog:index')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        return super().form_valid(form)
    
class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'
    
    def get_queryset(self):
        
        return Post.objects.filter(owner = self.request.user)
    
class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'image', 'tags'] # image 추가
    success_url = reverse_lazy('blog:index')
    
class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
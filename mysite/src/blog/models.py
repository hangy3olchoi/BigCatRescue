from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse  # url 패턴을 만들어 준다.
from django.utils.text import slugify
from taggit.managers import TaggableManager

from photo.fields import ThumbnailImageField


# Java의 'vo'클래스의 기능
# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name = 'TITLE', max_length = 50)
    
    slug = models.SlugField('SLUG', unique = True, allow_unicode = True, help_text = 'one word for title alias.')
    
    description = models.CharField('DESCRITPTION', max_length = 100, blank = True, help_text = 'simple description text.')
    
    content = models.TextField('CONTENT')
    
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add = True)
    
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now = True)
    
    tags = TaggableManager(blank=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)

    image = ThumbnailImageField('IMAGE', upload_to='blog/%Y/%m', null=True) # image 추가
    
    # 이너 클래스
    class Meta:
        verbose_name = 'post'
        # 'verbose_name_plural' -> 복수명칭
        verbose_name_plural = 'posts'
        # 'db_table' -> 테이블 명을 명시하면 임의로 설정 가능.
        db_table = 'blog_posts'
        # 'ordering = ('+/-modify_dt',)' -> '+'면 오름차순, '-'면 내림차순 ','는 자료의 다량일때를 위해 있는 것
        # ordering = ('-modify_dt',) # id 순으로 정렬하기 위해서 주석처리.
        ordering = ('-id',) # id순으로 내림차순 정렬.
        
    # 객체를 표현하는 방식    
    def __str__(self):
        return self.title
    
    # 'url'을 리턴하는 방식
    def get_absolute_url(self):
        return reverse('blog:post_detail', args = (self.slug,))
    
    def get_previous(self):
        return self.get_previous_by_modify_dt()
    
    def get_next(self):
        return self.get_next_by_modify_dt()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
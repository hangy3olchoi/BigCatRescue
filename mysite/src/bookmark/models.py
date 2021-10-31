from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# vo 클래스
    # 'models.Model'를 반드시 상속받아야 한다.
class Bookmark(models.Model):
    title = models.CharField('TITLE', max_length=100, blank=True) # 'TITLE'자리 - verbose_name 입력.
    url = models.URLField('URL', unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    # 객체표현 양식 - Java의 tostring()
    def __str__(self):
        return self.title
    
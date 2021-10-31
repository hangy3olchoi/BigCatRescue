from django.db import models
from photo.fields import ThumbnailImageField

# Create your models here.
class Question(models.Model): # 설문
    # id는 정수타입으로 자동 생성
    question_text = models.CharField(max_length=200) # 길이를 200자로 제한
    pub_date = models.DateTimeField('date published') # verbose - 'date published'
    
    # class Meta:
    #     ordering = ('-votes',)    
    
    # 객체표현양식
    def __str__(self):
        return self.question_text
    
class Choice(models.Model): # 설답
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200) # 길이를 200자로 제한
    image = ThumbnailImageField('IMAGE', upload_to='polls/%Y/%m', null=True) # image 추가
    
    # 설답 수 저장.
    votes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('choice_text',)    
    
    # 객체표현양식
    def __str__(self):
        return self.choice_text
    